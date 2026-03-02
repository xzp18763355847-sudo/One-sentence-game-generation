"""
游戏生成器模块 - 处理不同游戏类型的剧本生成
"""
import json
import logging
from typing import Dict, Any, Optional, Tuple

from game_types import GameType, get_game_type_info

logger = logging.getLogger(__name__)


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
SCRIPT_GENERATOR_SYSTEM_PROMPT = """
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

【重要规则】
1. 根据游戏类型调整输出结构：
   - 角色陪伴类：重点生成角色信息，章节可以为空或只有一个
   - 剧情游戏类：必须生成多个章节（至少3-5个），章节编号从1开始
   - 有结局的游戏：章节列表必须包含明确的结局章节
   - 无结局的游戏：章节列表可以为空或只有一个开放式章节

2. 人物关系数组：列出主要角色之间的关系，格式为对象数组

3. 角色数组：列出所有主要角色，包括玩家角色（如果有）

4. 章节数组：
   - 有章节的游戏：必须包含多个章节，每个章节有编号和介绍
   - 无章节的游戏：可以为空数组或只有一个开放式章节

5. 只输出 JSON，不要添加任何解释或注释

6. 【重要】必须使用指定的语言输出（language_code 会通过用户提示提供）。JSON 中的所有文本内容（包括 introduction、info、rules、关系描述、角色介绍等）都必须使用指定语言。
""".strip()


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
    has_ending = game_info.get("has_ending", True)
    has_chapters = game_info.get("has_chapters", False)
    
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
是否有结局：{'是' if has_ending else '否'}
是否有章节：{'是' if has_chapters else '否'}
输出语言：{language_name}（language_code: {language_code}）

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


# =========================
# 辅助函数
# =========================
def extract_first_json_object(raw: str) -> Tuple[Optional[dict], str]:
    """
    从模型输出里尽量抠出第一个 JSON object
    
    功能：从大模型的文本输出中提取第一个有效的 JSON 对象
    参数：
        raw: 模型输出的原始文本字符串
    返回：元组 (JSON对象或None, 错误信息字符串)
    """
    if not isinstance(raw, str) or not raw.strip():
        return None, "empty"

    raw = raw.strip()
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict):
            return obj, ""
    except Exception:
        pass

    start = raw.find("{")
    if start == -1:
        return None, "no_brace"

    depth = 0
    for i in range(start, len(raw)):
        ch = raw[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                candidate = raw[start : i + 1]
                try:
                    obj = json.loads(candidate)
                    if isinstance(obj, dict):
                        return obj, ""
                except Exception:
                    return None, "json_parse_failed"
                break

    return None, "unterminated_json"


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
