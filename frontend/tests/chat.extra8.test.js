const test = require('node:test');
const assert = require('node:assert');

test('ChatPage fallbacks for getElementById', () => {
    const ChatPage = require('../js/chat.js');
    let nullReturned = false;

    // We can simulate calling some mock methods and returning null to cover lines
    global.document = {
        getElementById: (id) => {
            nullReturned = true;
            return null;
        }
    };

    // these shouldn't throw but might return or skip
    ChatPage.updateSendBtn();
    ChatPage.scrollToBottom();

    assert.strictEqual(nullReturned, true);

    delete global.document;
});
