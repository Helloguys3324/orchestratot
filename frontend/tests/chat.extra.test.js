const test = require('node:test');
const assert = require('node:assert');
const ChatPage = require('../js/chat.js');

test('ChatPage.addMessage returns early if no container', () => {
    global.document = { getElementById: () => null };
    assert.doesNotThrow(() => ChatPage.addMessage({ role: 'user' }));
    delete global.document;
});

test('ChatPage.showTyping returns early if no container', () => {
    global.document = { getElementById: () => null };
    assert.doesNotThrow(() => ChatPage.showTyping());
    delete global.document;
});

test('ChatPage.updateSendBtn handles missing button', () => {
    global.document = { getElementById: () => null };
    assert.doesNotThrow(() => ChatPage.updateSendBtn());
    delete global.document;
});

test('ChatPage.scrollToBottom handles missing container', () => {
    global.document = { getElementById: () => null };
    assert.doesNotThrow(() => ChatPage.scrollToBottom());
    delete global.document;
});

test('ChatPage.send returns early if input not found', async () => {
    global.document = { getElementById: () => null };
    ChatPage.currentSession = { id: 'test' };
    ChatPage.isRunning = false;
    await assert.doesNotReject(() => ChatPage.send());
    delete global.document;
});
