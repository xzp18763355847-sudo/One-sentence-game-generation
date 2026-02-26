"""
统一日志配置：控制台 + 根目录 logs 目录下的文件。
"""
import logging
import sys
from pathlib import Path

# 项目根目录（本文件所在目录）
PROJECT_ROOT = Path(__file__).resolve().parent
LOGS_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOGS_DIR / "statem.log"

_LOG_INITIALIZED = False


def setup_logging(
    level: int = logging.INFO,
    log_file: Path | None = LOG_FILE,
) -> None:
    """配置根 logger：格式、级别，并添加控制台与文件 Handler。"""
    global _LOG_INITIALIZED
    if _LOG_INITIALIZED:
        return
    _LOG_INITIALIZED = True

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    root = logging.getLogger()
    root.setLevel(level)

    # 避免重复添加（例如多模块 import 时）
    if not root.handlers:
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(formatter)
        root.addHandler(sh)

    if log_file is not None:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fh.setFormatter(formatter)
        root.addHandler(fh)


def get_logger(name: str) -> logging.Logger:
    """获取已应用统一配置的 logger。首次调用时会执行 setup_logging。"""
    setup_logging()
    return logging.getLogger(name)
