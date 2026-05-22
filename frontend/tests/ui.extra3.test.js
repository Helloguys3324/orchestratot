const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderModelOptions handles objects with unexpected types', () => {
    const models = [
        { id: 123, name: null, icon: undefined, rate_limits: { rpm: 'abc' } }
    ];
    const html = UI.renderModelOptions(models, 123);
    assert.ok(html.includes('<option value="123" selected>undefined null (abc RPM)</option>'));
});

test('UI.renderSkillCheckboxes handles unexpected types in skills', () => {
    const skills = [
        { id: 123, name: null, icon: undefined }
    ];
    const html = UI.renderSkillCheckboxes(skills, [123], 'test-class');
    assert.ok(html.includes('class="test-class" value="123" checked'));
    assert.ok(html.includes('undefined null'));
});

test('UI.withLoading handles finally block when actionFn returns a rejected promise', async () => {
    let btnState = { textContent: 'Initial', disabled: false };
    global.document = {
        getElementById: () => btnState
    };

    let actionCalled = false;
    const actionFn = () => {
        actionCalled = true;
        return Promise.reject(new Error('Rejected promise'));
    };

    await assert.rejects(
        UI.withLoading('btn', 'Wait...', actionFn),
        { message: 'Rejected promise' }
    );

    assert.strictEqual(actionCalled, true);
    assert.strictEqual(btnState.textContent, 'Initial');
    assert.strictEqual(btnState.disabled, false);

    delete global.document;
});

test('UI.renderEmptyState handles null icon and title', () => {
    const html = UI.renderEmptyState(null, null, 'Message');
    assert.ok(html.includes('<div class="icon">null</div>'));
    assert.ok(html.includes('<h3>null</h3>'));
});
