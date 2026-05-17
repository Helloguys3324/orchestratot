// Chat page UI — real-time agent conversation
const ChatPage = {
  currentSession: null,
  isRunning: false,

  async render(container, headerActions, sessionId) {
    if (!sessionId) {
      // Show session picker
      const sessions = await API.getSessions();
      if (!sessions.length) {
        container.innerHTML = UI.renderEmptyState(
          '💬',
          'No Active Sessions',
          'Create a session with agents to start chatting.',
          `<button class="btn btn-primary" onclick="App.navigate('sessions')">Go to Sessions</button>`
        );
        return;
      }
      container.innerHTML = `
        <div style="max-width:500px;margin:40px auto">
          <h3 style="margin-bottom:16px">Select a Session</h3>
          <div class="session-list">
            ${sessions.map(s => `
              <div class="session-item" onclick="App.openSession('${s.id}')">
                <div class="s-name">💬 ${s.name}</div>
                <div class="s-meta">${s.agent_ids.length} agents · ${(s.messages||[]).length} messages</div>
              </div>`).join('')}
          </div>
        </div>`;
      return;
    }

    // Load session
    const session = await API.getSession(sessionId);
    this.currentSession = session;
    headerActions.innerHTML = `
      <button class="btn btn-sm" onclick="ChatPage.showFiles()">📂 Files</button>
      <button class="btn btn-sm" onclick="ChatPage.clearChat()">🗑️ Clear</button>
      <button class="btn btn-sm" onclick="App.navigate('sessions')">📋 Sessions</button>`;

    // Connect websocket (clear old listeners first)
    ws.listeners = [];
    ws.connect(sessionId);
    ws.onMessage((data) => {
      if (data.type === 'agent_message') {
        this.addMessage(data.data);
        const isComplete = data.data.role === 'system' || 
                           (data.data.content && data.data.content.includes('TASK_COMPLETE'));
        if (isComplete) {
          this.isRunning = false;
          this.updateSendBtn();
        } else {
          this.showTyping();
        }
      }
    });

    // Render chat
    container.innerHTML = `
      <div class="chat-container">
        <div class="chat-messages" id="chat-messages">
          ${(session.messages || []).map(m => this.renderMessage(m)).join('')}
        </div>
        <div class="chat-input-area">
          <input class="form-input" id="chat-input" placeholder="Type your message..."
            onkeydown="if(event.key==='Enter')ChatPage.send()">
          <button class="btn btn-primary" id="chat-send-btn" onclick="ChatPage.send()">
            Send ➤
          </button>
        </div>
      </div>`;

    this.scrollToBottom();
    document.getElementById('chat-input')?.focus();
  },

  renderMessage(m) {
    const isUser = m.role === 'user';
    const isSys = m.role === 'system';
    const bg = isUser ? 'transparent' : (isSys ? 'var(--bg-primary)' : 'var(--bg-card)');
    const border = isUser ? 'var(--accent)' : (isSys ? 'var(--border)' : 'var(--border)');
    const content = this.formatContent(m.content || '');
    return `
      <div class="chat-message" style="background:${bg};border-color:${border}${isSys ? ';font-size:13px;opacity:0.85' : ''}">
        <div class="chat-avatar" style="background:${m.color || '#64748B'}20;color:${m.color || '#64748B'}">
          ${m.icon || '🤖'}
        </div>
        <div style="flex:1;min-width:0">
          <div class="chat-msg-header">
            <span class="chat-sender" style="color:${m.color || 'var(--text-primary)'}">${m.sender}</span>
            <span class="chat-time">${m.timestamp ? new Date(m.timestamp).toLocaleTimeString() : ''}</span>
          </div>
          <div class="chat-content">${content}</div>
        </div>
      </div>`;
  },

  formatContent(text) {
    let html = text
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      .replace(/&lt;&lt;&lt;FILE:\s*(.+?)&gt;&gt;&gt;/g, '<div style="background:var(--accent-glow);padding:6px 10px;border-radius:6px;margin:6px 0;font-size:12px;color:var(--accent-hover)">📄 Writing file: <strong>$1</strong></div>')
      .replace(/&lt;&lt;&lt;END_FILE&gt;&gt;&gt;/g, '<div style="font-size:11px;color:var(--text-muted);margin-bottom:6px">── end file ──</div>')
      .replace(/\n/g, '<br>');
    return html;
  },

  addMessage(msg) {
    const container = document.getElementById('chat-messages');
    if (!container) return;
    container.querySelector('.typing-msg')?.remove();
    container.insertAdjacentHTML('beforeend', this.renderMessage(msg));
    this.scrollToBottom();
  },

  showTyping() {
    const container = document.getElementById('chat-messages');
    if (!container) return;
    container.querySelector('.typing-msg')?.remove();
    container.insertAdjacentHTML('beforeend', `
      <div class="chat-message typing-msg" style="opacity:0.6">
        <div class="chat-avatar">🤖</div>
        <div><div class="typing-dots"><span></span><span></span><span></span></div></div>
      </div>`);
    this.scrollToBottom();
  },

  async send() {
    const input = document.getElementById('chat-input');
    const msg = input?.value?.trim();
    if (!msg || !this.currentSession || this.isRunning) return;

    input.value = '';
    this.isRunning = true;
    this.updateSendBtn();

    const userMsg = {
      role: 'user', sender: 'You', content: msg,
      timestamp: new Date().toISOString(), icon: '👤', color: '#FFFFFF',
    };
    this.addMessage(userMsg);
    this.showTyping();

    try {
      await API.sendMessage(this.currentSession.id, msg);
    } catch (e) {
      this.addMessage({
        role: 'system', sender: 'System', content: '❌ Error: ' + e.message,
        timestamp: new Date().toISOString(), icon: '⚠️', color: '#EF4444',
      });
      this.isRunning = false;
      this.updateSendBtn();
    }
  },

  updateSendBtn() {
    const btn = document.getElementById('chat-send-btn');
    if (btn) {
      btn.disabled = this.isRunning;
      btn.textContent = this.isRunning ? '⏳ Working...' : 'Send ➤';
    }
  },

  scrollToBottom() {
    const el = document.getElementById('chat-messages');
    if (el) el.scrollTop = el.scrollHeight;
  },

  async clearChat() {
    if (!this.currentSession) return;
    if (!confirm('Clear all messages?')) return;
    await API.clearSession(this.currentSession.id);
    App.openSession(this.currentSession.id);
  },

  async showFiles() {
    if (!this.currentSession) return;
    const files = await API.getSessionFiles(this.currentSession.id);
    
    let content;
    if (!files.length) {
      content = UI.renderEmptyState('📂', 'No files yet', 'Agents will create files here as they work.');
    } else {
      content = files.map(f => `
        <div style="margin-bottom:12px">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
            <span>📄</span>
            <strong style="font-size:13px">${f.path}</strong>
            <span class="tag" style="font-size:10px">${f.size} bytes</span>
          </div>
          <pre style="background:var(--bg-primary);border:1px solid var(--border);border-radius:8px;padding:10px;font-size:12px;max-height:200px;overflow:auto;margin:0">${f.content.replace(/</g,'&lt;')}</pre>
        </div>
      `).join('');
    }

    const html = `
      <div class="modal-overlay" id="files-modal" onclick="if(event.target===this)this.remove()">
        <div class="modal" style="max-width:700px">
          <div class="modal-header">
            <h3>📂 Project Workspace</h3>
            <button class="modal-close" onclick="document.getElementById('files-modal').remove()">✕</button>
          </div>
          <div style="max-height:60vh;overflow-y:auto">${content}</div>
          <div class="modal-footer">
            <span style="font-size:12px;color:var(--text-muted)">${files.length} file(s)</span>
            <button class="btn" onclick="document.getElementById('files-modal').remove()">Close</button>
          </div>
        </div>
      </div>`;
    document.body.insertAdjacentHTML('beforeend', html);
  },
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = ChatPage;
}
