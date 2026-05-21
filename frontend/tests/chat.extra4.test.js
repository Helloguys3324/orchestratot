const test = require('node:test');
const assert = require('node:assert');

test('ChatPage empty string branch in formatContent - explicit undefined text', async () => {
    const ChatPage = require('../js/chat.js');
    assert.throws(() => ChatPage.formatContent(), TypeError);
});

test('ChatPage addMessage handles undefined container', () => {
    const ChatPage = require('../js/chat.js');
    const originalDocument = global.document;
    global.document = {
        getElementById: () => null
    };

    assert.doesNotThrow(() => {
        ChatPage.addMessage({ type: 'agent_message', data: { role: 'user', content: 'test' } });
    });

    global.document = originalDocument;
});

test('ChatPage showTyping handles undefined container', () => {
    const ChatPage = require('../js/chat.js');
    const originalDocument = global.document;
    global.document = {
        getElementById: () => null
    };

    assert.doesNotThrow(() => {
        ChatPage.showTyping();
    });

    global.document = originalDocument;
});

test('ChatPage scrollToBottom handles undefined container', () => {
    const ChatPage = require('../js/chat.js');
    const originalDocument = global.document;
    global.document = {
        getElementById: () => null
    };

    assert.doesNotThrow(() => {
        ChatPage.scrollToBottom();
    });

    global.document = originalDocument;
});
