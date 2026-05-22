const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderModelOptions handles models with missing properties gracefully', () => {
    const models = [{}];
    const result = UI.renderModelOptions(models);
    assert.ok(result.includes('undefined undefined'));
    assert.ok(result.includes('(0 RPM)'));
});

test('UI.renderSkillCheckboxes handles skills with missing properties gracefully', () => {
    const skills = [{}];
    const result = UI.renderSkillCheckboxes(skills);
    assert.ok(result.includes('undefined undefined'));
    assert.ok(result.includes('value="undefined"'));
});

test('UI.showError handles element missing textContent property gracefully', () => {
    const orig = global.document;
    const errDiv = { style: {} }; // no textContent
    global.document = {
        getElementById: () => errDiv
    };
    try {
        UI.showError('err-id', 'An error occurred');
        assert.strictEqual(errDiv.textContent, 'An error occurred');
        assert.strictEqual(errDiv.style.display, 'block');
    } finally {
        global.document = orig;
    }
});

test('UI.withLoading handles missing btnId when actionFn throws an error', async () => {
    const orig = global.document;
    global.document = {
        getElementById: () => null
    };

    try {
        await assert.rejects(
            async () => {
                await UI.withLoading('non-existent-btn', 'Loading...', async () => {
                    throw new Error('Action failed');
                });
            },
            Error,
            'Action failed'
        );
    } finally {
        global.document = orig;
    }
});
