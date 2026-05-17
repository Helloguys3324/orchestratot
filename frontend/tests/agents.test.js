const test = require('node:test');
const assert = require('node:assert');
const AgentsPage = require('../js/agents.js');
global.UI = require('../js/ui.js');

test('AgentsPage.render handles no agents', async () => {
    global.API = {
        getAgents: async () => []
    };
    global.UI.renderEmptyState = () => 'Empty';
    global.document = { getElementById: () => ({ textContent: '' }) };

    let containerHtml = '';
    const container = {
        set innerHTML(val) { containerHtml = val; }
    };

    let headerHtml = '';
    const headerActions = {
        set innerHTML(val) { headerHtml = val; }
    };

    await AgentsPage.render(container, headerActions);

    assert.ok(headerHtml.includes('New Agent'));
    assert.strictEqual(containerHtml, 'Empty');

    delete global.API;
    delete global.document;
});

test('AgentsPage.render handles populated agents', async () => {
    global.API = {
        getAgents: async () => [
            { id: '1', name: 'Agent 1', model: 'gpt', enabled: true, color: '#fff', icon: 'A', description: 'Desc', skills: ['skill1'] },
            { id: '2', name: 'Agent 2', model: 'gpt2', enabled: false, color: '#000', icon: 'B', description: '' }
        ]
    };
    global.document = { getElementById: () => ({ textContent: '' }) };

    let containerHtml = '';
    const container = {
        set innerHTML(val) { containerHtml = val; }
    };

    let headerHtml = '';
    const headerActions = {
        set innerHTML(val) { headerHtml = val; }
    };

    await AgentsPage.render(container, headerActions);

    assert.ok(containerHtml.includes('Agent 1'));
    assert.ok(containerHtml.includes('gpt'));
    assert.ok(containerHtml.includes('online'));
    assert.ok(containerHtml.includes('skill1'));
    assert.ok(containerHtml.includes('Agent 2'));
    assert.ok(containerHtml.includes('offline'));
    assert.ok(containerHtml.includes('No description'));

    delete global.API;
    delete global.document;
});

test('AgentsPage.showCreateModal works', async () => {
    global.API = {
        getTemplates: async () => [{ id: 't1', name: 'T1' }],
        getChatModels: async () => [{ id: 'm1', name: 'M1', rate_limits: {} }],
        getSkills: async () => [{ id: 's1', name: 'S1' }]
    };

    let insertedHtml = '';
    global.document = {
        body: {
            insertAdjacentHTML: (pos, html) => { insertedHtml = html; }
        }
    };

    AgentsPage.templates = [];
    await AgentsPage.showCreateModal();

    assert.ok(insertedHtml.includes('Create Agent'));
    assert.ok(insertedHtml.includes('T1'));

    delete global.API;
    delete global.document;
});

test('AgentsPage.selectTemplate works', () => {
    AgentsPage.templates = [{ id: 't1', name: 'T1', icon: 'X', system_prompt: 'P1' }];

    const elements = {};
    global.document = {
        querySelectorAll: () => [],
        querySelector: () => ({ classList: { add: () => {} } }),
        getElementById: (id) => {
            if (!elements[id]) elements[id] = {};
            return elements[id];
        }
    };

    AgentsPage.selectTemplate('t1');
    AgentsPage.selectTemplate('t2'); // test not found

    assert.strictEqual(elements['ag-name'].value, 'T1');
    assert.strictEqual(elements['ag-icon'].value, 'X');
    assert.strictEqual(elements['ag-prompt'].value, 'P1');

    delete global.document;
});

test('AgentsPage.create validates and saves', async () => {
    let errShown = null;
    let savedData = null;
    global.UI.showError = (id, msg) => { errShown = msg; };
    global.UI.hideError = () => {};
    global.UI.withLoading = async (id, text, fn) => { await fn(); };

    global.API = {
        createAgent: async (data) => { savedData = data; }
    };

    const elements = {
        'ag-name': { value: '' },
        'ag-prompt': { value: '' },
        'ag-icon': { value: 'X' },
        'ag-model': { value: 'm1' },
        'ag-temp': { value: '0.5' }
    };

    global.document = {
        getElementById: (id) => elements[id],
        querySelectorAll: () => []
    };

    await AgentsPage.create();
    assert.strictEqual(errShown, 'Name is required.');

    elements['ag-name'].value = 'Name';
    await AgentsPage.create();
    assert.strictEqual(errShown, 'System Prompt is required.');

    elements['ag-prompt'].value = 'Prompt';
    let navigated = null;
    global.App = { navigate: (p) => { navigated = p; } };

    await AgentsPage.create();

    assert.strictEqual(savedData.name, 'Name');
    assert.strictEqual(savedData.system_prompt, 'Prompt');
    assert.strictEqual(navigated, 'agents');

    delete global.API;
    delete global.document;
    delete global.App;
});

test('AgentsPage.create handles API errors', async () => {
    let errShown = null;
    global.UI.showError = (id, msg) => { errShown = msg; };
    global.UI.hideError = () => {};
    global.UI.withLoading = async (id, text, fn) => { await fn(); };

    global.API = {
        createAgent: async () => { throw new Error('API Fail'); }
    };

    const elements = {
        'ag-name': { value: 'Name' },
        'ag-prompt': { value: 'Prompt' },
        'ag-icon': { value: '' }, // test fallback
        'ag-model': { value: 'm1' },
        'ag-temp': { value: '0.5' }
    };

    global.document = {
        getElementById: (id) => elements[id],
        querySelectorAll: () => []
    };

    await AgentsPage.create();
    assert.strictEqual(errShown, 'API Fail');

    delete global.API;
    delete global.document;
});

test('AgentsPage.showEditModal works', async () => {
    global.API = {
        getAgent: async () => ({ id: 'a1', name: 'A1', enabled: true, skills: [] }),
        getChatModels: async () => [{ id: 'm1', name: 'M1', rate_limits: {} }],
        getSkills: async () => []
    };

    let insertedHtml = '';
    global.document = {
        body: {
            insertAdjacentHTML: (pos, html) => { insertedHtml = html; }
        }
    };

    await AgentsPage.showEditModal('a1');
    assert.ok(insertedHtml.includes('Edit:'));

    delete global.API;
    delete global.document;
});

test('AgentsPage.update works', async () => {
    let savedData = null;
    global.UI.showError = () => {};
    global.UI.hideError = () => {};
    global.UI.withLoading = async (id, text, fn) => { await fn(); };

    global.API = {
        updateAgent: async (id, data) => { savedData = data; }
    };

    const elements = {
        'age-name': { value: 'Name' },
        'age-prompt': { value: 'Prompt' },
        'age-icon': { value: 'X' },
        'age-model': { value: 'm1' },
        'age-temp': { value: '0.5' },
        'age-enabled': { classList: { contains: () => true } }
    };

    global.document = {
        getElementById: (id) => elements[id],
        querySelectorAll: () => []
    };

    let navigated = null;
    global.App = { navigate: (p) => { navigated = p; } };

    await AgentsPage.update('a1');
    assert.strictEqual(savedData.name, 'Name');

    delete global.API;
    delete global.document;
    delete global.App;
});

test('AgentsPage.update validates', async () => {
    let errShown = null;
    global.UI.showError = (id, msg) => { errShown = msg; };
    global.UI.hideError = () => {};

    const elements = {
        'age-name': { value: '' },
        'age-prompt': { value: '' },
    };

    global.document = {
        getElementById: (id) => elements[id],
        querySelectorAll: () => []
    };

    await AgentsPage.update('a1');
    assert.strictEqual(errShown, 'Name is required.');

    elements['age-name'].value = 'Name';
    await AgentsPage.update('a1');
    assert.strictEqual(errShown, 'System Prompt is required.');

    delete global.document;
});

test('AgentsPage.update handles API errors', async () => {
    let errShown = null;
    global.UI.showError = (id, msg) => { errShown = msg; };
    global.UI.hideError = () => {};
    global.UI.withLoading = async (id, text, fn) => { await fn(); };

    global.API = {
        updateAgent: async () => { throw new Error('API Fail'); }
    };

    const elements = {
        'age-name': { value: 'Name' },
        'age-prompt': { value: 'Prompt' },
        'age-icon': { value: 'X' },
        'age-model': { value: 'm1' },
        'age-temp': { value: '0.5' },
        'age-enabled': { classList: { contains: () => true } }
    };

    global.document = {
        getElementById: (id) => elements[id],
        querySelectorAll: () => []
    };

    await AgentsPage.update('a1');
    assert.strictEqual(errShown, 'API Fail');

    delete global.API;
    delete global.document;
});

test('AgentsPage.duplicate works', async () => {
    let duped = null;
    global.API = {
        duplicateAgent: async (id) => { duped = id; }
    };
    let navigated = null;
    global.App = { navigate: (p) => { navigated = p; } };

    await AgentsPage.duplicate('a1');
    assert.strictEqual(duped, 'a1');

    delete global.API;
    delete global.App;
});

test('AgentsPage.remove works', async () => {
    let removed = null;
    global.API = {
        deleteAgent: async (id) => { removed = id; }
    };
    global.confirm = () => true;
    let navigated = null;
    global.App = { navigate: (p) => { navigated = p; } };

    await AgentsPage.remove('a1');
    assert.strictEqual(removed, 'a1');

    delete global.API;
    delete global.confirm;
    delete global.App;
});

test('AgentsPage.remove cancels on prompt', async () => {
    let removed = null;
    global.API = {
        deleteAgent: async (id) => { removed = id; }
    };
    global.confirm = () => false;
    let navigated = null;
    global.App = { navigate: (p) => { navigated = p; } };

    await AgentsPage.remove('a1');
    assert.strictEqual(removed, null);

    delete global.API;
    delete global.confirm;
    delete global.App;
});
