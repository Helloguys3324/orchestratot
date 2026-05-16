// API Client for AutoGen Orchestrator
const API = {
  base: '',

  async request(method, path, body = null) {
    const opts = { method, headers: { 'Content-Type': 'application/json' } };
    if (body) opts.body = JSON.stringify(body);
    const resp = await fetch(this.base + path, opts);
    if (!resp.ok) {
      const err = await resp.json().catch(() => ({ detail: resp.statusText }));
      let errMsg = 'Request failed';
      if (err.detail) {
        if (Array.isArray(err.detail)) {
          errMsg = err.detail.map(e => {
            const loc = e.loc ? e.loc[e.loc.length - 1] : '';
            return loc ? `${loc}: ${e.msg}` : e.msg;
          }).join(', ');
        } else if (typeof err.detail === 'string') {
          errMsg = err.detail;
        } else {
          errMsg = JSON.stringify(err.detail);
        }
      } else if (err.message) {
        errMsg = err.message;
      }
      throw new Error(errMsg);
    }
    return resp.json();
  },

  // Settings
  getSettings() { return this.request('GET', '/api/settings'); },
  saveSettings(data) { return this.request('POST', '/api/settings', data); },

  // Templates
  getTemplates() { return this.request('GET', '/api/templates'); },

  // Agents
  getAgents() { return this.request('GET', '/api/agents'); },
  getAgent(id) { return this.request('GET', `/api/agents/${id}`); },
  createAgent(data) { return this.request('POST', '/api/agents', data); },
  updateAgent(id, data) { return this.request('PUT', `/api/agents/${id}`, data); },
  deleteAgent(id) { return this.request('DELETE', `/api/agents/${id}`); },
  duplicateAgent(id) { return this.request('POST', `/api/agents/${id}/duplicate`); },

  // Models
  getModels() { return this.request('GET', '/api/models'); },
  getModelsByCategory() { return this.request('GET', '/api/models/categories'); },
  getChatModels() { return this.request('GET', '/api/models/chat'); },

  // Skills
  getSkills() { return this.request('GET', '/api/skills'); },
  getMarketplace() { return this.request('GET', '/api/skills/marketplace'); },
  createSkill(data) { return this.request('POST', '/api/skills', data); },
  deleteSkill(id) { return this.request('DELETE', `/api/skills/${id}`); },
  installSkill(url, name) { return this.request('POST', '/api/skills/install', { url, name }); },

  // Sessions
  getSessions() { return this.request('GET', '/api/sessions'); },
  getSession(id) { return this.request('GET', `/api/sessions/${id}`); },
  createSession(data) { return this.request('POST', '/api/sessions', data); },
  deleteSession(id) { return this.request('DELETE', `/api/sessions/${id}`); },
  sendMessage(sessionId, message) { return this.request('POST', `/api/sessions/${sessionId}/chat`, { message }); },
  clearSession(id) { return this.request('POST', `/api/sessions/${id}/clear`); },
  getSessionFiles(id) { return this.request('GET', `/api/sessions/${id}/files`); },
};
