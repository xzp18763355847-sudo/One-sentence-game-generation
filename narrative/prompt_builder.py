"""
Narrative State Machine - director layer prompt construction.

Builds text to inject into system prompt to constrain LLM output.
Genre-aware: conditional sections by active_lines/line_weights.
"""

import logging
from typing import Optional

from narrative.state_models import NarrativeState, DisclosureLevel, RiskLevel
from narrative.genre_presets import get_preset

logger = logging.getLogger(__name__)


# Phase descriptions by phase string (all templates)
PHASE_DESCRIPTIONS: dict = {
    "initial": "当前处于【初始引入阶段】。叙事应建立情境、介绍角色与背景，不宜过快推进冲突。",
    "world_building": "当前处于【世界观展开阶段】。叙事应丰富世界细节、地点与规则，让玩家逐步熟悉环境。",
    "conflict_intro": "当前处于【冲突出现阶段】。叙事应引入主要矛盾或对立，但尚未激化。",
    "conflict_escalation": "当前处于【冲突升级阶段】。叙事需加强张力，让危机感上升。",
    "secret": "当前处于【关键秘密阶段】。叙事可逐步揭示核心秘密，但仍需控制披露节奏。",
    "climax": "当前处于【高潮阶段】。叙事应推向高潮，做出关键抉择或转折。",
    "resolution": "当前处于【结局收束阶段】。叙事应收束主线，给出结局感。",
    "intro": "当前处于【引入阶段】。叙事应建立谜题情境、介绍关键人物与环境。",
    "clue_gathering": "当前处于【线索收集阶段】。叙事应提供可调查的线索，但不得直接揭晓真相。",
    "theory": "当前处于【推理阶段】。叙事可允许玩家提出假设，逐步逼近真相。",
    "revelation": "当前处于【真相揭晓阶段】。叙事可逐步揭示核心秘密。",
    "meeting": "当前处于【相遇阶段】。叙事应建立初次印象、营造氛围。",
    "bonding": "当前处于【互动升温阶段】。叙事应推进关系发展、情感铺垫。",
    "tension": "当前处于【情感张力阶段】。叙事应制造暧昧或冲突，为表白铺垫。",
    "confession": "当前处于【告白阶段】。叙事应收束情感线，给出关系走向。",
    "discovery": "当前处于【探索发现阶段】。叙事应呈现新区域、新事物。",
    "mapping": "当前处于【区域探索阶段】。叙事应丰富环境细节、提示可探索方向。",
    "deeper": "当前处于【深入探索阶段】。叙事应增加神秘感与发现感。",
    "secret_area": "当前处于【隐藏区域阶段】。叙事可揭示重要发现或秘密。",
}


DISCLOSURE_CONSTRAINTS = {
    DisclosureLevel.UNKNOWN: "【信息披露】当前仅允许完全未知：不得透露任何真相或暗示，仅可描述表象。",
    DisclosureLevel.VAGUE_HINT: "【信息披露】当前仅允许模糊暗示：可给出极模糊的暗示，禁止直接说出真相或关键线索。",
    DisclosureLevel.CLUE: "【信息披露】当前允许线索阶段：可给出具体线索，但不得直接揭露核心真相。",
    DisclosureLevel.HALF_TRUTH: "【信息披露】当前允许半真相：可部分揭露真相，但仍保留关键秘密。",
    DisclosureLevel.FULL_REVEAL: "【信息披露】当前允许完全揭露：可根据剧情需要揭露真相。",
}


RISK_DESCRIPTIONS = {
    RiskLevel.SAFE: "【风险等级】当前为安全状态。叙事语气可平和，无需强调危机。",
    RiskLevel.WARNING: "【风险等级】当前为警告状态。叙事可略带紧张感，提示潜在风险。",
    RiskLevel.DANGER: "【风险等级】当前为危险状态。叙事应体现危机感与紧迫感。",
    RiskLevel.CRITICAL: "【风险等级】当前为临界状态。叙事应高度紧张，失败后果严重。",
    RiskLevel.COLLAPSE: "【风险等级】当前为崩溃状态。叙事应体现局势失控或重大失败。",
}


def _relationship_summary(state: NarrativeState) -> str:
    """
    生成关系状态摘要文本
    
    功能：根据当前关系向量生成描述关系状态的文本，用于导演提示
    参数：
        state: 当前叙事状态
    返回：关系状态描述字符串
    """
    r = state.relationship
    parts = []
    if r.trust >= 0.7:
        parts.append("NPC 信任度高，语气应偏合作、坦诚。")
    elif r.trust >= 0.4:
        parts.append("NPC 信任度中等，语气可略带保留。")
    else:
        parts.append("NPC 信任度低，语气应偏戒备、疏离。")
    if r.hostility >= 0.5:
        parts.append("对立度较高，NPC 可能表现出敌意或对抗。")
    elif r.hostility >= 0.2:
        parts.append("对立度中等，NPC 可能有所保留或试探。")
    else:
        parts.append("对立度低，NPC 态度相对友好。")
    if r.intimacy >= 0.5:
        parts.append("亲密度较高，可体现亲密或私密对话。")
    return "【关系状态】" + " ".join(parts)


def build_director_prompt(narrative_state: NarrativeState, genre: Optional[str] = None) -> str:
    """
    构建导演提示文本
    
    功能：根据当前叙事状态构建导演指令文本，用于约束 LLM 的输出
    参数：
        narrative_state: 当前叙事状态
        genre: 游戏类型（影响哪些部分被包含，通过 line_weights 控制）
    返回：导演提示文本字符串
    """
    preset = get_preset(genre)
    weights = preset.line_weights

    lines = [
        "---",
        "【导演指令层】以下约束必须遵守：",
        "",
        PHASE_DESCRIPTIONS.get(
            (narrative_state.phase_value or "").lower(),
            "当前剧情阶段需保持连贯。"
        ),
    ]

    if weights.get("relationship", 0.8) > 0:
        lines.extend(["", _relationship_summary(narrative_state)])
    if weights.get("disclosure", 0.8) > 0:
        lines.extend([
            "",
            DISCLOSURE_CONSTRAINTS.get(narrative_state.disclosure_level, "不得提前暴露关键真相。"),
        ])
    if weights.get("risk", 0.8) > 0:
        lines.extend([
            "",
            RISK_DESCRIPTIONS.get(narrative_state.risk_level, "根据当前风险控制叙事节奏。"),
        ])

    lines.extend([
        "",
        "语言风格与情绪表现需与上述阶段、关系、风险一致；禁止提前披露未允许的信息；本阶段不宜过快收尾。",
        "---",
    ])
    return "\n".join(lines)


OFFCIAL_GAME_PROMPT = {
    "og001": {
        "cn": {
            "name": "非法死亡",
            "type": "story_based",
            "rule": "你是一名医生，今天你要去做一件大事——帮助母亲安乐死。你的母亲患上了一种罕见病，多年来十分痛苦，活着对她而言是一种折磨。但在科技发达、意识上传已成铁律的3026年，死亡是被严厉禁止的。你来到了一处废旧殡仪馆，这里的老板私下里偷偷经营着“非法死亡”的生意……",
            "rule_extra": "根据上述章节划分转场，选择不同选项导向不同剧情分支，共11题，进而导向不同结局。",
            "background": """3026年，人类达到了前所未有的科技巅峰。脑机接口已普及全球90%的人口，意识上传成为常态，死亡被重新定义为“非自然信息中断”——一种可以避免的故障。在这个世界上，肉体死亡只是短暂的不便，任何人都可以选择在任意年龄脱离肉体，让意识在新载体上延续。在这个永生成为常态的时代，拒绝数字永生、接受自然死亡的人成为异类。
国际联邦政府在3026年1月1日出台新法律，规定：
1.死亡是一种非法行为。所有人必须在肉体死亡前上传意识，确保意识永生。
2.人类肉体的自然寿命为120岁，120岁前肉体自杀者犯重罪。
3.任何人上传意识后，肉体都由政府依法供养。""",
            "role": "Orpheus",
            "role_setting": "",
        },
        "en": {
            "name": "Illegal Death",
            "type": "story_based",
            "rule": "",
            "rule_extra": "",
            "background": "",
            "role": "Orpheus",
            "role_setting": "",
        }
    },
    "og002": {
        "cn": {
            "name": "逃离天堂岛",
            "type": "story_based",
            "rule": "欢迎来到天堂岛，这里是属于所有动物的家园。所有人类访客必须遵守动物规则，并解锁每一条动物规则存在的原因，否则……将成为岛的一部分。",
            "rule_extra": """在最开始进入游戏后不公布动物规则是什么，只说明存在“动物规则”这个东西。
每一章节对应一条动物规则，由山羊引导玩家在特殊情境下触发规则，然后接着玩家需要和山羊对话，解谜每条规则背后的原因。
设置解锁度，总共100%，每解锁一条规则，解锁度+20%，最后一章结算（确保玩家即使前面全解锁了也能玩到最后），解锁度≥60%，玩家可以安全离开天堂岛。""",
            "background": """3026年，世界末日来临，地球90%的陆地寸草不生，难以居住。你们是研究“无污染生态系统”的顶尖科学家，受邀来到天堂岛——这座传说中“动物自治的净土”。
天堂岛的动物们制定了一系列“动物规则”，作为访客，你们必须严格遵守，否则会受到惩罚。
请注意：
1.动物们为了捉弄你们，并不打算直接告诉你们规则是什么，请在接下来的旅途中处处小心。
2.每条“动物规则”对应一条人类罪行，请认真思考，这是你安全离开的钥匙。""",
            "role": "山羊，乌鸦",
            "role_setting": "",
        },
        "en": {
            "name": "",
            "type": "story_based",
            "rule": "",
            "rule_extra": "",
            "background": "",
            "role": "Orpheus",
            "role_setting": "",
        }
    }
}


def get_official_game_prompt(game_id: str, language_code: str):
    """
    获取官方游戏提示文本

    参数：
        game_id: 游戏ID
        language_code: 语言代码
    返回：官方游戏提示文本
    """
    prompt_dict = OFFCIAL_GAME_PROMPT.get(game_id, {}).get(language_code, {})
    if not prompt_dict:
        logger.warning(f"未找到游戏配置: game_id={game_id}, language_code={language_code}")
    else:
        logger.info(f"找到游戏配置: game_id={game_id}, language_code={language_code}, name={prompt_dict.get('name', '')}")
    prompts = f"""基于输入的结构化游戏信息，生成一个可分章节推进的完整游戏剧本设计稿。
    【游戏名称】
    {prompt_dict.get("name", "")}

    【游戏类型】
    {prompt_dict.get("type", "")}

    【核心规则（世界观层）】
    {prompt_dict.get("rule", "")}

    【规则补充与玩法约束（可能为空）】
    {prompt_dict.get("rule_extra", "")}

    【世界观背景】
    {prompt_dict.get("background", "")}

    【可用角色 / NPC】
    {prompt_dict.get("role", "")}

    【角色补充设定（可能为空）】
    {prompt_dict.get("role_setting", "")}
    """.strip()
    game_type = prompt_dict.get("type", "")
    return prompts, game_type
