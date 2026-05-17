const test = require('node:test');
const assert = require('node:assert');
const ChatPage = require('../js/chat.js');

test('ChatPage.formatContent escapes HTML correctly', () => {
    const rawText = '<script>alert("hello & welcome");</script>';
    const html = ChatPage.formatContent(rawText);

    assert.ok(html.includes('&lt;script&gt;'));
    assert.ok(html.includes('&lt;/script&gt;'));
    assert.ok(html.includes('hello &amp; welcome'));
});

test('ChatPage.formatContent parses markdown properly', () => {
    const rawText = 'This is **bold** and *italic*.\nHere is `code`.\n```javascript\nconsole.log(1);\n```';
    const html = ChatPage.formatContent(rawText);

    assert.ok(html.includes('<strong>bold</strong>'));
    assert.ok(html.includes('<em>italic</em>'));
    assert.ok(html.includes('<code>code</code>'));
    assert.ok(html.includes('<pre><code>console.log(1);<br></code></pre>'));
    assert.ok(html.includes('<br>'));
});

test('ChatPage.formatContent handles custom FILE markers', () => {
    const rawText = '<<<FILE: test.js>>>\nconsole.log(1);\n<<<END_FILE>>>';
    const html = ChatPage.formatContent(rawText);

    assert.ok(html.includes('📄 Writing file: <strong>test.js</strong>'));
    assert.ok(html.includes('── end file ──'));
});

test('ChatPage.renderMessage renders user message structure correctly', () => {
    const msg = {
        role: 'user',
        content: 'Hello world',
        sender: 'You',
        icon: '👤',
        color: '#FFFFFF'
    };

    const html = ChatPage.renderMessage(msg);

    assert.ok(html.includes('class="chat-message"'));
    assert.ok(html.includes('style="background:transparent;border-color:var(--accent)"'));
    assert.ok(html.includes('class="chat-avatar"'));
    assert.ok(html.includes('👤'));
    assert.ok(html.includes('class="chat-msg-header"'));
    assert.ok(html.includes('class="chat-sender"'));
    assert.ok(html.includes('You'));
    assert.ok(html.includes('class="chat-content"'));
    assert.ok(html.includes('Hello world'));
});

test('ChatPage.renderMessage renders system message structure correctly', () => {
    const msg = {
        role: 'system',
        content: 'Agent error',
        sender: 'System',
        icon: '⚠️',
        color: '#EF4444'
    };

    const html = ChatPage.renderMessage(msg);

    assert.ok(html.includes('class="chat-message"'));
    assert.ok(html.includes('var(--bg-primary)'));
    assert.ok(html.includes('opacity:0.85'));
    assert.ok(html.includes('⚠️'));
    assert.ok(html.includes('System'));
    assert.ok(html.includes('Agent error'));
});

test('ChatPage.addMessage adds message and scrolls', () => {
    let htmlInserted = '';
    let removeCalled = false;
    let scrollTopValue = 0;

    global.document = {
        getElementById: (id) => {
            if (id === 'chat-messages') {
                return {
                    querySelector: (sel) => {
                        if (sel === '.typing-msg') {
                            return { remove: () => { removeCalled = true; } };
                        }
                        return null;
                    },
                    insertAdjacentHTML: (pos, html) => {
                        if (pos === 'beforeend') htmlInserted = html;
                    },
                    get scrollHeight() { return 200; },
                    set scrollTop(val) { scrollTopValue = val; }
                };
            }
            return null;
        }
    };

    const msg = { role: 'user', content: 'test', sender: 'You' };
    ChatPage.addMessage(msg);

    assert.ok(htmlInserted.includes('class="chat-message"'));
    assert.ok(htmlInserted.includes('test'));
    assert.strictEqual(removeCalled, true);
    assert.strictEqual(scrollTopValue, 200);
});

test('ChatPage.showTyping adds typing indicator and scrolls', () => {
    let htmlInserted = '';
    let removeCalled = false;
    let scrollTopValue = 0;

    global.document = {
        getElementById: (id) => {
            if (id === 'chat-messages') {
                return {
                    querySelector: (sel) => {
                        if (sel === '.typing-msg') {
                            return { remove: () => { removeCalled = true; } };
                        }
                        return null;
                    },
                    insertAdjacentHTML: (pos, html) => {
                        if (pos === 'beforeend') htmlInserted = html;
                    },
                    get scrollHeight() { return 150; },
                    set scrollTop(val) { scrollTopValue = val; }
                };
            }
            return null;
        }
    };

    ChatPage.showTyping();

    assert.ok(htmlInserted.includes('typing-dots'));
    assert.strictEqual(removeCalled, true);
    assert.strictEqual(scrollTopValue, 150);
});

test('ChatPage.updateSendBtn updates button state based on isRunning', () => {
    let btnDisabled = false;
    let btnText = '';

    global.document = {
        getElementById: (id) => {
            if (id === 'chat-send-btn') {
                return {
                    set disabled(val) { btnDisabled = val; },
                    set textContent(val) { btnText = val; }
                };
            }
            return null;
        }
    };

    ChatPage.isRunning = true;
    ChatPage.updateSendBtn();
    assert.strictEqual(btnDisabled, true);
    assert.strictEqual(btnText, '⏳ Working...');

    ChatPage.isRunning = false;
    ChatPage.updateSendBtn();
    assert.strictEqual(btnDisabled, false);
    assert.strictEqual(btnText, 'Send ➤');
});

test('ChatPage.scrollToBottom updates scrollTop to scrollHeight', () => {
    let scrollTopValue = 0;
    global.document = {
        getElementById: (id) => {
            if (id === 'chat-messages') {
                return {
                    get scrollHeight() { return 300; },
                    set scrollTop(val) { scrollTopValue = val; }
                };
            }
            return null;
        }
    };

    ChatPage.scrollToBottom();
    assert.strictEqual(scrollTopValue, 300);
});

// Restore document after tests
test.afterEach(() => {
    delete global.document;
});

test('ChatPage.send successfully sends a message', async () => {
    let apiCalled = false;
    let addedMessages = [];

    global.document = {
        getElementById: (id) => {
            if (id === 'chat-input') {
                return { value: 'test message' };
            }
            if (id === 'chat-send-btn') {
                return { disabled: false, textContent: 'Send' };
            }
            if (id === 'chat-messages') {
                return {
                    querySelector: () => null,
                    insertAdjacentHTML: () => {},
                    scrollHeight: 100,
                    scrollTop: 0
                };
            }
            return null;
        }
    };

    global.API = {
        sendMessage: async (sessionId, msg) => {
            apiCalled = true;
            assert.strictEqual(sessionId, 'sess-123');
            assert.strictEqual(msg, 'test message');
        }
    };

    const originalAddMessage = ChatPage.addMessage;
    ChatPage.addMessage = (msg) => {
        addedMessages.push(msg);
    };

    let showTypingCalled = false;
    const originalShowTyping = ChatPage.showTyping;
    ChatPage.showTyping = () => {
        showTypingCalled = true;
    };

    ChatPage.currentSession = { id: 'sess-123' };
    ChatPage.isRunning = false;

    await ChatPage.send();

    assert.strictEqual(apiCalled, true);
    assert.strictEqual(showTypingCalled, true);
    assert.strictEqual(addedMessages.length, 1);
    assert.strictEqual(addedMessages[0].role, 'user');
    assert.strictEqual(addedMessages[0].content, 'test message');
    assert.strictEqual(ChatPage.isRunning, true);

    ChatPage.addMessage = originalAddMessage;
    ChatPage.showTyping = originalShowTyping;
    delete global.document;
    delete global.API;
});

test('ChatPage.send handles empty messages and invalid state', async () => {
    let apiCalled = false;
    global.API = { sendMessage: async () => { apiCalled = true; } };

    global.document = {
        getElementById: (id) => {
            if (id === 'chat-input') return { value: '   ' };
            return null;
        }
    };
    ChatPage.currentSession = { id: 'sess-123' };
    ChatPage.isRunning = false;
    await ChatPage.send();
    assert.strictEqual(apiCalled, false);

    global.document = {
        getElementById: (id) => {
            if (id === 'chat-input') return { value: 'valid' };
            return null;
        }
    };
    ChatPage.currentSession = null;
    ChatPage.isRunning = false;
    await ChatPage.send();
    assert.strictEqual(apiCalled, false);

    global.document = {
        getElementById: (id) => {
            if (id === 'chat-input') return { value: 'valid' };
            return null;
        }
    };
    ChatPage.currentSession = { id: 'sess-123' };
    ChatPage.isRunning = true;
    await ChatPage.send();
    assert.strictEqual(apiCalled, false);

    delete global.document;
    delete global.API;
});

test('ChatPage.send handles API errors correctly', async () => {
    let addedMessages = [];

    global.document = {
        getElementById: (id) => {
            if (id === 'chat-input') return { value: 'valid' };
            if (id === 'chat-send-btn') return { disabled: false, textContent: 'Send' };
            if (id === 'chat-messages') return { querySelector: () => null, insertAdjacentHTML: () => {}, scrollHeight: 100, scrollTop: 0 };
            return null;
        }
    };

    global.API = {
        sendMessage: async () => {
            throw new Error('Network failure');
        }
    };

    const originalAddMessage = ChatPage.addMessage;
    ChatPage.addMessage = (msg) => { addedMessages.push(msg); };

    let showTypingCalled = false;
    const originalShowTyping = ChatPage.showTyping;
    ChatPage.showTyping = () => { showTypingCalled = true; };

    ChatPage.currentSession = { id: 'sess-123' };
    ChatPage.isRunning = false;

    await ChatPage.send();

    assert.strictEqual(addedMessages.length, 2);
    assert.strictEqual(addedMessages[0].role, 'user');
    assert.strictEqual(addedMessages[1].role, 'system');
    assert.ok(addedMessages[1].content.includes('Network failure'));
    assert.strictEqual(ChatPage.isRunning, false);

    ChatPage.addMessage = originalAddMessage;
    ChatPage.showTyping = originalShowTyping;
    delete global.document;
    delete global.API;
});

test('ChatPage.clearChat handles clearing session correctly', async () => {
    let confirmCalled = false;
    let apiCalled = false;
    let openSessionCalled = false;

    global.confirm = (msg) => {
        confirmCalled = true;
        assert.strictEqual(msg, 'Clear all messages?');
        return true;
    };

    global.API = {
        clearSession: async (id) => {
            apiCalled = true;
            assert.strictEqual(id, 'sess-123');
        }
    };

    global.App = {
        openSession: (id) => {
            openSessionCalled = true;
            assert.strictEqual(id, 'sess-123');
        }
    };

    ChatPage.currentSession = { id: 'sess-123' };

    await ChatPage.clearChat();

    assert.strictEqual(confirmCalled, true);
    assert.strictEqual(apiCalled, true);
    assert.strictEqual(openSessionCalled, true);

    delete global.confirm;
    delete global.API;
    delete global.App;
});

test('ChatPage.clearChat handles cancelled confirm and invalid state', async () => {
    let apiCalled = false;
    global.API = {
        clearSession: async () => { apiCalled = true; }
    };

    // Case 1: Cancelled
    global.confirm = () => false;
    ChatPage.currentSession = { id: 'sess-123' };
    await ChatPage.clearChat();
    assert.strictEqual(apiCalled, false);

    // Case 2: No current session
    global.confirm = () => true;
    ChatPage.currentSession = null;
    await ChatPage.clearChat();
    assert.strictEqual(apiCalled, false);

    delete global.confirm;
    delete global.API;
});

test('ChatPage.showFiles handles empty files properly', async () => {
    let apiCalled = false;
    let htmlInserted = '';

    global.API = {
        getSessionFiles: async (id) => {
            apiCalled = true;
            assert.strictEqual(id, 'sess-123');
            return [];
        }
    };

    global.UI = {
        renderEmptyState: (icon, title, message) => {
            return `<div class="empty">${icon} ${title} ${message}</div>`;
        }
    };

    global.document = {
        body: {
            insertAdjacentHTML: (pos, html) => {
                if (pos === 'beforeend') htmlInserted = html;
            }
        }
    };

    ChatPage.currentSession = { id: 'sess-123' };

    await ChatPage.showFiles();

    assert.strictEqual(apiCalled, true);
    assert.ok(htmlInserted.includes('files-modal'));
    assert.ok(htmlInserted.includes('class="empty"'));
    assert.ok(htmlInserted.includes('No files yet'));

    delete global.API;
    delete global.UI;
    delete global.document;
});

test('ChatPage.showFiles handles populated files properly', async () => {
    let apiCalled = false;
    let htmlInserted = '';

    global.API = {
        getSessionFiles: async (id) => {
            apiCalled = true;
            return [
                { path: 'test.js', size: 1024, content: 'console.log("<test>");' }
            ];
        }
    };

    global.document = {
        body: {
            insertAdjacentHTML: (pos, html) => {
                if (pos === 'beforeend') htmlInserted = html;
            }
        }
    };

    ChatPage.currentSession = { id: 'sess-123' };

    await ChatPage.showFiles();

    assert.strictEqual(apiCalled, true);
    assert.ok(htmlInserted.includes('files-modal'));
    assert.ok(htmlInserted.includes('test.js'));
    assert.ok(htmlInserted.includes('1024 bytes'));
    assert.ok(htmlInserted.includes('&lt;test>')); // tests escaping

    delete global.API;
    delete global.document;
});

test('ChatPage.showFiles handles no current session properly', async () => {
    let apiCalled = false;
    global.API = {
        getSessionFiles: async () => { apiCalled = true; return []; }
    };

    ChatPage.currentSession = null;
    await ChatPage.showFiles();

    assert.strictEqual(apiCalled, false);
    delete global.API;
});

test('ChatPage.render handles missing sessionId (no sessions)', async () => {
    let apiCalled = false;
    let htmlInserted = '';

    global.API = {
        getSessions: async () => { apiCalled = true; return []; }
    };

    global.UI = {
        renderEmptyState: (icon, title, message, btn) => {
            return `<div class="empty">${title}</div>`;
        }
    };

    const container = {
        set innerHTML(val) { htmlInserted = val; }
    };

    await ChatPage.render(container, null, null);

    assert.strictEqual(apiCalled, true);
    assert.ok(htmlInserted.includes('class="empty"'));
    assert.ok(htmlInserted.includes('No Active Sessions'));

    delete global.API;
    delete global.UI;
});

test('ChatPage.render handles missing sessionId (has sessions)', async () => {
    let apiCalled = false;
    let htmlInserted = '';

    global.API = {
        getSessions: async () => {
            apiCalled = true;
            return [
                { id: 's1', name: 'S1', agent_ids: ['a1'], messages: [{}] }
            ];
        }
    };

    const container = {
        set innerHTML(val) { htmlInserted = val; }
    };

    await ChatPage.render(container, null, null);

    assert.strictEqual(apiCalled, true);
    assert.ok(htmlInserted.includes('Select a Session'));
    assert.ok(htmlInserted.includes('S1'));
    assert.ok(htmlInserted.includes('1 agents'));
    assert.ok(htmlInserted.includes('1 messages'));

    delete global.API;
});

test('ChatPage.render handles existing sessionId', async () => {
    let apiCalled = false;
    let wsConnectCalled = false;
    let wsOnMessageCalled = false;
    let scrollToBottomCalled = false;
    let htmlInserted = '';
    let headerInserted = '';

    global.API = {
        getSession: async (id) => {
            apiCalled = true;
            assert.strictEqual(id, 'sess-123');
            return {
                id: 'sess-123',
                messages: [{ role: 'user', content: 'hello' }]
            };
        }
    };

    global.ws = {
        listeners: [],
        connect: (id) => {
            wsConnectCalled = true;
            assert.strictEqual(id, 'sess-123');
        },
        onMessage: (cb) => {
            wsOnMessageCalled = true;
        }
    };

    const originalScrollToBottom = ChatPage.scrollToBottom;
    ChatPage.scrollToBottom = () => { scrollToBottomCalled = true; };

    global.document = {
        getElementById: () => null
    };

    const container = { set innerHTML(val) { htmlInserted = val; } };
    const headerActions = { set innerHTML(val) { headerInserted = val; } };

    await ChatPage.render(container, headerActions, 'sess-123');

    assert.strictEqual(apiCalled, true);
    assert.strictEqual(wsConnectCalled, true);
    assert.strictEqual(wsOnMessageCalled, true);
    assert.strictEqual(scrollToBottomCalled, true);
    assert.ok(headerInserted.includes('Files'));
    assert.ok(htmlInserted.includes('chat-container'));
    assert.ok(htmlInserted.includes('hello')); // message rendered

    ChatPage.scrollToBottom = originalScrollToBottom;
    delete global.API;
    delete global.ws;
    delete global.document;
});

test('ChatPage WebSocket onMessage handles agent_message', async () => {
    let wsOnMessageCb;
    let addMessageCalled = false;
    let showTypingCalled = false;
    let updateSendBtnCalled = false;

    global.API = {
        getSession: async () => ({ id: 'sess-123', messages: [] })
    };

    global.ws = {
        listeners: [],
        connect: () => {},
        onMessage: (cb) => { wsOnMessageCb = cb; }
    };

    const originalAddMessage = ChatPage.addMessage;
    ChatPage.addMessage = (msg) => {
        addMessageCalled = true;
        assert.strictEqual(msg.content, 'hello');
    };

    const originalShowTyping = ChatPage.showTyping;
    ChatPage.showTyping = () => { showTypingCalled = true; };

    const originalUpdateSendBtn = ChatPage.updateSendBtn;
    ChatPage.updateSendBtn = () => { updateSendBtnCalled = true; };

    ChatPage.scrollToBottom = () => {};

    const container = { set innerHTML(val) {} };
    const headerActions = { set innerHTML(val) {} };

    global.document = {
        getElementById: () => null
    };

    await ChatPage.render(container, headerActions, 'sess-123');

    assert.ok(wsOnMessageCb);

    // Simulate non-complete message
    ChatPage.isRunning = true;
    wsOnMessageCb({ type: 'agent_message', data: { role: 'assistant', content: 'hello' } });
    assert.strictEqual(addMessageCalled, true);
    assert.strictEqual(showTypingCalled, true);
    assert.strictEqual(updateSendBtnCalled, false);
    assert.strictEqual(ChatPage.isRunning, true);

    // Reset flags
    addMessageCalled = false;
    showTypingCalled = false;
    updateSendBtnCalled = false;
    ChatPage.addMessage = (msg) => { addMessageCalled = true; };

    // Simulate complete message (system role)
    wsOnMessageCb({ type: 'agent_message', data: { role: 'system', content: 'done' } });
    assert.strictEqual(addMessageCalled, true);
    assert.strictEqual(showTypingCalled, false);
    assert.strictEqual(updateSendBtnCalled, true);
    assert.strictEqual(ChatPage.isRunning, false);

    // Reset flags
    addMessageCalled = false;
    showTypingCalled = false;
    updateSendBtnCalled = false;
    ChatPage.isRunning = true;
    ChatPage.addMessage = (msg) => { addMessageCalled = true; };

    // Simulate complete message (TASK_COMPLETE content)
    wsOnMessageCb({ type: 'agent_message', data: { role: 'assistant', content: 'I am finished. TASK_COMPLETE.' } });
    assert.strictEqual(addMessageCalled, true);
    assert.strictEqual(showTypingCalled, false);
    assert.strictEqual(updateSendBtnCalled, true);
    assert.strictEqual(ChatPage.isRunning, false);

    // Simulate irrelevant message type
    addMessageCalled = false;
    wsOnMessageCb({ type: 'other_message', data: {} });
    assert.strictEqual(addMessageCalled, false);

    ChatPage.addMessage = originalAddMessage;
    ChatPage.showTyping = originalShowTyping;
    ChatPage.updateSendBtn = originalUpdateSendBtn;
    delete global.API;
    delete global.ws;
});
