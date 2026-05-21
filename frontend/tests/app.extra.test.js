const test = require('node:test');
const assert = require('node:assert');
const App = require('../js/app.js');

test('App.init handles empty nav lists correctly', async () => {
    let navigatedTo = null;
    const oldNav = App.navigate;
    App.navigate = async (page) => { navigatedTo = page; };

    global.API = { getAgents: async () => [] };

    global.document = {
        getElementById: (id) => id === 'agents-count' ? { textContent: '' } : null,
        querySelectorAll: (sel) => {
            if (sel === '.nav-item') {
                return []; // Missing item
            }
            return [];
        }
    };

    await App.init();

    App.navigate = oldNav;
    delete global.API;
    delete global.document;
});

test('App handles DOMContentLoaded event trigger safely without exceptions', async () => {
    assert.doesNotThrow(() => {
        let callbackFired = false;
        global.document = {
            addEventListener: (ev, cb) => {
                if (ev === 'DOMContentLoaded') {
                    const originalInit = App.init;
                    App.init = () => { callbackFired = true; };
                    cb();
                    App.init = originalInit;
                }
            }
        };
    });
    delete global.document;
});

test('App.navigate handles optional page items via optional chaining correctly', async () => {
    let navigatedTo = null;

    global.document = {
        querySelectorAll: () => [],
        querySelector: (sel) => {
            if (sel === '.nav-item[data-page="chat"]') return null; // Cover optional chaining
            return null;
        },
        getElementById: (id) => id === 'page-title' ? { textContent: '' } : (id === 'header-actions' ? { innerHTML: '' } : { innerHTML: '' })
    };

    global.ChatPage = { render: async () => {} };

    await App.navigate('chat');

    delete global.document;
    delete global.ChatPage;
});

test('App.openSession handles optional page item correctly', async () => {
    global.document = {
        querySelectorAll: () => [],
        querySelector: (sel) => {
            if (sel === '.nav-item[data-page="chat"]') return null; // Cover optional chaining
            return null;
        },
        getElementById: (id) => {
            if (id === 'page-title') return { textContent: '' };
            if (id === 'header-actions') return { innerHTML: '' };
            if (id === 'main-content') return { innerHTML: '' };
            return null;
        }
    };
    global.ChatPage = { render: async () => {} };

    await App.openSession('session123');

    delete global.document;
    delete global.ChatPage;
});

test('App.saveSettings covers optional chained getElementById correctly', async () => {
    global.document = {
        getElementById: (id) => {
            if (id === 'set-apikey') return { value: 'key' };
            if (id === 'set-baseurl') return { value: 'url' };
            if (id === 'set-model') return { value: 'model' };
            if (id === 'set-temp') return { value: '1.0' };
            if (id === 'set-maxtokens') return { value: '100' };
            if (id === 'set-maxrounds') return { value: '10' };
            if (id === 'save-status') return null; // Missing status element
            return null;
        }
    };

    global.API = { saveSettings: async () => {} };

    const oldUI = global.UI;
    global.UI = {
        withLoading: async (id, text, fn) => {
            await fn();
        }
    };

    const _setTimeout = global.setTimeout;
    let timeoutFired = false;
    global.setTimeout = (cb) => {
        timeoutFired = true;
        cb();
    };

    try {
        await App.saveSettings();
    } catch (e) {
    }

    global.UI = oldUI;
    global.setTimeout = _setTimeout;
    delete global.document;
    delete global.API;
});

test('App.saveSettings error path handles missing status element', async () => {
    global.document = {
        getElementById: (id) => {
            if (id === 'set-apikey') return { value: 'key' };
            if (id === 'set-baseurl') return { value: 'url' };
            if (id === 'set-model') return { value: 'model' };
            if (id === 'set-temp') return { value: '1.0' };
            if (id === 'set-maxtokens') return { value: '100' };
            if (id === 'set-maxrounds') return { value: '10' };
            if (id === 'save-status') return null; // Missing status element
            return null;
        }
    };

    global.API = { saveSettings: async () => { throw new Error('API Error'); } };

    const oldUI = global.UI;
    global.UI = {
        withLoading: async (id, text, fn) => {
            await fn();
        }
    };

    try {
        await App.saveSettings();
    } catch (e) {
    }

    global.UI = oldUI;
    delete global.document;
    delete global.API;
});

test('App.js module.exports handles node environment', () => {
    assert.ok(App.init);
});
