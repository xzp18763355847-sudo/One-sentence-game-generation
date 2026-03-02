"""API 层公共配置常量，优先从环境变量读取；.env 位于项目根目录."""

import os
from pathlib import Path

from dotenv import load_dotenv

# 项目根目录下的 .env（src/api/config.py -> 向上两级 -> 项目根）
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(_PROJECT_ROOT / ".env")


DEFAULT_GROUP_ID = "group001"

# 服务监听：优先从环境变量读取，默认与 uvicorn 原有一致
HOST = os.getenv("API_HOST", "0.0.0.0")
PORT = int(os.getenv("API_PORT", "4000"))

# Redis 相关（预留，后续接入时使用）
REDIS_URL = os.getenv("REDIS_URL", "")  # 例如 redis://localhost:6379/0
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
