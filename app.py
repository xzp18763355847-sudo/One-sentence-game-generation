# """
# AI 剧情游戏 - Flask API 服务（兼容旧海龟汤接口）

# 新端点：
# - GET  /api/status  - 获取当前游戏状态
# - POST /api/start   - 开始新剧情游戏（可传 rough_outline）
# - POST /api/action  - 添加玩家行动（不触发 AI 回合）
# - POST /api/submit  - 提交本轮，AI 推进剧情并更新状态
# - POST /api/end     - 结束游戏
# """

import json
import logging
import uuid
from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context
from flask_cors import CORS

from game_manager import GameManager
from game_types import GameType, is_valid_game_type
from narrative.prompt_builder import OFFCIAL_GAME_PROMPT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app, resources={r"/api/*": {"origins": "*"}})

game_manager = GameManager()

DEFAULT_GROUP_ID = "group001"


def _get_group_id(data: dict) -> str:
    """从请求数据中提取 group_id，不存在则返回默认值"""
    return (data.get("group_id") or "").strip() or DEFAULT_GROUP_ID


@app.route("/")
def serve_index():
    """
    提供前端首页
    
    功能：返回前端静态文件 index.html
    返回：index.html 文件内容
    """
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/status", methods=["GET"])
def get_status():
    """
    获取游戏状态 API
    
    功能：返回指定群的完整游戏状态信息
    查询参数：group_id（可选，默认 "default"）
    返回：包含游戏状态的 JSON 响应
    """
    group_id = (request.args.get("group_id") or "").strip() or DEFAULT_GROUP_ID
    logger.info(f"GET /api/status group_id={group_id}")
    return jsonify(game_manager.get_status(group_id))


@app.route("/api/start", methods=["POST"])
def start_game():
    """
    开始新游戏 API
    
    功能：初始化并开始一个新的游戏会话
    请求体：{"group_id": "群ID", "game_type": "游戏类型", "text": "初始文本", "language_code": "语言代码（cn/en，默认cn）"}（可选）
    返回：包含完整游戏状态的 JSON 响应（包括 messages、state、script 等）
    """
    data = request.get_json(silent=True) or {}
    print("开始游戏输入data================")
    print(data)
    print("开始游戏输入data================")
    group_id = _get_group_id(data)
    game_type = data.get("game_type", "").strip()
    text = data.get("text", "").strip()
    language_code = data.get("language_code", "cn").strip()

    # 验证游戏类型
    if game_type and not is_valid_game_type(game_type):
        return jsonify({"error": f"无效的游戏类型: {game_type}"}), 400

    logger.info(
        f"POST /api/start 开始新游戏 group_id={group_id} game_type={game_type} text_len={len(text)} language_code={language_code}")

    # 返回完整的游戏状态（包含 messages、state、script 等）
    # 这样前端可以正常显示游戏内容
    result = game_manager.start_game(group_id=group_id, game_type=game_type, text=text, language_code=language_code)
    print("开始游戏输出result（完整状态）================")
    print(result)
    print("开始游戏输出result（完整状态）================")

    return jsonify(result)
    
    # 如果只需要返回剧本格式（符合 game_generators.py 72-100 行格式），可以使用下面的代码：
    # script = result.get("script", {})
    # return jsonify(script)
    
    # 原来的调用（已注释）
    # print("开始游戏输出result================")
    # print(game_manager.start_game(game_type=game_type, text=text))
    # print("开始游戏输出result================")
    # return jsonify(game_manager.start_game(game_type=game_type, text=text))


@app.route("/api/start_offcial_game", methods=["POST"])
def start_offcial_game():
    """
    开始官方游戏 API
    
    功能：初始化并开始一个新的官方游戏会话
    请求体：{"group_id": "群ID", "text": "游戏ID", "language_code": "语言代码"}
    """
    data = request.get_json(silent=True) or {}
    group_id = _get_group_id(data)
    game_id = data.get("text", "").strip()
    if game_id not in OFFCIAL_GAME_PROMPT.keys():
        return jsonify({"error": f"无效的游戏ID: {game_id}"}), 400
    # language_code = data.get("language_code", "cn").strip()
    language_code = "en"
    logger.info(f"POST /api/start_offcial_game group_id={group_id} game_id={game_id}")
    result = game_manager.create_official_game(group_id=group_id, game_id=game_id, language_code=language_code)
    return jsonify(result)


@app.route("/api/message", methods=["POST"])
def send_message():
    """
    发送玩家消息 API
    
    功能：处理玩家发送的消息，推进游戏剧情
    请求体：{"group_id": "群ID", "text": "玩家消息", "player_name": "玩家名称"}
    返回：包含更新后游戏状态的 JSON 响应
    """
    data = request.get_json(silent=True) or {}
    print("输入data================")
    print(data)
    print("输入data================")
    group_id = _get_group_id(data)
    text = (data.get("text") or "").strip()
    player_name = (data.get("player_name") or "玩家").strip() or "玩家"
    logger.info("POST /api/message group_id=%s player=%s len=%d text_preview=%s",
                group_id, player_name, len(text),
                (text[:30] + "..." if len(text) > 30 else text))
    result = game_manager.send_message(group_id=group_id, text=text, player_name=player_name)
    code = 200 if "error" not in result else 400
    if "error" in result:
        logger.warning("POST /api/message group_id=%s error=%s", group_id, result.get("error"))
    print("输出result================")
    print(result)
    print("输出result================")
    return jsonify(result), code


@app.route("/api/message_sse", methods=["POST"])
def send_message_sse():
    """
    发送玩家消息 API（SSE 分段返回）

    请求体：与 /api/message 相同 {"group_id", "text", "player_name"}
    返回：text/event-stream，按顺序推送（每条以 { 开头的 JSON，无 event/data 前缀；统一顶层格式）：
      - {"type":"reply","payload":{"content":{...}},"message_id":"..."}  （第 1 条：transition）
      - 同上，content 含 narration、sound
      - 同上，content 含 dialogues、hooks，可选 aigc_generate
      - 同上，content 为完整游戏状态
    错误时返回 400 + JSON {"error": "..."}，不走 SSE。
    """
    data = request.get_json(silent=True) or {}
    group_id = _get_group_id(data)
    text = (data.get("text") or "").strip()
    player_name = (data.get("player_name") or "玩家").strip() or "玩家"

    result = game_manager.send_message(group_id=group_id, text=text, player_name=player_name)
    if "error" in result:
        logger.warning("POST /api/message_sse group_id=%s error=%s", group_id, result.get("error"))
        return jsonify(result), 400

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
    message_id = str(uuid.uuid4())

    def _wrap_reply(content: dict) -> dict:
        return {"type": "reply", "payload": {"content": content}, "message_id": message_id}

    def generate():
        # 1) transition
        yield json.dumps(_wrap_reply({"transition": transition}), ensure_ascii=False) + "\n\n"
        # 2) narration + sound
        yield json.dumps(_wrap_reply({"narration": narration, "sound": sound}), ensure_ascii=False) + "\n\n"
        # 3) dialogues + hooks（若 result 含 aigc_generate 则一并返回）
        dialogues_payload: dict = {"dialogues": dialogues, "hooks": hooks}
        if aigc_generate is not None:
            dialogues_payload["aigc_generate"] = aigc_generate
        yield json.dumps(_wrap_reply(dialogues_payload), ensure_ascii=False) + "\n\n"
        # 4) 完整状态，便于前端更新 UI
        yield json.dumps(_wrap_reply(result), ensure_ascii=False) + "\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@app.route("/api/narrative/state", methods=["GET"])
def get_narrative_state():
    """
    获取叙事状态 API（调试接口）
    
    功能：返回指定群当前四条主线叙事状态，用于调试和监控
    查询参数：group_id（可选）
    返回：包含叙事状态的 JSON 响应
    """
    group_id = (request.args.get("group_id") or "").strip() or DEFAULT_GROUP_ID
    logger.info(f"GET /api/narrative/state group_id={group_id}")
    return jsonify(game_manager.get_narrative_state(group_id))


@app.route("/api/narrative/log", methods=["GET"])
def get_narrative_log():
    """
    获取叙事日志 API（调试接口）
    
    功能：返回指定群状态变更日志和事件日志，用于调试和监控
    查询参数：group_id（可选）
    返回：包含日志信息的 JSON 响应
    """
    group_id = (request.args.get("group_id") or "").strip() or DEFAULT_GROUP_ID
    logger.info(f"GET /api/narrative/log group_id={group_id}")
    return jsonify(game_manager.get_narrative_log(group_id))


@app.route("/api/end", methods=["POST"])
def end_game():
    """
    结束游戏 API
    
    功能：手动结束指定群的游戏会话
    请求体：{"group_id": "群ID"}
    返回：包含结束状态信息的 JSON 响应
    """
    data = request.get_json(silent=True) or {}
    group_id = _get_group_id(data)
    logger.info(f"POST /api/end 手动结束游戏 group_id={group_id}")
    return jsonify(game_manager.end_game(group_id))


if __name__ == "__main__":
    logger.info("server: http://0.0.0.0:4000")
    app.run(debug=False, use_reloader=False, host="0.0.0.0", port=4000)
