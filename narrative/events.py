"""
Narrative State Machine - event pool and trigger dispatch.

Phase / risk / relationship / disclosure events; trigger conditions; override narrative.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from narrative.state_models import NarrativeState, DisclosureLevel, RiskLevel
from narrative.genre_presets import get_preset


@dataclass
class NarrativeEvent:
    event_id: str
    trigger_condition: str  # e.g. "phase:secret", "risk_level:critical"
    priority: int  # higher = checked first
    narrative_template: str  # text to show as this round's narrative (or key for lookup)
    state_mutate: Optional[Dict[str, Any]] = None  # optional changes to NarrativeState


def _trigger_phase(state: NarrativeState, event: NarrativeEvent) -> bool:
    """
    检查阶段触发条件
    
    功能：检查事件是否因当前阶段而触发（trigger_condition 格式：phase:secret）
    参数：
        state: 当前叙事状态
        event: 要检查的事件
    返回：如果触发条件满足返回 True，否则返回 False
    """
    parts = event.trigger_condition.split(":", 1)
    if len(parts) != 2 or parts[0].strip().lower() != "phase":
        return False
    want = parts[1].strip().lower()
    return state.phase_value == want


def _trigger_risk_level(state: NarrativeState, event: NarrativeEvent) -> bool:
    """
    检查风险等级触发条件
    
    功能：检查事件是否因当前风险等级而触发（trigger_condition 格式：risk_level:danger）
    参数：
        state: 当前叙事状态
        event: 要检查的事件
    返回：如果触发条件满足返回 True，否则返回 False
    """
    parts = event.trigger_condition.split(":", 1)
    if len(parts) != 2 or parts[0].strip().lower() != "risk_level":
        return False
    want = parts[1].strip().lower()
    return state.risk_level.value == want


def _trigger_disclosure(state: NarrativeState, event: NarrativeEvent) -> bool:
    """
    检查信息披露等级触发条件
    
    功能：检查事件是否因当前信息披露等级而触发（trigger_condition 格式：disclosure:full_reveal）
    参数：
        state: 当前叙事状态
        event: 要检查的事件
    返回：如果触发条件满足返回 True，否则返回 False
    """
    parts = event.trigger_condition.split(":", 1)
    if len(parts) != 2 or parts[0].strip().lower() != "disclosure":
        return False
    want = parts[1].strip().lower()
    return state.disclosure_level.value == want


def _trigger_relationship(state: NarrativeState, event: NarrativeEvent) -> bool:
    """
    检查关系触发条件
    
    功能：检查事件是否因关系值而触发（trigger_condition 格式：trust_above:0.8 或 hostility_above:0.5）
    参数：
        state: 当前叙事状态
        event: 要检查的事件
    返回：如果触发条件满足返回 True，否则返回 False
    """
    parts = event.trigger_condition.split(":", 1)
    if len(parts) != 2:
        return False
    key = parts[0].strip().lower()
    try:
        threshold = float(parts[1].strip())
    except ValueError:
        return False
    if key == "trust_above":
        return state.relationship.trust >= threshold
    if key == "trust_below":
        return state.relationship.trust <= threshold
    if key == "hostility_above":
        return state.relationship.hostility >= threshold
    if key == "intimacy_above":
        return state.relationship.intimacy >= threshold
    return False


def check_event_trigger(state: NarrativeState, event: NarrativeEvent) -> bool:
    """
    检查事件是否应该触发
    
    功能：检查事件的触发条件是否满足，且该事件尚未被触发过
    参数：
        state: 当前叙事状态
        event: 要检查的事件
    返回：如果应该触发返回 True，否则返回 False
    """
    if event.event_id in state.triggered_event_ids:
        return False
    cond = event.trigger_condition.strip().lower()
    if cond.startswith("phase:"):
        return _trigger_phase(state, event)
    if cond.startswith("risk_level:"):
        return _trigger_risk_level(state, event)
    if cond.startswith("disclosure:"):
        return _trigger_disclosure(state, event)
    if "trust_" in cond or "hostility_" in cond or "intimacy_" in cond:
        return _trigger_relationship(state, event)
    return False


def apply_state_mutate(state: NarrativeState, mutate: Dict[str, Any]) -> None:
    """
    应用状态变更到叙事状态
    
    功能：将状态变更字典应用到叙事状态对象上（原地修改）
    参数：
        state: 要修改的叙事状态对象
        mutate: 状态变更字典（可能包含 phase, disclosure_level, risk_value, flags 等）
    """
    if not mutate:
        return
    if "phase" in mutate and isinstance(mutate["phase"], str):
        state.phase = mutate["phase"]
    if "disclosure_level" in mutate and isinstance(mutate["disclosure_level"], str):
        for d in DisclosureLevel:
            if d.value == mutate["disclosure_level"]:
                state.disclosure_level = d
                break
    if "risk_value" in mutate:
        try:
            state.risk_value = max(0.0, min(1.0, float(mutate["risk_value"])))
        except (TypeError, ValueError):
            pass
    if "flags" in mutate and isinstance(mutate["flags"], dict):
        state.flags.update(mutate["flags"])


# ---------------------------------------------------------------------------
# Default event pool (configurable list)
# ---------------------------------------------------------------------------
DEFAULT_EVENT_POOL: List[NarrativeEvent] = [
    NarrativeEvent(
        event_id="phase_secret",
        trigger_condition="phase:secret",
        priority=100,
        narrative_template="【关键秘密阶段】真相的一角正在浮现，空气中弥漫着不安与期待。",
        state_mutate=None,
    ),
    NarrativeEvent(
        event_id="phase_climax",
        trigger_condition="phase:climax",
        priority=100,
        narrative_template="【高潮阶段】一切推向顶点，此刻的选择将决定故事的走向。",
        state_mutate=None,
    ),
    NarrativeEvent(
        event_id="risk_danger",
        trigger_condition="risk_level:danger",
        priority=80,
        narrative_template="【危险逼近】局势急转直下，危机近在眼前。",
        state_mutate=None,
    ),
    NarrativeEvent(
        event_id="risk_critical",
        trigger_condition="risk_level:critical",
        priority=90,
        narrative_template="【临界状态】再进一步便是万劫不复，必须做出抉择。",
        state_mutate=None,
    ),
    NarrativeEvent(
        event_id="risk_collapse",
        trigger_condition="risk_level:collapse",
        priority=95,
        narrative_template="【崩溃】局势失控，后果已然发生。",
        state_mutate=None,
    ),
    NarrativeEvent(
        event_id="disclosure_full",
        trigger_condition="disclosure:full_reveal",
        priority=70,
        narrative_template="【真相大白】所有的秘密终于被揭开。",
        state_mutate=None,
    ),
    # Romance-specific
    NarrativeEvent(
        event_id="phase_confession",
        trigger_condition="phase:confession",
        priority=85,
        narrative_template="【告白时刻】空气中弥漫着紧张与期待，是时候说出心里话了。",
        state_mutate=None,
    ),
    NarrativeEvent(
        event_id="relationship_confession",
        trigger_condition="intimacy_above:0.7",
        priority=75,
        narrative_template="【心意渐明】你们之间的关系似乎即将迎来重要的转折。",
        state_mutate=None,
    ),
    # Mystery-specific
    NarrativeEvent(
        event_id="phase_revelation",
        trigger_condition="phase:revelation",
        priority=90,
        narrative_template="【真相揭晓】关键线索串联起来，真相正在浮出水面。",
        state_mutate=None,
    ),
]


def get_event_pool_for_genre(genre: Optional[str] = None) -> List[NarrativeEvent]:
    """
    获取指定游戏类型的事件池
    
    功能：根据游戏类型返回对应的事件池，可能会根据类型预设进行过滤
    参数：
        genre: 游戏类型（如 "mystery", "romance" 等）
    返回：事件列表
    """
    preset = get_preset(genre)
    if not preset.event_pool_filter:
        return DEFAULT_EVENT_POOL
    filtered = []
    for ev in DEFAULT_EVENT_POOL:
        for prefix in preset.event_pool_filter:
            stem = prefix.rstrip("_")
            if ev.event_id.startswith(stem):
                filtered.append(ev)
                break
    return filtered if filtered else DEFAULT_EVENT_POOL


def get_triggered_events(
    state: NarrativeState,
    event_pool: Optional[List[NarrativeEvent]] = None,
) -> List[NarrativeEvent]:
    """
    获取本回合触发的事件列表
    
    功能：检查事件池中哪些事件在本回合被触发（尚未在 triggered_event_ids 中）
    参数：
        state: 当前叙事状态
        event_pool: 事件池（可选，默认使用 DEFAULT_EVENT_POOL）
    返回：按优先级降序排列的触发事件列表
    注意：返回所有匹配的事件，调用者可以选择优先级最高的
    """
    pool = event_pool or DEFAULT_EVENT_POOL
    triggered: List[NarrativeEvent] = []
    for ev in sorted(pool, key=lambda e: -e.priority):
        if check_event_trigger(state, ev):
            triggered.append(ev)
    return triggered


def mark_events_triggered(state: NarrativeState, events: List[NarrativeEvent]) -> None:
    """
    标记事件为已触发
    
    功能：将事件 ID 添加到状态的已触发事件列表中，避免重复触发
    参数：
        state: 叙事状态对象
        events: 要标记的事件列表
    """
    for ev in events:
        if ev.event_id not in state.triggered_event_ids:
            state.triggered_event_ids.append(ev.event_id)
