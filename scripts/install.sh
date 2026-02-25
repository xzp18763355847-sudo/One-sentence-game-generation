#!/usr/bin/env bash
# statem 项目依赖安装脚本（使用 uv）
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

if ! command -v uv &>/dev/null; then
    echo "未检测到 uv，请先安装: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

echo "项目根目录: $PROJECT_ROOT"
echo "创建虚拟环境并安装依赖..."
uv sync

echo "安装完成。激活环境: source $PROJECT_ROOT/.venv/bin/activate"
