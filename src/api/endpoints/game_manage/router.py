"""游戏管理 API 路由：状态、开始/结束游戏、消息与 SSE."""

import asyncio
import json
import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import StreamingResponse

from src.api.endpoints.game_manage.schemas import (
    EndGameRequest,
    MessageRequest,
    StartGameRequest,
    StartOfficialGameRequest,
)

# 项目根模块（需从项目根目录运行 uvicorn）
from config import DEFAULT_GROUP_ID
from game_types import is_valid_game_type
from log_config import get_logger
from narrative.prompt_builder import OFFCIAL_GAME_PROMPT

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["game"])


def get_game_manager(request: Request) -> Any:
    """从 app.state 获取 GameManager 实例."""
    return request.app.state.game_manager


@router.get("/status")
async def get_status(
    group_id: str = Query(default=DEFAULT_GROUP_ID),
    gm: Any = Depends(get_game_manager),
) -> Any:
    """获取指定群的游戏状态."""
    gid = (group_id or "").strip() or DEFAULT_GROUP_ID
    logger.info("GET /api/status group_id=%s", gid)
    return await asyncio.to_thread(gm.get_status, gid)


@router.post("/start")
async def start_game(
    req: StartGameRequest,
    gm: Any = Depends(get_game_manager),
) -> Any:
    """开始新游戏."""
    gid = (req.group_id or "").strip() or DEFAULT_GROUP_ID
    if req.game_type and not is_valid_game_type(req.game_type):
        raise HTTPException(status_code=400, detail=f"无效的游戏类型: {req.game_type}")
    logger.info(
        "POST /api/start group_id=%s game_type=%s text_len=%d language_code=%s",
        gid,
        req.game_type,
        len(req.text or ""),
        req.language_code,
    )
    return await asyncio.to_thread(
        gm.start_game,
        group_id=gid,
        game_type=req.game_type or "",
        text=req.text or "",
        language_code=req.language_code or "cn",
    )


@router.post("/start_offcial_game")
async def start_official_game(
    req: StartOfficialGameRequest,
    gm: Any = Depends(get_game_manager),
) -> Any:
    """开始官方游戏."""
    gid = (req.group_id or "").strip() or DEFAULT_GROUP_ID
    if req.game_id not in OFFCIAL_GAME_PROMPT:
        raise HTTPException(status_code=400, detail=f"无效的游戏ID: {req.game_id}")
    logger.info("POST /api/start_offcial_game group_id=%s game_id=%s", gid, req.game_id)
    return await asyncio.to_thread(
        gm.create_official_game,
        group_id=gid,
        game_id=req.game_id,
        language_code=req.language_code or "en",
    )


@router.post("/message")
async def send_message(
    req: MessageRequest,
    gm: Any = Depends(get_game_manager),
) -> Any:
    """发送玩家消息（同步返回完整状态）."""
    gid = (req.group_id or "").strip() or DEFAULT_GROUP_ID
    text = (req.text or "").strip()
    player_name = (req.player_name or "").strip() or "玩家"
    language_code = (req.language_code or "en").strip()
    logger.info(
        "POST /api/message group_id=%s player=%s len=%d language_code=%s",
        gid,
        player_name,
        len(text),
        language_code,
    )
    result = await asyncio.to_thread(
        gm.send_message,
        group_id=gid,
        text=text,
        player_name=player_name,
        language_code=language_code,
    )
    if "error" in result:
        logger.warning("POST /api/message group_id=%s error=%s", gid, result.get("error"))
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/message_sse")
async def send_message_sse(
    req: MessageRequest,
    gm: Any = Depends(get_game_manager),
) -> StreamingResponse:
    """发送玩家消息，SSE 流式返回 3 条 event: reply."""
    gid = (req.group_id or "").strip() or DEFAULT_GROUP_ID
    text = (req.text or "").strip()
    player_name = (req.player_name or "").strip() or "玩家"
    language_code = (req.language_code or "en").strip()

    result = await asyncio.to_thread(
        gm.send_message,
        group_id=gid,
        text=text,
        player_name=player_name,
        language_code=language_code,
    )
    if "error" in result:
        logger.warning(
            "POST /api/message_sse group_id=%s error=%s", gid, result.get("error")
        )
        raise HTTPException(status_code=400, detail=result["error"])

    transition = result.get("transition", "") or ""
    narration = result.get("narration", "") or ""
    sound = result.get("sound", "") or ""
    dialogues = result.get("dialogues", [])
    if not isinstance(dialogues, list):
        dialogues = []
    hooks = result.get("hooks", {}) or {}
    if not isinstance(hooks, dict):
        hooks = {}
    if "player_goal" not in hooks:
        hooks["player_goal"] = ""
    aigc_generate = result.get("aigc_generate") if "aigc_generate" in result else None
    message_id = str(uuid.uuid4())  # 是否需要返回

    def _wrap_reply(content: dict) -> dict:
        return {
            "type": "reply",
            "payload": {"can_feedback": False, "can_rating": True, "content": content},
            "message_id": message_id,
        }

    def _sse_line(obj: dict) -> str:
        return f"event: reply\ndata: {json.dumps(obj, ensure_ascii=False)}\n\n"

    async def generate() -> Any:
        yield _sse_line(_wrap_reply({"transition": transition}))
        yield _sse_line(_wrap_reply({"narration": narration, "sound": sound}))
        dialogues_payload: dict = {"dialogues": dialogues, "hooks": hooks}
        if aigc_generate is not None:
            dialogues_payload["aigc_generate"] = aigc_generate  # 多模态事件
        yield _sse_line(_wrap_reply(dialogues_payload))

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@router.get("/narrative/state")
async def get_narrative_state(
    group_id: str = Query(default=DEFAULT_GROUP_ID),
    gm: Any = Depends(get_game_manager),
) -> Any:
    """获取叙事状态（调试）."""
    gid = (group_id or "").strip() or DEFAULT_GROUP_ID
    logger.info("GET /api/narrative/state group_id=%s", gid)
    return await asyncio.to_thread(gm.get_narrative_state, gid)


@router.get("/narrative/log")
async def get_narrative_log(
    group_id: str = Query(default=DEFAULT_GROUP_ID),
    gm: Any = Depends(get_game_manager),
) -> Any:
    """获取叙事日志（调试）."""
    gid = (group_id or "").strip() or DEFAULT_GROUP_ID
    logger.info("GET /api/narrative/log group_id=%s", gid)
    return await asyncio.to_thread(gm.get_narrative_log, gid)


@router.post("/end")
async def end_game(
    req: EndGameRequest,
    gm: Any = Depends(get_game_manager),
) -> Any:
    """结束游戏."""
    gid = (req.group_id or "").strip() or DEFAULT_GROUP_ID
    logger.info("POST /api/end group_id=%s", gid)
    return await asyncio.to_thread(gm.end_game, gid)
