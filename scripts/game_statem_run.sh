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

echo "项目根目录: $PROJECT_ROOT"
echo "启动服务: uv run python app.py"
uv run python app.py
# uv run python src/api/app.py
