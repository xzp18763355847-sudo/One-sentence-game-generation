# """
# AI 剧情游戏 - FastAPI 服务（异步版本）

# 新端点：
# - GET  /api/status  - 获取当前游戏状态
# - POST /api/start   - 开始新剧情游戏（可传 rough_outline）
# - POST /api/action  - 添加玩家行动（不触发 AI 回合）
# - POST /api/submit  - 提交本轮，AI 推进剧情并更新状态
# - POST /api/end     - 结束游戏
# """

import json
import uuid
import asyncio
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import DEFAULT_GROUP_ID
from game_manager import GameManager, Game
from game_statics.preset_games import PRESET_GAME_SNAPSHOTS
from game_types import is_valid_game_type
from narrative.prompt_builder import OFFCIAL_GAME_PROMPT
from utils.log_config import get_logger

logger = get_logger(__name__)

app = FastAPI(title="STATEM AI Game", version="2.0.0")

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务
game_manager = GameManager()


# Pydantic 模型定义
class StartGameRequest(BaseModel):
    group_id: str = DEFAULT_GROUP_ID
    game_type: str = ""
    text: str = ""
    language_code: str = "cn"


class StartOfficialGameRequest(BaseModel):
    group_id: str = DEFAULT_GROUP_ID
    game_id: str  # 这里实际是 game_id
    # language_code: str = "en"


class SendMessageRequest(BaseModel):
    group_id: str = DEFAULT_GROUP_ID
    text: str
    player_name: str = "玩家"
    language_code: str = "en"

class SendMessageSseRequest(BaseModel):
    group_id: str = DEFAULT_GROUP_ID
    text: str
    player_name: str = "玩家"
    custom_variables: Optional[dict] = {}  # 扩展字段 


class EndGameRequest(BaseModel):
    group_id: Optional[str] = DEFAULT_GROUP_ID


def _get_group_id(data: Dict[str, Any]) -> str:
    """从请求数据中提取 group_id，不存在则返回默认值"""
    return (data.get("group_id") or "").strip() or DEFAULT_GROUP_ID


@app.get("/api/status")
async def get_status(group_id: str = DEFAULT_GROUP_ID):
    """
    获取游戏状态 API

    功能：返回指定群的完整游戏状态信息
    查询参数：group_id（可选，默认 "group001"）
    返回：包含游戏状态的 JSON 响应
    """
    group_id = group_id.strip() or DEFAULT_GROUP_ID
    logger.info(f"GET /api/status group_id={group_id}")
    result = await game_manager.get_status(group_id)
    return JSONResponse(result)


@app.post("/api/start")
async def start_game(request: StartGameRequest):
    """
    开始新游戏 API

    功能：初始化并开始一个新的游戏会话
    请求体：StartGameRequest
    返回：包含完整游戏状态的 JSON 响应（包括 messages、state、script 等）
    """
    data = request.dict()
    print("开始游戏输入data================")
    print(data)
    print("开始游戏输入data================")

    group_id = _get_group_id(data)
    game_type = request.game_type.strip()
    text = request.text.strip()
    language_code = request.language_code.strip()

    # 验证游戏类型
    if game_type and not is_valid_game_type(game_type):
        raise HTTPException(status_code=400, detail=f"无效的游戏类型: {game_type}")

    logger.info(
        f"POST /api/start 开始新游戏 group_id={group_id} game_type={game_type} text_len={len(text)} language_code={language_code}")

    # 返回完整的游戏状态（包含 messages、state、script 等）
    # 这样前端可以正常显示游戏内容
    result = await game_manager.start_game(group_id=group_id, game_type=game_type, text=text,
                                           language_code=language_code)
    print("开始游戏输出result（完整状态）================")
    print(result)
    print("开始游戏输出result（完整状态）================")

    return JSONResponse(result)


@app.post("/api/start_offcial_game")
async def start_offcial_game(request: StartOfficialGameRequest):
    """
    开始官方游戏 API

    功能：初始化并开始一个新的官方游戏会话
    请求体：StartOfficialGameRequest
    """
    data = request.dict()
    logger.info(f"POST /api/start_offcial_game 入参: {data}")
    group_id = _get_group_id(data)
    game_id = data.get("game_id", "").strip()
    # game_id = request.text.strip()  # 这里 text 字段实际是 game_id
    if game_id not in OFFCIAL_GAME_PROMPT.keys():
        raise HTTPException(status_code=400, detail=f"无效的游戏ID: {game_id}")

    language_code = "en"  # 固定为英文
    logger.info(f"POST /api/start_official_game group_id={group_id} game_id={game_id}")

    # 检测是否为预设游戏ID，如果是则直接加载预设游戏，跳过模型生成
    if game_id in PRESET_GAME_SNAPSHOTS:
        logger.info(f"检测到预设游戏ID ({game_id})，直接加载预设游戏数据，跳过模型生成")
        preset_snapshot = PRESET_GAME_SNAPSHOTS[game_id]

        # 使用事务加载预设游戏并保存到对应的 group_id 快照文件
        async def _load_preset_game():
            # 从预设游戏快照创建 Game 对象
            game_manager.game = Game.from_snapshot(preset_snapshot)
            logger.info(f"预设游戏已加载到内存")

        # 使用事务保存预设游戏
        await game_manager._with_txn_for_group(group_id, _load_preset_game)

        # 返回游戏状态
        result = await game_manager.get_status(group_id)
        return JSONResponse(result)

    # 普通 game_id: 使用原有逻辑生成游戏
    result = await game_manager.create_official_game(group_id=group_id, game_id=game_id, language_code=language_code)
    return JSONResponse(result)


@app.post("/api/message")
async def send_message(request: SendMessageRequest):
    """
    发送玩家消息 API

    功能：处理玩家发送的消息，推进游戏剧情
    请求体：SendMessageRequest
    返回：包含更新后游戏状态的 JSON 响应
    """
    data = request.dict()
    print("输入data================")
    print(data)
    print("输入data================")

    group_id = _get_group_id(data)
    text = request.text.strip()
    language_code = request.language_code.strip()
    player_name = request.player_name.strip()

    logger.info("POST /api/message group_id=%s player=%s len=%d text_preview=%s",
                group_id, player_name, len(text),
                (text[:30] + "..." if len(text) > 30 else text))

    result = await game_manager.send_message(group_id=group_id, text=text, player_name=player_name,
                                             language_code=language_code)
    game_type = result.get("game_type") or result.get("global_state", {}).get("game_type")
    logger.info(f"----游戏类型{game_type}------")
    if "error" in result:
        logger.warning("POST /api/message group_id=%s error=%s", group_id, result.get("error"))
        raise HTTPException(status_code=400, detail=result.get("error"))

    print("输出result================")
    print(result)
    print("输出result================")
    return JSONResponse(result)


@app.post("/api/message_sse")
async def send_message_sse(request: SendMessageSseRequest):
    """
    发送玩家消息 API（SSE 分段返回）

    请求体：与 /api/message 相同 SendMessageRequest
    返回：text/event-stream，按顺序推送（每条为 event: reply + data: JSON）：
      - event: reply / data: {"type":"reply","payload":{"can_feedback":false,"content":{...}},"message_id":"..."}
      - 第 1 条 content：transition；第 2 条 narration、sound；第 3 条 dialogues、hooks（可选 aigc_generate）；第 4 条完整状态
    错误时返回 400 + JSON {"error": "..."}，不走 SSE。
    """
    data = request.dict()
    logger.info(f"POST /api/message_sse 入参: {data}")
    group_id = _get_group_id(data)
    text = request.text.strip()
    player_name = request.player_name.strip() or "玩家"
    custom_variables = request.custom_variables or {}
    language_code = custom_variables.get("language_code", "en")

    result = await game_manager.send_message(group_id=group_id, text=text, player_name=player_name,
                                             language_code=language_code)
    if "error" in result:
        logger.warning("POST /api/message_sse group_id=%s error=%s", group_id, result.get("error"))
        raise HTTPException(status_code=400, detail=result.get("error"))
    game_type = result.get("game_type") or result.get("global_state", {}).get("game_type")
    logger.info(f"----游戏类型   {game_type}------")
    transition = result.get("transition", "") or ""
    narration = result.get("narration", "") or ""
    sound = result.get("sound", "") or ""
    dialogues = result.get("dialogues", [])
    if not isinstance(dialogues, list):
        dialogues = []
    hooks = result.get("hooks", {}) or {}
    if not isinstance(hooks, dict):
        hooks = {}
    if "player_goal" not in hooks:
        hooks["player_goal"] = ""

    # 判断是否为“私聊角色类”（角色陪伴类），如果是则不向前端返回 narration
    game_type = result.get("game_type") or result.get("global_state", {}).get("game_type")
        
    aigc_generate = result.get("aigc_generate") if "aigc_generate" in result else None
    message_id = str(uuid.uuid4())

    def _wrap_reply(content: dict) -> dict:
        return {
            "type": "reply",
            "payload": {"can_feedback": False, "can_rating": True, "content": content},
            "message_id": message_id,
        }

    def _sse_chunk(obj: dict) -> str:
        return f"event: reply\ndata: {json.dumps(obj, ensure_ascii=False)}\n\n"

    async def generate():
        # 1) transition
        if transition:
            yield _sse_chunk(_wrap_reply({"transition": transition}))
        # 2) narration + sound
        if game_type not in ["私聊角色类", ]:
            yield _sse_chunk(_wrap_reply({"narration": narration, "sound": sound}))
        # 3) dialogues + hooks（若 result 含 aigc_generate 则一并返回）
        dialogues_payload: dict = {"dialogues": dialogues, "hooks": hooks}
        if aigc_generate is not None:
            dialogues_payload["aigc_generate"] = aigc_generate
        yield _sse_chunk(_wrap_reply(dialogues_payload))
        # 4) 完整状态，便于前端更新 UI
        # yield _sse_chunk(_wrap_reply(result))

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@app.get("/api/narrative/state")
async def get_narrative_state(group_id: str = DEFAULT_GROUP_ID):
    """
    获取叙事状态 API（调试接口）

    功能：返回指定群当前四条主线叙事状态，用于调试和监控
    查询参数：group_id（可选）
    返回：包含叙事状态的 JSON 响应
    """
    group_id = group_id.strip() or DEFAULT_GROUP_ID
    logger.info(f"GET /api/narrative/state group_id={group_id}")
    result = await game_manager.get_narrative_state(group_id)
    return JSONResponse(result)


@app.get("/api/narrative/log")
async def get_narrative_log(group_id: str = DEFAULT_GROUP_ID):
    """
    获取叙事日志 API（调试接口）

    功能：返回指定群状态变更日志和事件日志，用于调试和监控
    查询参数：group_id（可选）
    返回：包含日志信息的 JSON 响应
    """
    group_id = group_id.strip() or DEFAULT_GROUP_ID
    logger.info(f"GET /api/narrative/log group_id={group_id}")
    result = await game_manager.get_narrative_log(group_id)
    return JSONResponse(result)


@app.post("/api/end")
# async def end_game(request: EndGameRequest):
async def end_game(group_id: str = DEFAULT_GROUP_ID):
    """
    结束游戏 API

    功能：手动结束指定群的游戏会话
    请求体：EndGameRequest
    返回：包含结束状态信息的 JSON 响应
    """
    # group_id = _get_group_id(request.dict())
    logger.info(f"POST /api/end 手动结束游戏 group_id={group_id}")
    result = await game_manager.end_game(group_id)
    return JSONResponse(result)


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化Redis连接"""
    from utils.redis_cache import dao as redis_dao
    try:
        await redis_dao.init_pools()
        logger.info("✅ Redis connection initialized on startup")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Redis on startup: {e}")
        raise


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    logger.error(f"全局异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

if __name__ == "__main__":
    import uvicorn

    logger.info("server: http://0.0.0.0:4000")
    uvicorn.run(app, host="0.0.0.0", port=4000, log_level="info")
