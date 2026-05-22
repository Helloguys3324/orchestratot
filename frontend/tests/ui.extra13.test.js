const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.withLoading handles non-function actionFn gracefully by restoring button state and propagating error', async () => {
    const orig = global.document;
    const btn = { textContent: 'Original', disabled: false };
    global.document = {
        getElementById: () => btn
    };

    try {
        await assert.rejects(
            async () => {
                await UI.withLoading('btnId', 'Loading...', null);
            },
            TypeError
        );
        assert.strictEqual(btn.textContent, 'Original');
        assert.strictEqual(btn.disabled, false);
    } finally {
        global.document = orig;
    }
});

test('UI.renderModelOptions throws TypeError when models is not an array', () => {
    assert.throws(() => {
        UI.renderModelOptions(null);
    }, TypeError);
});

test('UI.renderSkillCheckboxes throws TypeError when skills is not an array', () => {
    assert.throws(() => {
        UI.renderSkillCheckboxes(null);
    }, TypeError);
});

test('UI.renderEmptyState interpolates HTML strings correctly without escaping', () => {
    const html = UI.renderEmptyState('<span>icon</span>', '<b>Title</b>', '<i>msg</i>', '<button>Act</button>');
    assert.ok(html.includes('<span>icon</span>'));
    assert.ok(html.includes('<b>Title</b>'));
    assert.ok(html.includes('<i>msg</i>'));
    assert.ok(html.includes('<button>Act</button>'));
});
