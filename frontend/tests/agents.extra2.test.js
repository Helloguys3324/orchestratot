const test = require('node:test');
const assert = require('node:assert');
const AgentsPage = require('../js/agents.js');
const UI = require('../js/ui.js');

test('AgentsPage.agentCard maps skills', () => {
    const html = AgentsPage.agentCard({
        id: '1', name: 'A1', skills: ['skill1']
    });
    assert.ok(html.includes('<span class="tag">skill1</span>'));
});

test('AgentsPage.showCreateModal array map and filter', async () => {
    global.API = {
        getTemplates: async () => [{ id: 'custom', name: 'Custom' }, { id: 't1', name: 'T1' }],
        getChatModels: async () => [],
        getSkills: async () => []
    };
    global.document = { body: { insertAdjacentHTML: () => {} } };
    const originalTemplates = AgentsPage.templates;
    AgentsPage.templates = [];

    // UI required
    global.UI = UI;

    await AgentsPage.showCreateModal();
    delete global.API;
    delete global.document;
    delete global.UI;
});

test('AgentsPage.selectTemplate filter', () => {
    AgentsPage.templates = [{ id: 't1', name: 'T1' }];
    global.document = {
        querySelectorAll: () => [{ classList: { remove: () => {} } }],
        querySelector: () => null,
        getElementById: () => ({ value: '' })
    };
    AgentsPage.selectTemplate('t1');
    delete global.document;
});

test('AgentsPage.create and update skill map', async () => {
    const oldUI = global.UI;
    global.UI = { showError: () => {}, hideError: () => {}, withLoading: async (id, msg, fn) => { await fn(); } };
    global.API = { createAgent: async () => {}, updateAgent: async () => {} };
    global.App = { navigate: () => {} };

    global.document = {
        getElementById: () => ({ value: '1', classList: { contains: () => true } }),
        querySelectorAll: () => [{ value: 's1' }]
    };

    await AgentsPage.create();
    await AgentsPage.update('1');

    if (oldUI === undefined) {
        delete global.UI;
    } else {
        global.UI = oldUI;
    }
    delete global.API;
    delete global.App;
    delete global.document;
});
