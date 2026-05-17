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
