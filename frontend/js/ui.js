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
  }
};
