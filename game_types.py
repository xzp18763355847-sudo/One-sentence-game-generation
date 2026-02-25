"""
游戏类型定义和枚举
"""
from enum import Enum


class GameCategory(str, Enum):
    """游戏类别"""
    CHARACTER_COMPANION = "character_companion"  # 角色陪伴类
    STORY_GAME = "story_game"  # 剧情游戏类


class GameType(str, Enum):
    """游戏类型"""
    # 角色陪伴类
    COMPANION_ROUTE = "companion_route"  # 攻略类（有结局）
    COMPANION_OPEN = "companion_open"  # 开放式陪伴类（无结局）
    
    # 剧情游戏类
    STORY_CHAPTER = "story_chapter"  # 章节剧情类（有结局）
    STORY_OPEN = "story_open"  # 开放式剧情（无结局）


# 游戏类型配置
GAME_TYPE_CONFIG = {
    GameType.COMPANION_ROUTE: {
        "category": GameCategory.CHARACTER_COMPANION,
        "name": "攻略类（有结局）",
        "has_ending": True,
        "has_chapters": False,
    },
    GameType.COMPANION_OPEN: {
        "category": GameCategory.CHARACTER_COMPANION,
        "name": "开放式陪伴类（无结局）",
        "has_ending": False,
        "has_chapters": False,
    },
    GameType.STORY_CHAPTER: {
        "category": GameCategory.STORY_GAME,
        "name": "章节剧情类（有结局）",
        "has_ending": True,
        "has_chapters": True,
    },
    GameType.STORY_OPEN: {
        "category": GameCategory.STORY_GAME,
        "name": "开放式剧情（无结局）",
        "has_ending": False,
        "has_chapters": False,
    },
}


def get_game_type_info(game_type: str) -> dict:
    """
    获取游戏类型信息
    
    参数:
        game_type: 游戏类型字符串
        
    返回:
        游戏类型配置字典
    """
    try:
        gt = GameType(game_type)
        return GAME_TYPE_CONFIG.get(gt, {})
    except ValueError:
        return {}


def is_valid_game_type(game_type: str) -> bool:
    """
    检查游戏类型是否有效
    
    参数:
        game_type: 游戏类型字符串
        
    返回:
        是否为有效的游戏类型
    """
    try:
        GameType(game_type)
        return True
    except ValueError:
        return False
