const test = require('node:test');
const assert = require('node:assert');

test('ChatPage empty string branch in formatContent', () => {
    const ChatPage = require('../js/chat.js');
    // Mute dependencies
    global.API = {};

    const html = ChatPage.renderMessage({ role: 'user', content: null });
    assert.ok(html.includes('<div class="chat-content"></div>'));

    delete global.API;
});
