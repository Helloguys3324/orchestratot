const test = require('node:test');
const assert = require('node:assert');
const ChatPage = require('../js/chat.js');

test('ChatPage.renderMessage handles missing content', () => {
    const html = ChatPage.renderMessage({ role: 'user', sender: 'Me' });
    assert.ok(html.includes('<div class="chat-content"></div>'));
});

test('ChatPage.renderMessage handles missing timestamp', () => {
    const html = ChatPage.renderMessage({ role: 'user', sender: 'Me', content: 'test' });
    assert.ok(html.includes('<span class="chat-time"></span>'));
});

test('ChatPage.renderMessage handles missing color and icon', () => {
    const html = ChatPage.renderMessage({ role: 'user', sender: 'Me', content: 'test' });
    assert.ok(html.includes('background:#64748B20;color:#64748B'));
    assert.ok(html.includes('🤖'));
});

test('ChatPage.showTyping ignores missing container', () => {
    global.document = { getElementById: () => null };
    assert.doesNotThrow(() => ChatPage.showTyping());
    delete global.document;
});

test('ChatPage.send ignores missing input', async () => {
    global.document = { getElementById: () => null };
    await ChatPage.send();
    delete global.document;
});

test('ChatPage.send ignores missing session', async () => {
    global.document = {
        getElementById: (id) => id === 'chat-input' ? { value: 'hi' } : null
    };
    ChatPage.currentSession = null;
    await ChatPage.send();
    delete global.document;
});

test('ChatPage.send ignores if already running', async () => {
    global.document = {
        getElementById: (id) => id === 'chat-input' ? { value: 'hi' } : null
    };
    ChatPage.currentSession = { id: 'sess' };
    ChatPage.isRunning = true;
    await ChatPage.send();
    delete global.document;
});

test('ChatPage.updateSendBtn ignores missing btn', () => {
    global.document = { getElementById: () => null };
    assert.doesNotThrow(() => ChatPage.updateSendBtn());
    delete global.document;
});

test('ChatPage.scrollToBottom ignores missing container', () => {
    global.document = { getElementById: () => null };
    assert.doesNotThrow(() => ChatPage.scrollToBottom());
    delete global.document;
});

test('ChatPage.clearChat ignores missing session', async () => {
    ChatPage.currentSession = null;
    await ChatPage.clearChat();
});

test('ChatPage.showFiles ignores missing session', async () => {
    ChatPage.currentSession = null;
    await ChatPage.showFiles();
});
