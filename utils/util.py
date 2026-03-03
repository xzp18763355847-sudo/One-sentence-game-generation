import json
import os
import tempfile
from typing import Any, Tuple, Optional

from game_statics.intern_map import SYSTEM_MESSAGES


def get_system_message(key: str, language_code: str = "cn", **kwargs) -> str:
    """
    根据 language_code 获取系统消息

    参数:
        key: 消息键名
        language_code: 语言代码（cn/en，默认cn）
        **kwargs: 用于格式化消息的参数

    返回:
        格式化后的消息字符串
    """
    lang = language_code.lower() if language_code else "cn"
    if lang not in ("cn", "en"):
        lang = "cn"

    message_template = SYSTEM_MESSAGES.get(lang, SYSTEM_MESSAGES["cn"]).get(key, "")
    if not message_template:
        # 如果找不到消息，尝试从中文获取
        message_template = SYSTEM_MESSAGES["cn"].get(key, key)

    return message_template.format(**kwargs) if kwargs else message_template


# =========================
# helpers
# =========================
def deep_merge(dst: dict, src: dict) -> dict:
    """
    递归合并：dict->dict 深合并，其它类型直接覆盖

    功能：将源字典深度合并到目标字典中，字典类型递归合并，其他类型直接覆盖
    参数：
        dst: 目标字典
        src: 源字典
    返回：合并后的字典
    """
    for k, v in src.items():
        if isinstance(v, dict) and isinstance(dst.get(k), dict):
            deep_merge(dst[k], v)
        else:
            dst[k] = v
    return dst


def strip_secrets(obj: Any) -> Any:
    """
    递归剔除任何层级的 secrets 字段

    功能：从对象中递归移除所有名为 "secrets" 的字段，避免敏感信息泄露
    参数：
        obj: 要处理的对象（可以是字典、列表或其他类型）
    返回：处理后的对象，所有 secrets 字段已被移除
    """
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k == "secrets":
                continue
            out[k] = strip_secrets(v)
        return out
    if isinstance(obj, list):
        return [strip_secrets(x) for x in obj]
    return obj


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
                candidate = raw[start: i + 1]
                try:
                    obj = json.loads(candidate)
                    if isinstance(obj, dict):
                        return obj, ""
                except Exception:
                    return None, "json_parse_failed"
                break

    return None, "unterminated_json"


def atomic_write_json(path: str, data: dict) -> None:
    """
    原子写入 JSON，避免写一半

    功能：使用临时文件+替换的方式原子性地写入 JSON，确保不会出现文件损坏
    参数：
        path: 目标文件路径
        data: 要写入的字典数据
    """
    tmp_dir = os.path.dirname(path) or "."
    os.makedirs(tmp_dir, exist_ok=True)

    fd, tmp_path = tempfile.mkstemp(prefix="story_game_", suffix=".tmp", dir=tmp_dir)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
        raise
