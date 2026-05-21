const test = require('node:test');
const assert = require('node:assert');
const API = require('../js/api.js');

test('API fallback checks correct request mappings for UI inputs', async () => {
    const originalRequest = API.request;
    const calls = [];
    API.request = async (method, path, body) => {
        calls.push({ method, path, body });
        return {};
    };

    await API.createSkill({ name: 'Skill2' });
    assert.deepStrictEqual(calls[0], { method: 'POST', path: '/api/skills', body: { name: 'Skill2' } });

    await API.getSettings();
    assert.deepStrictEqual(calls[1], { method: 'GET', path: '/api/settings', body: undefined });

    await API.saveSettings({ theme: 'dark' });
    assert.deepStrictEqual(calls[2], { method: 'POST', path: '/api/settings', body: { theme: 'dark' } });

    await API.getTemplates();
    assert.deepStrictEqual(calls[3], { method: 'GET', path: '/api/templates', body: undefined });

    await API.getModelsByCategory();
    assert.deepStrictEqual(calls[4], { method: 'GET', path: '/api/models/categories', body: undefined });

    await API.getChatModels();
    assert.deepStrictEqual(calls[5], { method: 'GET', path: '/api/models/chat', body: undefined });

    API.request = originalRequest;
});
