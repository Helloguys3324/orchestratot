// Main Application Controller
const App = {
  currentPage: 'chat',
  currentSessionId: null,

  async init() {
    // Set up navigation
    document.querySelectorAll('.nav-item[data-page]').forEach(item => {
      item.addEventListener('click', () => {
        this.navigate(item.dataset.page);
      });
    });

    // Load initial data
    try {
      const agents = await API.getAgents();
      document.getElementById('agents-count').textContent = agents.length;
    } catch (e) {
      console.warn('Could not load agents:', e);
    }

    // Start on chat page
    this.navigate('chat');
  },

  async navigate(page) {
    this.currentPage = page;
    this.currentSessionId = null;

    // Update nav
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.querySelector(`.nav-item[data-page="${page}"]`)?.classList.add('active');

    const container = document.getElementById('main-content');
    const headerActions = document.getElementById('header-actions');
    const pageTitle = document.getElementById('page-title');
    headerActions.innerHTML = '';

    const titles = {
      chat: '💬 Chat',
      agents: '🤖 Agents',
      sessions: '📋 Sessions',
      models: '🧬 Models',
      skills: '⚡ Skills',
      marketplace: '🏪 Skill Marketplace',
      settings: '⚙️ Settings',
    };
    pageTitle.textContent = titles[page] || page;

    try {
      switch (page) {
        case 'chat':
          await ChatPage.render(container, headerActions, null);
          break;
        case 'agents':
          await AgentsPage.render(container, headerActions);
          break;
        case 'sessions':
          await SessionsPage.render(container, headerActions);
          break;
        case 'models':
          await ModelsPage.render(container);
          break;
        case 'skills':
          await SkillsPage.render(container, headerActions);
          break;
        case 'marketplace':
          await MarketplacePage.render(container, headerActions);
          break;
        case 'settings':
          await this.renderSettings(container);
          break;
      }
    } catch (e) {
      container.innerHTML = UI.renderEmptyState('⚠️', 'Error', e.message);
    }
  },

  async openSession(sessionId) {
    this.currentPage = 'chat';
    this.currentSessionId = sessionId;
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.querySelector('.nav-item[data-page="chat"]')?.classList.add('active');
    document.getElementById('page-title').textContent = '💬 Chat';

    const container = document.getElementById('main-content');
    const headerActions = document.getElementById('header-actions');
    await ChatPage.render(container, headerActions, sessionId);
  },

  async renderSettings(container) {
    const settings = await API.getSettings();
    const chatModels = await API.getChatModels();
    const modelOpts = UI.renderModelOptions(chatModels, settings.default_model);

    // Show actual key value so user can see/edit it
    const apiKey = settings.api_key || '';

    container.innerHTML = `
      <div style="max-width:600px">
        <div class="card" style="margin-bottom:20px">
          <h3 style="margin-bottom:16px">🔑 API Configuration</h3>
          <div class="form-group">
            <label class="form-label">Google AI Studio API Key</label>
            <div style="display:flex;gap:8px">
              <input class="form-input" id="set-apikey" type="text"
                placeholder="Paste your API key here..." value="${apiKey}"
                style="flex:1;font-family:monospace;font-size:13px">
            </div>
            <div style="font-size:12px;color:var(--text-muted);margin-top:6px">
              Get your key at <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color:var(--accent)">aistudio.google.com</a>
              ${apiKey ? ' · <span style="color:#10B981">✅ Key is set (' + apiKey.substring(0,8) + '...)</span>' : ' · <span style="color:#EF4444">❌ No key — agents will not work!</span>'}
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Base URL</label>
            <input class="form-input" id="set-baseurl" value="${settings.base_url || 'https://generativelanguage.googleapis.com/v1beta/openai/'}">
          </div>
        </div>

        <div class="card" style="margin-bottom:20px">
          <h3 style="margin-bottom:16px">🎛️ Default Parameters</h3>
          <div class="form-group">
            <label class="form-label">Default Model</label>
            <select class="form-select" id="set-model">${modelOpts}</select>
            <div style="font-size:11px;color:var(--text-muted);margin-top:4px">
              RPM = Requests Per Minute (free tier limits)
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Temperature: <span id="set-temp-val">${settings.temperature || 0.7}</span></label>
            <input type="range" class="range-slider" id="set-temp" min="0" max="2" step="0.1" value="${settings.temperature || 0.7}"
              oninput="document.getElementById('set-temp-val').textContent=this.value">
          </div>
          <div class="form-group">
            <label class="form-label">Max Tokens</label>
            <input class="form-input" id="set-maxtokens" type="number" value="${settings.max_tokens || 4096}">
          </div>
          <div class="form-group">
            <label class="form-label">Max Rounds (Group Chat)</label>
            <input class="form-input" id="set-maxrounds" type="number" value="${settings.max_rounds || 15}">
          </div>
        </div>

        <button class="btn btn-primary" id="save-settings-btn" onclick="App.saveSettings()">💾 Save Settings</button>
        <span id="save-status" style="margin-left:12px;font-size:13px;color:var(--success);display:none">✅ Saved!</span>
      </div>`;
  },

  async saveSettings() {
    const status = document.getElementById('save-status');

    const data = {
      api_key: document.getElementById('set-apikey').value.trim(),
      base_url: document.getElementById('set-baseurl').value.trim(),
      default_model: document.getElementById('set-model').value,
      temperature: parseFloat(document.getElementById('set-temp').value),
      max_tokens: parseInt(document.getElementById('set-maxtokens').value),
      max_rounds: parseInt(document.getElementById('set-maxrounds').value),
    };

    await UI.withLoading('save-settings-btn', '⏳ Saving...', async () => {
      try {
        await API.saveSettings(data);
        status.style.display = 'inline';
        status.style.color = 'var(--success)';
        status.textContent = '✅ Saved!';
        setTimeout(() => { status.style.display = 'none'; }, 3000);
      } catch (e) {
        status.style.display = 'inline';
        status.style.color = 'var(--danger)';
        status.textContent = '❌ Error: ' + e.message;
      }
    });
  },
};

// Initialize
document.addEventListener('DOMContentLoaded', () => App.init());

