"""游戏管理 API 请求体模型."""

from pydantic import BaseModel
from typing import Optional


class StartGameRequest(BaseModel):
    """开始新游戏请求."""

    group_id: Optional[str] = None
    game_type: str = ""
    text: str = ""
    language_code: str = "cn"


class StartOfficialGameRequest(BaseModel):
    """开始官方游戏请求."""

    group_id: Optional[str] = None
    game_id: str
    language_code: str = "en"


class MessageRequest(BaseModel):
    """发送玩家消息请求."""

    group_id: Optional[str] = None
    text: str
    player_name: str = "玩家"
    language_code: str = "en"

class SendMessageSseRequest(BaseModel):
    group_id: Optional[str] = None
    text: str
    player_name: str = "玩家"
    custom_variables: Optional[dict] = {}  # 扩展字段 


class EndGameRequest(BaseModel):
    """结束游戏请求."""

    group_id: Optional[str] = None
