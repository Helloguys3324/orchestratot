// Agents page UI
const AgentsPage = {
  templates: [],

  async render(container, headerActions) {
    headerActions.innerHTML = `<button class="btn btn-primary" onclick="AgentsPage.showCreateModal()">+ New Agent</button>`;
    const agents = await API.getAgents();
    document.getElementById('agents-count').textContent = agents.length;

    if (!agents.length) {
      container.innerHTML = UI.renderEmptyState(
        '🤖',
        'No Agents Yet',
        'Create your first AI agent to start building your orchestrator team.',
        `<button class="btn btn-primary" onclick="AgentsPage.showCreateModal()">+ Create Agent</button>`
      );
      return;
    }

    container.innerHTML = `<div class="card-grid">${agents.map(a => this.agentCard(a)).join('')}</div>`;
  },

  agentCard(a) {
    const skills = (a.skills || []).map(s => `<span class="tag">${s}</span>`).join(' ');
    return `
      <div class="card" id="agent-${a.id}">
        <div class="card-header">
          <div class="card-icon" style="background:${a.color}20;color:${a.color}">${a.icon}</div>
          <div>
            <div class="card-title">${a.name}</div>
            <div style="font-size:11px;color:var(--text-muted)">${a.model}</div>
          </div>
          <div style="margin-left:auto">
            <span class="status-dot ${a.enabled ? 'online' : 'offline'}"></span>
          </div>
        </div>
        <div class="card-desc">${a.description || 'No description'}</div>
        <div style="margin-top:10px;display:flex;gap:4px;flex-wrap:wrap">${skills}</div>
        <div class="card-actions">
          <button class="btn btn-sm" onclick="AgentsPage.showEditModal('${a.id}')">✏️ Edit</button>
          <button class="btn btn-sm" onclick="AgentsPage.duplicate('${a.id}')">📋 Clone</button>
          <button class="btn btn-sm btn-danger" onclick="AgentsPage.remove('${a.id}')">🗑️</button>
        </div>
      </div>`;
  },

  async showCreateModal() {
    if (!this.templates.length) {
      this.templates = await API.getTemplates();
    }

    const models = await API.getChatModels();
    const skills = await API.getSkills();

    const tplGrid = this.templates.filter(t => t.id !== 'custom').map(t => `
      <div class="template-card" data-tid="${t.id}" onclick="AgentsPage.selectTemplate('${t.id}')">
        <div class="t-icon">${t.icon}</div>
        <div class="t-name">${t.name}</div>
      </div>`).join('');

    const modelOpts = UI.renderModelOptions(models);
    const skillChecks = UI.renderSkillCheckboxes(skills, [], 'skill-check');

    const html = `
      <div class="modal-overlay" id="agent-modal" onclick="if(event.target===this)this.remove()">
        <div class="modal">
          <div class="modal-header">
            <h3>🤖 Create Agent</h3>
            <button class="modal-close" onclick="document.getElementById('agent-modal').remove()">✕</button>
          </div>

          <div class="form-group">
            <label class="form-label">Template</label>
            <div class="template-grid">${tplGrid}</div>
          </div>

          <div class="form-group">
            <label class="form-label">Name</label>
            <input class="form-input" id="ag-name" placeholder="Agent name">
          </div>
          <div class="form-group">
            <label class="form-label">Icon</label>
            <input class="form-input" id="ag-icon" placeholder="🤖" style="width:80px">
          </div>
          <div class="form-group">
            <label class="form-label">Model</label>
            <select class="form-select" id="ag-model">${modelOpts}</select>
          </div>
          <div class="form-group">
            <label class="form-label">System Prompt</label>
            <textarea class="form-textarea" id="ag-prompt" rows="5" placeholder="Agent instructions..."></textarea>
          </div>
          <div class="form-group">
            <label class="form-label">Temperature: <span id="ag-temp-val">0.7</span></label>
            <input type="range" class="range-slider" id="ag-temp" min="0" max="2" step="0.1" value="0.7"
              oninput="document.getElementById('ag-temp-val').textContent=this.value">
          </div>
          <div class="form-group">
            <label class="form-label">Skills</label>
            <div style="max-height:120px;overflow-y:auto">${skillChecks}</div>
          </div>

          <div id="ag-error" style="color:var(--danger);font-size:13px;display:none;margin-bottom:12px"></div>

          <div class="modal-footer">
            <button class="btn" onclick="document.getElementById('agent-modal').remove()">Cancel</button>
            <button class="btn btn-primary" id="ag-create-btn" onclick="AgentsPage.create()">Create Agent</button>
          </div>
        </div>
      </div>`;
    document.body.insertAdjacentHTML('beforeend', html);
  },

  selectTemplate(tid) {
    const tpl = this.templates.find(t => t.id === tid);
    if (!tpl) return;
    document.querySelectorAll('.template-card').forEach(c => c.classList.remove('selected'));
    document.querySelector(`.template-card[data-tid="${tid}"]`)?.classList.add('selected');
    document.getElementById('ag-name').value = tpl.name;
    document.getElementById('ag-icon').value = tpl.icon;
    document.getElementById('ag-prompt').value = tpl.system_prompt;
    this._selectedTemplate = tid;
  },

  async create() {
    UI.hideError('ag-error');

    const name = document.getElementById('ag-name').value.trim();
    const system_prompt = document.getElementById('ag-prompt').value.trim();

    if (!name) {
      UI.showError('ag-error', 'Name is required.');
      return;
    }
    if (!system_prompt) {
      UI.showError('ag-error', 'System Prompt is required.');
      return;
    }

    const data = {
      template: this._selectedTemplate || 'custom',
      name: name,
      icon: document.getElementById('ag-icon').value || '🤖',
      model: document.getElementById('ag-model').value,
      system_prompt: system_prompt,
      temperature: parseFloat(document.getElementById('ag-temp').value),
      skills: [...document.querySelectorAll('.skill-check:checked')].map(c => c.value),
    };

    await UI.withLoading('ag-create-btn', '⏳ Creating...', async () => {
      try {
        await API.createAgent(data);
        document.getElementById('agent-modal')?.remove();
        this._selectedTemplate = null;
        App.navigate('agents');
      } catch (e) {
        UI.showError('ag-error', e.message);
      }
    });
  },

  async showEditModal(id) {
    const a = await API.getAgent(id);
    const models = await API.getChatModels();
    const skills = await API.getSkills();
    const modelOpts = UI.renderModelOptions(models, a.model);
    const skillChecks = UI.renderSkillCheckboxes(skills, a.skills || [], 'skill-check-edit');

    const html = `
      <div class="modal-overlay" id="agent-edit-modal" onclick="if(event.target===this)this.remove()">
        <div class="modal">
          <div class="modal-header">
            <h3>✏️ Edit: ${a.icon} ${a.name}</h3>
            <button class="modal-close" onclick="document.getElementById('agent-edit-modal').remove()">✕</button>
          </div>
          <div class="form-group">
            <label class="form-label">Name</label>
            <input class="form-input" id="age-name" value="${a.name}">
          </div>
          <div class="form-group">
            <label class="form-label">Icon</label>
            <input class="form-input" id="age-icon" value="${a.icon}" style="width:80px">
          </div>
          <div class="form-group">
            <label class="form-label">Model</label>
            <select class="form-select" id="age-model">${modelOpts}</select>
          </div>
          <div class="form-group">
            <label class="form-label">System Prompt</label>
            <textarea class="form-textarea" id="age-prompt" rows="5">${a.system_prompt}</textarea>
          </div>
          <div class="form-group">
            <label class="form-label">Temperature: <span id="age-temp-val">${a.temperature}</span></label>
            <input type="range" class="range-slider" id="age-temp" min="0" max="2" step="0.1" value="${a.temperature}"
              oninput="document.getElementById('age-temp-val').textContent=this.value">
          </div>
          <div class="form-group">
            <label class="form-label">Skills</label>
            <div style="max-height:120px;overflow-y:auto">${skillChecks}</div>
          </div>
          <div class="form-group" style="display:flex;align-items:center;gap:12px">
            <label class="form-label" style="margin:0">Enabled</label>
            <div class="toggle ${a.enabled?'active':''}" id="age-enabled" onclick="this.classList.toggle('active')"></div>
          </div>

          <div id="age-error" style="color:var(--danger);font-size:13px;display:none;margin-bottom:12px"></div>

          <div class="modal-footer">
            <button class="btn" onclick="document.getElementById('agent-edit-modal').remove()">Cancel</button>
            <button class="btn btn-primary" id="age-save-btn" onclick="AgentsPage.update('${a.id}')">Save</button>
          </div>
        </div>
      </div>`;
    document.body.insertAdjacentHTML('beforeend', html);
  },

  async update(id) {
    UI.hideError('age-error');

    const name = document.getElementById('age-name').value.trim();
    const system_prompt = document.getElementById('age-prompt').value.trim();

    if (!name) {
      UI.showError('age-error', 'Name is required.');
      return;
    }
    if (!system_prompt) {
      UI.showError('age-error', 'System Prompt is required.');
      return;
    }

    const data = {
      name: name,
      icon: document.getElementById('age-icon').value,
      model: document.getElementById('age-model').value,
      system_prompt: system_prompt,
      temperature: parseFloat(document.getElementById('age-temp').value),
      skills: [...document.querySelectorAll('.skill-check-edit:checked')].map(c => c.value),
      enabled: document.getElementById('age-enabled').classList.contains('active'),
    };

    await UI.withLoading('age-save-btn', '⏳ Saving...', async () => {
      try {
        await API.updateAgent(id, data);
        document.getElementById('agent-edit-modal')?.remove();
        App.navigate('agents');
      } catch (e) {
        UI.showError('age-error', e.message);
      }
    });
  },

  async duplicate(id) {
    await API.duplicateAgent(id);
    App.navigate('agents');
  },

  async remove(id) {
    if (!confirm('Delete this agent?')) return;
    await API.deleteAgent(id);
    App.navigate('agents');
  },
};
