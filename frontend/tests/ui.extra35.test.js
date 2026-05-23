const test = require('node:test');
const assert = require('node:assert');

test('UI additional checks', () => {
    delete require.cache[require.resolve('../js/ui.js')];
    const UI = require('../js/ui.js');

    // Test showError / hideError mutation tracking
    const mockErrDiv = { textContent: '', style: { display: 'none' } };
    global.document = {
        getElementById: (id) => id === 'err-div' ? mockErrDiv : null
    };

    UI.showError('err-div', 'An error occurred');
    assert.strictEqual(mockErrDiv.textContent, 'An error occurred');
    assert.strictEqual(mockErrDiv.style.display, 'block');

    UI.hideError('err-div');
    assert.strictEqual(mockErrDiv.style.display, 'none');

    // Test withLoading rejecting promise
    const mockBtn = { textContent: 'Go', disabled: false };
    global.document = {
        getElementById: (id) => id === 'btn-submit' ? mockBtn : null
    };

    return UI.withLoading('btn-submit', 'Wait...', async () => {
        assert.strictEqual(mockBtn.textContent, 'Wait...');
        assert.strictEqual(mockBtn.disabled, true);
        throw new Error('Action failed');
    }).catch((err) => {
        assert.strictEqual(err.message, 'Action failed');
        // Finally block should restore original state
        assert.strictEqual(mockBtn.textContent, 'Go');
        assert.strictEqual(mockBtn.disabled, false);
    });
});
