/**
 * 游戏前端脚本
 */

// const API_BASE = 'http://183.166.183.2:43000/api';
const API_BASE = 'http://127.0.0.1:4000/api';

const chatMessages = document.getElementById('chatMessages');
const questionInput = document.getElementById('questionInput');
const playerName = document.getElementById('playerName');
const sendBtn = document.getElementById('sendBtn');
const startBtn = document.getElementById('startBtn');
const endBtn = document.getElementById('endBtn');
const gameTypeSelect = document.getElementById('gameType');
const languageCodeSelect = document.getElementById('languageCode');
const gameStateEl = document.getElementById('gameState');
const chapterInfoEl = document.getElementById('chapterInfo');
const roundCountEl = document.getElementById('roundCount');
const pendingCountEl = document.getElementById('pendingCount');
const loadingOverlay = document.getElementById('loadingOverlay');

const userStateList = document.getElementById('userStateList');
const globalStateList = document.getElementById('globalStateList');
const globalDirectionEl = document.getElementById('globalDirection');
const attributesPanel = document.getElementById('attributesPanel');
const attributesBars = document.getElementById('attributesBars');
const attributesTags = document.getElementById('attributesTags');
const attributesEmpty = document.getElementById('attributesEmpty');

let gameState = 'not_started';

/** 从 story_state 中解析“玩家/角色”对象（AI 可自由定义 player、角色、character 等） */
function getPlayerAttrsFromStoryState(storyState) {
  if (!storyState || typeof storyState !== 'object') return { bars: [], tags: [] };
  const player = storyState.player ?? storyState.角色 ?? storyState.character ?? storyState.主角 ?? null;
  if (!player || typeof player !== 'object') return { bars: [], tags: [] };

  const bars = [];
  const barPairs = [
    { current: 'hp', max: 'max_hp', label: '生命', type: 'hp' },
    { current: '生命', max: '最大生命', label: '生命', type: 'hp' },
    { current: 'health', max: 'max_health', label: '生命', type: 'hp' },
    { current: '体力', max: '最大体力', label: '体力', type: 'default' },
    { current: 'mp', max: 'max_mp', label: '法力', type: 'mp' },
    { current: '法力', max: '最大法力', label: '法力', type: 'mp' },
    { current: '精力', max: '最大精力', label: '精力', type: 'default' }
  ];
  const usedKeys = new Set();
  for (const { current, max, label, type } of barPairs) {
    if (usedKeys.has(current)) continue;
    const curVal = player[current];
    const maxVal = player[max];
    const c = typeof curVal === 'number' ? curVal : parseInt(curVal, 10);
    const m = typeof maxVal === 'number' ? maxVal : parseInt(maxVal, 10);
    if (!Number.isFinite(c) || !Number.isFinite(m) || m <= 0) continue;
    usedKeys.add(current);
    bars.push({ label, current: Math.max(0, c), max: m, type });
  }

  const tags = [];
  for (const k of Object.keys(player)) {
    if (usedKeys.has(k)) continue;
    const v = player[k];
    if (v === null || v === undefined) continue;
    if (typeof v === 'object' && !Array.isArray(v)) continue;
    const value = Array.isArray(v) ? v.join(', ') : String(v);
    if (value.length > 80) continue;
    tags.push({ name: k, value });
  }
  return { bars, tags };
}

/** 根据当前 story_state 渲染角色属性面板（血条 + 属性标签） */
function updateAttributesPanel(data) {
  if (!attributesPanel || !attributesBars || !attributesTags || !attributesEmpty) return;
  const globalState = data && data.global_state ? data.global_state : {};
  const storyState = globalState.story_state || {};
  const { bars, tags } = getPlayerAttrsFromStoryState(storyState);

  if (bars.length === 0 && tags.length === 0) {
    attributesPanel.classList.remove('has-content');
    attributesBars.innerHTML = '';
    attributesTags.innerHTML = '';
    attributesEmpty.style.display = '';
    return;
  }
  attributesPanel.classList.add('has-content');
  attributesEmpty.style.display = 'none';

  attributesBars.innerHTML = bars.map((b) => {
    const pct = Math.min(100, Math.round((b.current / b.max) * 100));
    return `
      <div class="attr-bar">
        <span class="attr-bar-label">${escapeHtml(b.label)}</span>
        <div class="attr-bar-track">
          <div class="attr-bar-fill ${b.type}" style="width:${pct}%"></div>
        </div>
        <span class="attr-bar-value">${b.current} / ${b.max}</span>
      </div>
    `;
  }).join('');

  attributesTags.innerHTML = tags.map((t) =>
    `<span class="attr-tag"><span class="attr-tag-name">${escapeHtml(t.name)}:</span>${escapeHtml(t.value)}</span>`
  ).join('');
}

function showLoading(show = true) {
  if (show) loadingOverlay.classList.remove('hidden');
  else loadingOverlay.classList.add('hidden');
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

async function apiCall(endpoint, method = 'GET', body = null) {
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' }
  };
  if (body) options.body = JSON.stringify(body);

  const resp = await fetch(`${API_BASE}${endpoint}`, options);
  const data = await resp.json().catch(() => ({}));
  if (data && data.error) throw new Error(data.error);
  return data;
}

function renderMessages(messages) {
  if (!messages || messages.length === 0) return;

  const welcomeMsg = chatMessages.querySelector('.welcome-message');
  if (welcomeMsg) welcomeMsg.remove();

  chatMessages.innerHTML = '';

  messages.forEach((msg, idx) => {
    const messageEl = document.createElement('div');
    messageEl.className = `message message-${msg.role}`;
    if (msg.is_system) messageEl.classList.add('message-system');

    const avatar = msg.role === 'ai' ? '🐢' : '👤';

    messageEl.innerHTML = `
      <div class="message-header">
        <div class="message-avatar">${avatar}</div>
        <span class="message-name">${escapeHtml(msg.player_name)}</span>
      </div>
      <div class="message-content">${escapeHtml(msg.content)}</div>
    `;

    messageEl.style.animationDelay = `${idx * 0.03}s`;
    chatMessages.appendChild(messageEl);
  });

  setTimeout(() => {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }, 50);
}

/** 流式渲染：最后一条 AI 消息用打字机效果逐字显示 */
function renderMessagesWithStreamingLast(messages) {
  if (!messages || messages.length === 0) return;

  const welcomeMsg = chatMessages.querySelector('.welcome-message');
  if (welcomeMsg) welcomeMsg.remove();

  chatMessages.innerHTML = '';

  const lastIdx = messages.length - 1;
  const lastMsg = messages[lastIdx];
  const isLastAiWithContent = lastMsg && lastMsg.role === 'ai' && typeof lastMsg.content === 'string' && lastMsg.content.length > 0;

  messages.forEach((msg, idx) => {
    const messageEl = document.createElement('div');
    messageEl.className = `message message-${msg.role}`;
    if (msg.is_system) messageEl.classList.add('message-system');

    const avatar = msg.role === 'ai' ? '🐢' : '👤';
    const isStreamingLast = isLastAiWithContent && idx === lastIdx;
    const content = isStreamingLast ? '' : escapeHtml(msg.content);

    messageEl.innerHTML = `
      <div class="message-header">
        <div class="message-avatar">${avatar}</div>
        <span class="message-name">${escapeHtml(msg.player_name)}</span>
      </div>
      <div class="message-content">${content}<span class="streaming-cursor"></span></div>
    `;

    messageEl.style.animationDelay = `${idx * 0.03}s`;
    chatMessages.appendChild(messageEl);
  });

  chatMessages.scrollTop = chatMessages.scrollHeight;

  if (isLastAiWithContent) {
    const contentEl = chatMessages.querySelector('.message:last-child .message-content');
    const cursorEl = contentEl && contentEl.querySelector('.streaming-cursor');
    if (!contentEl || !cursorEl) return;

    const fullText = lastMsg.content;
    const chunkMs = 18;
    const charsPerChunk = 2;
    let pos = 0;

    function tick() {
      if (pos >= fullText.length) {
        if (cursorEl.parentNode) cursorEl.remove();
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return;
      }
      const end = Math.min(pos + charsPerChunk, fullText.length);
      const segment = fullText.slice(pos, end);
      const textNode = document.createTextNode(segment);
      contentEl.insertBefore(textNode, cursorEl);
      pos = end;
      chatMessages.scrollTop = chatMessages.scrollHeight;
      setTimeout(tick, chunkMs);
    }
    setTimeout(tick, 80);
  }
}

function compactText(text, maxLen = 120) {
  const cleaned = String(text || '').replace(/\s+/g, ' ').trim();
  if (!cleaned) return '';
  if (cleaned.length > maxLen) return `${cleaned.slice(0, maxLen).trim()}...`;
  return cleaned;
}

function formatKey(key) {
  return String(key || '')
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (match) => match.toUpperCase());
}

function formatValue(value) {
  if (value === null || value === undefined) return '-';
  if (typeof value === 'string') return compactText(value, 160) || '-';
  if (typeof value === 'number') return Number.isFinite(value) ? String(value) : '-';
  if (typeof value === 'boolean') return value ? 'true' : 'false';
  return compactText(JSON.stringify(value), 160) || '-';
}

function tryParseJson(text) {
  if (typeof text !== 'string') return null;
  const trimmed = text.trim();
  if (!(trimmed.startsWith('{') || trimmed.startsWith('['))) return null;
  try {
    return JSON.parse(trimmed);
  } catch {
    return null;
  }
}

function renderJsonTree(value, depth = 0, maxDepth = 4) {
  if (depth > maxDepth) {
    return `<span class="kv-tree-value">${escapeHtml(formatValue(value))}</span>`;
  }
  if (value === null || value === undefined) {
    return `<span class="kv-tree-value">-</span>`;
  }
  if (typeof value !== 'object') {
    return `<span class="kv-tree-value">${escapeHtml(formatValue(value))}</span>`;
  }

  const entries = Array.isArray(value) ? value.map((v, i) => [String(i), v]) : Object.entries(value);
  if (entries.length === 0) {
    return `<span class="kv-tree-value">{}</span>`;
  }

  return `
    <div class="kv-tree">
      ${entries.map(([k, v]) => {
        const nested = typeof v === 'object' && v !== null;
        return `
          <div class="kv-tree-row">
            <span class="kv-tree-key">${escapeHtml(formatKey(k))}</span>
            ${nested
              ? `<div class="kv-tree-nested">${renderJsonTree(v, depth + 1, maxDepth)}</div>`
              : `<span class="kv-tree-value">${escapeHtml(formatValue(v))}</span>`
            }
          </div>
        `;
      }).join('')}
    </div>
  `;
}

function renderKeyValueList(obj, excludeKeys = []) {
  if (!obj || typeof obj !== 'object') {
    return '<div class="user-empty">No state yet.</div>';
  }

  const keys = Object.keys(obj).filter((k) => !excludeKeys.includes(k));
  if (keys.length === 0) {
    return '<div class="user-empty">No state yet.</div>';
  }

  return `
    <div class="kv-list">
      ${keys.sort().map((key) => `
        <div class="kv-row">
          <span class="kv-key">${escapeHtml(formatKey(key))}</span>
          ${(() => {
            const raw = obj[key];
            const parsed = tryParseJson(raw);
            if (parsed) {
              return `<div class="kv-value kv-json">${renderJsonTree(parsed)}</div>`;
            }
            if (typeof raw === 'object' && raw !== null) {
              return `<div class="kv-value kv-json">${renderJsonTree(raw)}</div>`;
            }
            return `<span class="kv-value">${escapeHtml(formatValue(raw))}</span>`;
          })()}
        </div>
      `).join('')}
    </div>
  `;
}

function updateUserState(data) {
    if (!userStateList || !globalStateList) {
        return;
    }

    const globalState = data.global_state || {};
    const users = globalState.users || {};
    const direction = globalState.direction || '';

    if (globalDirectionEl) {
        globalDirectionEl.textContent = direction ? `Direction: ${direction}` : 'Direction: -';
    }

    globalStateList.innerHTML = renderKeyValueList(globalState, ['users', 'direction']);

    const names = Object.keys(users);
    // if (userCountEl) {
    //     userCountEl.textContent = `${names.length} users`;
    // }

    // if (names.length === 0) {
    //     userStateList.innerHTML = '<div class="user-empty">No user state yet.</div>';
    //     return;
    // }

    userStateList.innerHTML = '';
    names.sort().forEach((name) => {
        const state = users[name] || {};
        const card = document.createElement('div');
        card.className = 'user-card';
        card.innerHTML = `
            <div class="user-card-header">
                <span class="user-name">${escapeHtml(name)}</span>
            </div>
            ${renderKeyValueList(state)}
        `;
        userStateList.appendChild(card);
    });
}

function updateGameUI(data, options) {
  gameState = data.state;

  const stateTexts = {
    'not_started': '等待开始',
    'awaiting_initial_input': '等待初始想法',
    'awaiting_outline_review': '审核大纲',
    'awaiting_outline': '等待大纲',
    'in_progress': '剧情进行中',
    'ended': '游戏结束'
  };

  gameStateEl.textContent = stateTexts[gameState] || gameState;
  gameStateEl.className = 'value';

  if (gameState === 'not_started') gameStateEl.classList.add('state-waiting');
  else if (gameState === 'awaiting_initial_input' || gameState === 'awaiting_outline_review' || gameState === 'awaiting_outline' || gameState === 'in_progress') gameStateEl.classList.add('state-playing');
  else gameStateEl.classList.add('state-ended');

  roundCountEl.textContent = `${data.round_count} / ${data.max_rounds}`;

  pendingCountEl.textContent = `-`;
  pendingCountEl.className = 'value pending-count';

  // 更新章节信息
  const globalState = data.global_state || {};
  const currentChapter = globalState.current_chapter || 1;
  const chapters = globalState.chapters || [];
  if (chapters.length > 0 && currentChapter <= chapters.length) {
    const chapter = chapters[currentChapter - 1];
    const chapterTitle = chapter.title || `第${currentChapter}章`;
    const chapterGoal = chapter.goal || '';
    if (chapterGoal) {
      chapterInfoEl.textContent = `${chapterTitle} - ${chapterGoal}`;
    } else {
      chapterInfoEl.textContent = chapterTitle;
    }
    chapterInfoEl.title = chapter.description || chapterTitle;
  } else {
    chapterInfoEl.textContent = '-';
    chapterInfoEl.title = '';
  }

  const isPlaying = (gameState === 'awaiting_initial_input' || gameState === 'awaiting_outline_review' || gameState === 'awaiting_outline' || gameState === 'in_progress');
  startBtn.disabled = isPlaying;
  startBtn.textContent = (gameState === 'ended') ? '🎮 重新开始' : '🎮 开始游戏';

  endBtn.disabled = (gameState === 'not_started');

  // 输入框始终保持开启
  questionInput.disabled = false;
  // not_started 时不能直接发言，只能先点开始
  if (gameState === 'not_started') {
    sendBtn.disabled = true;
  } else {
    sendBtn.disabled = false;
  }

  // 游戏进行中不允许切换类型和语言
  if (gameTypeSelect) {
    gameTypeSelect.disabled = isPlaying;
  }
if (languageCodeSelect) {
    languageCodeSelect.disabled = false;
    // 同步服务器返回的语言代码到语言选择器
    if (data && data.global_state && data.global_state.language_code) {
      languageCodeSelect.value = data.global_state.language_code;
    }
  }

  // 根据阶段切换 placeholder
  if (gameState === 'awaiting_initial_input') {
    questionInput.placeholder = '输入几句话描述你的游戏想法（可以是关键词、场景等）...';
  } else if (gameState === 'awaiting_outline_review') {
    questionInput.placeholder = '发送「确认」或「开始」生成游戏，或修改大纲内容...';
  } else if (gameState === 'awaiting_outline') {
    questionInput.placeholder = '请输入剧情大纲（第一条消息会被当作大纲）...';
  } else if (gameState === 'in_progress') {
    questionInput.placeholder = '输入你的行动/对白/尝试...';
  } else if (gameState === 'ended') {
    questionInput.placeholder = '游戏已结束，你仍可以继续对话...';
  } else {
    questionInput.placeholder = '先在这里输入一句话描述你的游戏，再点击「开始游戏」...';
  }

  updateUserState(data);
  updateAttributesPanel(data);
  if (options && options.streamLast && data.messages && data.messages.length > 0) {
    renderMessagesWithStreamingLast(data.messages);
  } else {
    renderMessages(data.messages);
  }
}

async function getStatus() {
  try {
    const data = await apiCall('/status');
    updateGameUI(data);
  } catch (e) {
    console.error('status error:', e);
  }
}

async function startGame() {
  showLoading(true);
  try {
    const game_type = (gameTypeSelect && gameTypeSelect.value) ? String(gameTypeSelect.value) : 'story_chapter';
    const language_code = (languageCodeSelect && languageCodeSelect.value) ? String(languageCodeSelect.value) : 'cn';
    const initialText = questionInput.value.trim();
    const body = { game_type, language_code };
    if (initialText) {
      body.text = initialText;
    }
    // const data = await apiCall('/start', 'POST', body);
    const data = await apiCall('/start_offcial_game', 'POST', body);
    updateGameUI(data);
  } catch (e) {
    alert('启动失败: ' + e.message);
  } finally {
    showLoading(false);
    if (!questionInput.disabled) questionInput.focus();
  }
}

async function sendMessage() {
  const text = questionInput.value.trim();
  if (!text) return;

  // 发送消息时临时禁用按钮，但输入框保持开启
  sendBtn.disabled = true;
  showLoading(true);
  const language_code = (languageCodeSelect && languageCodeSelect.value)
      ? String(languageCodeSelect.value)
      : 'cn';
  try {
    const data = await apiCall('/message', 'POST', {
      player_name: playerName?.value || '玩家',
      text: text,
      language_code: language_code
    });
    questionInput.value = '';
    updateGameUI(data, { streamLast: true });
  } catch (e) {
    alert('发送失败: ' + e.message);
  } finally {
    showLoading(false);
    // 输入框始终保持开启
    questionInput.disabled = false;
    sendBtn.disabled = false;
    questionInput.focus();
  }
}

async function endGame() {
  if (!confirm('确定要结束游戏吗？')) return;
  showLoading(true);
  try {
    const data = await apiCall('/end', 'POST');
    updateGameUI(data);
    // 游戏结束后，确保输入框开启并聚焦
    if (questionInput) {
      questionInput.disabled = false;
      questionInput.focus();
    }
    if (sendBtn) {
      sendBtn.disabled = false;
    }
  } catch (e) {
    alert('结束失败: ' + e.message);
  } finally {
    showLoading(false);
  }
}

// listeners
startBtn.addEventListener('click', startGame);
sendBtn.addEventListener('click', sendMessage);
endBtn.addEventListener('click', endGame);

questionInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

document.addEventListener('DOMContentLoaded', () => {
  console.log('[story] DOMContentLoaded -> getStatus');
  getStatus();
});
