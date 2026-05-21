const test = require('node:test');
const assert = require('node:assert');
const App = require('../js/app.js');

test('App.renderSettings covers empty apiKey branch', async () => {
    const elements = {
        'main-content': { innerHTML: '' }
    };
    global.document = {
        getElementById: (id) => elements[id] || null
    };

    global.API = {
        getSettings: async () => ({ api_key: '', default_model: 'm1' }),
        getChatModels: async () => [{ id: 'm1', name: 'Model 1', icon: 'I' }]
    };

    global.UI = {
        renderModelOptions: () => '<option value="m1">Model 1</option>'
    };

    await App.renderSettings(elements['main-content']);

    assert.ok(elements['main-content'].innerHTML.includes('No key'));

    delete global.document;
    delete global.API;
    delete global.UI;
});
