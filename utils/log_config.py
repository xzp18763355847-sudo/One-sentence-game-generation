"""
统一日志配置（loguru）：控制台 + 项目根 logs 目录文件，适用于高并发异步场景。
loguru 内部使用队列与独立 sink，不阻塞事件循环。
"""

import sys
from pathlib import Path
from typing import Any

from loguru import logger

# 项目根目录（本文件所在目录）
PROJECT_ROOT = Path(__file__).resolve().parent
LOGS_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOGS_DIR / "statem.log"

_LOG_INITIALIZED = False

# 统一格式：时间 | 级别 | 模块名 | 消息
_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{extra[module]}</cyan> | "
    "<level>{message}</level>"
)


def setup_logging(
    level: str = "INFO",
    log_file: Path | None = LOG_FILE,
) -> None:
    """配置 loguru：移除默认 handler，添加控制台与文件 sink。"""
    global _LOG_INITIALIZED
    if _LOG_INITIALIZED:
        return
    _LOG_INITIALIZED = True

    logger.remove()  # 去掉默认 stderr sink

    logger.add(
        sys.stdout,
        format=_FORMAT,
        level=level,
        colorize=True,
    )

    if log_file is not None:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            log_path,
            format=_FORMAT,
            level=level,
            encoding="utf-8",
            rotation="10 MB",
            retention="15 days",
        )

    # 默认 extra，避免直接使用 logger 时缺少 module
    logger.configure(extra={"module": "root"})


def get_logger(name: str) -> Any:
    """获取带模块名的 logger，兼容现有 get_logger(__name__) 用法；首次调用时执行 setup_logging。"""
    setup_logging()
    return logger.bind(module=name)
