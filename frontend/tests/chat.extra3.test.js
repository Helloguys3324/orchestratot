const test = require('node:test');
const assert = require('node:assert');

test('ChatPage handles Node environment without module.exports', () => {
    const originalModule = global.module;
    global.module = undefined; // Force the if condition to fail

    // Evaluate the code using eval
    const fs = require('fs');
    const path = require('path');
    const code = fs.readFileSync(path.join(__dirname, '../js/chat.js'), 'utf8');

    eval(code);

    assert.strictEqual(typeof ChatPage.render, 'function');

    global.module = originalModule;
});

test('ChatPage empty messages array and empty ws listener', async () => {
    const ChatPage = require('../js/chat.js');
    let wsCallback = null;
    global.ws = {
        connect: () => {},
        onMessage: (cb) => { wsCallback = cb; }
    };

    global.API = {
        getSession: async () => ({ id: '123' }) // no messages array
    };

    let containerHtml = '';
    const container = { set innerHTML(val) { containerHtml = val; }, querySelector: () => null, insertAdjacentHTML: () => {} };
    const headerActions = { set innerHTML(val) {} };

    const originalDocument = global.document;
    global.document = {
        getElementById: () => null,
        body: { insertAdjacentHTML: () => {} }
    };

    await ChatPage.render(container, headerActions, '123');

    // Simulate non-agent message
    wsCallback({ type: 'other_message', data: {} });

    assert.ok(containerHtml.includes('<div class="chat-messages" id="chat-messages">'));

    global.document = originalDocument;
    delete global.ws;
    delete global.API;
});

test('ChatPage empty string branch in formatContent - else case', () => {
    // Already covered mostly, but maybe ws callback branch with agent message and NO content
    const ChatPage = require('../js/chat.js');
    let wsCallback = null;
    global.ws = {
        connect: () => {},
        onMessage: (cb) => { wsCallback = cb; }
    };

    global.API = {
        getSession: async () => ({ id: '123' })
    };

    ChatPage.render({ set innerHTML() {}, querySelector:()=>null, insertAdjacentHTML:()=>{} }, { set innerHTML() {} }, '123');

    // simulate agent message without content and non-system
    ChatPage.addMessage = () => {};
    ChatPage.showTyping = () => {};
    ChatPage.scrollToBottom = () => {};

    wsCallback({ type: 'agent_message', data: { role: 'user', content: null } });
});
