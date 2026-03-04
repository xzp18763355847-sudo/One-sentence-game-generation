"""
AI 剧情游戏 - 单人版 GameManager（不写死 state 字段）

特点：
- start_game: 进入 awaiting_outline，让玩家先发剧情大纲
- send_message: 若 awaiting_outline -> 用大模型生成 assets + initial_state；否则用小模型推进
- story_state 顶层字段完全由 initial_state 决定（不写死）
- state_patch 采用 deep merge 继承更新
- 对外返回会 strip 掉任何层级的 secrets 字段（避免泄露）
- 持久化：存储到 Redis，刷新/重启不丢（前端能看到 status 才行）

修复点（针对 gunicorn 多 worker 丢档/坏档/进度不一致）：
✅ 方案 A：事务化（Redis分布式锁内 read -> modify -> write）
- 每次 start_game / send_message / end_game 都会：
  1) 获取Redis分布式锁
  2) 从Redis加载快照（覆盖内存）
  3) 执行业务逻辑推进状态
  4) 持久化到Redis
- 这样不会出现"worker B 用旧内存覆盖 worker A 的新存档"的回滚问题
"""

import json
import re
import threading
import time
import asyncio
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Coroutine

from game_statics.intern_map import SYSTEM_MESSAGES
from utils.util import strip_secrets, get_system_message, extract_first_json_object
from utils.redis_cache import dao as redis_dao

# 每个工作线程独立保存当前正在处理的 Game 实例
_tls = threading.local()

import httpx
from openai import AsyncOpenAI
import config
import redis.asyncio as redis
from state_schema import StateSchema, safe_merge_state
from narrative.state_models import NarrativeState
from narrative.engine import (
    init_narrative_state,
    update_and_get_events,
    apply_post_turn_updates,
    compute_ending_id,
)
from narrative.prompt_builder import build_director_prompt, get_official_game_prompt
from narrative.events import mark_events_triggered, apply_state_mutate
from game_types import get_game_type_info, is_valid_game_type
from game_generators import (
    build_outline_prompt,
    build_script_prompt,
    build_world_builder_prompt,
    validate_script_structure,
    normalize_script,
    OUTLINE_GENERATOR_SYSTEM_PROMPT,
    SCRIPT_GENERATOR_SYSTEM_PROMPT,
    WORLD_BUILDER_SYSTEM_PROMPT, TURN_ENGINE_SYSTEM_PROMPT,
)

# Linux 文件锁（gunicorn 多 worker 必备）已移除，改用 Redis 分布式锁
# import fcntl

from utils.log_config import get_logger

logger = get_logger(__name__)

T = TypeVar("T")


async def async_with_redis_lock(lock_key: str, fn: Callable[[], T], timeout: int = 30) -> T:
    """
    Redis 分布式锁异步版本

    功能：使用 Redis 分布式锁机制实现跨进程同步，确保多进程环境下的数据一致性
    参数：
        lock_key: Redis 锁的键名
        fn: 要在锁保护下执行的异步函数
        timeout: 锁超时时间（秒）
    返回：函数的返回值
    """
    # 确保Redis连接已初始化
    if redis_dao.redis is None:
        await redis_dao.init_pools()

    # 生成唯一的锁值
    import uuid
    lock_value = str(uuid.uuid4())

    # 尝试获取锁
    acquired = await redis_dao.redis.set(
        lock_key,
        lock_value,
        nx=True,  # 只在键不存在时设置
        ex=timeout  # 设置过期时间
    )

    if not acquired:
        # 等待锁释放，最多等待 timeout 秒
        for _ in range(timeout * 10):  # 每100ms检查一次
            await asyncio.sleep(0.1)
            acquired = await redis_dao.redis.set(lock_key, lock_value, nx=True, ex=timeout)
            if acquired:
                break
        else:
            raise TimeoutError(f"无法获取Redis锁: {lock_key}")

    try:
        return await fn()
    finally:
        # 使用Lua脚本安全释放锁（只有持有锁的进程才能释放）
        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        await redis_dao.redis.eval(lua_script, 1, lock_key, lock_value)


# =========================
# state
# =========================
class Progress(str, Enum):
    NOT_STARTED = "not_started"
    AWAITING_INITIAL_INPUT = "awaiting_initial_input"  # 等待用户输入几句话
    AWAITING_OUTLINE_REVIEW = "awaiting_outline_review"  # 等待用户审核/修改大纲
    IN_PROGRESS = "in_progress"
    ENDED = "ended"


@dataclass
class GlobalState:
    progress: Progress = Progress.NOT_STARTED
    round_count: int = 0
    max_rounds: int = 20
    ended_reason: Optional[str] = None

    game_type: str = ""  # 游戏类型
    outline: str = ""
    script: Dict[str, Any] = field(default_factory=dict)  # 游戏剧本（包含大纲、背景故事、章节、角色）
    assets: Dict[str, Any] = field(default_factory=dict)
    story_state: Dict[str, Any] = field(default_factory=dict)
    direction: str = ""
    language_code: str = "cn"  # 语言代码，默认为中文

    # 章节系统
    current_chapter: int = 1  # 当前章节编号（从1开始）
    chapters: List[Dict[str, Any]] = field(default_factory=list)  # 章节列表，每个章节包含：title, goal, description
    chapter_goal_completed: bool = False  # 当前章节目标是否已完成

    def to_public_dict(self) -> dict:
        """
        转换为公开字典（去除敏感信息）
        
        功能：将全局状态转换为可返回给前端的字典，会移除 secrets 字段
        返回：包含公开状态信息的字典
        """
        d = asdict(self)
        d["progress"] = self.progress.value
        debug = bool(getattr(config, "DEBUG_EXPOSE_FULL_STATE", False))
        if not debug:
            d["assets"] = {}
            d["story_state"] = strip_secrets(d.get("story_state", {}))
        else:
            d["story_state"] = strip_secrets(d.get("story_state", {}))
        return d

    def to_private_dict(self) -> dict:
        """
        转换为私有字典（包含完整信息）
        
        功能：将全局状态转换为包含所有信息的字典，用于持久化存储
        返回：包含完整状态信息的字典
        """
        d = asdict(self)
        d["progress"] = self.progress.value
        return d

    @staticmethod
    def from_private_dict(d: Any) -> "GlobalState":
        """
        从私有字典创建 GlobalState 对象
        
        功能：从持久化的字典数据中恢复全局状态对象
        参数：
            d: 字典数据
        返回：GlobalState 对象
        """
        gs = GlobalState()
        if not isinstance(d, dict):
            return gs
        p = d.get("progress", Progress.NOT_STARTED.value)
        if isinstance(p, str) and p in Progress._value2member_map_:
            gs.progress = Progress(p)
        gs.round_count = int(d.get("round_count", 0) or 0)
        gs.max_rounds = int(
            d.get("max_rounds", getattr(config, "MAX_ROUNDS", 20)) or getattr(config, "MAX_ROUNDS", 20)
        )
        gs.ended_reason = d.get("ended_reason")
        gs.game_type = d.get("game_type", "") or ""
        gs.outline = d.get("outline", "") or ""
        gs.script = d.get("script", {}) if isinstance(d.get("script"), dict) else {}
        gs.assets = d.get("assets", {}) if isinstance(d.get("assets"), dict) else {}
        gs.story_state = d.get("story_state", {}) if isinstance(d.get("story_state"), dict) else {}
        gs.direction = d.get("direction", "") or ""
        gs.language_code = d.get("language_code", "cn") or "cn"
        gs.current_chapter = int(d.get("current_chapter", 1) or 1)
        gs.chapters = d.get("chapters", []) if isinstance(d.get("chapters"), list) else []
        gs.chapter_goal_completed = bool(d.get("chapter_goal_completed", False))
        return gs

    def allowed_top_level_keys(self) -> List[str]:
        """
        返回允许的顶层字段名
        
        注意：现在使用固定的 StateSchema，但为了兼容性，
        如果 story_state 已存在，则返回已存在的键（这样模型只能更新已存在的字段）
        """
        if isinstance(self.story_state, dict) and self.story_state:
            # 返回已存在的键（这样模型只能更新已存在的字段，不能新增）
            return list(self.story_state.keys())
        # 如果 story_state 为空，返回 schema 中定义的键（用于世界构建器参考）
        return list(StateSchema.get_allowed_top_level_keys())


@dataclass
class Message:
    role: str  # "player" or "ai"
    player_name: str
    content: str
    is_system: bool = False

    def to_dict(self) -> dict:
        """
        转换为字典
        
        功能：将消息对象转换为字典格式
        返回：包含消息信息的字典
        """
        return {
            "role": self.role,
            "player_name": self.player_name,
            "content": self.content,
            "is_system": self.is_system,
        }

    @staticmethod
    def from_dict(d: Any) -> "Message":
        """
        从字典创建 Message 对象
        
        功能：从字典数据中恢复消息对象
        参数：
            d: 字典数据
        返回：Message 对象
        """
        if not isinstance(d, dict):
            return Message(role="ai", player_name="主持人", content="（坏消息）", is_system=True)
        return Message(
            role=d.get("role", "ai"),
            player_name=d.get("player_name", "主持人"),
            content=d.get("content", ""),
            is_system=bool(d.get("is_system", False)),
        )


@dataclass
class Game:
    global_state: GlobalState = field(default_factory=GlobalState)
    messages: List[Message] = field(default_factory=list)
    narrative_state: Optional["NarrativeState"] = None
    state_change_log: List[Dict[str, Any]] = field(default_factory=list)
    event_log: List[Dict[str, Any]] = field(default_factory=list)
    last_turn_response: Optional[Dict[str, Any]] = None  # 保存最后一条LLM返回的原始数据
    all_dialogues: List[Dict[str, Any]] = field(default_factory=list)  # 保留字段用于向后兼容，但不再使用（dialogues只存当前轮次NPC对话）

    def to_snapshot(self) -> dict:
        """
        转换为快照字典（用于持久化）
        
        功能：将游戏状态转换为可持久化的快照字典
        返回：包含游戏完整状态的字典
        """
        snap = {
            "global_state": self.global_state.to_private_dict(),
            "messages": [m.to_dict() for m in self.messages],
        }
        if self.narrative_state is not None:
            snap["narrative_state"] = self.narrative_state.to_dict()
        if self.state_change_log:
            snap["state_change_log"] = self.state_change_log
        if self.event_log:
            snap["event_log"] = self.event_log
        if self.last_turn_response:
            snap["last_turn_response"] = self.last_turn_response
        if self.all_dialogues:
            snap["all_dialogues"] = self.all_dialogues
        return snap

    @staticmethod
    def from_snapshot(s: Any) -> "Game":
        """
        从快照字典创建 Game 对象
        
        功能：从持久化的快照数据中恢复游戏对象
        参数：
            s: 快照字典数据
        返回：Game 对象
        """
        g = Game()
        if not isinstance(s, dict):
            return g
        g.global_state = GlobalState.from_private_dict(s.get("global_state", {}))
        msgs = s.get("messages", [])
        if isinstance(msgs, list):
            g.messages = [Message.from_dict(x) for x in msgs]
        ns_raw = s.get("narrative_state")
        if isinstance(ns_raw, dict):
            try:
                g.narrative_state = NarrativeState.from_dict(ns_raw)
            except Exception:
                g.narrative_state = None
        g.state_change_log = s.get("state_change_log", [])
        if not isinstance(g.state_change_log, list):
            g.state_change_log = []
        g.event_log = s.get("event_log", [])
        if not isinstance(g.event_log, list):
            g.event_log = []
        g.last_turn_response = s.get("last_turn_response")
        g.all_dialogues = s.get("all_dialogues", [])
        if not isinstance(g.all_dialogues, list):
            g.all_dialogues = []
        return g


# =========================
# manager（方案 A：锁内 read -> modify -> write）
# =========================
class GameManager:
    def __init__(self):
        """
        初始化游戏管理器

        功能：初始化游戏管理器，设置 OpenAI 客户端、模型配置。
        每个 group_id 对应独立的 Redis 键，实现群级别的游戏隔离。
        """
        http_client = httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=10.0))
        self.client = AsyncOpenAI(
            api_key=config.OPENAI_API_KEY,
            base_url=config.OPENAI_BASE_URL,
            http_client=http_client,
        )

        self.world_model = getattr(config, "STORY_WORLD_MODEL", config.OPENAI_MODEL)
        self.turn_model = getattr(config, "STORY_TURN_MODEL", config.OPENAI_MODEL)

        logger.info(f"🚀 GameManager initialized, using Redis for persistence")

    # ---------- group_id Redis键工具 ----------
    @staticmethod
    def _sanitize_group_id(group_id: str) -> str:
        """只保留字母/数字/下划线/连字符，防止键名冲突"""
        return re.sub(r"[^\w\-]", "_", group_id or "default")

    def _redis_game_key(self, group_id: str) -> str:
        """兼容旧键：game:snapshot（迁移时使用）"""
        return f"game:snapshot:{self._sanitize_group_id(group_id)}"

    def _redis_meta_key(self, group_id: str) -> str:
        """生成游戏元数据的 Redis 键名（长期存储）"""
        return f"game:meta:{self._sanitize_group_id(group_id)}"

    def _redis_messages_key(self, group_id: str) -> str:
        """生成游戏消息的 Redis 键名（TTL 5 天，最多 15 条）"""
        return f"game:messages:{self._sanitize_group_id(group_id)}"

    def _redis_lock_key(self, group_id: str) -> str:
        """生成分布式锁的Redis键名"""
        return f"game:lock:{self._sanitize_group_id(group_id)}"

    # ---------- thread-local game 属性 ----------
    @property
    def game(self) -> Optional[Game]:
        """当前请求线程正在处理的 Game 实例（线程安全）"""
        return getattr(_tls, "game", None)

    @game.setter
    def game(self, value: Optional[Game]) -> None:
        _tls.game = value

    # ---------- txn (方案 A 核心，按 group_id 隔离) ----------
    async def _with_txn_for_group(self, group_id: str, fn: Callable[[], T]) -> T:
        """
        单次请求事务（按 group_id 隔离，保证数据一致性）

        流程：
            1. 获取该群专属Redis分布式锁
            2. 从Redis加载状态到线程局部变量
            3. 执行业务逻辑
            4. 将线程局部变量持久化回Redis
        """
        lock_key = self._redis_lock_key(group_id)

        async def _txn():
            await self._load_snapshot_from_redis(group_id)
            result = await fn()
            await self._persist_to_redis(group_id)
            return result

        return await async_with_redis_lock(lock_key, _txn)

    # ---------- 统一日志（流程清晰，状态不重复） ----------
    def _log_flow(self, stage: str, detail: str = "") -> None:
        """
        记录流程节点日志
        
        功能：记录游戏流程中的关键阶段和说明信息
        参数：
            stage: 流程阶段名称
            detail: 详细说明（可选）
        """
        msg = f"[流程] {stage}"
        if detail:
            msg += f" | {detail}"
        logger.info(msg)

    def _log_state_summary(self, action: str = "") -> None:
        """
        记录状态摘要日志
        
        功能：统一记录游戏层、叙事层、剧情层的状态摘要信息
        参数：
            action: 触发该日志记录的动作名称
        """
        if not self.game:
            logger.info(f"[状态] {action} | 游戏未初始化")
            return
        gs = self.game.global_state
        lines = [f"[状态] {action}"]
        lines.append(f"  [游戏] progress={gs.progress.value} round={gs.round_count}/{gs.max_rounds} ended={gs.ended_reason or '-'}")
        if self.game.narrative_state:
            ns = self.game.narrative_state
            r = ns.relationship
            lines.append(
                f"  [叙事] phase={ns.phase_value} risk={ns.risk_level.value} "
                f"disclosure={ns.disclosure_level.value} rel(trust={r.trust:.1f} hostility={r.hostility:.1f})"
            )
        if gs.story_state:
            parts = []
            for k, v in gs.story_state.items():
                if isinstance(v, dict):
                    sub = ",".join(f"{sk}={v.get(sk)}" for sk in list(v.keys())[:4])
                    parts.append(f"{k}({sub})")
            lines.append(f"  [剧情] {' '.join(parts)}")
        logger.info("\n".join(lines))

    def _log_story_delta(self, round_num: int, delta: dict, applied: bool) -> None:
        """
        记录剧情状态变更日志

        功能：记录每回合剧情状态的变化项，只输出变更部分
        参数：
            round_num: 回合编号
            delta: 状态变更字典
            applied: 是否已应用变更
        """
        if not delta:
            logger.info(f"[剧情变更] 回合{round_num} 无变化")
            return
        parts = [f"{tk}.{k}={v}" for tk, kv in delta.items() if isinstance(kv, dict) for k, v in kv.items()]
        status = "已应用" if applied else "校验后为空"
        logger.info(f"[剧情变更] 回合{round_num} {status}: {' '.join(parts)}")

    # ---------- aigc_generate ----------
    # 第 2 回合、第 5 回合及之后每 5 回合触发；多种类型时按触发次序交替
    # _AIGC_GENERATE_VALUES = ("game_image", "game_video_with_audio_self")
    _AIGC_GENERATE_VALUES = ("game_video_with_audio_self",)

    @staticmethod
    def _pick_aigc_generate(round_count: int) -> Optional[str]:
        """
        根据当前回合数决定是否下发 aigc_generate 指令。

        规则：第 2 回合触发一次，第 5 回合触发，之后每 5 回合触发一次（第 5、10、15… 轮）。
        多种类型时按触发次序交替返回。
        返回 None 表示本轮不触发。
        """
        if round_count <= 0:
            return None
        values = GameManager._AIGC_GENERATE_VALUES
        if round_count == 2:
            return values[0]
        if round_count >= 5 and round_count % 5 == 0:
            idx = (round_count // 5 - 1) % len(values)
            return values[idx]
        return None

    # ---------- persistence ----------
    async def _persist_to_redis(self, group_id: str) -> None:
        """将当前线程的 game 状态持久化到 Redis：元数据长期存，消息单独 key、TTL 5 天、最多 15 条"""
        if not self.game:
            return

        if redis_dao.redis is None:
            await redis_dao.init_pools()

        self.game.messages = self.game.messages[-config.GAME_MESSAGES_MAX:]
        snapshot = self.game.to_snapshot()
        meta = {k: v for k, v in snapshot.items() if k != "messages"}
        messages_payload = [m.to_dict() for m in self.game.messages]

        meta_key = self._redis_meta_key(group_id)
        messages_key = self._redis_messages_key(group_id)

        await redis_dao.redis.set(meta_key, json.dumps(meta, ensure_ascii=False))
        await redis_dao.redis.set(
            messages_key,
            json.dumps(messages_payload, ensure_ascii=False),
            ex=config.GAME_MESSAGES_TTL_SECONDS,
        )
        logger.debug(f"📁 Game state persisted: meta={meta_key}, messages={messages_key}")

    async def _load_snapshot_from_redis(self, group_id: str) -> None:
        """从 Redis 加载快照到线程局部变量：先读 meta，再读 messages；支持旧键迁移；读到时刷新消息 TTL"""
        if redis_dao.redis is None:
            await redis_dao.init_pools()

        meta_key = self._redis_meta_key(group_id)
        messages_key = self._redis_messages_key(group_id)

        try:
            meta_json = await redis_dao.redis.get(meta_key)
            if meta_json is None:
                legacy_key = self._redis_game_key(group_id)
                legacy_json = await redis_dao.redis.get(legacy_key)
                if legacy_json is not None:
                    snapshot = json.loads(legacy_json)
                    self.game = Game.from_snapshot(snapshot)
                    await self._persist_to_redis(group_id)
                    await redis_dao.redis.delete(legacy_key)
                    logger.debug(f"📁 Migrated from legacy key to meta+messages: {group_id}")
                    return
                self.game = None
                logger.debug(f"📁 No game state found for group_id: {group_id}")
                return

            meta = json.loads(meta_json)
            messages_json = await redis_dao.redis.get(messages_key)
            if messages_json is not None:
                meta["messages"] = json.loads(messages_json)
                await redis_dao.redis.expire(messages_key, config.GAME_MESSAGES_TTL_SECONDS)
            else:
                meta["messages"] = []
            meta["messages"] = meta["messages"][-config.GAME_MESSAGES_MAX:]

            self.game = Game.from_snapshot(meta)
            logger.debug(f"📁 Game state loaded: meta={meta_key}, messages={messages_key}")
        except Exception as e:
            logger.warning(f"load snapshot from redis failed: {e} (group_id={group_id})")
            self.game = None

    # ---------- openai ----------
    async def _call_openai(self, model: str, messages: list, temperature: float) -> str:
        """
        调用 OpenAI API

        功能：向 OpenAI API 发送请求并获取响应
        参数：
            model: 模型名称
            messages: 消息列表
            temperature: 温度参数（控制随机性）
        返回：模型返回的文本内容
        """
        resp = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return resp.choices[0].message.content or ""

    async def _generate_outline(self, user_input: str, game_type: str = "", language_code: str = "cn") -> str:
        """
        根据用户输入的几句话生成剧情大纲
        
        功能：使用大模型根据用户的简短输入生成详细的剧情游戏大纲
        参数：
            user_input: 用户输入的几句话或关键词
            game_type: 游戏类型（可选）
            language_code: 语言代码（cn=中文, en=英文）
        返回：生成的剧情大纲文本
        """
        logger.info(f"📝 开始生成大纲，用户输入: {user_input[:100]}, game_type: {game_type}, language: {language_code}")
        raw = await self._call_openai(
            model=self.world_model,
            messages=[
                {"role": "system", "content": OUTLINE_GENERATOR_SYSTEM_PROMPT},
                {"role": "user", "content": build_outline_prompt(user_input, game_type, language_code)},
            ],
            temperature=0.7,
        )
        outline = raw.strip() if raw else ""
        if not outline:
            outline = f"基于以下想法构建的剧情游戏：\n{user_input}\n\n（请在此基础上补充详细设定）"
        logger.info(f"📝 大纲生成完成，长度: {len(outline)}")
        return outline

    async def _generate_script(self, outline: str, game_type: str = "", language_code: str = "cn") -> dict:
        """
        根据大纲生成游戏剧本
        
        功能：使用大模型根据剧情大纲生成包含大纲、背景故事、章节、角色的完整剧本
        参数：
            outline: 剧情大纲文本
            game_type: 游戏类型
            language_code: 语言代码（cn=中文, en=英文）
        返回：生成的剧本字典
        """
        logger.info(f"📜 开始生成剧本，大纲长度: {len(outline)}, game_type: {game_type}, language: {language_code}")
        raw = await self._call_openai(
            model=self.world_model,
            messages=[
                {"role": "system", "content": SCRIPT_GENERATOR_SYSTEM_PROMPT},
                {"role": "user", "content": build_script_prompt(outline, game_type, language_code)},
            ],
            temperature=0.2,
        )
        script, err = extract_first_json_object(raw)
        if script is None:
            logger.warning(f"script generator parse failed: {err}")
            # 返回默认剧本结构
            script = {
                "outline": {
                    "introduction": outline,
                    "info": "剧情游戏",
                    "rules": "根据剧情推进游戏"
                },
                "background": {
                    "relationships": []
                },
                "chapters": [],
                "characters": []
            }
        else:
            # 验证和规范化剧本结构
            is_valid, error_msg = validate_script_structure(script)
            if not is_valid:
                logger.warning(f"剧本结构验证失败: {error_msg}，进行规范化")
                script = normalize_script(script)
            else:
                script = normalize_script(script)
        
        logger.info(f"📜 剧本生成完成，包含 {len(script.get('characters', []))} 个角色，{len(script.get('chapters', []))} 个章节")
        return script

    def _fallback_world(self) -> dict:
        """
        生成备用世界（当世界构建失败时使用）
        
        功能：当世界构建器失败时，返回一个符合 schema 的默认世界结构
        返回：包含 assets、initial_state 等字段的字典
        """
        template = StateSchema.create_initial_state_template()
        template["player"]["hp"] = 100
        template["player"]["max_hp"] = 100
        template["player"]["level"] = 1
        template["player"]["status"] = "迷茫"
        template["player"]["name"] = "玩家"
        template["world"]["scene"] = "黑暗房间"
        template["world"]["time"] = "未知"
        template["world"]["location"] = "未知"
        
        return {
            "assets": {"style": "fallback", "notes": "world builder failed"},
            "initial_state": template,
            "player_facing_introduction": "（世界构建失败：进入 fallback 故事）",
            "first_scene_prompt": "你在一间黑暗房间醒来，门缝漏出冷光。你要做什么？",
        }

    async def _build_world(self, script: dict, game_type: str = "", language_code: str = "cn") -> dict:
        """
        构建游戏世界

        功能：根据游戏剧本使用大模型生成游戏世界资产和初始状态
        参数：
            script: 游戏剧本字典（包含大纲、背景故事、章节、角色）
            game_type: 游戏类型
            language_code: 语言代码（cn=中文, en=英文）
        返回：包含 assets、initial_state、chapters 等字段的字典
        """
        logger.info(f"🌍 开始构建世界，剧本包含 {len(script.get('characters', []))} 个角色，{len(script.get('chapters', []))} 个章节，language: {language_code}")
        raw = await self._call_openai(
            model=self.world_model,
            messages=[
                {"role": "system", "content": WORLD_BUILDER_SYSTEM_PROMPT},
                {"role": "user", "content": build_world_builder_prompt(script, game_type, language_code)},
            ],
            temperature=0.2,
        )
        obj, err = extract_first_json_object(raw)
        if obj is None:
            logger.warning(f"world builder parse failed: {err}")
            return self._fallback_world()

        if not isinstance(obj.get("assets"), dict):
            obj["assets"] = {}
        genre = (obj.get("game_genre") or "story")
        if not isinstance(genre, str) or genre not in ("mystery", "romance", "exploration", "adventure", "story", "mixed"):
            genre = "story"
        obj["assets"]["game_genre"] = genre
        if not isinstance(obj.get("initial_state"), dict) or not obj["initial_state"]:
            obj["initial_state"] = self._fallback_world()["initial_state"]
        if not isinstance(obj.get("player_facing_introduction"), str):
            obj["player_facing_introduction"] = "欢迎来到剧情游戏。"
        if not isinstance(obj.get("first_scene_prompt"), str):
            obj["first_scene_prompt"] = "故事开始了。你要做什么？"
        
        # 验证和初始化章节列表
        # 优先使用剧本中的章节信息
        script_chapters = []
        if isinstance(script, dict):
            script_chapters = script.get("chapters", [])
        game_info = get_game_type_info(game_type)
        has_chapters = game_info.get("has_chapters", False)
        
        if has_chapters and script_chapters:
            # 如果有章节要求且剧本中有章节，从剧本中提取章节信息
            chapters = []
            for ch in script_chapters:
                ch_num = ch.get("number", len(chapters) + 1)
                ch_intro = ch.get("introduction", "")
                chapters.append({
                    "title": f"第{ch_num}章",
                    "goal": ch_intro[:50] if ch_intro else f"完成第{ch_num}章",
                    "description": ch_intro
                })
            if chapters:
                obj["chapters"] = chapters
        
        # 如果世界构建器返回了章节，使用它；否则检查是否需要默认章节
        if not isinstance(obj.get("chapters"), list) or len(obj.get("chapters", [])) == 0:
            if has_chapters:
                # 有章节要求的游戏，生成默认章节
                obj["chapters"] = [
                    {"title": "第一章：开端", "goal": "了解基本情况和目标", "description": "故事开始，熟悉环境和角色"},
                    {"title": "第二章：发展", "goal": "推进主要剧情", "description": "深入故事，面对挑战"},
                    {"title": "第三章：高潮", "goal": "解决核心冲突", "description": "故事达到高潮，做出关键选择"},
                    {"title": "第四章：结局", "goal": "完成故事", "description": "根据选择迎来结局"}
                ]
            else:
                # 无章节要求的游戏，章节列表为空
                obj["chapters"] = []

        # 验证 initial_state 是否符合 schema（至少包含 player 和 world）
        initial_state = obj.get("initial_state", {})
        if not isinstance(initial_state, dict):
            initial_state = self._fallback_world()["initial_state"]
            obj["initial_state"] = initial_state
        
        # 确保至少包含 player 和 world（必需字段）
        if "player" not in initial_state:
            logger.warning("⚠️ initial_state 缺少 'player' 字段，使用 fallback")
            fallback = self._fallback_world()["initial_state"]
            initial_state["player"] = fallback.get("player", {})
        if "world" not in initial_state:
            logger.warning("⚠️ initial_state 缺少 'world' 字段，使用 fallback")
            fallback = self._fallback_world()["initial_state"]
            initial_state["world"] = fallback.get("world", {})
        
        # 章节类游戏：确保包含 chapter 字段
        if game_type == "story_chapter":
            if "chapter" not in initial_state:
                logger.warning("⚠️ 章节类游戏缺少 'chapter' 字段，自动添加")
                initial_state["chapter"] = {
                    "current_chapter": 1,
                    "chapter_progress": "刚开始",
                    "chapter_goal_completed": False
                }
            else:
                # 验证 chapter 字段的完整性
                chapter = initial_state.get("chapter", {})
                if not isinstance(chapter, dict):
                    chapter = {}
                if "current_chapter" not in chapter:
                    chapter["current_chapter"] = 1
                if "chapter_progress" not in chapter:
                    chapter["chapter_progress"] = "刚开始"
                if "chapter_goal_completed" not in chapter:
                    chapter["chapter_goal_completed"] = False
                initial_state["chapter"] = chapter
                logger.info("🔧 章节类游戏：已确保 chapter 字段完整")
        
        # 角色类游戏特殊处理：移除 player 中的 hp 和 max_hp 字段
        if game_type in ("companion_route", "companion_open"):
            if isinstance(initial_state.get("player"), dict):
                player = initial_state["player"]
                if "hp" in player:
                    del player["hp"]
                    logger.info("🔧 角色类游戏：已移除 player.hp 字段")
                if "max_hp" in player:
                    del player["max_hp"]
                    logger.info("🔧 角色类游戏：已移除 player.max_hp 字段")
            
            # 确保只有一个 NPC
            if "npc" in initial_state:
                # 如果 npc 是列表，只保留第一个
                if isinstance(initial_state["npc"], list):
                    if len(initial_state["npc"]) > 0:
                        initial_state["npc"] = initial_state["npc"][0]
                        logger.info("🔧 角色类游戏：已确保只有一个 NPC")
                    else:
                        logger.warning("⚠️ 角色类游戏：NPC 列表为空")
                # 如果 npc 是字典，保持不变
                elif not isinstance(initial_state["npc"], dict):
                    logger.warning("⚠️ 角色类游戏：NPC 格式不正确，应为字典")

        logger.info(f"🌍 世界构建完成，assets 键: {list(obj.get('assets', {}).keys())}, initial_state 键: {list(obj.get('initial_state', {}).keys())}")
        logger.info(f"🌍 initial_state 结构验证: player={bool(initial_state.get('player'))}, world={bool(initial_state.get('world'))}, npc={bool(initial_state.get('npc'))}")
        return obj

    def _compact_assets_for_turn(self, assets: Dict[str, Any]) -> Dict[str, Any]:
        """
        压缩资产用于回合引擎（移除 secrets）
        
        功能：移除资产中的 secrets 字段，准备发送给回合引擎
        参数：
            assets: 原始资产字典
        返回：移除 secrets 后的资产字典
        """
        if not isinstance(assets, dict):
            return {}
        return strip_secrets(assets)

    def _recent_log(self, limit: int = 10) -> List[Dict[str, str]]:
        """
        获取最近的对话记录
        
        功能：获取最近 N 条消息，转换为回合引擎需要的格式
        参数：
            limit: 返回的消息数量上限
        返回：消息字典列表，格式为 [{"role": "user/assistant", "content": "..."}]
        """
        if not self.game:
            return []
        msgs = self.game.messages[-limit:]
        out = []
        for m in msgs:
            role = "assistant" if m.role == "ai" else "user"
            out.append({"role": role, "content": f"{m.player_name}: {m.content}"})
        return out

    # ---------- public API ----------
    async def start_game(self, group_id: str, game_type: str = "", text: str = "", language_code: str = "cn") -> dict:
        """
        开始新游戏（按 group_id 隔离）

        参数：
            group_id: 群 ID（决定使用哪个快照）
            game_type: 游戏类型（可选）
            text: 初始文本（可选）
            language_code: 语言代码（cn=中文, en=英文，默认cn）
        返回：包含游戏状态的字典
        """
        async def _impl():
            self.game = Game()
            gs = self.game.global_state
            gs.progress = Progress.AWAITING_INITIAL_INPUT
            gs.round_count = 0
            gs.max_rounds = getattr(config, "MAX_ROUNDS", 20)
            gs.ended_reason = None
            gs.game_type = game_type or ""
            gs.language_code = language_code or "cn"  # 保存语言代码到状态
            gs.outline = ""
            gs.script = {}
            gs.assets = {}
            gs.story_state = {}
            gs.direction = ""
            gs.current_chapter = 1
            gs.chapters = []
            gs.chapter_goal_completed = False

            # 如果提供了游戏类型和文本，直接开始生成流程
            if game_type and text:
                if not is_valid_game_type(game_type):
                    return {"error": f"无效的游戏类型: {game_type}"}

                gs.game_type = game_type
                # 直接生成大纲
                generated_outline = await self._generate_outline(text, game_type, gs.language_code)
                gs.outline = generated_outline
                gs.progress = Progress.AWAITING_OUTLINE_REVIEW

                outline_msg = get_system_message("outline_generated", gs.language_code, outline=generated_outline)
                self.game.messages.append(
                    Message(role="ai", player_name="主持人", content=outline_msg, is_system=False)
                )
                self.game.last_turn_response = {
                    "transition": "", "narration": "", "sound": "",
                    "dialogues": [], "hooks": {"player_goal": ""}
                }
                self._log_flow("大纲生成完成", "等待用户审核/修改")
                return self._build_status_response()

            start_msg = get_system_message("game_started", gs.language_code)
            self.game.messages.append(
                Message(role="ai", player_name="主持人", content=start_msg, is_system=True)
            )
            # 更新 last_turn_response
            self.game.last_turn_response = {
                "transition": "", "narration": "", "sound": "",
                "dialogues": [], "hooks": {"player_goal": ""}
            }
            self._log_flow("开始游戏", "等待玩家输入初始想法")
            return self._build_status_response()

        return await self._with_txn_for_group(group_id, _impl)

    async def send_message(self, group_id: str, text: str, player_name: str = "玩家", language_code: str = "en") -> dict:
        """
        发送玩家消息并推进游戏（按 group_id 隔离）
        
        参数：
            group_id: 群 ID
            text: 玩家输入的文本
            player_name: 玩家名称（默认为"玩家"）
        返回：包含更新后游戏状态的字典
        """
        text = (text or "").strip()
        if not text:
            return {"error": "请输入内容"}

        async def _impl():
            s = time.time()   # 记录开始时间
            # 捕获外部作用域的变量，避免闭包作用域问题
            nonlocal text, player_name, language_code
            
            if not self.game:
                return {"error": "游戏未开始"}

            gs = self.game.global_state
            if gs.progress == Progress.ENDED:
                return {"error": "游戏已结束"}

            # 记录玩家消息
            self.game.messages.append(Message(role="player", player_name=player_name, content=text))
            gs.language_code = language_code
            # 1) 等待初始输入：生成大纲
            if gs.progress == Progress.AWAITING_INITIAL_INPUT:
                generated_outline = await self._generate_outline(text, gs.game_type, gs.language_code)
                gs.outline = generated_outline
                gs.progress = Progress.AWAITING_OUTLINE_REVIEW
                
                outline_msg = get_system_message("outline_generated", gs.language_code, outline=generated_outline)
                self.game.messages.append(
                    Message(
                        role="ai",
                        player_name="主持人",
                        content=outline_msg,
                        is_system=False,
                    )
                )
                # 更新 last_turn_response
                self.game.last_turn_response = {
                    "transition": "",
                    "narration": "",
                    "sound": "",
                    "dialogues": [],
                    "hooks": {"player_goal": ""}
                }
                self._log_flow("大纲生成完成", "等待用户审核/修改")
                return self._build_status_response()

            # 2) 等待大纲审核：用户确认或修改
            if gs.progress == Progress.AWAITING_OUTLINE_REVIEW:
                # 检查是否是确认指令
                text_lower = text.lower().strip()
                if text_lower in ("确认", "开始", "ok", "yes", "确认生成", "开始游戏", "生成游戏"):
                    # 使用当前大纲生成游戏
                    final_outline = gs.outline
                    # 添加确认提示消息
                    confirm_msg = get_system_message("confirm_generating", gs.language_code)
                    self.game.messages.append(
                        Message(
                            role="ai",
                            player_name="主持人",
                            content=confirm_msg,
                            is_system=True,
                        )
                    )
                else:
                    # 用户修改了大纲，更新 outline
                    final_outline = text
                    gs.outline = text
                    update_msg = get_system_message("outline_updated", gs.language_code)
                    self.game.messages.append(
                        Message(
                            role="ai",
                            player_name="主持人",
                            content=update_msg,
                            is_system=False,
                        )
                    )
                    # 更新 last_turn_response
                    self.game.last_turn_response = {
                        "transition": "",
                        "narration": "",
                        "sound": "",
                        "dialogues": [],
                        "hooks": {"player_goal": ""}
                    }
                    self._log_flow("大纲已更新", "等待用户确认")
                    return self._build_status_response()
                
                # 确认后先生成剧本，再构建世界
                script = await self._generate_script(final_outline, gs.game_type, gs.language_code)
                gs.script = script

                # 构建世界
                built = await self._build_world(script, gs.game_type, gs.language_code)

                gs.assets = built.get("assets", {}) or {}
                gs.story_state = built.get("initial_state", {}) or {}
                gs.progress = Progress.IN_PROGRESS
                gs.round_count = 0
                gs.current_chapter = 1
                gs.chapters = built.get("chapters", []) or []
                gs.chapter_goal_completed = False
                _genre = gs.assets.get("game_genre", "story")
                self.game.narrative_state = init_narrative_state(genre=_genre)

                intro = (built.get("player_facing_introduction") or "").strip()
                first = (built.get("first_scene_prompt") or "").strip()

                if intro:
                    self.game.messages.append(Message(role="ai", player_name="主持人", content=intro, is_system=True))
                
                # 显示第一章开始提示
                if gs.chapters and len(gs.chapters) > 0:
                    chapter = gs.chapters[0]
                    chapter_title = chapter.get("title", "第一章")
                    chapter_goal = chapter.get("goal", "")
                    chapter_start_msg = f"📖 {chapter_title}：开始\n\n"
                    if chapter_goal:
                        chapter_start_msg += f"🎯 本章目标：{chapter_goal}\n\n"
                    chapter_start_msg += first
                    self.game.messages.append(Message(role="ai", player_name="主持人", content=chapter_start_msg, is_system=False))
                    
                    # 设置第一章开始的transition输出
                    self.game.last_turn_response = {
                        "transition": "chapter_1",
                        "narration": "",
                        "sound": "",
                        "dialogues": [],
                        "hooks": {"player_goal": ""}
                    }
                else:
                    self.game.messages.append(Message(role="ai", player_name="主持人", content=first, is_system=False))
                    # 更新 last_turn_response
                    self.game.last_turn_response = {
                        "transition": "",
                        "narration": "",
                        "sound": "",
                        "dialogues": [],
                        "hooks": {"player_goal": ""}
                    }

                self._log_flow("世界构建完成", f"genre={_genre} phase={self.game.narrative_state.phase_value}")
                self._log_state_summary("进入游戏")
                return self._build_status_response()

            # 2) 正常回合
            if gs.progress != Progress.IN_PROGRESS:
                return {"error": "游戏状态异常"}

            gs.round_count += 1

            _genre = gs.assets.get("game_genre", "story")

            # 叙事状态机：确保存在（兼容旧存档）
            if self.game.narrative_state is None:
                self.game.narrative_state = init_narrative_state(genre=_genre)
            ns = self.game.narrative_state
            old_ns_dict = ns.to_dict()

            # 规则引擎 + 事件检查
            updated_ns, triggered_events = update_and_get_events(ns, text, gs.round_count, genre=_genre)
            self.game.state_change_log.append({
                "round": gs.round_count,
                "from_state": old_ns_dict,
                "to_state": updated_ns.to_dict(),
                "reason": "rules_update",
            })
            self.game.narrative_state = updated_ns

            event_used = None
            if triggered_events:
                ev = triggered_events[0]
                mark_events_triggered(updated_ns, triggered_events)
                if ev.state_mutate:
                    apply_state_mutate(updated_ns, ev.state_mutate)
                self.game.event_log.append({
                    "round": gs.round_count,
                    "event_id": ev.event_id,
                    "narrative_snippet": ev.narrative_template[:100] if ev.narrative_template else "",
                })
                event_used = ev

            # 获取当前章节信息
            current_chapter_info = None
            if gs.chapters and len(gs.chapters) >= gs.current_chapter:
                current_chapter_info = gs.chapters[gs.current_chapter - 1]
            
            turn_input = {
                "assets": self._compact_assets_for_turn(gs.assets),
                "current_state": gs.story_state,
                "recent_log": self._recent_log(limit=12),
                "player_message": text,
                "game_type": gs.game_type,  # 添加游戏类型信息
            }
            if current_chapter_info:
                turn_input["current_chapter"] = current_chapter_info

            self._log_flow(f"回合 {gs.round_count} 开始", f"genre={_genre} phase={updated_ns.phase_value} risk={updated_ns.risk_level.value}")
            logger.info(f"[玩家] {text[:80]}{'...' if len(text) > 80 else ''}")

            # 即使事件触发也调用 LLM 推进剧情（事件仅记录，不替代 LLM 输出）
            director_prompt = build_director_prompt(updated_ns, genre=_genre)
            if event_used:
                director_prompt += f"\n\n【本回合触发事件】{event_used.event_id}：{event_used.narrative_template}\n请据此强化叙事氛围，但仍由你输出完整叙事推进剧情。"
                self._log_flow("事件触发", f"{event_used.event_id} → 注入导演提示，LLM 继续输出")

            # 根据 language_code 添加语言要求
            language_code = gs.language_code or "en"
            # language_map = {
            #     "cn": "中文",
            #     "en": "English",
            #     "zh": "中文",
            # }
            # language_name = language_map.get(language_code.lower(), "中文")
            # language_instruction = f"\n\n【重要语言要求】\n你必须使用language_code: {language_code}输出所有内容。包括：\n- narration（场景描述）\n- sound（声音描述）\n- dialogues[].text（NPC对话）\n- hooks.player_goal（行动建议）\n所有文本内容都必须使用 {language_code}，不得混用其他语言。"
            language_instruction = (
                f"\n\n【重要语言要求】\n"
                f"你必须使用language_code: {language_code}输出所有内容。包括：\n"
                f"- narration（场景描述）\n"
                f"- sound（声音描述）\n"
                f"- dialogues[].text（NPC对话）\n"
                f"- hooks.player_goal（行动建议）\n"
                f"所有文本内容都必须使用 {language_code}，不得混用其他语言。\n\n"
                f"【重要结构要求】\n"
                f"- dialogues 字段必须是一个数组，但最多只包含 1 条 NPC 对话；如果你有多句想说的话，请把它们合并到同一条 text 里，用换行或合适的分句连接。\n"
                f"- 严禁在同一轮输出多条 NPC 对话对象（即 dialogues.length 不能大于 1）。"
            )

            system_content = TURN_ENGINE_SYSTEM_PROMPT + language_instruction + "\n\n" + director_prompt
            start = time.time()
            raw = await self._call_openai(
                model=self.turn_model,
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": json.dumps(turn_input, ensure_ascii=False)},
                ],
                temperature=0.7,
            )
            logger.info(f"---------- LLM耗时: {time.time() - start:.2f}s -------------")
            out, err = extract_first_json_object(raw)
            if out is None:
                logger.warning(f"turn engine parse failed: {err}")
                out = {}
            
            # 提取数据（确保所有字段都存在）
            transition = out.get("transition", "")
            narrative = out.get("narration", "")
            sound = out.get("sound", "")
            dialogues = out.get("dialogues", [])
            hooks = out.get("hooks", {})
            state_delta_raw = out.get("state_delta", {})
            flags = out.get("flags", {})
            
            # 确保所有字段都有默认值
            if not isinstance(transition, str):
                transition = ""
            if not isinstance(narrative, str):
                narrative = ""
            if not isinstance(sound, str):
                sound = ""
            if not isinstance(dialogues, list):
                dialogues = []

            # 强制限定：每轮最多只保留 1 条 NPC 对话，避免模型输出多条导致前端展示两轮
            if isinstance(dialogues, list) and len(dialogues) > 1:
                logger.warning(
                    f"[turn_engine] dialogues 超过 1 条（{len(dialogues)}），仅保留第一条。"
                )
                dialogues = dialogues[:1]
            if not isinstance(hooks, dict):
                hooks = {}
            if not isinstance(hooks.get("player_goal"), str):
                hooks["player_goal"] = hooks.get("player_goal", "") or ""

            if gs.game_type in ("companion_route", "companion_open", "私聊角色类"):
                hooks = {}   # 角色陪伴类游戏 hooks 设为空

            # 保存最后一条LLM返回的原始数据（确保包含所有字段）
            # narration 字段只包含当前回合的旁白
            # dialogues 只包含当前轮次的NPC对话，不累加历史
            self.game.last_turn_response = {
                "transition": transition,
                "narration": narrative if narrative else "",  # 只包含当前回合的旁白
                # "sound": sound,
                "sound": "",
                "dialogues": dialogues if isinstance(dialogues, list) else [],  # 只包含当前轮次的NPC对话
                "hooks": hooks,
                "state_delta": state_delta_raw,
                "flags": flags
            }
            
            # 兼容旧格式（player_options）
            player_options = out.get("player_options", [])
            if not player_options and hooks and isinstance(hooks, dict):
                player_goal = hooks.get("player_goal", "")
                if player_goal:
                    player_options = [player_goal]
            
            chapter_goal_completed = flags.get("chapter_goal_completed", False)
            updated_ns = apply_post_turn_updates(updated_ns, state_delta_raw or out)
            self.game.narrative_state = updated_ns
            
            # 记录日志
            if transition:
                self._log_flow("LLM 返回", f"transition={transition}")
            if dialogues:
                self._log_flow("LLM 返回", f"dialogues={len(dialogues)}条")
            if narrative:
                self._log_flow("LLM 返回", f"narration={len(narrative)}字 sound={sound}")
            self._log_flow("LLM 返回", f"game_ended={flags.get('game_ended', False)}")

            # 剧情状态合并（校验 + 应用）
            validated_delta = {}
            if isinstance(state_delta_raw, dict):
                validated_delta = StateSchema.validate_state_delta(state_delta_raw, gs.story_state)
                if validated_delta:
                    gs.story_state = safe_merge_state(gs.story_state, validated_delta)
            shown = validated_delta if validated_delta else (state_delta_raw if isinstance(state_delta_raw, dict) else {})
            self._log_story_delta(gs.round_count, shown, bool(validated_delta))
            
            # 检查角色攻略类游戏的好感度满值
            if gs.game_type == "companion_route" and gs.story_state.get("npc"):
                npc = gs.story_state.get("npc", {})
                if isinstance(npc, dict) and "affection" in npc:
                    affection = npc.get("affection", 0)
                    if affection >= 100:
                        # 好感度满值，结束游戏
                        if not isinstance(flags, dict):
                            flags = {}
                        flags["game_ended"] = True
                        flags["reason"] = "affection_max"
                        self._log_flow("好感度满值", f"好感度达到 {affection}，游戏结束")

            # 输出到聊天（构建消息内容）
            if transition:
                # 章节转换，添加章节提示
                # 从 transition 中提取章节编号（如 "chapter_2" -> 2）
                if transition.startswith("chapter_") and len(transition) > 8:
                    try:
                        transition_chapter = int(transition[8:])
                        # 如果章节编号发生变化，同步更新 story_state
                        if gs.game_type == "story_chapter" and transition_chapter != gs.current_chapter:
                            if "chapter" not in gs.story_state:
                                gs.story_state["chapter"] = {}
                            gs.story_state["chapter"]["current_chapter"] = transition_chapter
                            gs.story_state["chapter"]["chapter_progress"] = "刚开始"
                            gs.story_state["chapter"]["chapter_goal_completed"] = False
                            logger.info(f"🔧 章节类游戏：transition触发，已同步更新 story_state.chapter.current_chapter = {transition_chapter}")
                    except ValueError:
                        pass
                
                chapter_num = gs.current_chapter
                if gs.chapters and len(gs.chapters) >= chapter_num:
                    chapter = gs.chapters[chapter_num - 1]
                    chapter_title = chapter.get("title", f"第{chapter_num}章")
                    content = f"📖 {chapter_title}：开始"
                    if chapter.get("goal"):
                        content += f"\n🎯 本章目标：{chapter.get('goal')}"
                    self.game.messages.append(Message(role="ai", player_name="主持人", content=content, is_system=True))
            
            # 构建主要内容
            content_parts = []
            
            if narrative:
                content_parts.append(narrative.strip())
                if sound:
                    content_parts.append(f"[声音：{sound}]")
            
            if dialogues:
                dialogue_texts = []
                for d in dialogues:
                    name = d.get("name", "NPC")
                    dialogue_text = d.get("text", "")
                    if dialogue_text:
                        dialogue_texts.append(f"{name}：{dialogue_text}")
                if dialogue_texts:
                    content_parts.append("\n".join(dialogue_texts))
            
            if hooks and hooks.get("player_goal"):
                content_parts.append(f"\n你可以尝试：{hooks.get('player_goal')}")
            
            if content_parts:
                content = "\n".join(content_parts)
                self.game.messages.append(Message(role="ai", player_name="主持人", content=content))
            elif not transition:
                # 如果没有内容，使用默认提示
                content = f"📖 第 {gs.round_count} 回合：\n\n（等待剧情推进...）"
                self.game.messages.append(Message(role="ai", player_name="主持人", content=content))

            # 检查章节目标是否完成
            if chapter_goal_completed and not gs.chapter_goal_completed:
                gs.chapter_goal_completed = True
                
                # 同步更新 story_state 中的 chapter 字段（如果是章节类游戏）
                if gs.game_type == "story_chapter" and "chapter" in gs.story_state:
                    if not isinstance(gs.story_state["chapter"], dict):
                        gs.story_state["chapter"] = {}
                    gs.story_state["chapter"]["chapter_goal_completed"] = True
                    gs.story_state["chapter"]["chapter_progress"] = "已完成"
                    logger.info(f"🔧 章节类游戏：已同步更新 story_state.chapter.chapter_goal_completed = True")
                
                # 显示章节结束提示
                if current_chapter_info:
                    chapter_title = current_chapter_info.get("title", f"第{gs.current_chapter}章")
                    chapter_end_msg = f"✨ {chapter_title}：结束\n\n"
                    chapter_end_msg += f"🎉 恭喜！你已完成本章目标：{current_chapter_info.get('goal', '')}\n\n"
                    
                    # 检查是否有下一章节
                    if gs.chapters and len(gs.chapters) > gs.current_chapter:
                        # 先显示章节结束消息
                        self.game.messages.append(Message(role="ai", player_name="主持人", content=chapter_end_msg, is_system=True))
                        
                        # 进入下一章节
                        gs.current_chapter += 1
                        
                        # 同步更新 story_state 中的 chapter 字段
                        if gs.game_type == "story_chapter":
                            if "chapter" not in gs.story_state:
                                gs.story_state["chapter"] = {}
                            gs.story_state["chapter"]["current_chapter"] = gs.current_chapter
                            gs.story_state["chapter"]["chapter_progress"] = "刚开始"
                            gs.story_state["chapter"]["chapter_goal_completed"] = False
                            logger.info(f"🔧 章节类游戏：已同步更新 story_state.chapter.current_chapter = {gs.current_chapter}")
                        
                        next_chapter = gs.chapters[gs.current_chapter - 1]
                        next_title = next_chapter.get("title", f"第{gs.current_chapter}章")
                        next_goal = next_chapter.get("goal", "")
                        next_description = next_chapter.get("description", "")
                        
                        # 显示下一章节开始提示
                        next_chapter_start_msg = f"📖 {next_title}：开始\n\n"
                        if next_goal:
                            next_chapter_start_msg += f"🎯 本章目标：{next_goal}\n\n"
                        if next_description:
                            next_chapter_start_msg += f"{next_description}\n\n"
                        next_chapter_start_msg += "故事继续..."
                        
                        self.game.messages.append(Message(role="ai", player_name="主持人", content=next_chapter_start_msg, is_system=False))
                        gs.chapter_goal_completed = False  # 重置下一章节的完成状态
                        
                        # 设置章节转换的transition输出
                        self.game.last_turn_response = {
                            "transition": f"chapter_{gs.current_chapter}"
                        }
                        self._log_flow("章节完成", f"章节{gs.current_chapter - 1}完成，进入章节{gs.current_chapter}")
                    else:
                        chapter_end_msg += "🏁 所有章节已完成！故事即将迎来结局..."
                        self.game.messages.append(Message(role="ai", player_name="主持人", content=chapter_end_msg, is_system=True))
                        self._log_flow("章节完成", f"所有章节完成，游戏即将结束")

            # 打印每轮的 story_state
            logger.info(f"[story_state] 回合 {gs.round_count} 的 story_state:")
            logger.info(json.dumps(gs.story_state, ensure_ascii=False, indent=2))
            
            self._log_flow(f"回合 {gs.round_count} 完成", "持久化")
            _aigc = self._pick_aigc_generate(gs.round_count)
            if _aigc:
                logger.info(f"[aigc_generate] 回合 {gs.round_count} 触发 → {_aigc}")

            # flags 结束
            if isinstance(flags, dict) and flags.get("game_ended") is True:
                gs.progress = Progress.ENDED
                gs.ended_reason = flags.get("reason") or "game_ended"
                ending_id = ""
                if self.game.narrative_state:
                    ending_id = compute_ending_id(self.game.narrative_state, genre=_genre)
                
                # 根据结束原因生成不同的消息
                if gs.ended_reason == "affection_max":
                    npc_name = "角色"
                    if gs.story_state.get("npc") and isinstance(gs.story_state.get("npc"), dict):
                        npc_name = gs.story_state.get("npc", {}).get("name", "角色")
                    msg = f"💕 恭喜！你与{npc_name}的好感度已达到满值（100），达成了完美结局！"
                    if ending_id and ending_id != "ending_unknown":
                        msg += f"\n结局：{ending_id}"
                    msg += "\n\n你可以点击「开始游戏」重开。"
                else:
                    msg = f"🏁 故事结束（原因：{gs.ended_reason}）"
                    if ending_id and ending_id != "ending_unknown":
                        msg += f"。结局：{ending_id}"
                    msg += "。你可以点击「开始游戏」重开。"
                
                self.game.messages.append(
                    Message(role="ai", player_name="主持人", content=msg, is_system=True)
                )
                self._log_flow("游戏结束", f"AI判定 {gs.ended_reason}")

            # 回合数上限（已注释：暂时取消轮次限制）
            # if gs.round_count >= gs.max_rounds and gs.progress != Progress.ENDED:
            #     gs.progress = Progress.ENDED
            #     gs.ended_reason = "max_rounds"
            #     ending_id = ""
            #     if self.game.narrative_state:
            #         ending_id = compute_ending_id(self.game.narrative_state, genre=_genre)
            #     msg = f"⏰ 已到最大回合数 {gs.max_rounds}，故事在此收束"
            #     if ending_id and ending_id != "ending_unknown":
            #         msg += f"。结局：{ending_id}"
            #     msg += "。你可以点击「开始游戏」重开。"
            #     self.game.messages.append(
            #         Message(role="ai", player_name="主持人", content=msg, is_system=True)
            #     )
            #     self._log_flow("游戏结束", f"达到最大回合数 {gs.max_rounds}")

            resp = self._build_status_response()
            if _aigc:
                resp["aigc_generate"] = _aigc
            logger.info(f"---------- 总耗时: {time.time() - s:.2f}s -------------")
            return resp

        return await self._with_txn_for_group(group_id, _impl)

    async def end_game(self, group_id: str) -> dict:
        """
        手动结束游戏（按 group_id 隔离）
        
        参数：
            group_id: 群 ID
        返回：包含更新后游戏状态的字典
        """
        async def _impl():
            if not self.game:
                return {"error": "游戏未开始"}
            gs = self.game.global_state
            gs.progress = Progress.ENDED
            gs.ended_reason = "manual"
            self.game.messages.append(
                Message(
                    role="ai",
                    player_name="主持人",
                    content="🏁 已结束游戏。你可以点击「开始游戏」重开。",
                    is_system=True,
                )
            )
            self._log_flow("游戏结束", "手动结束")
            return self._build_status_response()

        return await self._with_txn_for_group(group_id, _impl)

    def _format_response_for_frontend(self) -> dict:
        """
        格式化返回给前端的数据
        
        功能：直接返回模型输出的格式，确保包含所有字段
        返回：包含 transition、narration、sound、dialogues（当前轮次NPC对话）、hooks 等所有字段的字典
        注意：dialogues只包含当前轮次的NPC对话，不累加历史，也不包含系统提示消息
        """
        if not self.game:
            return {
                "transition": "",
                "narration": "",
                "sound": "",
                "dialogues": [],
                "hooks": {}
            }
        
        # 如果有保存的模型原始输出，直接使用并确保所有字段存在
        if self.game.last_turn_response:
            response = self.game.last_turn_response
            
            result = {
                "transition": response.get("transition", "") or "",
                "narration": response.get("narration", "") or "",  # 只返回当前最新的旁白
                "sound": response.get("sound", "") or "",
                "dialogues": response.get("dialogues", []) if isinstance(response.get("dialogues"), list) else [],  # 只返回当前轮次的NPC对话
                "hooks": response.get("hooks", {}) or {}
            }
            
            # 确保 hooks 有 player_goal 字段
            if not isinstance(result["hooks"], dict):
                result["hooks"] = {}
            if "player_goal" not in result["hooks"]:
                result["hooks"]["player_goal"] = ""
            
            logger.info(f"[格式化] 返回完整格式: transition={bool(result['transition'])}, narration={len(result['narration'])}字, dialogues={len(result['dialogues'])}条当前轮次对话")
            print(f"[格式化输出] {json.dumps(result, ensure_ascii=False, indent=2)}")
            return result
        
        # 如果没有保存的模型输出
        result = {
            "transition": "",
            "narration": "",
            "sound": "",
            "dialogues": [],
            "hooks": {"player_goal": ""}
        }
        logger.warning("[格式化] 没有保存的模型输出，返回空字段")
        return result

    def _build_status_response(self) -> dict:
        """
        从当前线程的 self.game 构建状态响应（不访问磁盘）。
        供 txn 内部调用（game 已由 _load_snapshot_if_any 加载）。
        """
        if not self.game:
            gs = GlobalState(max_rounds=getattr(config, "MAX_ROUNDS", 20))
            return {
                "global_state": gs.to_public_dict(),
                "state": gs.progress.value,
                "round_count": gs.round_count,
                "max_rounds": gs.max_rounds,
                "messages": [],
            }

        gs = self.game.global_state
        
        # 获取新格式的响应数据
        frontend_format = self._format_response_for_frontend()
        
        # 合并基础字段和新格式数据
        result = {
            "global_state": gs.to_public_dict(),
            "state": gs.progress.value,
            "round_count": gs.round_count,
            "max_rounds": gs.max_rounds,
            "messages": [m.to_dict() for m in self.game.messages],
            "game_type": gs.game_type,
            "script": gs.script if gs.script else {},  # 返回剧本信息
        }
        
        # 将新格式数据合并到结果中（如果有的话）
        if frontend_format:
            result.update(frontend_format)
        return result

    async def get_status(self, group_id: str) -> dict:
        """
        获取指定群的游戏状态（公开接口，从Redis加载最新快照）

        参数：
            group_id: 群 ID
        返回：包含游戏状态的字典
        """
        await self._load_snapshot_from_redis(group_id)
        return self._build_status_response()

    async def get_narrative_state(self, group_id: str) -> dict:
        """
        获取指定群的叙事状态（调试接口）

        参数：
            group_id: 群 ID
        返回：包含 narrative_state 和 round 的字典
        """
        await self._load_snapshot_from_redis(group_id)
        if not self.game or self.game.narrative_state is None:
            return {"narrative_state": None, "round": 0}
        return {
            "narrative_state": self.game.narrative_state.to_dict(),
            "round": self.game.global_state.round_count,
        }

    async def get_narrative_log(self, group_id: str) -> dict:
        """
        获取指定群的叙事日志（调试接口）

        参数：
            group_id: 群 ID
        返回：包含 state_change_log 和 event_log 的字典
        """
        await self._load_snapshot_from_redis(group_id)
        if not self.game:
            return {"state_change_log": [], "event_log": []}
        return {
            "state_change_log": self.game.state_change_log,
            "event_log": self.game.event_log,
        }


    async def create_official_game(self, group_id: str, game_id: str, language_code: str = "cn"):
        """
        创建官方游戏（按 group_id 隔离）
        
        参数：
            group_id: 群 ID（决定使用哪个快照）
            game_id: 官方游戏 ID（映射游戏设定/提示词）
            language_code: 语言代码
        返回：包含游戏初始化信息的字典
        """
        async def _impl():
            # 1. 初始化游戏状态
            self.game = Game()
            gs = self.game.global_state
            gs.progress = Progress.AWAITING_INITIAL_INPUT
            gs.round_count = 0
            gs.max_rounds = getattr(config, "MAX_ROUNDS", 200)
            gs.ended_reason = None
            gs.language_code = language_code  # 保存语言代码到状态

            # 获取官方游戏设定
            prompts, game_type = get_official_game_prompt(game_id, "cn")  # 默认用中文设定
            gs.game_type = game_type

            # 2. 生成游戏大纲
            self._log_flow("官方游戏", f"开始生成大纲，game_id={game_id}, language={language_code}")
            generated_outline = await self._generate_outline(prompts, game_type, language_code)
            gs.outline = generated_outline
            gs.progress = Progress.AWAITING_OUTLINE_REVIEW
            
            # 3. 添加大纲消息（模拟 send_message 中的逻辑）
            outline_msg = (
                f"📝 我已根据你的输入生成了以下剧情大纲：\n\n"
                f"{generated_outline}\n\n"
                f"你可以直接发送「确认」或「开始」来使用这个大纲生成游戏，"
                f"或者发送修改后的大纲内容来替换它。"
            )
            self.game.messages.append(
                Message(role="ai", player_name="主持人", content=outline_msg, is_system=False)
            )
            self.game.last_turn_response = {
                "transition": "", "narration": "", "sound": "",
                "dialogues": [], "hooks": {"player_goal": ""}
            }
            self._log_flow("大纲生成完成", "等待确认")
        
        # 先完成大纲生成的事务（_with_txn 会自动持久化状态）
        await self._with_txn_for_group(group_id, _impl)

        # 5. 调用 send_message("确认") 来触发剧本生成和世界构建
        # 注意：send_message 内部会处理事务，所以这里不需要再包装事务
        self._log_flow("官方游戏", "模拟用户确认，开始生成剧本和构建世界")
        result = await self.send_message(group_id, "确认", player_name="系统")
        return result
        
        # 原来的实现（已注释）
        # def _impl():
        #     # 1. 初始化游戏状态
        #     self.game = Game()
        #     gs = self.game.global_state
        #     
        #     # 获取官方游戏设定
        #     prompts, game_type = get_official_game_prompt(game_id, language_code)
        #     
        #     # 2. 生成游戏大纲（跳过用户输入阶段）
        #     self._log_flow("官方游戏", f"开始生成大纲，game_id={game_id}, language={language_code}")
        #     generated_outline = self._generate_outline(prompts, game_type)
        #     gs.outline = generated_outline
        #     gs.game_type = game_type
        #     
        #     # 3. 直接生成游戏剧本（跳过用户审核）
        #     self._log_flow("官方游戏", "生成剧本")
        #     script = self._generate_script(generated_outline, game_type)
        #     gs.script = script
        #     
        #     # 4. 构建游戏世界
        #     self._log_flow("官方游戏", "构建世界")
        #     built = self._build_world(script, game_type)
        #     
        #     # 5. 完整的状态更新
        #     gs.assets = built.get("assets", {}) or {}
        #     gs.story_state = built.get("initial_state", {}) or {}
        #     gs.progress = Progress.IN_PROGRESS  # 直接进入游戏进行状态
        #     gs.round_count = 0
        #     gs.max_rounds = getattr(config, "MAX_ROUNDS", 20)
        #     gs.ended_reason = None
        #     gs.direction = ""
        #     gs.current_chapter = 1
        #     gs.chapters = built.get("chapters", []) or []
        #     gs.chapter_goal_completed = False
        #     
        #     # 6. 初始化叙事状态
        #     _genre = gs.assets.get("game_genre", "story")
        #     self.game.narrative_state = init_narrative_state(genre=_genre)
        #     
        #     # 7. 初始化消息队列和对话历史
        #     # 添加游戏介绍消息
        #     intro = (built.get("player_facing_introduction") or "").strip()
        #     if intro:
        #         intro_msg = Message(role="ai", player_name="主持人", content=intro, is_system=True)
        #         self.game.messages.append(intro_msg)
        #     
        #     # 添加第一场景提示
        #     first_scene = (built.get("first_scene_prompt") or "").strip()
        #     if first_scene:
        #         first_scene_msg = Message(role="ai", player_name="主持人", content=first_scene, is_system=False)
        #         self.game.messages.append(first_scene_msg)
        #     
        #     # 8. 初始化最后回合响应
        #     # 显示第一章开始提示（如果有章节）
        #     if gs.chapters and len(gs.chapters) > 0:
        #         chapter = gs.chapters[0]
        #         chapter_title = chapter.get("title", "第一章")
        #         chapter_goal = chapter.get("goal", "")
        #         chapter_start_msg = f"📖 {chapter_title}：开始\n\n"
        #         if chapter_goal:
        #             chapter_start_msg += f"🎯 本章目标：{chapter_goal}\n\n"
        #         chapter_start_msg += first_scene
        #         
        #         # 更新最后回合响应，包含章节转换信息
        #         self.game.last_turn_response = {
        #             "transition": "chapter_1",
        #             "narration": "",
        #             "sound": "",
        #             "dialogues": [],
        #             "hooks": {"player_goal": ""}
        #         }
        #     else:
        #         # 无章节情况
        #         self.game.last_turn_response = {
        #             "transition": "",
        #             "narration": "",
        #             "sound": "",
        #             "dialogues": [],
        #             "hooks": {"player_goal": ""}
        #         }
        #     
        #     self._log_flow("官方游戏", "初始化完成")
        #     self._log_state_summary("官方游戏创建")
        #     
        #     # 9. 返回游戏状态
        #     return self._build_status_response()
        # 
        # return self._with_txn(_impl)
