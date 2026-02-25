"""
Narrative State Machine - engine: init, update_and_get_events, apply_post_turn.

Orchestrates rules + events; used by GameManager.
Genre-aware initialization and updates.
"""

from typing import Any, Dict, List, Optional, Tuple

from narrative.state_models import NarrativeState, PHASE_TEMPLATES
from narrative.rules import apply_rules
from narrative.events import (
    NarrativeEvent,
    get_triggered_events,
    get_event_pool_for_genre,
    mark_events_triggered,
    apply_state_mutate,
    DEFAULT_EVENT_POOL,
)
from narrative.genre_presets import get_preset


def init_narrative_state(genre: Optional[str] = None) -> NarrativeState:
    """
    初始化叙事状态
    
    功能：在世界构建完成后创建默认的叙事状态对象，根据游戏类型设置初始阶段
    参数：
        genre: 游戏类型（如 "story", "mystery", "romance" 等）
    返回：初始化的 NarrativeState 对象
    """
    preset = get_preset(genre)
    template = PHASE_TEMPLATES.get(preset.phase_template, PHASE_TEMPLATES["story"])
    initial_phase = template[0] if template else "initial"
    return NarrativeState(phase=initial_phase)


def update_and_get_events(
    state: NarrativeState,
    player_message: str,
    round_count: int,
    genre: Optional[str] = None,
    event_pool: Optional[List[NarrativeEvent]] = None,
) -> Tuple[NarrativeState, List[NarrativeEvent]]:
    """
    更新叙事状态并检查事件触发
    
    功能：应用规则更新叙事状态，然后检查是否有事件被触发
    参数：
        state: 当前叙事状态
        player_message: 玩家消息
        round_count: 当前回合数
        genre: 游戏类型
        event_pool: 事件池（可选，默认使用类型对应的事件池）
    返回：元组 (更新后的叙事状态, 触发的事件列表)
    注意：如果事件被触发，调用者可以使用事件叙事；否则使用导演提示+LLM
    """
    updated = apply_rules(state, player_message, round_count, genre=genre)
    pool = event_pool
    if pool is None:
        pool = get_event_pool_for_genre(genre)
    triggered = get_triggered_events(updated, pool)
    return updated, triggered


def apply_post_turn_updates(
    state: NarrativeState,
    state_patch: Optional[Dict[str, Any]] = None,
) -> NarrativeState:
    """
    应用回合后的更新
    
    功能：在 LLM 返回后，可选地应用 state_patch 中的提示到叙事状态
    参数：
        state: 当前叙事状态
        state_patch: 状态补丁（可选，可能包含 narrative_state_delta）
    返回：更新后的叙事状态
    注意：目前如果 state_patch 包含 narrative_state_delta，会应用它；否则返回原状态
    """
    if not state_patch or not isinstance(state_patch, dict):
        return state
    # Optional: if state_patch contains narrative_state_delta, apply to state
    delta = state_patch.get("narrative_state_delta")
    if isinstance(delta, dict):
        apply_state_mutate(state, delta)
    return state


def compute_ending_id(state: NarrativeState, genre: Optional[str] = None) -> str:
    """
    计算结局 ID（多结局系统）
    
    功能：根据决策因素、阶段、风险等级等计算当前应触发的结局 ID
    参数：
        state: 当前叙事状态
        genre: 游戏类型（不同类型有不同的结局映射）
    返回：结局 ID 字符串（如 "ending_together", "ending_solved" 等）
    """
    factors = state.decision_factors
    trust = factors.get("trust_npc", 0.5)
    risk_taken = factors.get("risk_taken", 0.0)
    intimacy = state.relationship.intimacy
    phase = state.phase_value
    risk = state.risk_level.value

    if risk == "collapse":
        return "ending_collapse"

    if genre == "romance":
        if phase == "resolution" and intimacy >= 0.7:
            return "ending_together"
        if phase == "resolution" and intimacy >= 0.4 and intimacy < 0.7:
            return "ending_friendzone"
        if phase == "resolution" and intimacy < 0.4:
            return "ending_rejected"
        return "ending_unknown"

    if genre == "mystery":
        if phase == "resolution":
            return "ending_solved"
        return "ending_unsolved"

    if phase == "resolution" and trust >= 0.7 and risk_taken < 0.5:
        return "ending_peace"
    if phase == "resolution" and trust < 0.3:
        return "ending_betrayal"
    if phase == "resolution" and risk_taken >= 0.6:
        return "ending_risk"
    if phase == "resolution":
        return "ending_neutral"
    return "ending_unknown"
