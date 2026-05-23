const test = require('node:test');
const assert = require('node:assert');
const ChatPage = require('../js/chat.js');

test('ChatPage missing container rendering lines', () => {
    // We want to test missing element handles for addMessage, showTyping, and missing currentSession logic.
    global.document = {
        getElementById: () => null
    };

    // test addMessage
    assert.doesNotThrow(() => {
        ChatPage.addMessage({});
    });

    // test showTyping
    assert.doesNotThrow(() => {
        ChatPage.showTyping();
    });
});

test('ChatPage missing currentSession in send()', async () => {
    ChatPage.currentSession = null;
    let showErrorCalled = false;
    global.UI = {
        showError: () => { showErrorCalled = true; }
    };

    // Test send early return when not in a session
    await ChatPage.send();
    // It actually returns undefined right away if !this.currentSession
    // But since UI is not used there, let's verify no throw
    delete global.UI;
});
