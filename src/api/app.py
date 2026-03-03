"""AI 剧情游戏 - FastAPI 应用入口."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from config import HOST, PORT
from game_manager import GameManager

from src.api.endpoints.game_manage.router import router as game_router

app = FastAPI(title="AI 剧情游戏 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注入 GameManager，供 router 依赖使用
app.state.game_manager = GameManager()

# 先注册 API 路由，保证 /api/* 优先匹配（prefix 在 include 时统一指定）
app.include_router(game_router, prefix="/api")

# 静态首页（路径相对于项目根，需从项目根运行）
_frontend_dir = Path(__file__).resolve().parent.parent.parent / "frontend"


@app.get("/")
async def serve_index() -> FileResponse:
    """提供前端首页 index.html."""
    return FileResponse(_frontend_dir / "index.html")


# 静态资源（可选，避免覆盖 /）
if _frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(_frontend_dir)), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.app:app",
        host=HOST,
        port=PORT,
        reload=False,
    )
