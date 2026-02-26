# game_statem 接口文档

本文档描述以下 API 的请求与响应格式。

---

## 1. 开始官方游戏

**接口**：`POST /api/start_offcial_game`

**说明**：按群 ID 初始化并开始一个官方游戏会话（使用预置游戏设定与提示词）。

### 请求

- **Content-Type**：`application/json`
- **Body**：


| 字段            | 类型     | 必填  | 说明                                    |
| ------------- | ------ | --- | ------------------------------------- |
| group_id      | string | 否   | 群 ID，不传时使用默认 `group001`               |
| text          | string | 是   | 游戏 ID，需为已配置的官方游戏（如 `og001`），无效时返回 400 |
| language_code | string | 否   | 语言代码，默认 `cn （暂不支持多语种）`                |


示例：

```json
{
  "group_id": "group_01",
  "text": "og001",
  "language_code": "cn"
}
```

CURL请求：

```text
curl -X POST "http://localhost:4000/api/start_offcial_game"   
-H "Content-Type: application/json"   
-d "{\"group_id\": \"group_01\", \"text\": \"og001\", \"language_code\": \"cn\"}"
```

### 响应

- **成功**：`200 OK`，Body 为 JSON，内容为 `game_manager.create_official_game` 的返回值（包含游戏初始化/状态信息）。
- **失败**：`400 Bad Request`，Body 为 JSON，例如：

```json
{
  "error": "无效的游戏ID: xxx"
}
```

---

## 2. 发送玩家消息（SSE 流式）

**接口**：`POST /api/message_sse`

**说明**：发送玩家消息并推进剧情，以流式方式返回多段 JSON（无 `event`/`data` 前缀，每条为完整 JSON 对象，以 `\n\n` 分隔）。

### 请求

- **Content-Type**：`application/json`
- **Body**：与 `/api/message` 相同


| 字段          | 类型     | 必填  | 说明                      |
| ----------- | ------ | --- | ----------------------- |
| group_id    | string | 否   | 群 ID，不传时使用默认 `group001` |
| text        | string | 是   | 玩家发送的文本内容               |
| player_name | string | 否   | 玩家名称，默认 `"玩家"`          |


示例：

```json
{
  "group_id": "group_01",
  "text": "你好",
  "player_name": "玩家"
}
```

CURL请求：

```text
curl -X POST "http://localhost:4000/api/message_sse"   
-H "Content-Type: application/json"   
-d '{"group_id": "group_01", "text": "我接受上传", "player_name": "user_1"} 
```

### 响应

- **Content-Type**：`text/event-stream`
- **成功**：按顺序推送 **4 条** JSON 字符串，每条以 `{` 开头，两条之间用 `\n\n` 分隔。每条为统一顶层结构：

```json
{
  "type": "reply",
  "payload": {
    "content": { ... }
  },
  "message_id": "<uuid>"
}
```

同一次请求的 4 条使用同一个 `message_id`。`payload.content` 含义依次为：


| 顺序    | content 含义                                                                                   |
| ----- | -------------------------------------------------------------------------------------------- |
| 第 1 条 | `{"transition": "章节标识或空字符串"}`                                                                |
| 第 2 条 | `{"narration": "旁白文本", "sound": "音效"}`                                                       |
| 第 3 条 | `{"dialogues": [...], "hooks": {"player_goal": "..."}}`，若后端有 `aigc_generate` 会一并放在 content 中 |
| 第 4 条 | 完整游戏状态（与 GET /api/status 结构一致），便于前端整体更新 UI                                                   |


前端解析方式：按 `\n\n` 拆分为多条，每条 `JSON.parse` 后从 `payload.content` 取业务数据，可根据 content 中出现的字段区分是 transition / narration / dialogues / 完整状态。

- **失败**：`400 Bad Request`，不走 SSE，Body 为普通 JSON，例如：

```json
{
  "error": "错误描述"
}
```

---

## 默认值说明

- **group_id**：两接口在未传或传空时均使用默认 `group001`（见 `app.py` 中 `DEFAULT_GROUP_ID`）。
- 官方游戏 ID 的合法取值由项目内 `OFFCIAL_GAME_PROMPT` 配置决定（如 `og001` 等）。

