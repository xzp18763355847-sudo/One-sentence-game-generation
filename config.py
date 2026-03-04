"""
Configuration for the Turtle Soup game backend.
Set these environment variables before running:
- OPENAI_API_KEY: Your OpenAI API key
- OPENAI_BASE_URL: (Optional) Custom API base URL, defaults to https://api.openai.com/v1
- OPENAI_MODEL: (Optional) Model to use, defaults to gpt-3.5-turbo
"""
import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://app.onerouter.pro/v1")
# 用于一次性世界构建（大模型）
STORY_WORLD_MODEL = os.getenv("STORY_WORLD_MODEL")
# 用于每回合更新（小模型）
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

# Game settings
MAX_ROUNDS = 200
HINT_ROUND_THRESHOLD = 10  # Start giving hints after this many rounds

# 可选：是否把完整 assets/state 暴露给前端（调试用）
DEBUG_EXPOSE_FULL_STATE = True


DEFAULT_GROUP_ID = "group001"

# 服务监听：优先从环境变量读取，默认与 uvicorn 原有一致
HOST = os.getenv("API_HOST", "0.0.0.0")
PORT = int(os.getenv("API_PORT", "4000"))

# Redis 相关（预留，后续接入时使用）
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
