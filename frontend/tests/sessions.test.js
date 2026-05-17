const test = require('node:test');
const assert = require('node:assert');
const SessionsPage = require('../js/sessions.js');

test('SessionsPage.render handles no sessions', async () => {
    global.API = {
        getSessions: async () => []
    };
    global.UI = {
        renderEmptyState: (icon, title, desc, btn) => `${icon} ${title}`
    };

    let containerHtml = '';
    const container = {
        set innerHTML(val) { containerHtml = val; }
    };

    let headerHtml = '';
    const headerActions = {
        set innerHTML(val) { headerHtml = val; }
    };

    await SessionsPage.render(container, headerActions);

    assert.ok(headerHtml.includes('New Session'));
    assert.ok(containerHtml.includes('No Sessions'));

    delete global.API;
    delete global.UI;
});

test('SessionsPage.render handles populated sessions', async () => {
    global.API = {
        getSessions: async () => [
            {
                id: '1',
                name: 'Session 1',
                strategy: 'auto',
                agent_ids: ['a1', 'a2'],
                messages: [1, 2, 3],
                status: 'running',
                created_at: new Date().toISOString()
            },
            {
                id: '2',
                name: 'Session 2',
                strategy: 'round_robin',
                agent_ids: ['a1'],
                messages: [],
                status: 'idle',
                created_at: new Date().toISOString()
            }
        ]
    };

    let containerHtml = '';
    const container = {
        set innerHTML(val) { containerHtml = val; }
    };

    let headerHtml = '';
    const headerActions = {
        set innerHTML(val) { headerHtml = val; }
    };

    await SessionsPage.render(container, headerActions);

    assert.ok(containerHtml.includes('Session 1'));
    assert.ok(containerHtml.includes('auto'));
    assert.ok(containerHtml.includes('3 msgs'));
    assert.ok(containerHtml.includes('tag-warning'));
    assert.ok(containerHtml.includes('Session 2'));
    assert.ok(containerHtml.includes('round_robin'));
    assert.ok(containerHtml.includes('0 msgs'));
    assert.ok(containerHtml.includes('tag-success'));

    delete global.API;
});

test('SessionsPage.showCreateModal alerts if no agents', async () => {
    global.API = {
        getAgents: async () => []
    };
    let alerted = false;
    global.alert = (msg) => { alerted = msg; };
    let navigatedTo = false;
    global.App = {
        navigate: (path) => { navigatedTo = path; }
    };

    await SessionsPage.showCreateModal();

    assert.strictEqual(alerted, 'Create agents first before making a session!');
    assert.strictEqual(navigatedTo, 'agents');

    delete global.API;
    delete global.alert;
    delete global.App;
});

test('SessionsPage.remove prompts and deletes', async () => {
    let deletedId = null;
    global.API = {
        deleteSession: async (id) => { deletedId = id; }
    };
    global.confirm = () => true;
    let navigatedTo = null;
    global.App = {
        navigate: (path) => { navigatedTo = path; }
    };

    await SessionsPage.remove('123');

    assert.strictEqual(deletedId, '123');
    assert.strictEqual(navigatedTo, 'sessions');

    // Cancel prompt
    global.confirm = () => false;
    deletedId = null;
    await SessionsPage.remove('456');
    assert.strictEqual(deletedId, null);

    delete global.API;
    delete global.confirm;
    delete global.App;
});

test('SessionsPage.showCreateModal injects HTML with agents', async () => {
    const originalSetTimeout = global.setTimeout;
    global.setTimeout = (fn) => fn();
    global.API = {
        getAgents: async () => [
            { id: 'a1', name: 'Agent 1', icon: '🤖' }
        ]
    };

    let insertedHtml = '';
    global.document = {
        body: {
            insertAdjacentHTML: (pos, html) => { insertedHtml = html; }
        },
        querySelectorAll: (selector) => {
            if (selector === '.agent-chip') {
                return [];
            }
            return [];
        }
    };

    await SessionsPage.showCreateModal();

    assert.ok(insertedHtml.includes('session-modal'));
    assert.ok(insertedHtml.includes('Agent 1'));

    delete global.API;
        delete global.document;
});

test('SessionsPage.create handles validation', async () => {
    global.UI = {
        hideError: () => {},
        showError: (id, msg) => { throw new Error(msg); },
        withLoading: async (id, text, fn) => { await fn(); }
    };

    global.document = {
        querySelectorAll: (selector) => {
            if (selector === '.session-agent-check:checked') return [];
            return [];
        }
    };

    try {
        await SessionsPage.create();
        assert.fail('Should have thrown validation error');
    } catch (e) {
        assert.strictEqual(e.message, 'Select at least one agent');
    }

    delete global.UI;
    delete global.document;

});

test('SessionsPage.create successfully creates session', async () => {
    let createdData = null;
    let loadingCalled = false;
    global.API = {
        createSession: async (data) => {
            createdData = data;
            return { id: 'new-session' };
        }
    };
    global.UI = {
        hideError: () => {},
        showError: () => {},
        withLoading: async (id, text, fn) => { loadingCalled = true; await fn(); }
    };

    global.document = {
        querySelectorAll: (selector) => {
            if (selector === '.session-agent-check:checked') return [{ value: 'a1' }];
            return [];
        },
        getElementById: (id) => {
            const vals = {
                'sess-name': { value: 'Test Session' },
                'sess-strategy': { value: 'auto' },
                'sess-rounds': { value: '20' },
                'session-modal': { remove: () => {} }
            };
            return vals[id] || null;
        }
    };

    let navigatedTo = null;
    global.App = {
        openSession: (id) => { navigatedTo = id; }
    };

    await SessionsPage.create();

    assert.strictEqual(loadingCalled, true);
    assert.deepStrictEqual(createdData, {
        name: 'Test Session',
        agent_ids: ['a1'],
        strategy: 'auto',
        max_rounds: 20
    });
    assert.strictEqual(navigatedTo, 'new-session');

    delete global.API;
    delete global.UI;
    delete global.document;
    delete global.App;
});

test('SessionsPage.create handles API errors', async () => {
    let errorShown = null;
    global.API = {
        createSession: async () => { throw new Error('API failed'); }
    };
    global.UI = {
        hideError: () => {},
        showError: (id, msg) => { errorShown = msg; },
        withLoading: async (id, text, fn) => { await fn(); }
    };

    global.document = {
        querySelectorAll: (selector) => {
            if (selector === '.session-agent-check:checked') return [{ value: 'a1' }];
            return [];
        },
        getElementById: (id) => {
            const vals = {
                'sess-name': { value: '' }, // test default
                'sess-strategy': { value: 'auto' },
                'sess-rounds': { value: '20' },
                'session-modal': null
            };
            return vals[id] || null;
        }
    };

    await SessionsPage.create();

    assert.strictEqual(errorShown, 'API failed');

    delete global.API;
    delete global.UI;
    delete global.document;
});

test('SessionsPage.showCreateModal handles DOM operations on chip click', async () => {
    // Override setTimeout globally so we can run the toggle logic immediately
    const originalSetTimeout = global.setTimeout;
    let timeoutCb = null;
    global.setTimeout = (cb) => { timeoutCb = cb; };

    global.API = {
        getAgents: async () => [
            { id: 'a1', name: 'Agent 1', icon: '🤖' }
        ]
    };

    let insertedHtml = '';

    // Create a mock chip element with addEventListener logic
    const mockInput = { checked: false };
    const classList = {
        classes: new Set(),
        toggle: (cls, force) => {
            if (force) classList.classes.add(cls);
            else classList.classes.delete(cls);
        }
    };

    let clickListener = null;
    const mockChip = {
        addEventListener: (event, cb) => {
            if (event === 'click') clickListener = cb;
        },
        querySelector: (selector) => {
            if (selector === 'input') return mockInput;
            return null;
        },
        classList: classList
    };

    global.document = {
        body: {
            insertAdjacentHTML: (pos, html) => { insertedHtml = html; }
        },
        querySelectorAll: (selector) => {
            if (selector === '.agent-chip') {
                return [mockChip];
            }
            return [];
        }
    };

    await SessionsPage.showCreateModal();

    // Call the setTimeout callback which attaches events
    if (timeoutCb) timeoutCb();

    // Simulate clicking the chip
    if (clickListener) clickListener();

    assert.strictEqual(mockInput.checked, true);
    assert.ok(classList.classes.has('selected'));

    delete global.API;
    delete global.document;

});

test('SessionsPage.showCreateModal handles no agents successfully without throwing', async () => {
    global.API = {
        getAgents: async () => [],
        getChatModels: async () => []
    };
    let alertCalled = false;
    global.alert = () => { alertCalled = true; };
    global.App = { navigate: () => {} };

    await SessionsPage.showCreateModal();

    assert.strictEqual(alertCalled, true);
    delete global.API;
    delete global.alert;
    delete global.App;
});
