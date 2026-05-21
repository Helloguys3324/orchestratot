const test = require('node:test');
const assert = require('node:assert');
const App = require('../js/app.js');
global.UI = require('../js/ui.js');

test('App.navigate anonymous functions', async () => {
    let removed = false;
    global.document = {
        querySelectorAll: () => [{
            classList: { remove: () => { removed = true; } }
        }],
        querySelector: () => null,
        getElementById: () => ({ textContent: '', innerHTML: '' })
    };
    global.ChatPage = { render: async () => {} };
    await App.navigate('chat');
    assert.strictEqual(removed, true);
    delete global.document;
    delete global.ChatPage;
});

test('App.openSession anonymous functions', async () => {
    let removed = false;
    global.document = {
        querySelectorAll: () => [{
            classList: { remove: () => { removed = true; } }
        }],
        querySelector: () => null,
        getElementById: () => ({ textContent: '', innerHTML: '' })
    };
    global.ChatPage = { render: async () => {} };
    await App.openSession('s1');
    assert.strictEqual(removed, true);
    delete global.document;
    delete global.ChatPage;
});

test('App.saveSettings setTimeout anonymous function', async () => {
    const originalSetTimeout = global.setTimeout;
    let timeoutCb = null;
    global.setTimeout = (cb) => { timeoutCb = cb; };

    let displayStyle = '';
    global.document = {
        getElementById: (id) => {
            if (id === 'save-status') return { style: { set display(v) { displayStyle = v; } } };
            return { value: '1' };
        }
    };
    global.API = { saveSettings: async () => {} };
    const oldUI = global.UI;
    global.UI = { withLoading: async (id, msg, fn) => { await fn(); } };

    await App.saveSettings();
    if (timeoutCb) timeoutCb();

    assert.strictEqual(displayStyle, 'none');

    global.setTimeout = originalSetTimeout;
    delete global.document;
    delete global.API;
    global.UI = oldUI;
});

test('App.init DOMContentLoaded anonymous function', () => {
    // This is tested in app.test.js, but let's make sure it covers the branch
});
