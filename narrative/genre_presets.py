"""
Genre-aware narrative presets.

Each genre defines: active lines, line weights, phase template, event filter.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

VALID_GENRES = ("story", "mystery", "romance", "exploration", "adventure", "mixed")
DEFAULT_GENRE = "story"


@dataclass
class GenrePreset:
    active_lines: List[str]  # phase, relationship, disclosure, risk
    line_weights: Dict[str, float]  # 0 = skip, >0 = weight for rules/prompt
    phase_template: str  # key in PHASE_TEMPLATES
    event_pool_filter: Optional[List[str]] = None  # event_id prefixes to include, None = all


# Phase templates: ordered list of phase strings per genre
# state_models.PHASE_TEMPLATES will be defined there; we reference by name
PHASE_TEMPLATE_KEYS = {
    "story": "story",
    "mystery": "mystery",
    "romance": "romance",
    "exploration": "exploration",
    "adventure": "story",  # same as story
    "mixed": "story",
}

GENRE_PRESETS: Dict[str, GenrePreset] = {
    "story": GenrePreset(
        active_lines=["phase", "relationship", "disclosure", "risk"],
        line_weights={"phase": 1.0, "relationship": 0.8, "disclosure": 0.8, "risk": 0.8},
        phase_template="story",
        event_pool_filter=None,
    ),
    "mystery": GenrePreset(
        active_lines=["phase", "disclosure", "relationship", "risk"],
        line_weights={"phase": 1.0, "relationship": 0.3, "disclosure": 1.0, "risk": 0.4},
        phase_template="mystery",
        event_pool_filter=["phase_", "disclosure_", "risk_"],
    ),
    "romance": GenrePreset(
        active_lines=["phase", "relationship", "disclosure", "risk"],
        line_weights={"phase": 1.0, "relationship": 1.0, "disclosure": 0.5, "risk": 0.2},
        phase_template="romance",
        event_pool_filter=["phase_", "relationship_"],
    ),
    "exploration": GenrePreset(
        active_lines=["phase", "disclosure", "risk", "relationship"],
        line_weights={"phase": 1.0, "relationship": 0.3, "disclosure": 0.8, "risk": 0.9},
        phase_template="exploration",
        event_pool_filter=["phase_", "risk_", "disclosure_"],
    ),
    "adventure": GenrePreset(
        active_lines=["phase", "relationship", "disclosure", "risk"],
        line_weights={"phase": 1.0, "relationship": 0.7, "disclosure": 0.7, "risk": 1.0},
        phase_template="story",
        event_pool_filter=None,
    ),
    "mixed": GenrePreset(
        active_lines=["phase", "relationship", "disclosure", "risk"],
        line_weights={"phase": 1.0, "relationship": 0.8, "disclosure": 0.8, "risk": 0.8},
        phase_template="story",
        event_pool_filter=None,
    ),
}


def get_preset(genre: Optional[str]) -> GenrePreset:
    """
    获取游戏类型预设
    
    功能：根据游戏类型返回对应的预设配置（包含活跃线、线权重、阶段模板等）
    参数：
        genre: 游戏类型字符串（如 "story", "mystery", "romance" 等）
    返回：GenrePreset 对象，如果类型无效则返回默认预设
    """
    g = (genre or "").strip().lower()
    if g not in VALID_GENRES:
        return GENRE_PRESETS[DEFAULT_GENRE]
    return GENRE_PRESETS[g]
