const test = require('node:test');
const assert = require('node:assert');
const ChatPage = require('../js/chat.js');

test('ChatPage focus coverage', async () => {
    // Tests for lines 74 and 91 (as seen in coverage output)

    // Line 74: document.getElementById('chat-input')?.focus()
    // Need to test with 'chat-input' element that has a focus method
    global.API = {
        getSession: async () => ({ messages: [], agents: [] })
    };
    global.ws = { connect: () => {}, onMessage: () => {}, listeners: [] };

    let focusCalled = false;
    global.document = {
        getElementById: (id) => {
            if (id === 'chat-input') {
                return { focus: () => { focusCalled = true; } };
            }
            return null;
        }
    };

    const container = { innerHTML: '' };
    let headerActions = { innerHTML: '' };
    await ChatPage.render(container, headerActions, 'sess1');
    assert.strictEqual(focusCalled, true);

    // Line 91: m.timestamp is truthy
    const html = ChatPage.renderMessage({ timestamp: '2023-01-01T12:00:00Z', role: 'assistant' });
    assert.ok(html.includes('chat-time'));

    // Clean up
    delete global.API;
    delete global.ws;
    delete global.document;
});
