const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderModelOptions handles objects with missing id gracefully', () => {
    const models = [
        { name: 'No ID Model', icon: '?', rate_limits: { rpm: 50 } }
    ];
    const html = UI.renderModelOptions(models, undefined);
    assert.ok(html.includes('<option value="undefined" >? No ID Model (50 RPM)</option>'));
});

test('UI.renderSkillCheckboxes handles selectedIds with mixed types (string vs number)', () => {
    const skills = [
        { id: '123', name: 'String ID', icon: 'A' },
        { id: 456, name: 'Number ID', icon: 'B' }
    ];
    // .includes uses strict equality, so passing numbers won't match strings unless types match
    const html = UI.renderSkillCheckboxes(skills, [123, '456'], 'test-class');
    // Neither should be checked because types don't match strictly
    assert.ok(!html.includes('value="123" checked'));
    assert.ok(!html.includes('value="456" checked'));
});

test('UI.showError gracefully handles when elementId is empty string', () => {
    global.document = {
        getElementById: (id) => {
            assert.strictEqual(id, '');
            return null;
        }
    };
    assert.doesNotThrow(() => {
        UI.showError('', 'Empty ID error');
    });
    delete global.document;
});

test('UI.hideError gracefully handles when elementId is undefined', () => {
    global.document = {
        getElementById: (id) => {
            assert.strictEqual(id, undefined);
            return null;
        }
    };
    assert.doesNotThrow(() => {
        UI.hideError(undefined);
    });
    delete global.document;
});

test('UI.withLoading sets disabled correctly and restores correctly', async () => {
    let btnState = { textContent: 'Initial', disabled: false };
    global.document = {
        getElementById: () => btnState
    };

    let actionCalled = false;
    await UI.withLoading('btn', 'Loading...', async () => {
        actionCalled = true;
        assert.strictEqual(btnState.disabled, true);
        assert.strictEqual(btnState.textContent, 'Loading...');
    });

    assert.strictEqual(actionCalled, true);
    assert.strictEqual(btnState.disabled, false);
    assert.strictEqual(btnState.textContent, 'Initial');

    delete global.document;
});
