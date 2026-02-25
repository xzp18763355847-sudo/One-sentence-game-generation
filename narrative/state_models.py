"""
Narrative State Machine - state models and four narrative lines.

Four lines: Story Phase, Relationship Tension, Knowledge Disclosure, Risk/Tension.
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# 1. Story Phase (剧情阶段线)
# ---------------------------------------------------------------------------
class StoryPhase(str, Enum):
    INITIAL = "initial"                    # 初始引入阶段
    WORLD_BUILDING = "world_building"      # 世界观展开阶段
    CONFLICT_INTRO = "conflict_intro"      # 冲突出现阶段
    CONFLICT_ESCALATION = "conflict_escalation"  # 冲突升级阶段
    SECRET = "secret"                      # 关键秘密阶段
    CLIMAX = "climax"                      # 高潮阶段
    RESOLUTION = "resolution"             # 结局收束阶段


# Ordered for "next phase" checks; only allow advancing along this sequence.
PHASE_ORDER: List[StoryPhase] = [
    StoryPhase.INITIAL,
    StoryPhase.WORLD_BUILDING,
    StoryPhase.CONFLICT_INTRO,
    StoryPhase.CONFLICT_ESCALATION,
    StoryPhase.SECRET,
    StoryPhase.CLIMAX,
    StoryPhase.RESOLUTION,
]

# Phase templates per genre (phase as string for flexibility)
PHASE_TEMPLATES: Dict[str, List[str]] = {
    "story": [p.value for p in PHASE_ORDER],
    "mystery": ["intro", "clue_gathering", "theory", "revelation", "resolution"],
    "romance": ["meeting", "bonding", "tension", "confession", "resolution"],
    "exploration": ["discovery", "mapping", "deeper", "secret_area", "resolution"],
}


# ---------------------------------------------------------------------------
# 2. Relationship Tension (关系张力线) - single primary NPC for v1
# ---------------------------------------------------------------------------
@dataclass
class RelationshipVector:
    """trust, intimacy, hostility in [0, 1]."""
    trust: float = 0.5
    intimacy: float = 0.0
    hostility: float = 0.0

    def clamp(self) -> "RelationshipVector":
        """
        限制关系值在有效范围内
        
        功能：确保 trust、intimacy、hostility 都在 [0, 1] 范围内
        返回：限制后的新 RelationshipVector 对象
        """
        return RelationshipVector(
            trust=max(0.0, min(1.0, self.trust)),
            intimacy=max(0.0, min(1.0, self.intimacy)),
            hostility=max(0.0, min(1.0, self.hostility)),
        )

    def to_dict(self) -> dict:
        """
        转换为字典
        
        功能：将关系向量转换为字典格式
        返回：包含 trust、intimacy、hostility 的字典
        """
        return {"trust": self.trust, "intimacy": self.intimacy, "hostility": self.hostility}

    @staticmethod
    def from_dict(d: Any) -> "RelationshipVector":
        """
        从字典创建 RelationshipVector 对象
        
        功能：从字典数据中恢复关系向量对象
        参数：
            d: 字典数据
        返回：RelationshipVector 对象
        """
        if not isinstance(d, dict):
            return RelationshipVector()
        return RelationshipVector(
            trust=float(d.get("trust", 0.5)),
            intimacy=float(d.get("intimacy", 0.0)),
            hostility=float(d.get("hostility", 0.0)),
        ).clamp()


# ---------------------------------------------------------------------------
# 3. Knowledge Disclosure (信息揭露线)
# ---------------------------------------------------------------------------
class DisclosureLevel(str, Enum):
    UNKNOWN = "unknown"           # 完全未知
    VAGUE_HINT = "vague_hint"     # 模糊暗示
    CLUE = "clue"                 # 线索阶段
    HALF_TRUTH = "half_truth"     # 半真相阶段
    FULL_REVEAL = "full_reveal"   # 完全揭露阶段


DISCLOSURE_ORDER: List[DisclosureLevel] = [
    DisclosureLevel.UNKNOWN,
    DisclosureLevel.VAGUE_HINT,
    DisclosureLevel.CLUE,
    DisclosureLevel.HALF_TRUTH,
    DisclosureLevel.FULL_REVEAL,
]


# ---------------------------------------------------------------------------
# 4. Risk / Tension (风险与紧张线)
# ---------------------------------------------------------------------------
class RiskLevel(str, Enum):
    SAFE = "safe"
    WARNING = "warning"
    DANGER = "danger"
    CRITICAL = "critical"
    COLLAPSE = "collapse"


RISK_ORDER: List[RiskLevel] = [
    RiskLevel.SAFE,
    RiskLevel.WARNING,
    RiskLevel.DANGER,
    RiskLevel.CRITICAL,
    RiskLevel.COLLAPSE,
]


def risk_value_to_level(value: float) -> RiskLevel:
    """
    将风险值映射为风险等级
    
    功能：将 [0, 1] 范围的风险值转换为对应的风险等级枚举
    参数：
        value: 风险值（0-1）
    返回：RiskLevel 枚举值
    """
    value = max(0.0, min(1.0, value))
    if value < 0.2:
        return RiskLevel.SAFE
    if value < 0.4:
        return RiskLevel.WARNING
    if value < 0.6:
        return RiskLevel.DANGER
    if value < 0.8:
        return RiskLevel.CRITICAL
    return RiskLevel.COLLAPSE


# ---------------------------------------------------------------------------
# 5. Unified Narrative State (phase as str for genre flexibility)
# ---------------------------------------------------------------------------
@dataclass
class NarrativeState:
    phase: str = "initial"  # str for genre-specific phases
    relationship: RelationshipVector = field(default_factory=RelationshipVector)
    disclosure_level: DisclosureLevel = DisclosureLevel.UNKNOWN
    risk_value: float = 0.0  # [0, 1]; risk_level derived
    flags: Dict[str, Any] = field(default_factory=dict)
    decision_factors: Dict[str, float] = field(default_factory=dict)
    triggered_event_ids: List[str] = field(default_factory=list)

    @property
    def risk_level(self) -> RiskLevel:
        """
        获取当前风险等级（属性）
        
        功能：根据 risk_value 计算并返回对应的风险等级
        返回：RiskLevel 枚举值
        """
        return risk_value_to_level(self.risk_value)

    @property
    def phase_value(self) -> str:
        """
        获取阶段字符串值（属性）
        
        功能：返回阶段的字符串值，用于事件、提示等场景
        返回：阶段名称字符串
        """
        return self.phase if isinstance(self.phase, str) else getattr(self.phase, "value", "initial")

    def to_dict(self) -> dict:
        return {
            "phase": self.phase_value,
            "relationship": self.relationship.to_dict(),
            "disclosure_level": self.disclosure_level.value,
            "risk_value": self.risk_value,
            "flags": self.flags,
            "decision_factors": self.decision_factors,
            "triggered_event_ids": list(self.triggered_event_ids),
        }

    @staticmethod
    def from_dict(d: Any) -> "NarrativeState":
        """
        从字典创建 NarrativeState 对象
        
        功能：从字典数据中恢复叙事状态对象
        参数：
            d: 字典数据
        返回：NarrativeState 对象
        """
        if not isinstance(d, dict):
            return NarrativeState()
        ns = NarrativeState()
        p = d.get("phase", "initial")
        ns.phase = p if isinstance(p, str) else str(p)
        ns.relationship = RelationshipVector.from_dict(d.get("relationship", {}))
        dl = d.get("disclosure_level", DisclosureLevel.UNKNOWN.value)
        if isinstance(dl, str) and dl in {e.value for e in DisclosureLevel}:
            ns.disclosure_level = DisclosureLevel(dl)
        ns.risk_value = float(d.get("risk_value", 0.0))
        ns.risk_value = max(0.0, min(1.0, ns.risk_value))
        ns.flags = d.get("flags", {}) if isinstance(d.get("flags"), dict) else {}
        ns.decision_factors = d.get("decision_factors", {}) if isinstance(d.get("decision_factors"), dict) else {}
        ids_raw = d.get("triggered_event_ids", [])
        ns.triggered_event_ids = [x for x in ids_raw if isinstance(x, str)]
        return ns
