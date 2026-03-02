"""游戏管理 API 请求体模型."""

from pydantic import BaseModel


class StartGameRequest(BaseModel):
    """开始新游戏请求."""

    group_id: str = "group001"
    game_type: str = ""
    text: str = ""
    language_code: str = "cn"


class StartOfficialGameRequest(BaseModel):
    """开始官方游戏请求."""

    group_id: str = "group001"
    game_id: str
    language_code: str = "en"


class MessageRequest(BaseModel):
    """发送玩家消息请求."""

    group_id: str = "group001"
    text: str
    player_name: str = "玩家"
    language_code: str = "en"


class EndGameRequest(BaseModel):
    """结束游戏请求."""

    group_id: str = "group001"
