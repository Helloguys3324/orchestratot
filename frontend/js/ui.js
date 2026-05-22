// UI utility for shared component generation
const UI = {
  renderModelOptions(models, selectedId = null) {
    return models.map(m => {
      const rl = m.rate_limits || {};
      const rpm = rl.rpm === null ? '-' : (rl.rpm || 0);
      const sel = selectedId === m.id ? 'selected' : '';
      return `<option value="${m.id}" ${sel}>${m.icon} ${m.name} (${rpm} RPM)</option>`;
    }).join('');
  },

  renderSkillCheckboxes(skills, selectedIds = [], className = '') {
    return skills.map(s => {
      const isChecked = selectedIds.includes(s.id) ? 'checked' : '';
      return `
      <label style="display:flex;align-items:center;gap:8px;cursor:pointer;padding:4px 0">
        <input type="checkbox" class="${className}" value="${s.id}" ${isChecked}> ${s.icon} ${s.name}
      </label>`;
    }).join('');
  },

  renderEmptyState(icon, title, message, actionHtml = '') {
    return `
      <div class="empty-state">
        <div class="icon">${icon}</div>
        <h3>${title}</h3>
        <p>${message}</p>
        ${actionHtml}
      </div>`;
  },

  showError(elementId, message) {
    const errDiv = document.getElementById(elementId);
    if (errDiv) {
      errDiv.textContent = message;
      errDiv.style.display = 'block';
    }
  },

  hideError(elementId) {
    const errDiv = document.getElementById(elementId);
    if (errDiv) {
      errDiv.style.display = 'none';
    }
  },

  async withLoading(btnId, loadingText, actionFn) {
    const btn = document.getElementById(btnId);
    let originalText = '';
    if (btn) {
      originalText = btn.textContent;
      btn.textContent = loadingText;
      btn.disabled = true;
    }
    try {
      await actionFn();
    } finally {
      if (btn) {
        btn.textContent = originalText;
        btn.disabled = false;
      }
    }
  }
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = UI;
}
if (typeof window !== 'undefined') {
  window.UI = UI;
} else if (typeof global !== 'undefined') {
  global.UI = UI;
}
