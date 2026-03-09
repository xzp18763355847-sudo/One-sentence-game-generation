"""
State Schema 定义 - 固定的状态结构

核心原则：
- 状态层结构必须固定，只允许数值变化
- 严禁模型新增、删除或重命名任何 state 字段
- 所有状态变化必须显式体现在 state_delta 中
"""

from typing import Dict, Any, List, Optional, Set
import logging

logger = logging.getLogger(__name__)


class StateSchema:
    """
    定义固定的状态结构 schema
    
    最小Demo示例：RPG游戏
    - player: {hp, max_hp, level, status}
    - monster: {hp, max_hp, name} (可选)
    - world: {scene, time, location}
    
    或情感游戏示例：
    - player: {name, status}
    - npc: {name, affection, relationship}
    - world: {scene, time}
    """
    
    # 定义允许的顶层字段及其子字段结构
    # 格式: {顶层字段名: {子字段名: 类型约束}}
    # 类型约束可以是: int, float, str, dict, list, Any
    SCHEMA = {
        "player": {
            "hp": int,
            "max_hp": int,
            "level": int,
            "status": str,
            "name": str,
        },
        
        "npc": {  # 可选，如果游戏中有NPC
            "name": str,
            "affection": int,  # 好感度 0-100
            "relationship": str,
        },
        "world": {
            "scene": str,
            "time": str,
            "location": str,
        },
        "chapter": {  # 可选，如果游戏有章节系统
            "current_chapter": int,  # 当前章节编号（从1开始）
            "chapter_progress": str,  # 章节进度描述（如："进行中"、"已完成"）
            "chapter_goal_completed": bool,  # 当前章节目标是否已完成
        },
        "guide": {  # 对话引导，用于避免重复回复
            "already_suggested": str,  # 已经提出过的话
            "pending": str,  # 下一步引导工作
        },
    }
    
    @classmethod
    def get_allowed_top_level_keys(cls) -> Set[str]:
        """
        返回所有允许的顶层字段名
        
        功能：获取状态 schema 中定义的所有顶层字段名（如 player, monster, npc, world）
        返回：顶层字段名的集合
        """
        return set(cls.SCHEMA.keys())
    
    @classmethod
    def get_allowed_fields_for_key(cls, top_level_key: str) -> Set[str]:
        """
        返回某个顶层字段下允许的子字段名
        
        功能：获取指定顶层字段下允许的所有子字段名
        参数：
            top_level_key: 顶层字段名（如 "player"）
        返回：子字段名的集合
        """
        if top_level_key not in cls.SCHEMA:
            return set()
        return set(cls.SCHEMA[top_level_key].keys())
    
    @classmethod
    def validate_state_delta(cls, state_delta: Dict[str, Any], current_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        校验并过滤 state_delta
        
        规则：
        1. 允许更新已存在的顶层字段
        2. 允许添加新的 npc 字段（如果当前状态中没有 npc，可以在 state_delta 中添加完整的 npc 对象）
        3. 只允许更新已存在的子字段（不允许新增子字段，除非是添加新的 npc）
        4. 类型必须匹配（int/float/str/dict/list）
        5. 数值做 clamp（如 hp >= 0, affection 0-100）
        
        返回：过滤后的安全 state_delta
        """
        if not isinstance(state_delta, dict):
            logger.warning(f"state_delta 不是 dict，已丢弃: {type(state_delta)}")
            return {}
        
        if not isinstance(current_state, dict):
            logger.warning(f"current_state 不是 dict，无法校验")
            return {}
        
        filtered_delta = {}
        current_top_keys = set(current_state.keys())
        allowed_top_keys = cls.get_allowed_top_level_keys()
        dropped: List[str] = []

        for top_key, top_value in state_delta.items():
            # 检查是否是允许的顶层字段
            if top_key not in allowed_top_keys:
                dropped.append(f"顶层:{top_key}(不允许的字段)")
                continue
            
            # 特殊处理：允许添加新的 npc 字段
            if top_key == "npc" and top_key not in current_top_keys:
                # 当前状态中没有 npc，允许添加新的 npc
                if isinstance(top_value, dict):
                    # 验证新 npc 的字段是否符合 schema
                    allowed_npc_fields = cls.get_allowed_fields_for_key("npc")
                    filtered_npc = {}
                    for sub_key, sub_value in top_value.items():
                        if sub_key in allowed_npc_fields:
                            validated_value = cls._validate_and_clamp_value(
                                top_key, sub_key, sub_value, None
                            )
                            if validated_value is not None:
                                filtered_npc[sub_key] = validated_value
                            else:
                                dropped.append(f"{top_key}.{sub_key}(类型/转换失败)")
                        else:
                            dropped.append(f"{top_key}.{sub_key}(不允许的字段)")
                    
                    # 确保新 npc 至少包含 name 字段
                    if "name" in filtered_npc and filtered_npc["name"]:
                        filtered_delta[top_key] = filtered_npc
                        logger.info(f"[校验] 允许添加新NPC: {filtered_npc.get('name', '未知')}")
                    else:
                        dropped.append(f"{top_key}(缺少name字段)")
                else:
                    dropped.append(f"{top_key}:非dict")
                continue
            
            # 常规处理：更新已存在的顶层字段
            if top_key not in current_top_keys:
                dropped.append(f"顶层:{top_key}(不存在)")
                continue
            if not isinstance(top_value, dict):
                dropped.append(f"{top_key}:非dict")
                continue

            current_sub_fields = set(current_state[top_key].keys()) if isinstance(current_state[top_key], dict) else set()
            filtered_sub = {}

            for sub_key, sub_value in top_value.items():
                if sub_key not in current_sub_fields:
                    dropped.append(f"{top_key}.{sub_key}(不存在)")
                    continue
                validated_value = cls._validate_and_clamp_value(
                    top_key, sub_key, sub_value, current_state[top_key].get(sub_key)
                )
                if validated_value is not None:
                    filtered_sub[sub_key] = validated_value
                else:
                    dropped.append(f"{top_key}.{sub_key}(类型/转换失败)")

            if filtered_sub:
                filtered_delta[top_key] = filtered_sub

        if dropped:
            logger.info(f"[校验] state_delta 丢弃: {', '.join(dropped)}")
        return filtered_delta
    
    @classmethod
    def _validate_and_clamp_value(
        cls, top_key: str, sub_key: str, new_value: Any, old_value: Any
    ) -> Optional[Any]:
        """
        校验值的类型并做 clamp
        
        功能：校验状态值的类型是否正确，并对特定字段进行数值范围限制
        特殊规则：
            - hp >= 0
            - affection 0-100
            - max_hp >= 1
            - 其他数值保持原样
        参数：
            top_key: 顶层字段名
            sub_key: 子字段名
            new_value: 新值
            old_value: 旧值（用于参考）
        返回：校验并限制后的值，如果校验失败返回 None
        """
        # 获取期望的类型（如果有定义）
        expected_type = None
        if top_key in cls.SCHEMA and sub_key in cls.SCHEMA[top_key]:
            expected_type = cls.SCHEMA[top_key][sub_key]
        
        # 类型校验
        if expected_type:
            if expected_type == int:
                if not isinstance(new_value, int):
                    try:
                        new_value = int(new_value)
                    except (ValueError, TypeError):
                        return None
            elif expected_type == float:
                if not isinstance(new_value, (int, float)):
                    try:
                        new_value = float(new_value)
                    except (ValueError, TypeError):
                        return None
            elif expected_type == str:
                if not isinstance(new_value, str):
                    new_value = str(new_value)
        
        # 数值 clamp
        if isinstance(new_value, (int, float)):
            if sub_key == "hp":
                new_value = max(0, int(new_value))
            elif sub_key == "affection":
                new_value = max(0, min(100, int(new_value)))
            elif sub_key == "max_hp" and isinstance(new_value, (int, float)):
                new_value = max(1, int(new_value))
        
        return new_value
    
    @classmethod
    def create_initial_state_template(cls) -> Dict[str, Any]:
        """
        创建一个初始状态模板（用于世界构建器参考）
        
        功能：生成一个符合 schema 的初始状态模板，供世界构建器参考
        注意：这只是模板，实际 initial_state 由世界构建器生成，但世界构建器应该遵循这个结构
        返回：包含 player 和 world 字段的初始状态字典
        """
        return {
            "player": {
                "hp": 100,
                "max_hp": 100,
                "level": 1,
                "status": "正常",
                "name": "玩家",
            },
            "world": {
                "scene": "起始场景",
                "time": "早晨",
                "location": "未知",
            },
            "guide": {
                "already_suggested": "",  # 初始为空字符串
                "pending": "",  # 初始为空字符串
            },
        }


def safe_merge_state(current_state: Dict[str, Any], state_delta: Dict[str, Any]) -> Dict[str, Any]:
    """
    安全合并状态：current_state + state_delta
    
    功能：将状态变更合并到当前状态中，使用深拷贝避免修改原对象
    支持添加新的顶层字段（如新的 npc）
    参数：
        current_state: 当前状态字典
        state_delta: 状态变更字典
    返回：合并后的新状态字典
    """
    import copy
    
    result = copy.deepcopy(current_state)
    
    for top_key, top_value in state_delta.items():
        # 如果当前状态中没有这个顶层字段，直接添加（用于添加新NPC等）
        if top_key not in result:
            result[top_key] = copy.deepcopy(top_value)
            continue
        
        # 如果都是字典，进行深度合并
        if isinstance(top_value, dict) and isinstance(result[top_key], dict):
            result[top_key].update(top_value)
        else:
            result[top_key] = top_value
    
    return result
