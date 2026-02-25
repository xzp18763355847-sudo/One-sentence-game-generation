"""
Narrative State Machine - rule engine for updating the four lines.

Configurable phase transitions, relationship/disclosure/risk updates.
Genre-aware: phase template, line weights.
"""

import re
from typing import Any, Dict, List, Optional, Tuple

from narrative.state_models import (
    NarrativeState,
    StoryPhase,
    DisclosureLevel,
    RiskLevel,
    RelationshipVector,
    PHASE_ORDER,
    PHASE_TEMPLATES,
    DISCLOSURE_ORDER,
    risk_value_to_level,
)
from narrative.genre_presets import get_preset, GenrePreset, DEFAULT_GENRE


# ---------------------------------------------------------------------------
# Phase: allowed next phases (strict order, template-based)
# ---------------------------------------------------------------------------
def get_next_phase_for_template(phase: str, template: List[str]) -> Optional[str]:
    """
    获取模板中的下一个阶段
    
    功能：根据阶段模板顺序，返回当前阶段的下一个阶段
    参数：
        phase: 当前阶段名称
        template: 阶段模板列表（有序）
    返回：下一个阶段名称，如果已经是最后一个阶段则返回 None
    """
    try:
        i = template.index(phase)
        if i + 1 < len(template):
            return template[i + 1]
    except (ValueError, TypeError):
        pass
    return None


def can_advance_phase(state: NarrativeState, round_count: int, preset: GenrePreset) -> bool:
    """
    检查是否可以推进阶段
    
    功能：判断当前是否满足推进到下一个阶段的条件（每 N 回合推进一次）
    参数：
        state: 当前叙事状态
        round_count: 当前回合数
        preset: 游戏类型预设
    返回：如果可以推进返回 True，否则返回 False
    """
    phase_advance_rounds = 3
    template = PHASE_TEMPLATES.get(preset.phase_template, PHASE_TEMPLATES["story"])
    next_phase = get_next_phase_for_template(state.phase_value, template)
    if next_phase is None:
        return False
    return round_count > 0 and round_count % phase_advance_rounds == 0


# ---------------------------------------------------------------------------
# Phase -> max allowed disclosure (do not reveal beyond this)
# ---------------------------------------------------------------------------
PHASE_MAX_DISCLOSURE_STORY: Dict[str, DisclosureLevel] = {
    "initial": DisclosureLevel.UNKNOWN,
    "world_building": DisclosureLevel.VAGUE_HINT,
    "conflict_intro": DisclosureLevel.CLUE,
    "conflict_escalation": DisclosureLevel.CLUE,
    "secret": DisclosureLevel.HALF_TRUTH,
    "climax": DisclosureLevel.FULL_REVEAL,
    "resolution": DisclosureLevel.FULL_REVEAL,
}
PHASE_MAX_DISCLOSURE_MYSTERY: Dict[str, DisclosureLevel] = {
    "intro": DisclosureLevel.UNKNOWN,
    "clue_gathering": DisclosureLevel.CLUE,
    "theory": DisclosureLevel.HALF_TRUTH,
    "revelation": DisclosureLevel.FULL_REVEAL,
    "resolution": DisclosureLevel.FULL_REVEAL,
}
PHASE_MAX_DISCLOSURE_ROMANCE: Dict[str, DisclosureLevel] = {
    "meeting": DisclosureLevel.UNKNOWN,
    "bonding": DisclosureLevel.VAGUE_HINT,
    "tension": DisclosureLevel.CLUE,
    "confession": DisclosureLevel.HALF_TRUTH,
    "resolution": DisclosureLevel.FULL_REVEAL,
}
PHASE_MAX_DISCLOSURE_EXPLORATION: Dict[str, DisclosureLevel] = {
    "discovery": DisclosureLevel.UNKNOWN,
    "mapping": DisclosureLevel.VAGUE_HINT,
    "deeper": DisclosureLevel.CLUE,
    "secret_area": DisclosureLevel.HALF_TRUTH,
    "resolution": DisclosureLevel.FULL_REVEAL,
}
PHASE_MAX_DISCLOSURE_BY_TEMPLATE: Dict[str, Dict[str, DisclosureLevel]] = {
    "story": PHASE_MAX_DISCLOSURE_STORY,
    "mystery": PHASE_MAX_DISCLOSURE_MYSTERY,
    "romance": PHASE_MAX_DISCLOSURE_ROMANCE,
    "exploration": PHASE_MAX_DISCLOSURE_EXPLORATION,
}


def get_max_disclosure_for_phase(phase: str, template_key: str = "story") -> DisclosureLevel:
    """
    获取阶段允许的最大信息披露等级
    
    功能：根据当前阶段和模板类型，返回该阶段允许的最大信息披露等级
    参数：
        phase: 当前阶段名称
        template_key: 模板键（如 "story", "mystery" 等）
    返回：允许的最大信息披露等级
    """
    mapping = PHASE_MAX_DISCLOSURE_BY_TEMPLATE.get(template_key, PHASE_MAX_DISCLOSURE_STORY)
    return mapping.get((phase or "").lower(), DisclosureLevel.UNKNOWN)


def disclosure_level_index(level: DisclosureLevel) -> int:
    """
    获取信息披露等级的索引
    
    功能：返回信息披露等级在顺序列表中的索引位置
    参数：
        level: 信息披露等级
    返回：索引值（0 为最低等级）
    """
    try:
        return DISCLOSURE_ORDER.index(level)
    except ValueError:
        return 0


def can_raise_disclosure(state: NarrativeState, template_key: str = "story") -> bool:
    """
    检查是否可以提升信息披露等级
    
    功能：判断当前是否可以提升信息披露等级（不超过阶段允许的最大值）
    参数：
        state: 当前叙事状态
        template_key: 模板键
    返回：如果可以提升返回 True，否则返回 False
    """
    max_d = get_max_disclosure_for_phase(state.phase_value, template_key)
    return disclosure_level_index(state.disclosure_level) < disclosure_level_index(max_d)


# ---------------------------------------------------------------------------
# Simple behavior hints from player message (keyword-based)
# ---------------------------------------------------------------------------
COOPERATIVE_KEYWORDS = re.compile(
    r"帮助|合作|一起|相信|信任|同意|支持|谢谢|感谢|拜托"
)
CONFLICT_KEYWORDS = re.compile(
    r"反对|拒绝|攻击|威胁|欺骗|隐瞒|偷|抢|杀"
)
INTIMACY_KEYWORDS = re.compile(
    r"关心|担心|喜欢|爱|拥抱|安慰|陪伴|表白|牵手|约会|告白"
)
RISKY_KEYWORDS = re.compile(
    r"冒险|赌|拼命|豁出去|冲|闯入|偷袭"
)
MYSTERY_KEYWORDS = re.compile(
    r"调查|推理|破解|搜索|检查|分析|线索|证据"
)


def classify_player_behavior(message: str, genre: Optional[str] = None) -> Dict[str, float]:
    """
    分类玩家行为并返回状态变化增量
    
    功能：通过关键词匹配分析玩家消息，返回对关系、风险、信息披露等状态的影响增量
    参数：
        message: 玩家消息文本
        genre: 游戏类型（可选，影响某些行为的识别）
    返回：包含各种增量值的字典（如 trust_delta, hostility_delta, risk_delta 等），值范围在 [-0.2, 0.2]
    """
    text = (message or "").strip()
    if not text:
        return {}
    out: Dict[str, float] = {}
    if COOPERATIVE_KEYWORDS.search(text):
        out["trust_delta"] = 0.1
        out["hostility_delta"] = -0.05
    if CONFLICT_KEYWORDS.search(text):
        out["trust_delta"] = -0.1
        out["hostility_delta"] = 0.15
    if INTIMACY_KEYWORDS.search(text):
        out["intimacy_delta"] = 0.1
    if RISKY_KEYWORDS.search(text):
        out["risk_delta"] = 0.1
    if genre == "mystery" and MYSTERY_KEYWORDS.search(text):
        out["disclosure_delta"] = 0.1
    return out


# ---------------------------------------------------------------------------
# Apply rules: update state from current state + player message + round
# ---------------------------------------------------------------------------
def apply_rules(
    state: NarrativeState,
    player_message: str,
    round_count: int,
    genre: Optional[str] = None,
) -> NarrativeState:
    """
    应用规则更新叙事状态
    
    功能：根据规则计算下一个叙事状态，不修改输入状态
    参数：
        state: 当前叙事状态
        player_message: 玩家消息
        round_count: 当前回合数
        genre: 游戏类型（影响阶段模板、线权重和行为分类）
    返回：更新后的新叙事状态对象
    """
    preset = get_preset(genre)
    template = PHASE_TEMPLATES.get(preset.phase_template, PHASE_TEMPLATES["story"])
    weights = preset.line_weights

    next_state = NarrativeState(
        phase=state.phase_value,
        relationship=RelationshipVector(
            trust=state.relationship.trust,
            intimacy=state.relationship.intimacy,
            hostility=state.relationship.hostility,
        ),
        disclosure_level=state.disclosure_level,
        risk_value=state.risk_value,
        flags=dict(state.flags),
        decision_factors=dict(state.decision_factors),
        triggered_event_ids=list(state.triggered_event_ids),
    )

    deltas = classify_player_behavior(player_message, genre)

    # 1) Phase: advance if condition met, strict order
    if can_advance_phase(next_state, round_count, preset):
        nxt = get_next_phase_for_template(next_state.phase_value, template)
        if nxt is not None:
            next_state.phase = nxt

    # 2) Relationship: apply behavior deltas (weighted)
    w_rel = weights.get("relationship", 0.8)
    if w_rel > 0:
        next_state.relationship.trust = max(0.0, min(1.0, next_state.relationship.trust + deltas.get("trust_delta", 0) * w_rel))
        next_state.relationship.intimacy = max(0.0, min(1.0, next_state.relationship.intimacy + deltas.get("intimacy_delta", 0) * w_rel))
        next_state.relationship.hostility = max(0.0, min(1.0, next_state.relationship.hostility + deltas.get("hostility_delta", 0) * w_rel))

    # 3) Disclosure: advance one step if phase allows, or apply disclosure_delta (mystery)
    w_disc = weights.get("disclosure", 0.8)
    if w_disc > 0:
        if "disclosure_delta" in deltas:
            idx = disclosure_level_index(next_state.disclosure_level)
            if idx + 1 < len(DISCLOSURE_ORDER):
                next_state.disclosure_level = DISCLOSURE_ORDER[idx + 1]
        elif can_raise_disclosure(next_state, preset.phase_template):
            idx = disclosure_level_index(next_state.disclosure_level)
            max_d = get_max_disclosure_for_phase(next_state.phase_value, preset.phase_template)
            max_idx = disclosure_level_index(max_d)
            if idx + 1 <= max_idx and idx + 1 < len(DISCLOSURE_ORDER):
                next_state.disclosure_level = DISCLOSURE_ORDER[idx + 1]

    # 4) Risk: apply delta (weighted)
    w_risk = weights.get("risk", 0.8)
    if w_risk > 0:
        next_state.risk_value = max(0.0, min(1.0, next_state.risk_value + deltas.get("risk_delta", 0) * w_risk))

    # 5) Decision factors (for multi-ending): accumulate from deltas
    if "trust_delta" in deltas:
        next_state.decision_factors["trust_npc"] = next_state.decision_factors.get("trust_npc", 0.5) + deltas["trust_delta"] * 0.5
    if "risk_delta" in deltas:
        next_state.decision_factors["risk_taken"] = next_state.decision_factors.get("risk_taken", 0.0) + deltas.get("risk_delta", 0) * 0.5
    for k, v in next_state.decision_factors.items():
        next_state.decision_factors[k] = max(0.0, min(1.0, v))

    return next_state
