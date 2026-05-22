const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderModelOptions handles parameter type mismatches and rendering null properties', () => {
    const models = [
        { id: undefined, name: undefined, icon: undefined, rate_limits: undefined }
    ];
    const html = UI.renderModelOptions(models, undefined);
    assert.ok(html.includes('undefined undefined (0 RPM)'));
});

test('UI.renderSkillCheckboxes handles parameter type mismatches and rendering null properties', () => {
    const skills = [
        { id: null, name: null, icon: null }
    ];
    const html = UI.renderSkillCheckboxes(skills, [null], undefined);
    assert.ok(html.includes('value="null" checked> null null'));
});

test('UI.renderEmptyState handles parameter type mismatches and rendering null properties', () => {
    const html = UI.renderEmptyState(null, null, null, null);
    assert.ok(html.includes('<div class="icon">null</div>'));
    assert.ok(html.includes('<h3>null</h3>'));
    assert.ok(html.includes('<p>null</p>'));
});

test('UI.withLoading gracefully handles rejected promises in finally blocks without corrupting global.document', async () => {
    const orig = global.document;
    let btnState = { textContent: 'Initial', disabled: false };
    global.document = {
        getElementById: () => btnState
    };

    const actionFn = () => Promise.reject(new Error('Action failed'));

    await assert.rejects(
        UI.withLoading('btn', 'Loading...', actionFn),
        { message: 'Action failed' }
    );

    assert.strictEqual(btnState.textContent, 'Initial');
    assert.strictEqual(btnState.disabled, false);

    global.document = orig;
});
