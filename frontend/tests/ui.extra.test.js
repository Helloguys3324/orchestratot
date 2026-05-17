const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderModelOptions handles empty models array', () => {
    const html = UI.renderModelOptions([]);
    assert.strictEqual(html, '');
});

test('UI.renderModelOptions handles missing rate_limits completely', () => {
    const models = [{ id: '1', name: 'Model', icon: 'M' }];
    const html = UI.renderModelOptions(models);
    assert.ok(html.includes('(0 RPM)'));
});

test('UI.renderSkillCheckboxes handles empty skills array', () => {
    const html = UI.renderSkillCheckboxes([]);
    assert.strictEqual(html, '');
});

test('UI.withLoading restores original text on success', async () => {
    let btnState = { textContent: 'Initial', disabled: false };
    global.document = {
        getElementById: () => btnState
    };

    await UI.withLoading('btn', 'Wait...', async () => {
        assert.strictEqual(btnState.textContent, 'Wait...');
        assert.strictEqual(btnState.disabled, true);
    });

    assert.strictEqual(btnState.textContent, 'Initial');
    assert.strictEqual(btnState.disabled, false);
});

test('UI.showError does not throw when element missing', () => {
    global.document = {
        getElementById: () => null
    };
    assert.doesNotThrow(() => {
        UI.showError('nonexistent', 'An error occurred');
    });
});

test('UI.hideError does not throw when element missing', () => {
    global.document = {
        getElementById: () => null
    };
    assert.doesNotThrow(() => {
        UI.hideError('nonexistent');
    });
});
