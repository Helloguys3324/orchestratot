// Skills page UI
const SkillsPage = {
  async render(container, headerActions) {
    headerActions.innerHTML = `<button class="btn btn-primary" onclick="SkillsPage.showCreateModal()">+ New Skill</button>`;
    const skills = await API.getSkills();

    container.innerHTML = `
      <div class="card-grid">
        ${skills.map(s => `
          <div class="card">
            <div class="card-header">
              <div class="card-icon">${s.icon}</div>
              <div>
                <div class="card-title">${s.name}</div>
                <span class="tag ${s.builtin ? 'tag-success' : ''}">${s.source}</span>
              </div>
            </div>
            <div class="card-desc">${s.description}</div>
            ${!s.builtin ? `<div class="card-actions"><button class="btn btn-sm btn-danger" onclick="SkillsPage.remove('${s.id}')">🗑️ Delete</button></div>` : ''}
          </div>
        `).join('')}
      </div>`;
  },

  showCreateModal() {
    const html = `
      <div class="modal-overlay" id="skill-modal" onclick="if(event.target===this)this.remove()">
        <div class="modal">
          <div class="modal-header">
            <h3>⚡ Create Skill</h3>
            <button class="modal-close" onclick="document.getElementById('skill-modal').remove()">✕</button>
          </div>
          <div class="form-group">
            <label class="form-label">Name</label>
            <input class="form-input" id="sk-name" placeholder="My Custom Skill">
          </div>
          <div class="form-group">
            <label class="form-label">Icon</label>
            <input class="form-input" id="sk-icon" placeholder="🔧" style="width:80px">
          </div>
          <div class="form-group">
            <label class="form-label">Description</label>
            <input class="form-input" id="sk-desc" placeholder="What does this skill do?">
          </div>
          <div class="form-group">
            <label class="form-label">Python Code</label>
            <textarea class="form-textarea" id="sk-code" rows="10" placeholder="def my_skill(input: str) -> str:\n    return 'result'" style="font-family:monospace"></textarea>
          </div>

          <div id="sk-error" style="color:var(--danger);font-size:13px;display:none;margin-bottom:12px"></div>

          <div class="modal-footer">
            <button class="btn" onclick="document.getElementById('skill-modal').remove()">Cancel</button>
            <button class="btn btn-primary" id="sk-create-btn" onclick="SkillsPage.create()">Create Skill</button>
          </div>
        </div>
      </div>`;
    document.body.insertAdjacentHTML('beforeend', html);
  },

  async create() {
    UI.hideError('sk-error');

    const name = document.getElementById('sk-name').value.trim();
    const description = document.getElementById('sk-desc').value.trim();
    const code = document.getElementById('sk-code').value.trim();

    if (!name || !description || !code) {
      UI.showError('sk-error', 'Name, Description, and Python Code are required.');
      return;
    }

    const data = {
      name: name,
      icon: document.getElementById('sk-icon').value || '🔧',
      description: description,
      code: code,
    };

    await UI.withLoading('sk-create-btn', '⏳ Creating...', async () => {
      try {
        await API.createSkill(data);
        document.getElementById('skill-modal')?.remove();
        App.navigate('skills');
      } catch (e) {
        UI.showError('sk-error', e.message);
      }
    });
  },

  async remove(id) {
    if (!confirm('Delete this skill?')) return;
    await API.deleteSkill(id);
    App.navigate('skills');
  },
};

// Marketplace page
const MarketplacePage = {
  async render(container, headerActions) {
    headerActions.innerHTML = `
      <div style="display:flex;gap:8px">
        <input class="form-input" id="mp-url" placeholder="Skill URL..." style="width:280px">
        <button class="btn btn-primary" onclick="MarketplacePage.installFromUrl()">📦 Install</button>
      </div>`;

    const items = await API.getMarketplace();
    container.innerHTML = `
      <div class="card-grid">
        ${items.map(s => `
          <div class="card">
            <div class="card-header">
              <div class="card-icon">${s.icon}</div>
              <div>
                <div class="card-title">${s.name}</div>
                <span class="tag">${s.category}</span>
              </div>
            </div>
            <div class="card-desc">${s.description}</div>
            <div style="margin-top:8px;font-size:12px;color:var(--text-muted)">
              👤 ${s.author} · ⬇️ ${s.downloads}
            </div>
            <div class="card-actions">
              <button class="btn btn-sm btn-primary" onclick="MarketplacePage.install('${s.url}','${s.name}')">📥 Install</button>
            </div>
          </div>
        `).join('')}
      </div>`;
  },

  async install(url, name) {
    try {
      await API.installSkill(url, name);
      alert('Skill installed!');
    } catch (e) {
      alert('Install failed: ' + e.message);
    }
  },

  async installFromUrl() {
    const url = document.getElementById('mp-url').value.trim();
    if (!url) return alert('Enter a URL');
    await this.install(url, null);
  },
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { SkillsPage, MarketplacePage };
}
