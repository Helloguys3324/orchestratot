const test = require('node:test');
const assert = require('node:assert');
const ChatPage = require('../js/chat.js');

test('ChatPage missing optional chaining cases', async () => {
    // Tests for lines 26, 74, 80-81, 91 (as seen in coverage output)

    // Line 26: session.messages or session.messages fallback
    global.App = { openSession: () => {} };
    global.API = {
        getSessions: async () => [{ id: 's1', name: 'S1', agent_ids: ['a1'], messages: null }]
    };

    const container = { innerHTML: '' };
    await ChatPage.render(container, {}, null);
    assert.ok(container.innerHTML.includes('0 messages'));

    // Line 74: document.getElementById('chat-input')?.focus()
    // Need to test missing 'chat-input'
    global.API = {
        getSession: async () => ({ messages: [], agents: [] })
    };
    global.ws = { connect: () => {}, onMessage: () => {}, listeners: [] };

    global.document = {
        getElementById: () => null
    };

    let headerActions = { innerHTML: '' };
    container.innerHTML = '';

    // This will hit line 74 without throwing since getElementById returns null.
    await ChatPage.render(container, headerActions, 'sess1');
    assert.ok(container.innerHTML.includes('chat-input-area'));

    // Line 80-81: background and border for system/user/other
    // Let's call renderMessage directly
    let html = ChatPage.renderMessage({ role: 'system' });
    assert.ok(html.includes('var(--bg-primary)'));

    html = ChatPage.renderMessage({ role: 'assistant' }); // neither user nor system
    assert.ok(html.includes('var(--bg-card)'));

    // Line 91: timestamp formatting fallback
    html = ChatPage.renderMessage({ timestamp: null, role: 'assistant' });
    assert.ok(!html.includes('toLocaleTimeString'));

    // Clean up
    delete global.App;
    delete global.API;
    delete global.ws;
    delete global.document;
});
