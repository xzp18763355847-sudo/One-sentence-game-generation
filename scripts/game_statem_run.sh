#!/usr/bin/env bash
# statem 项目启动脚本（uv run python app.py）
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

if ! command -v uv &>/dev/null; then
    echo "未检测到 uv，请先安装: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

# 环境变量（key 留空，请在本脚本中填写或通过 .env 覆盖）
export OPENAI_BASE_URL="${OPENAI_BASE_URL:-https://app.onerouter.pro/v1}"
export OPENAI_API_KEY="${OPENAI_API_KEY:-}"
export STORY_WORLD_MODEL="${STORY_WORLD_MODEL:-gpt-4.1}"
export OPENAI_MODEL="${OPENAI_MODEL:-google-ai-studio/gemini-2.5-flash}"

echo "项目根目录: $PROJECT_ROOT"
echo "启动服务: uv run python app.py"
uv run python app.py
