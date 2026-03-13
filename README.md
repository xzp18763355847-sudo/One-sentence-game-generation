# 🎮 AI 剧情游戏系统

一个基于 AI 的剧情游戏系统，支持多种游戏类型（角色攻略、章节剧情等），使用 OpenAI API 生成动态剧情并管理游戏状态。

## 📋 目录

- [游戏介绍](#游戏介绍)
- [功能特点](#功能特点)
- [游戏流程](#游戏流程)
- [Story State 状态机详解](#story-state-状态机详解)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [API 接口](#api-接口)
- [技术架构](#技术架构)

## 🎯 游戏介绍

这是一个 AI 驱动的剧情游戏系统，支持以下游戏类型：

- **角色攻略类（companion_route）**：有结局的攻略类游戏，通过互动提升好感度
- **开放式陪伴类（companion_open）**：无结局的开放式陪伴类游戏
- **章节剧情类（story_chapter）**：有结局的章节剧情类游戏
- **开放式剧情（story_open）**：无结局的开放式剧情游戏

游戏使用 AI 模型动态生成剧情，并通过 `story_state` 状态机管理游戏世界的状态变化。

## ✨ 功能特点

- 🎲 **AI 自动生成剧情**：根据玩家输入动态生成剧情内容
- 📖 **章节系统**：支持多章节剧情，每章有明确的目标
- 💾 **状态持久化**：游戏状态自动保存，刷新/重启不丢失
- 🔒 **多进程安全**：使用文件锁机制，支持多 worker 部署
- 🎭 **叙事状态机**：双层状态管理（流程状态 + 世界状态）
- 🔐 **安全机制**：自动过滤敏感信息（secrets），防止泄露

## 🎮 游戏流程

### 1. 游戏初始化阶段

```
用户点击"开始游戏"
    ↓
POST /api/start (可选 game_type, text)
    ↓
GameManager.start_game()
    ↓
progress = AWAITING_INITIAL_INPUT
```

### 2. 大纲生成阶段

```
用户输入初始描述（可选）
    ↓
POST /api/message (text="我想玩一个...")
    ↓
如果 progress == AWAITING_INITIAL_INPUT:
    - 生成大纲（outline）
    - progress = AWAITING_OUTLINE_REVIEW
    - 等待用户确认/修改大纲
```

### 3. 世界构建阶段

```
用户确认大纲
    ↓
POST /api/message (text="确认" 或修改后的大纲)
    ↓
如果 progress == AWAITING_OUTLINE_REVIEW:
    - 生成剧本（script）
    - 构建世界（build_world）：
      * 生成 assets（世界资产、规则、设定）
      * 生成 initial_state（初始 story_state）
      * 生成 chapters（章节列表）
    - progress = IN_PROGRESS
    - story_state = initial_state（首次设置）
```

### 4. 游戏进行阶段（核心循环）

```
每回合流程：
    ↓
POST /api/message (text="玩家行动")
    ↓
1. 更新叙事状态机（narrative_state）
   - 检查规则引擎
   - 触发事件（如果有）
    ↓
2. 构建回合输入（turn_input）
   {
     "assets": 世界资产（去除 secrets）,
     "current_state": story_state（上回合的状态）,
     "recent_log": 最近12条对话,
     "player_message": 玩家输入,
     "current_chapter": 当前章节信息,
     "game_type": 游戏类型
   }
    ↓
3. 调用 AI 模型（回合引擎）
   - 输入：system_prompt + turn_input (JSON)
   - 输出：{
       "narration": 场景描述,
       "sound": 声音效果,
       "dialogues": NPC对话,
       "hooks": 行动建议,
       "state_delta": 状态变化,
       "flags": 标志位
     }
    ↓
4. 应用状态变化
   - 验证 state_delta（结构校验）
   - 合并到 story_state: story_state = merge(story_state, state_delta)
   - 更新章节进度（如果 flags.chapter_goal_completed）
   - 检查游戏结束（如果 flags.game_ended）
    ↓
5. 持久化状态
   - 保存到 snapshot JSON
   - 返回更新后的游戏状态
```

### 5. 游戏结束

```
触发条件：
- flags.game_ended == true
- 好感度达到 100（角色攻略类）
- 所有章节完成（章节剧情类）
    ↓
progress = ENDED
ended_reason = flags.reason
    ↓
显示结局信息
```

## 🎯 Story State 状态机详解

### 什么是 Story State？

`story_state` 是游戏世界的**结构化状态表示**，它定义了游戏世界中所有可追踪的状态信息（如玩家血量、NPC好感度、世界场景等）。

### Story State 的核心特点

#### 1. **结构固定，数值可变**

- **结构固定**：顶层字段（如 `player`、`npc`、`world`）和子字段（如 `player.hp`、`npc.affection`）在 `initial_state` 生成后**不能新增、删除或重命名**
- **数值可变**：只能修改已存在字段的数值（如 `hp: 100 → 80`、`affection: 50 → 60`）

#### 2. **状态演化机制**

每回合的状态变化遵循以下公式：

```
S_{t+1} = merge(S_t, Δ_t)
```

其中：
- `S_t`：当前回合的 `story_state`
- `Δ_t`：模型输出的 `state_delta`（只包含变化的部分）
- `S_{t+1}`：下一回合的 `story_state`（合并后的结果）

#### 3. **状态 Schema 定义**

系统使用 `StateSchema` 定义允许的状态结构：

```python
SCHEMA = {
    "player": {
        "hp": int,
        "max_hp": int,
        "level": int,
        "status": str,
        "name": str,
    },
    "npc": {  # 可选
        "name": str,
        "affection": int,  # 好感度 0-100
        "relationship": str,
    },
    "world": {
        "scene": str,
        "time": str,
        "location": str,
    },
    "chapter": {  # 可选，章节类游戏
        "current_chapter": int,
        "chapter_progress": str,
        "chapter_goal_completed": bool,
    },
}
```

### Story State 的生命周期

#### 阶段 1：初始化（世界构建时）

```python
# 在世界构建阶段，模型生成 initial_state
initial_state = {
    "player": {
        "hp": 100,
        "max_hp": 100,
        "level": 1,
        "status": "健康",
        "name": "玩家"
    },
    "world": {
        "scene": "森林入口",
        "time": "清晨",
        "location": "神秘森林"
    }
}

# 首次设置 story_state
gs.story_state = initial_state
```

#### 阶段 2：状态演化（每回合）

```python
# 回合开始：模型接收 current_state（即上回合的 story_state）
turn_input = {
    "current_state": {
        "player": {"hp": 100, "max_hp": 100, ...},
        "world": {"scene": "森林入口", ...}
    },
    "player_message": "我向前走",
    ...
}

# 模型输出 state_delta（只包含变化）
state_delta = {
    "world": {
        "scene": "森林深处"  # 只写变化的部分
    }
}

# 服务端合并状态
validated_delta = StateSchema.validate_state_delta(state_delta, current_state)
gs.story_state = safe_merge_state(gs.story_state, validated_delta)

# 结果：story_state 更新为
{
    "player": {"hp": 100, "max_hp": 100, ...},  # 保持不变
    "world": {
        "scene": "森林深处",  # 已更新
        "time": "清晨",       # 保持不变
        "location": "神秘森林"  # 保持不变
    }
}
```

#### 阶段 3：状态验证

每次合并前，系统会验证 `state_delta`：

1. **结构校验**：只允许更新已存在的字段
2. **类型校验**：确保类型匹配（int/float/str/dict）
3. **数值约束**：自动 clamp（如 `hp >= 0`、`affection 0-100`）
4. **特殊规则**：允许在特定条件下添加新的 `npc` 字段

### Story State 如何影响游戏进程？

#### 1. **影响下一回合的叙事**

`story_state` 作为 `current_state` 传给模型，模型根据当前状态生成叙事：

- 如果 `player.hp` 很低 → 叙事可能强调危险
- 如果 `npc.affection` 很高 → NPC 对话更友好
- 如果 `world.scene` 改变 → 描述新场景

#### 2. **驱动章节系统**

```python
# 模型通过 flags.chapter_goal_completed 标记章节完成
flags = {"chapter_goal_completed": true}

# 服务端检测到章节完成，推进章节
if chapter_goal_completed:
    gs.current_chapter += 1
    # 同步更新 story_state.chapter
    gs.story_state["chapter"]["current_chapter"] = gs.current_chapter
```

#### 3. **触发游戏结束**

```python
# 角色攻略类：好感度满值
if npc.affection >= 100:
    flags["game_ended"] = True
    flags["reason"] = "affection_max"

# 模型也可以直接设置
flags = {"game_ended": True, "reason": "玩家死亡"}
```

### Story State 与上下文的关系

每回合传给模型的完整上下文包括：

```json
{
  "assets": {
    "world_rules": "...",
    "characters": {...},
    "secrets": "..."  // 会被 strip_secrets 移除
  },
  "current_state": {
    // 这就是 story_state，模型看到的世界状态
    "player": {...},
    "npc": {...},
    "world": {...}
  },
  "recent_log": [
    // 最近12条对话历史
    {"role": "user", "content": "玩家: 我向前走"},
    {"role": "assistant", "content": "主持人: 你进入了森林深处..."}
  ],
  "player_message": "我检查周围",
  "current_chapter": {
    "title": "第一章",
    "goal": "找到神秘物品",
    "description": "..."
  },
  "game_type": "story_chapter"
}
```

**关键点**：`story_state` 和对话历史、assets、章节信息一起传给模型，模型据此生成下一回合的内容和状态变化。

### Story State 的持久化

游戏状态会自动保存到 `story_game_snapshot.json`：

```python
snapshot = {
    "global_state": {
        "progress": "in_progress",
        "round_count": 5,
        "story_state": {
            "player": {...},
            "world": {...}
        },
        ...
    },
    "messages": [...],
    "narrative_state": {...},
    ...
}
```

每次请求都会：
1. 加载最新快照（覆盖内存）
2. 执行业务逻辑
3. 保存新快照

这确保了多进程环境下的数据一致性。

## 📁 项目结构

```
game_demo/
├── backend/                    # Flask 后端
│   ├── app.py                  # Flask API 入口
│   ├── game_manager.py         # 游戏逻辑管理（核心）
│   ├── game_types.py           # 游戏类型定义
│   ├── game_generators.py      # 世界构建器、大纲生成器
│   ├── state_schema.py         # Story State Schema 定义
│   ├── config.py               # 配置文件
│   ├── narrative/              # 叙事状态机模块
│   │   ├── state_models.py     # 叙事状态模型
│   │   ├── engine.py           # 叙事引擎
│   │   ├── prompt_builder.py   # 导演提示构建器
│   │   ├── rules.py            # 规则引擎
│   │   └── events.py            # 事件系统
│   └── requirements.txt        # Python 依赖
├── frontend/                   # 前端界面
│   ├── index.html              # 主页面
│   ├── style.css               # 样式表
│   └── script.js               # 前端逻辑
└── README.md                   # 项目说明
```

## 🚀 快速开始

### 1. 环境准备

确保已安装 Python 3.8+ 和 pip。

### 2. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置 OpenAI API

设置环境变量（Linux/Mac）：

```bash
export OPENAI_API_KEY=your_api_key_here
export OPENAI_BASE_URL=https://api.openai.com/v1
export OPENAI_MODEL=gpt-4o-mini
```

Windows CMD：

```cmd
set OPENAI_API_KEY=your_api_key_here
set OPENAI_BASE_URL=https://api.openai.com/v1
set OPENAI_MODEL=gpt-4o-mini
```

Windows PowerShell：

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
$env:OPENAI_BASE_URL="https://api.openai.com/v1"
$env:OPENAI_MODEL="gpt-4o-mini"
```

> 💡 提示：如果使用其他兼容 OpenAI 的 API（如 Azure OpenAI、国内代理等），修改 `OPENAI_BASE_URL` 为对应地址即可。

### 4. 启动后端服务

```bash
cd backend
python app.py
```

后端将在 `http://localhost:4000` 运行。

### 5. 启动前端

直接用浏览器打开 `frontend/index.html`，或者使用任何静态文件服务器：

```bash
cd frontend
python -m http.server 8080
```

然后访问 `http://localhost:8080`

## 📡 API 接口

| 端点 | 方法 | 说明 | 请求体 |
|------|------|------|--------|
| `/api/status` | GET | 获取当前游戏状态 | - |
| `/api/start` | POST | 开始新游戏 | `{"game_type": "story_chapter", "text": "..."}` |
| `/api/message` | POST | 发送玩家消息 | `{"text": "玩家行动", "player_name": "玩家"}` |
| `/api/narrative/state` | GET | 获取叙事状态（调试） | - |
| `/api/narrative/log` | GET | 获取叙事日志（调试） | - |
| `/api/end` | POST | 手动结束游戏 | - |

### 响应格式示例

```json
{
  "status": "in_progress",
  "round_count": 5,
  "messages": [
    {
      "role": "ai",
      "player_name": "主持人",
      "content": "你站在森林入口...",
      "is_system": false
    }
  ],
  "story_state": {
    "player": {
      "hp": 100,
      "max_hp": 100,
      "level": 1,
      "status": "健康",
      "name": "玩家"
    },
    "world": {
      "scene": "森林入口",
      "time": "清晨",
      "location": "神秘森林"
    }
  },
  "current_chapter": 1,
  "chapters": [
    {
      "title": "第一章",
      "goal": "找到神秘物品",
      "description": "..."
    }
  ]
}
```

## 🏗️ 技术架构

### 双层状态管理

1. **流程状态机（Progress）**：控制游戏流程阶段
   - `NOT_STARTED` → `AWAITING_INITIAL_INPUT` → `AWAITING_OUTLINE_REVIEW` → `IN_PROGRESS` → `ENDED`

2. **世界状态机（story_state）**：管理游戏世界状态
   - 结构固定，数值可变
   - 通过 `state_delta` 增量更新

### 叙事状态机（Narrative State）

独立的叙事状态系统，管理：
- **阶段（Phase）**：initial、world_building、conflict_intro、climax 等
- **信息披露等级（Disclosure）**：unknown、vague_hint、clue、full_reveal
- **风险等级（Risk）**：safe、warning、danger、critical
- **关系向量（Relationship）**：trust、hostility、intimacy

### 多进程安全机制

使用文件锁（`fcntl.flock`）确保多 worker 环境下的数据一致性：

```python
def _with_txn(self, fn):
    # 1. 获取锁
    # 2. 加载最新快照（覆盖内存）
    # 3. 执行业务逻辑
    # 4. 保存快照
    # 5. 释放锁
```

### 安全机制

- **Secrets 过滤**：自动移除 `assets` 和 `story_state` 中的 `secrets` 字段
- **状态验证**：严格校验 `state_delta` 的结构和类型
- **数值约束**：自动 clamp 数值范围（如 `hp >= 0`、`affection 0-100`）

## 📝 注意事项

- 需要有效的 OpenAI API Key
- 确保网络可以访问 OpenAI API（或配置的代理地址）
- 每次游戏会消耗一定的 API 额度
- 游戏状态保存在 `backend/story_game_snapshot.json`
- 支持多进程部署（使用 gunicorn 等），但需要确保文件锁正常工作

## 📄 License

MIT License
