"""AI 剧情游戏 - FastAPI 应用入口（与根目录 app.py 行为一致）."""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from game_manager import GameManager
from utils.log_config import get_logger

from config import HOST, PORT
from src.api.endpoints.game_manage.router import router as game_router

logger = get_logger(__name__)

app = FastAPI(title="STATEM AI Game", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注入 GameManager，供 router 依赖使用
app.state.game_manager = GameManager()

# 先注册 API 路由，保证 /api/* 优先匹配
app.include_router(game_router, prefix="/api")

# 静态首页（路径相对于项目根，需从项目根运行）
_frontend_dir = Path(__file__).resolve().parent.parent.parent / "frontend"


@app.get("/")
async def serve_index() -> FileResponse:
    """提供前端首页 index.html."""
    return FileResponse(_frontend_dir / "index.html")


if _frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(_frontend_dir)), name="static")


@app.on_event("startup")
async def startup_event() -> None:
    """应用启动时初始化 Redis 连接（与根目录 app.py 一致）."""
    try:
        from utils.redis_cache import dao as redis_dao
        await redis_dao.init_pools()
        logger.info("Redis connection initialized on startup")
    except ImportError:
        logger.warning("utils.redis_cache not found, skip Redis init")
    except Exception as e:
        logger.error("Failed to initialize Redis on startup: {}", e)
        raise


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """全局异常处理器（与根目录 app.py 一致）."""
    logger.error("全局异常: {}", exc, exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


if __name__ == "__main__":
    import uvicorn

    logger.info("server: http://0.0.0.0:4000")
    uvicorn.run("src.api.app:app", host=HOST, port=PORT, log_level="info")
