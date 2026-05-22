const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderModelOptions handles objects missing typical fields', () => {
    const models = [{ somethingElse: 'value' }];
    const result = UI.renderModelOptions(models);
    assert.ok(result.includes('undefined undefined'));
    assert.ok(result.includes('(0 RPM)'));
});

test('UI.renderSkillCheckboxes handles objects missing typical fields', () => {
    const skills = [{ somethingElse: 'value' }];
    const result = UI.renderSkillCheckboxes(skills);
    assert.ok(result.includes('undefined undefined'));
    assert.ok(result.includes('value="undefined"'));
});

test('UI.withLoading handles a synchronously throwing actionFn gracefully', async () => {
    const orig = global.document;
    const btn = { textContent: 'Initial', disabled: false };
    global.document = {
        getElementById: () => btn
    };

    try {
        await assert.rejects(
            async () => {
                await UI.withLoading('btn', 'Loading...', () => {
                    throw new Error('Sync error');
                });
            },
            Error,
            'Sync error'
        );
        assert.strictEqual(btn.textContent, 'Initial');
        assert.strictEqual(btn.disabled, false);
    } finally {
        global.document = orig;
    }
});
