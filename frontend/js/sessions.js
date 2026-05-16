// Sessions page UI
const SessionsPage = {
  async render(container, headerActions) {
    headerActions.innerHTML = `<button class="btn btn-primary" onclick="SessionsPage.showCreateModal()">+ New Session</button>`;
    const sessions = await API.getSessions();

    if (!sessions.length) {
      container.innerHTML = `
        <div class="empty-state">
          <div class="icon">📋</div>
          <h3>No Sessions</h3>
          <p>Create a session to start a multi-agent conversation.</p>
          <button class="btn btn-primary" onclick="SessionsPage.showCreateModal()">+ Create Session</button>
        </div>`;
      return;
    }

    container.innerHTML = `
      <div class="card-grid">
        ${sessions.map(s => {
          const msgCount = (s.messages || []).length;
          return `
            <div class="card" style="cursor:pointer" onclick="App.openSession('${s.id}')">
              <div class="card-header">
                <div class="card-icon">💬</div>
                <div>
                  <div class="card-title">${s.name}</div>
                  <div style="font-size:11px;color:var(--text-muted)">${s.strategy} · ${s.agent_ids.length} agents · ${msgCount} msgs</div>
                </div>
                <div style="margin-left:auto">
                  <span class="tag ${s.status==='running'?'tag-warning':'tag-success'}">${s.status}</span>
                </div>
              </div>
              <div style="font-size:12px;color:var(--text-muted)">Created: ${new Date(s.created_at).toLocaleString()}</div>
              <div class="card-actions">
                <button class="btn btn-sm" onclick="event.stopPropagation();App.openSession('${s.id}')">💬 Open</button>
                <button class="btn btn-sm btn-danger" onclick="event.stopPropagation();SessionsPage.remove('${s.id}')">🗑️</button>
              </div>
            </div>`;
        }).join('')}
      </div>`;
  },

  async showCreateModal() {
    const agents = await API.getAgents();
    if (!agents.length) {
      alert('Create agents first before making a session!');
      App.navigate('agents');
      return;
    }

    const agentChecks = agents.map(a => `
      <label class="agent-chip" style="cursor:pointer">
        <input type="checkbox" class="session-agent-check" value="${a.id}" style="display:none">
        <span>${a.icon} ${a.name}</span>
      </label>`).join('');

    // Toggle chip selection
    setTimeout(() => {
      document.querySelectorAll('.agent-chip').forEach(chip => {
        chip.addEventListener('click', () => {
          const cb = chip.querySelector('input');
          cb.checked = !cb.checked;
          chip.classList.toggle('selected', cb.checked);
        });
      });
    }, 100);

    const html = `
      <div class="modal-overlay" id="session-modal" onclick="if(event.target===this)this.remove()">
        <div class="modal">
          <div class="modal-header">
            <h3>📋 Create Session</h3>
            <button class="modal-close" onclick="document.getElementById('session-modal').remove()">✕</button>
          </div>
          <div class="form-group">
            <label class="form-label">Session Name</label>
            <input class="form-input" id="sess-name" placeholder="My Session">
          </div>
          <div class="form-group">
            <label class="form-label">Select Agents</label>
            <div style="display:flex;flex-wrap:wrap;gap:8px">${agentChecks}</div>
          </div>
          <div class="form-group">
            <label class="form-label">Chat Strategy</label>
            <select class="form-select" id="sess-strategy">
              <option value="round_robin">Round Robin — agents speak in order</option>
              <option value="auto">Auto — LLM picks who speaks next</option>
              <option value="random">Random — random agent each turn</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Max Rounds: <span id="sess-rounds-val">15</span></label>
            <input type="range" class="range-slider" id="sess-rounds" min="3" max="50" value="15"
              oninput="document.getElementById('sess-rounds-val').textContent=this.value">
          </div>

          <div id="sess-error" style="color:var(--danger);font-size:13px;display:none;margin-bottom:12px"></div>

          <div class="modal-footer">
            <button class="btn" onclick="document.getElementById('session-modal').remove()">Cancel</button>
            <button class="btn btn-primary" id="sess-create-btn" onclick="SessionsPage.create()">Create Session</button>
          </div>
        </div>
      </div>`;
    document.body.insertAdjacentHTML('beforeend', html);
  },

  async create() {
    const errDiv = document.getElementById('sess-error');
    errDiv.style.display = 'none';

    const agentIds = [...document.querySelectorAll('.session-agent-check:checked')].map(c => c.value);
    if (!agentIds.length) {
      errDiv.textContent = 'Select at least one agent';
      errDiv.style.display = 'block';
      return;
    }
    const data = {
      name: document.getElementById('sess-name').value || 'New Session',
      agent_ids: agentIds,
      strategy: document.getElementById('sess-strategy').value,
      max_rounds: parseInt(document.getElementById('sess-rounds').value),
    };

    const btn = document.getElementById('sess-create-btn');
    const originalText = btn.textContent;
    btn.textContent = '⏳ Creating...';
    btn.disabled = true;

    try {
      const session = await API.createSession(data);
      document.getElementById('session-modal')?.remove();
      App.openSession(session.id);
    } catch (e) {
      errDiv.textContent = e.message;
      errDiv.style.display = 'block';
      btn.textContent = originalText;
      btn.disabled = false;
    }
  },

  async remove(id) {
    if (!confirm('Delete this session?')) return;
    await API.deleteSession(id);
    App.navigate('sessions');
  },
};
