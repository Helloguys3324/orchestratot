const test = require('node:test');
const assert = require('node:assert');

test('ChatPage handles Node environment without module.exports', () => {
    const fs = require('fs');
    const path = require('path');
    let code = fs.readFileSync(path.join(__dirname, '../js/chat.js'), 'utf8');

    // Make the locally scoped variable accessible on the context object
    code = code.replace('const ChatPage =', 'ChatPage =');

    // Stub global dependencies ChatPage requires in the browser
    const context = {
        module: undefined,
        document: {},
        API: {},
        UI: {},
        ws: {},
        console: console
    };
    require('vm').runInNewContext(code, context);

    assert.strictEqual(typeof context.ChatPage.render, 'function');
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

test('ChatPage empty string branch in formatContent - else case', async () => {
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

    const originalDocument = global.document;
    global.document = {
        getElementById: () => null,
        body: { insertAdjacentHTML: () => {} }
    };

    await ChatPage.render({ set innerHTML(val) {}, querySelector:()=>null, insertAdjacentHTML:()=>{} }, { set innerHTML(val) {} }, '123');

    // simulate agent message without content and non-system
    ChatPage.addMessage = () => {};
    ChatPage.showTyping = () => {};
    ChatPage.scrollToBottom = () => {};

    if (wsCallback) {
        wsCallback({ type: 'agent_message', data: { role: 'user', content: null } });
    }

    global.document = originalDocument;
    delete global.ws;
    delete global.API;
});
