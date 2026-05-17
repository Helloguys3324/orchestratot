
const test = require('node:test');
const assert = require('node:assert');
const App = require('../js/app.js');
global.UI = require('../js/ui.js');

test('App.navigate routes correctly', async () => {
    global.ChatPage = { render: async () => {} };
    global.AgentsPage = { render: async () => {} };
    global.SessionsPage = { render: async () => {} };
    global.ModelsPage = { render: async () => {} };
    global.SkillsPage = { render: async () => {} };
    global.MarketplacePage = { render: async () => {} };

    let settingsRendered = false;
    const origRenderSettings = App.renderSettings;
    App.renderSettings = async () => { settingsRendered = true; };

    const elements = {
        'page-title': { textContent: '' },
        'header-actions': { innerHTML: '' },
        'main-content': { innerHTML: '' }
    };

    global.document = {
        querySelectorAll: () => [],
        querySelector: () => ({ classList: { add: () => {} } }),
        getElementById: (id) => elements[id] || null
    };

    await App.navigate('chat');
    assert.strictEqual(App.currentPage, 'chat');
    assert.strictEqual(elements['page-title'].textContent, '💬 Chat');

    await App.navigate('agents');
    assert.strictEqual(elements['page-title'].textContent, '🤖 Agents');

    await App.navigate('sessions');
    await App.navigate('models');
    await App.navigate('skills');
    await App.navigate('marketplace');

    await App.navigate('settings');
    assert.strictEqual(settingsRendered, true);

    App.renderSettings = origRenderSettings;
    delete global.document;
});

test('App.navigate handles unknown page', async () => {
    const elements = {
        'page-title': { textContent: '' },
        'header-actions': { innerHTML: '' },
        'main-content': { innerHTML: '' }
    };

    global.document = {
        querySelectorAll: () => [],
        querySelector: () => null,
        getElementById: (id) => elements[id] || null
    };

    await App.navigate('unknown');
    assert.strictEqual(elements['page-title'].textContent, 'unknown');

    delete global.document;
});

test('App.navigate catches component errors', async () => {
    global.ChatPage = { render: async () => { throw new Error('Render fail'); } };
    global.UI.renderEmptyState = (icon, title, desc) => `${title}: ${desc}`;

    const elements = {
        'page-title': { textContent: '' },
        'header-actions': { innerHTML: '' },
        'main-content': { innerHTML: '' }
    };

    global.document = {
        querySelectorAll: () => [],
        querySelector: () => null,
        getElementById: (id) => elements[id] || null
    };

    await App.navigate('chat');
    assert.strictEqual(elements['main-content'].innerHTML, 'Error: Render fail');

    delete global.ChatPage;
    delete global.document;
});

test('App.openSession works', async () => {
    global.ChatPage = { render: async () => {} };

    const elements = {
        'page-title': { textContent: '' },
        'header-actions': { innerHTML: '' },
        'main-content': { innerHTML: '' }
    };

    global.document = {
        querySelectorAll: () => [],
        querySelector: () => ({ classList: { add: () => {} } }),
        getElementById: (id) => elements[id] || null
    };

    await App.openSession('s1');

    assert.strictEqual(App.currentPage, 'chat');
    assert.strictEqual(App.currentSessionId, 's1');
    assert.strictEqual(elements['page-title'].textContent, '💬 Chat');

    delete global.ChatPage;
    delete global.document;
});

test('App.init works and loads agents', async () => {
    let navigatedTo = null;
    App.navigate = async (page) => { navigatedTo = page; };

    global.API = {
        getAgents: async () => [{id: '1'}]
    };

    const elements = {
        'agents-count': { textContent: '' }
    };

    global.document = {
        querySelectorAll: () => [],
        getElementById: (id) => elements[id] || null
    };

    await App.init();

    assert.strictEqual(elements['agents-count'].textContent, 1);
    assert.strictEqual(navigatedTo, 'chat');

    delete global.API;
    delete global.document;
});

test('App.init handles API error gracefully', async () => {
    let navigatedTo = null;
    App.navigate = async (page) => { navigatedTo = page; };

    global.API = {
        getAgents: async () => { throw new Error('API Fail'); }
    };

    global.document = {
        querySelectorAll: () => [],
        getElementById: () => null
    };

    const origWarn = console.warn;
    let warned = false;
    console.warn = () => { warned = true; };

    await App.init();

    assert.strictEqual(warned, true);
    assert.strictEqual(navigatedTo, 'chat');

    console.warn = origWarn;
    delete global.API;
    delete global.document;
});

test('App.renderSettings works', async () => {
    global.API = {
        getSettings: async () => ({ api_key: 'test', default_model: 'm1' }),
        getChatModels: async () => [{id: 'm1'}]
    };
    global.UI.renderModelOptions = () => '<option>m1</option>';

    const elements = {
        'main-content': { innerHTML: '' }
    };

    await App.renderSettings(elements['main-content']);

    assert.ok(elements['main-content'].innerHTML.includes('test'));
    assert.ok(elements['main-content'].innerHTML.includes('<option>m1</option>'));

    delete global.API;
});

test('App.saveSettings works', async () => {
    let savedData = null;
    global.API = {
        saveSettings: async (data) => { savedData = data; }
    };
    global.UI.withLoading = async (id, text, fn) => { await fn(); };

    let display = '';
    const statusEl = { style: { display: '', color: '' }, set textContent(val) {} };

    const elements = {
        'set-apikey': { value: 'key' },
        'set-baseurl': { value: 'url' },
        'set-model': { value: 'm1' },
        'set-temp': { value: '0.5' },
        'set-maxtokens': { value: '100' },
        'set-maxrounds': { value: '5' },
        'save-status': statusEl
    };

    global.document = {
        getElementById: (id) => elements[id] || null
    };

    const originalSetTimeout = global.setTimeout;
    global.setTimeout = (fn) => fn();

    await App.saveSettings();

    assert.deepStrictEqual(savedData, {
        api_key: 'key',
        base_url: 'url',
        default_model: 'm1',
        temperature: 0.5,
        max_tokens: 100,
        max_rounds: 5
    });

    global.setTimeout = originalSetTimeout;
    delete global.API;
    delete global.document;
});

test('App.saveSettings handles API errors', async () => {
    global.API = {
        saveSettings: async (data) => { throw new Error('API Fail'); }
    };
    global.UI.withLoading = async (id, text, fn) => { await fn(); };

    const statusEl = { style: { display: '', color: '' }, textContent: '' };

    const elements = {
        'set-apikey': { value: 'key' },
        'set-baseurl': { value: 'url' },
        'set-model': { value: 'm1' },
        'set-temp': { value: '0.5' },
        'set-maxtokens': { value: '100' },
        'set-maxrounds': { value: '5' },
        'save-status': statusEl
    };

    global.document = {
        getElementById: (id) => elements[id] || null
    };

    await App.saveSettings();

    assert.strictEqual(statusEl.textContent, '❌ Error: API Fail');

    delete global.API;
    delete global.document;
});


test('App.init sets up navigation event listeners', async () => {
    let navigatedTo = null;
    App.navigate = async (page) => { navigatedTo = page; };

    global.API = {
        getAgents: async () => [{id: '1'}]
    };

    const elements = {
        'agents-count': { textContent: '' }
    };

    let clickListener = null;
    const mockNavItem = {
        dataset: { page: 'agents' },
        addEventListener: (event, cb) => {
            if (event === 'click') clickListener = cb;
        }
    };

    global.document = {
        querySelectorAll: (selector) => {
            if (selector === '.nav-item[data-page]') return [mockNavItem];
            return [];
        },
        getElementById: (id) => elements[id] || null
    };

    await App.init();

    // Simulate click
    if (clickListener) clickListener();

    assert.strictEqual(navigatedTo, 'agents');

    delete global.API;
    delete global.document;
});

test('DOMContentLoaded event triggers App.init', async () => {
    let initCalled = false;
    const origInit = App.init;
    App.init = async () => { initCalled = true; };

    const eventListeners = {};
    global.document = {
        addEventListener: (event, cb) => {
            eventListeners[event] = cb;
        }
    };

    // Re-evaluate App.js so the event listener gets registered under mock document
    delete require.cache[require.resolve('../js/app.js')];
    const AppReloaded = require('../js/app.js');
    AppReloaded.init = async () => { initCalled = true; };

    if (eventListeners['DOMContentLoaded']) {
        eventListeners['DOMContentLoaded']();
    }

    assert.strictEqual(initCalled, true);

    App.init = origInit;
    delete global.document;
});
