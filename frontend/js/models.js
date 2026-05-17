// Models page UI — categorized with rate limits
const ModelsPage = {
  async render(container) {
    const categories = await API.getModelsByCategory();

    const tierColors = {
      premium: '#EC4899', advanced: '#8B5CF6', fast: '#10B981',
      standard: '#06B6D4', legacy: '#64748B', specialized: '#F59E0B',
      open: '#6366F1', utility: '#94A3B8',
    };

    let html = '';
    for (const [catId, cat] of Object.entries(categories)) {
      const info = cat.info;
      const models = cat.models;

      html += `
        <div style="margin-bottom:32px">
          <h3 style="margin-bottom:14px;font-size:16px;display:flex;align-items:center;gap:8px">
            <span>${info.icon}</span> ${info.label}
            <span class="tag" style="font-size:11px">${models.length}</span>
          </h3>
          <div class="card-grid">
            ${models.map(m => {
              const tc = tierColors[m.tier] || '#64748B';
              const rl = m.rate_limits || {};
              const rpm = rl.rpm === null ? '-' : (rl.rpm || 0);
              const tpm = rl.tpm === null ? '-' : (typeof rl.tpm === 'string' ? rl.tpm : (rl.tpm ? (rl.tpm >= 1000 ? Math.round(rl.tpm/1000) + 'K' : rl.tpm) : '0'));
              const rpd = rl.rpd === null ? '-' : (rl.rpd || 0);
              const maxOut = m.max_output_tokens ? (m.max_output_tokens >= 1000 ? Math.round(m.max_output_tokens/1000) + 'K' : m.max_output_tokens) : '-';

              return `
                <div class="card">
                  <div class="card-header">
                    <div class="card-icon" style="background:${tc}15;color:${tc};font-size:22px">${m.icon}</div>
                    <div style="flex:1;min-width:0">
                      <div class="card-title" style="font-size:14px">${m.name}</div>
                      <span class="tag" style="background:${tc}20;color:${tc};border-color:${tc}40;font-size:10px">${m.tier}</span>
                    </div>
                  </div>
                  <div class="card-desc" style="font-size:12px">${m.description}</div>
                  ${m.notes ? `<div style="margin-top:6px;font-size:11px;color:var(--warning)">⚠️ ${m.notes}</div>` : ''}
                  <div style="margin-top:12px;display:flex;gap:6px;flex-wrap:wrap">
                    ${m.supports_vision ? '<span class="tag tag-success" style="font-size:10px">👁️ Vision</span>' : ''}
                    ${m.supports_tools ? '<span class="tag tag-success" style="font-size:10px">🔧 Tools</span>' : ''}
                    ${m.context_window ? `<span class="tag" style="font-size:10px">📏 ${m.context_window} ctx</span>` : ''}
                    ${m.max_output_tokens ? `<span class="tag" style="font-size:10px">📤 ${maxOut} out</span>` : ''}
                  </div>
                  <div style="margin-top:10px;padding-top:10px;border-top:1px solid var(--border);display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;text-align:center">
                    <div>
                      <div style="font-size:10px;color:var(--text-muted)">RPM</div>
                      <div style="font-size:14px;font-weight:600;color:${rpm === 0 || rpm === '0' ? 'var(--text-muted)' : 'var(--text-primary)'}">${rpm}</div>
                    </div>
                    <div>
                      <div style="font-size:10px;color:var(--text-muted)">TPM</div>
                      <div style="font-size:14px;font-weight:600;color:${tpm === 0 || tpm === '0' ? 'var(--text-muted)' : 'var(--text-primary)'}">${tpm}</div>
                    </div>
                    <div>
                      <div style="font-size:10px;color:var(--text-muted)">RPD</div>
                      <div style="font-size:14px;font-weight:600;color:${rpd === 0 || rpd === '0' ? 'var(--text-muted)' : 'var(--text-primary)'}">${rpd}</div>
                    </div>
                  </div>
                </div>`;
            }).join('')}
          </div>
        </div>`;
    }

    container.innerHTML = html;
  }
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = ModelsPage;
}
