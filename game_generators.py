"""
游戏生成器模块 - 处理不同游戏类型的剧本生成
"""
import json
import logging
from typing import Dict, Any, Optional, Tuple

from game_types import GameType, get_game_type_info

logger = logging.getLogger(__name__)

# =========================
# 剧情游戏回合引擎  prompts
# =========================

# 通用基础提示词
_TURN_ENGINE_BASE_PROMPT = """
你是"剧情游戏回合引擎"。只输出严格 JSON（不要解释/markdown/注释）。

【核心原则】
1. 叙事层（Narrative）高度自由：可以即兴发挥，描述环境细节、情绪、临时事件、非关键NPC
2. 状态层（State）低自由度：结构必须固定，只允许数值变化

【输入 JSON 包含】
- assets：世界资产（服务端会裁剪并剔除部分 secrets）
- current_state：上回合的 story_state（结构固定，顶层字段：player/npc/world）
- recent_log：最近对话
- player_message：玩家本回合输入（动作/对白/尝试）
- current_chapter：当前章节信息（包含 title, goal, description）（如果有章节）
- game_type：游戏类型
- user_state_change_request：用户状态变更请求（可选，如果用户明确要求改变状态时会包含此字段）
  - intent：用户想要改变的状态字段和值（如 {"world.time": "晚上"}）
  - tone_intensity：语气强度（0.0-1.0，越高表示语气越强烈）
  - repeated_count：用户重复请求相同状态变更的次数（包括本次）

【输出格式（必须包含所有字段）】

每次输出必须包含以下所有字段，即使某些字段为空：

{
  "transition": "章节转换标识，如：chapter_1、chapter_2。如果当前回合不是章节开始/结束，则为空字符串",
  "narration": "场景描述文本，如：Dim hallway at midnight, faint echoes haunt your steps. 如果没有叙述则为空字符串",
  "sound": "声音描述，如：微弱回声、脚步声、风声等。如果没有声音则为空字符串",
  "dialogues": [
    {
      "name": "角色名称，如：Emma",
      "expression": "表情描述，如：pale tense、smile、angry等。如果没有表情则为空字符串",
      "text": "对话内容（只包含NPC的对话，不包含玩家说的话）"
    }
  ],
  "hooks": {
    "player_goal": "给玩家的行动建议，如：Ask Emma what she means by the pull。如果没有建议则为空字符串"
  },
  "state_delta": {},
  "flags": {"game_ended": false, "reason": "", "chapter_goal_completed": false}
}

【重要规则】
- 每次输出必须包含所有字段（transition、narration、sound、dialogues、hooks、state_delta、flags）
- dialogues 只包含NPC的对话，不要包含玩家说的话（玩家的话已经在 player_message 中提供，不需要重复放入 dialogues）
- 如果有NPC对话，在 dialogues 数组中添加对话对象，否则为空数组 []
- 如果有场景描述，填写 narration 字段，否则为空字符串
- 如果有声音效果，填写 sound 字段，否则为空字符串
- 如果有行动建议，在 hooks.player_goal 中填写，否则为空字符串
- 所有字段如果没有值，使用空字符串、空数组或空对象

【叙事层规则（高自由度）】
- 可以自由描述环境细节、角色情绪、临时事件、非关键NPC对话
- 可以即兴发挥，不追求确定性
- 必须遵守 assets 中的世界规则和设定
- 禁止泄露任何 "secrets" 内容
- 如果玩家输入不可行：narrative 中解释原因，并给替代建议

【状态层规则（低自由度 - 必须严格遵守）】
- 每次输出必须包含 state_delta 和 flags 字段
- state_delta 的顶层 key 必须是允许的顶层字段（player/npc/world/chapter）
- 对于已存在的顶层字段：只能更新已存在的子字段，严禁新增、删除或重命名任何子字段名
- 特殊规则：如果回合剧情中有新NPC出现，可以在 state_delta 中添加新的 "npc" 字段（包含完整的 npc 对象：name, affection, relationship）
  - 只有当 current_state 中没有 npc 字段时，才允许添加新的 npc
  - 新 npc 必须包含 name 字段，affection 初始值建议为 0，relationship 初始值建议为 "陌生" 或类似描述
- state_delta 只写变化，不要重写整个 current_state
- 只允许修改数值（如 hp, affection, level）或字符串（如 status, scene, time）
- 如果玩家输入导致状态变化：在 state_delta 中描述变化
- 如果玩家输入不导致状态变化：state_delta 可以为空对象 {}

【状态字段说明】
- player: {hp, max_hp, level, status, name} （hp/max_hp 仅剧情类游戏需要）
- npc: {name, affection, relationship} （可选）
- world: {scene, time, location}
- chapter: {current_chapter, chapter_progress, chapter_goal_completed} （可选，章节类游戏需要）
""".strip()

# 角色攻略类游戏（有结局）特殊规则
_TURN_ENGINE_COMPANION_ROUTE_RULES = """
【游戏类型：角色攻略类（有结局）】

【特殊规则】
- 这是角色攻略类游戏，核心目标是提升NPC的好感度
- npc.affection 表示好感度，范围 0-100
- player 字段中不包含 hp 和 max_hp（角色类游戏不需要血量）
- 当好感度达到 100 时，游戏应该结束并达成完美结局
- 在好感度接近 100（如 95+）时，应该给出暗示，让玩家知道即将达成目标
- 当好感度达到 100 时，在 flags 中设置 game_ended = true, reason = "affection_max"（好感度满值）
- transition 字段始终为空字符串（此类游戏没有章节系统）

【完整输出示例】

示例1 - 普通回合（有对话，好感度提升）：
{
  "transition": "",
  "narration": "你温柔地看着她，她的脸颊微微泛红。",
  "sound": "心跳声",
  "dialogues": [
    {
      "name": "艾米",
      "expression": "害羞",
      "text": "谢谢你一直陪着我...我真的很开心。"
    }
  ],
  "hooks": {
    "player_goal": "继续与艾米互动，加深你们的关系"
  },
  "state_delta": {
    "npc": {"affection": 65}
  },
  "flags": {"game_ended": false, "reason": "", "chapter_goal_completed": false}
}

示例2 - 好感度满值，游戏结束：
{
  "transition": "",
  "narration": "你们的心意终于相通，彼此都感受到了深深的爱意。",
  "sound": "温柔的音乐",
  "dialogues": [
    {
      "name": "艾米",
      "expression": "幸福",
      "text": "我爱你...我想和你永远在一起。"
    }
  ],
  "hooks": {
    "player_goal": ""
  },
  "state_delta": {
    "npc": {"affection": 100}
  },
  "flags": {"game_ended": true, "reason": "affection_max", "chapter_goal_completed": false}
}
""".strip()

# 开放式陪伴类游戏（无结局）特殊规则
_TURN_ENGINE_COMPANION_OPEN_RULES = """
【游戏类型：开放式陪伴类（无结局）】

【特殊规则】
- 这是开放式陪伴类游戏，没有固定结局，可以长期进行
- npc.affection 表示好感度，范围 0-100，但这只是关系指标，不是游戏目标
- player 字段中不包含 hp 和 max_hp（角色类游戏不需要血量）
- 重点在于日常互动、陪伴感和长期关系发展
- 不要设置 game_ended = true（此类游戏没有结局）
- transition 字段始终为空字符串（此类游戏没有章节系统）

【用户权限规则（重要 - 开放式陪伴类游戏增强）】
- 如果输入中包含 user_state_change_request 字段，表示用户明确要求改变某个状态
- 开放式陪伴类游戏强调用户主导和自由互动，用户权限更高
- 用户权限判断规则：
  1. 如果用户第一次提出状态变更请求（repeated_count = 1）：
     - 如果语气温和（tone_intensity < 0.5）：可以在 narration 或 dialogues 中与用户讨论或辩论，但不必立即更新状态
     - 如果语气强烈（tone_intensity >= 0.5）或用户表现出拉扯/坚持的态度：应该接受用户的要求，在 state_delta 中更新相应状态
  2. 如果用户第二次或更多次提出相同的状态变更请求（repeated_count >= 2）：
     - 无论语气如何，都必须尊重用户意愿，在 state_delta 中更新相应状态
     - 可以在 narration 或 dialogues 中简单说明状态已更新，无需过多解释或辩论
  3. 具体示例：
     - 当前状态：world.time = "白天"
     - 用户第一次说"现在是晚上"（语气温和，tone_intensity < 0.5）：可以在 dialogues 中回复"但现在是白天呢，你觉得呢？"，state_delta 可以为空
     - 用户第二次说"不，就是晚上"（语气强烈，tone_intensity >= 0.5）：必须接受，在 state_delta 中设置 {"world": {"time": "晚上"}}
     - 用户第三次说"我说了是晚上"：必须接受，在 state_delta 中更新状态
- 状态更新时，优先使用 user_state_change_request.intent 中指定的值，如果没有具体值，则根据用户描述合理推断
- 在开放式陪伴类游戏中，应该更倾向于满足用户的合理需求，营造轻松友好的互动氛围

【完整输出示例】

示例1 - 普通回合（日常互动）：
{
  "transition": "",
  "narration": "阳光透过窗户洒在房间里，你们一起享受着宁静的午后。",
  "sound": "鸟鸣声",
  "dialogues": [
    {
      "name": "艾米",
      "expression": "轻松",
      "text": "今天天气真好呢，要不要一起出去走走？"
    }
  ],
  "hooks": {
    "player_goal": "回应艾米的邀请，决定是否一起外出"
  },
  "state_delta": {
    "npc": {"affection": 45}
  },
  "flags": {"game_ended": false, "reason": "", "chapter_goal_completed": false}
}

示例2 - 用户第二次要求状态变更（必须接受）：
{
  "transition": "",
  "narration": "天色渐渐暗了下来，夜幕降临。",
  "sound": "",
  "dialogues": [
    {
      "name": "艾米",
      "expression": "理解",
      "text": "好的，你说得对，现在确实是晚上了。"
    }
  ],
  "hooks": {
    "player_goal": ""
  },
  "state_delta": {
    "world": {"time": "晚上"}
  },
  "flags": {"game_ended": false, "reason": "", "chapter_goal_completed": false}
}
""".strip()

# 章节剧情类游戏（有结局）特殊规则
_TURN_ENGINE_STORY_CHAPTER_RULES = """
【游戏类型：章节剧情类（有结局）】

【特殊规则】
- 这是章节剧情类游戏，有明确的章节结构和结局
- 当前章节信息会在输入中提供（current_chapter）
- 如果玩家在本回合完成了当前章节的目标，在 flags 中设置 chapter_goal_completed = true
- 章节目标完成的标准：玩家行动明显达成了章节目标（如：收集到关键物品、完成关键任务、达到关键地点等）
- 不要轻易判定章节完成，需要玩家确实达成了目标
- 如果当前回合是章节开始或结束，在 transition 字段中填写章节标识（如 "chapter_1"），否则为空字符串
- player 字段包含 hp, max_hp（剧情类游戏可能需要血量）
- 当所有章节完成或达成结局条件时，在 flags 中设置 game_ended = true, reason = "story_completed"（剧情完成）

【完整输出示例】

示例1 - 普通回合（有对话）：
{
  "transition": "",
  "narration": "Dim hallway at midnight, faint echoes haunt your steps.",
  "sound": "微弱回声",
  "dialogues": [
    {
      "name": "Emma",
      "expression": "pale tense",
      "text": "I noticed you staring earlier... Do you feel the pull too? It wants us to remember."
    }
  ],
  "hooks": {
    "player_goal": "Ask Emma what she means by the pull"
  },
  "state_delta": {
    "world": {"time": "midnight"}
  },
  "flags": {"game_ended": false, "reason": "", "chapter_goal_completed": false}
}

示例2 - 章节转换回合：
{
  "transition": "chapter_2",
  "narration": "新的章节开始了，你站在新的起点。",
  "sound": "",
  "dialogues": [],
  "hooks": {
    "player_goal": ""
  },
  "state_delta": {
    "chapter": {"current_chapter": 2, "chapter_progress": "刚开始", "chapter_goal_completed": false}
  },
  "flags": {"game_ended": false, "reason": "", "chapter_goal_completed": false}
}

示例3 - 章节目标完成：
{
  "transition": "",
  "narration": "你成功找到了关键线索，完成了这一章的目标。",
  "sound": "胜利的音效",
  "dialogues": [],
  "hooks": {
    "player_goal": "准备进入下一章节"
  },
  "state_delta": {
    "chapter": {"chapter_goal_completed": true}
  },
  "flags": {"game_ended": false, "reason": "", "chapter_goal_completed": true}
}
""".strip()

# 开放式剧情游戏（无结局）特殊规则
_TURN_ENGINE_STORY_OPEN_RULES = """
【游戏类型：开放式剧情（无结局）】

【特殊规则】
- 这是开放式剧情游戏，没有固定结局，可以持续探索和推进
- 如果有章节系统，当前章节信息会在输入中提供（current_chapter）
- 如果有章节，如果玩家在本回合完成了当前章节的目标，在 flags 中设置 chapter_goal_completed = true
- 如果有章节，如果当前回合是章节开始或结束，在 transition 字段中填写章节标识（如 "chapter_1"），否则为空字符串
- player 字段包含 hp, max_hp（剧情类游戏可能需要血量）
- 不要设置 game_ended = true（此类游戏没有结局）
- 重点在于持续探索、自由推进和开放互动

【完整输出示例】

示例1 - 普通回合（探索）：
{
  "transition": "",
  "narration": "你继续在未知的世界中探索，前方充满了可能性。",
  "sound": "风声",
  "dialogues": [
    {
      "name": "向导",
      "expression": "友好",
      "text": "你想去哪里？这个世界很大，有很多地方值得探索。"
    }
  ],
  "hooks": {
    "player_goal": "决定探索的方向"
  },
  "state_delta": {
    "world": {"location": "未知区域"}
  },
  "flags": {"game_ended": false, "reason": "", "chapter_goal_completed": false}
}
""".strip()

# 根据游戏类型拆分的提示词字典
TURN_ENGINE_SYSTEM_PROMPT_BY_TYPE = {
    GameType.COMPANION_ROUTE.value: (
        _TURN_ENGINE_BASE_PROMPT + "\n\n" + _TURN_ENGINE_COMPANION_ROUTE_RULES
    ),
    GameType.COMPANION_OPEN.value: (
        _TURN_ENGINE_BASE_PROMPT + "\n\n" + _TURN_ENGINE_COMPANION_OPEN_RULES
    ),
    GameType.STORY_CHAPTER.value: (
        _TURN_ENGINE_BASE_PROMPT + "\n\n" + _TURN_ENGINE_STORY_CHAPTER_RULES
    ),
    GameType.STORY_OPEN.value: (
        _TURN_ENGINE_BASE_PROMPT + "\n\n" + _TURN_ENGINE_STORY_OPEN_RULES
    ),
}

# 默认导出，保持历史代码兼容（默认使用章节剧情类）
TURN_ENGINE_SYSTEM_PROMPT = TURN_ENGINE_SYSTEM_PROMPT_BY_TYPE[
    GameType.STORY_CHAPTER.value
]


def get_turn_engine_system_prompt(game_type: str) -> str:
    """
    根据游戏类型获取回合引擎 system prompt
    
    参数:
        game_type: 游戏类型字符串
        
    返回:
        对应的提示词字符串
    """
    normalized_game_type = game_type or ""
    return TURN_ENGINE_SYSTEM_PROMPT_BY_TYPE.get(
        normalized_game_type, TURN_ENGINE_SYSTEM_PROMPT
    )

# =========================
# 大纲生成器提示词
# =========================
OUTLINE_GENERATOR_SYSTEM_PROMPT = """
你是一个专业的剧情游戏大纲生成器。根据用户提供的几句话和游戏类型，生成一个详细、有趣的剧情游戏大纲。

输入：用户提供的几句话（可能是零散的想法、关键词、场景描述等）和游戏类型
输出：一个结构化的剧情大纲，包含：
- 背景设定
- 主要角色
- 核心冲突/目标
- 关键场景/情节线索
- 可能的结局方向（如果有结局）

要求：
1. 大纲应该详细但不过于具体，给游戏留出发挥空间
2. 要有吸引力和可玩性
3. 语言清晰，结构分明
4. 只输出大纲文本，不要添加额外说明
5. 根据游戏类型调整大纲内容：
   - 角色陪伴类：重点突出角色设定、互动方式、关系发展
   - 剧情游戏类：重点突出剧情线索、章节结构、冲突发展
6. 【重要】必须使用指定的语言输出（language_code 会通过用户提示提供）
""".strip()


def build_outline_prompt(user_input: str, game_type: str, language_code: str = "cn") -> str:
    """
    构建大纲生成提示词
    
    参数:
        user_input: 用户输入的文本
        game_type: 游戏类型
        language_code: 语言代码（cn=中文, en=英文）
        
    返回:
        提示词字符串
    """
    game_info = get_game_type_info(game_type)
    game_name = game_info.get("name", "剧情游戏")
    
    language_map = {
        "cn": "中文",
        "en": "English",
        "zh": "中文",
    }
    language_name = language_map.get(language_code.lower(), "中文")
    
    prompt = f"""
用户输入：
{user_input}

游戏类型：{game_name}
输出语言：{language_name}（language_code: {language_code}）

【重要】请使用 {language_name} 生成一个详细的剧情游戏大纲。所有输出内容（包括背景设定、角色描述、情节线索等）都必须使用 {language_name}。
"""
    return prompt.strip()


# =========================
# 剧本生成器提示词
# =========================
_SCRIPT_GENERATOR_PROMPT_COMMON = """
你是"剧情游戏剧本生成器"。只输出严格 JSON（不要解释/markdown/注释）。

输入：玩家提供的剧情大纲 outline 和游戏类型
输出：一个 JSON 对象，必须包含以下四个字典：

{
  "outline": {
    "introduction": "游戏的整体介绍和背景",
    "info": "游戏的基本信息（类型、风格等）",
    "rules": "游戏的基本规则和玩法说明"
  },
  "background": {
    "relationships": [
      {"character1": "角色2", "relationship": "关系描述"},
      ...
    ]
  },
  "chapters": [
    {
      "number": 1,
      "introduction": "章节介绍"
    },
    ...
  ],
  "characters": [
    {
      "name": "角色名",
      "gender": "男/女/其他",
      "profile": "角色详细设定",
      "introduction": "角色介绍"
    },
    ...
  ]
}

【通用规则】
1. 角色数组：列出所有主要角色，包括玩家角色（如果有）
2. 只输出 JSON，不要添加任何解释或注释
3. 【重要】必须使用指定的语言输出（language_code 会通过用户提示提供）。JSON 中的所有文本内容（包括 introduction、info、rules、关系描述、角色介绍、章节介绍等）都必须使用指定语言。
""".strip()

SCRIPT_GENERATOR_SYSTEM_PROMPT_BY_TYPE = {
    GameType.STORY_CHAPTER.value: (
        _SCRIPT_GENERATOR_PROMPT_COMMON
        + "\n\n"
        + """
【游戏类型规则：章节剧情类（有结局）】
1. 必须生成多个章节（至少 3-5 个），章节编号从 1 开始
2. 章节列表必须包含明确的结局章节
3. relationships 必须为非空数组，列出主要角色之间的关系
4. 章节结构必须清晰体现冲突升级与结局收束
""".strip()
    ),
    GameType.STORY_OPEN.value: (
        _SCRIPT_GENERATOR_PROMPT_COMMON
        + "\n\n"
        + """
【游戏类型规则：开放式剧情（无结局）】
1. chapters 可以为空数组，或仅包含 1 个开放式章节
2. 不要设计“唯一终局”或“必然结束点”，保持可持续推进
3. relationships 应列出主要角色关系，支持长期演化
4. rules 需强调开放探索、持续互动和自由推进
""".strip()
    ),
    GameType.COMPANION_ROUTE.value: (
        _SCRIPT_GENERATOR_PROMPT_COMMON
        + "\n\n"
        + """
【游戏类型规则：角色陪伴-攻略类（有结局）】
1. relationships（人物关系数组）必须为空数组 []
2. chapters（章节数组）必须为空数组 []
3. 只生成一个核心 NPC 角色（从角色列表中选择最重要的一个）
4. 重点生成角色信息，确保角色设定详细完整，突出可攻略路径
5. rules 中需明确该玩法存在“可达成结局”
""".strip()
    ),
    GameType.COMPANION_OPEN.value: (
        _SCRIPT_GENERATOR_PROMPT_COMMON
        + "\n\n"
        + """
【游戏类型规则：角色陪伴-开放式（无结局）】
1. relationships（人物关系数组）必须为空数组 []
2. chapters（章节数组）必须为空数组 []
3. 只生成一个核心 NPC 角色（从角色列表中选择最重要的一个）
4. 重点生成角色信息，强调陪伴感、互动日常与长期关系变化
5. rules 中需明确该玩法无固定结局，可长期进行
""".strip()
    ),
}
# 兼容历史配置中的旧类型名称
SCRIPT_GENERATOR_SYSTEM_PROMPT_BY_TYPE["私聊角色类"] = SCRIPT_GENERATOR_SYSTEM_PROMPT_BY_TYPE[
    GameType.COMPANION_ROUTE.value
]

# 默认导出，保持历史代码兼容（默认使用章节剧情类）
SCRIPT_GENERATOR_SYSTEM_PROMPT = SCRIPT_GENERATOR_SYSTEM_PROMPT_BY_TYPE[
    GameType.STORY_CHAPTER.value
]


def get_script_generator_system_prompt(game_type: str) -> str:
    """
    根据游戏类型获取剧本生成 system prompt
    """
    normalized_game_type = game_type or ""
    return SCRIPT_GENERATOR_SYSTEM_PROMPT_BY_TYPE.get(
        normalized_game_type, SCRIPT_GENERATOR_SYSTEM_PROMPT
    )


def build_script_prompt(outline: str, game_type: str, language_code: str = "cn") -> str:
    """
    构建剧本生成提示词
    
    参数:
        outline: 剧情大纲
        game_type: 游戏类型
        language_code: 语言代码（cn=中文, en=英文）
        
    返回:
        提示词字符串
    """
    game_info = get_game_type_info(game_type)
    game_name = game_info.get("name", "剧情游戏")
    language_map = {
        "cn": "中文",
        "en": "English",
        "zh": "中文",
    }
    language_name = language_map.get(language_code.lower(), "中文")
    
    prompt = f"""
玩家剧情大纲 outline：
{outline}

游戏类型：{game_name}
输出语言：{language_name}（language_code: {language_code}）
"""
    
    prompt += f"""
【重要】请使用 {language_name} 生成游戏剧本。JSON 中的所有文本内容（包括 introduction、info、rules、关系描述、角色介绍、章节介绍等）都必须使用 {language_name}。只输出 JSON。
"""
    return prompt.strip()


# =========================
# 世界构建器提示词（用于生成游戏世界资产）
# =========================
WORLD_BUILDER_SYSTEM_PROMPT = """
你是"剧情游戏世界构建器"。只输出严格 JSON（不要解释/markdown/注释）。

输入：游戏剧本（包含大纲、背景故事、章节、角色）和游戏类型
输出：一个 JSON 对象，必须包含这些字段：
- "assets": {...}  （世界规则、背景设定、角色信息等）
- "initial_state": {...}  （初始游戏状态，必须符合固定结构）
- "player_facing_introduction": "..."  （给玩家的介绍）
- "first_scene_prompt": "..."  （第一场景的提示）
- "game_genre": 字符串，根据剧情大纲推断游戏类型，取值：mystery（解密推理）、romance（恋爱）、exploration（探索）、adventure（冒险）、story（一般剧情）、mixed（混合）。无法判断则填 "story"。
- "chapters": [...]  （章节列表，每个章节包含：title（章节标题）、goal（章节目标，简短明确）、description（章节描述））

【重要】必须使用指定的语言输出（language_code 会通过用户提示提供）。JSON 中的所有文本内容（包括 assets 中的描述、player_facing_introduction、first_scene_prompt、chapters 中的标题和描述等）都必须使用指定语言。

【状态结构要求（必须遵守）】
initial_state 必须包含以下顶层字段（可根据游戏类型选择）：
- "player": {hp, max_hp, level, status, name}  （玩家状态）
- "npc": {name, affection, relationship}  （可选，如果有NPC）
- "world": {scene, time, location}  （世界状态）
- "chapter": {current_chapter, chapter_progress, chapter_goal_completed}  （可选，章节类游戏需要）

【角色类游戏特殊规则】
如果游戏类型是角色陪伴类（companion_route 或 companion_open）：
1. 必须只创建一个 NPC（从剧本中的角色列表选择最重要的一个）
2. player 字段中不要包含 hp 和 max_hp（角色类游戏不需要血量）
3. 如果游戏类型是 companion_route（攻略类）：
   - npc 必须包含 affection 字段（好感度，初始值建议 0-30，满值为 100）
   - 在 assets 中说明：好感度达到 100 时游戏会结束并达成完美结局
4. 如果游戏类型是 companion_open（开放式陪伴类）：
   - npc 可以包含 affection 字段（好感度，0-100），但这不是游戏目标

重要规则：
1. 不得新增、删除或重命名这些顶层字段名
2. 不得新增、删除或重命名子字段名（如 player.hp, player.max_hp 等）
3. 只能设置这些字段的初始值
4. 可以在 assets 或 initial_state 里使用任何层级的 "secrets" 字段存放隐藏信息（服务端保留）
5. 在 player_facing_introduction / first_scene_prompt 里不得泄露 secrets

【章节系统】
- 如果游戏有章节，从剧本中的章节信息生成 chapters 数组
- 每个章节必须包含：title（标题）、goal（目标）、description（描述）
- 如果游戏没有章节，chapters 可以为空数组

【章节类游戏特殊规则】
如果游戏类型是章节类游戏（story_chapter）：
1. initial_state 必须包含 "chapter" 字段
2. chapter 字段必须包含：
   - current_chapter: 初始章节编号（整数，从1开始）
   - chapter_progress: 初始进度描述（字符串，建议为 "刚开始" 或 "进行中"）
   - chapter_goal_completed: 初始完成状态（布尔值，建议为 false）
3. 在 assets 中说明章节系统的规则和目标
""".strip()


def build_world_builder_prompt(script: dict, game_type: str, language_code: str = "cn") -> str:
    """
    构建世界构建器提示词
    
    参数:
        script: 游戏剧本字典
        game_type: 游戏类型
        language_code: 语言代码（cn=中文, en=英文）
        
    返回:
        提示词字符串
    """
    game_info = get_game_type_info(game_type)
    has_chapters = game_info.get("has_chapters", False)
    category = game_info.get("category", "")
    is_companion_route = game_type == GameType.COMPANION_ROUTE.value
    is_companion_open = game_type == GameType.COMPANION_OPEN.value
    
    language_map = {
        "cn": "中文",
        "en": "English",
        "zh": "中文",
    }
    language_name = language_map.get(language_code.lower(), "中文")
    
    prompt = f"""
游戏剧本：
{json.dumps(script, ensure_ascii=False, indent=2)}

游戏类型：{game_info.get('name', '剧情游戏')}
是否有章节：{'是' if has_chapters else '否'}
输出语言：{language_name}（language_code: {language_code}）
"""
    
    if is_companion_route or is_companion_open:
        prompt += f"""
【重要】这是角色陪伴类游戏，请特别注意：
1. 只创建一个 NPC（从剧本中选择最重要的一个角色）
2. player 字段中不要包含 hp 和 max_hp（不需要血量系统）
"""
        if is_companion_route:
            prompt += """
3. 这是攻略类游戏（有结局），npc 必须包含 affection 字段（好感度，初始值 0-30，满值 100）
4. 在 assets 中明确说明：好感度达到 100 时游戏会结束并达成完美结局
"""
        else:
            prompt += """
3. 这是开放式陪伴类游戏，npc 可以包含 affection 字段（好感度，0-100），但这不是游戏目标
"""
    
    prompt += f"""
【重要】请使用 {language_name} 生成世界资产与初始状态。JSON 中的所有文本内容（包括 assets 中的描述、player_facing_introduction、first_scene_prompt、chapters 中的标题和描述、initial_state 中的字符串字段等）都必须使用 {language_name}。只输出 JSON。
"""
    return prompt.strip()


def validate_script_structure(script: dict) -> Tuple[bool, str]:
    """
    验证剧本结构是否符合要求
    
    参数:
        script: 剧本字典
        
    返回:
        (是否有效, 错误信息)
    """
    required_keys = ["outline", "background", "chapters", "characters"]
    
    for key in required_keys:
        if key not in script:
            return False, f"缺少必需的键: {key}"
    
    # 验证大纲结构
    outline = script.get("outline", {})
    if not isinstance(outline, dict):
        return False, "大纲必须是字典"
    required_outline_keys = ["introduction", "info", "rules"]
    for key in required_outline_keys:
        if key not in outline:
            return False, f"大纲缺少必需的键: {key}"
    
    # 验证背景故事结构
    background = script.get("background", {})
    if not isinstance(background, dict):
        return False, "背景故事必须是字典"
    if "relationships" not in background:
        return False, "背景故事缺少人物关系"
    if not isinstance(background.get("relationships"), list):
        return False, "人物关系必须是数组"
    
    # 验证章节结构
    chapters = script.get("chapters", [])
    if not isinstance(chapters, list):
        return False, "章节必须是数组"
    for i, ch in enumerate(chapters):
        if not isinstance(ch, dict):
            return False, f"章节{i+1}必须是字典"
        if "number" not in ch or "introduction" not in ch:
            return False, f"章节{i+1}缺少必需的键: 编号或介绍"
    
    # 验证角色结构
    characters = script.get("characters", [])
    if not isinstance(characters, list):
        return False, "角色必须是数组"
    for i, char in enumerate(characters):
        if not isinstance(char, dict):
            return False, f"角色{i+1}必须是字典"
        required_char_keys = ["name", "gender", "profile", "introduction"]
        for key in required_char_keys:
            if key not in char:
                return False, f"角色{i+1}缺少必需的键: {key}"
    
    return True, ""


def normalize_script(script: dict) -> dict:
    """
    规范化剧本结构，确保所有必需字段都存在
    
    参数:
        script: 原始剧本字典
        
    返回:
        规范化后的剧本字典
    """
    normalized = {
        "outline": {
            "introduction": script.get("outline", {}).get("introduction", "") if isinstance(script.get("outline"), dict) else "",
            "info": script.get("outline", {}).get("info", "") if isinstance(script.get("outline"), dict) else "",
            "rules": script.get("outline", {}).get("rules", "") if isinstance(script.get("outline"), dict) else "",
        },
        "background": {
            "relationships": script.get("background", {}).get("relationships", []) if isinstance(script.get("background"), dict) else [],
        },
        "chapters": script.get("chapters", []) if isinstance(script.get("chapters"), list) else [],
        "characters": script.get("characters", []) if isinstance(script.get("characters"), list) else [],
    }
    
    return normalized
