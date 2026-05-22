const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderModelOptions handles selectedId matching by value but not strictly', () => {
    const models = [
        { id: 123, name: 'M1', icon: 'I1', rate_limits: { rpm: 10 } }
    ];
    // This tests if selectedId === m.id behaves as expected (strict equality)
    const html1 = UI.renderModelOptions(models, '123'); // Should NOT be selected
    assert.ok(!html1.includes('selected'));

    const html2 = UI.renderModelOptions(models, 123); // SHOULD be selected
    assert.ok(html2.includes('selected'));
});

test('UI.renderSkillCheckboxes handles selectedIds array safely when no class name is provided', () => {
    const skills = [
        { id: '1', name: 'S1', icon: 'I1' }
    ];
    const html = UI.renderSkillCheckboxes(skills, ['1']); // missing className
    assert.ok(html.includes('class=""'));
});

test('UI.withLoading handles finally block gracefully when button properties are read-only', async () => {
    const orig = global.document;
    const btn = {
        get textContent() { return 'Initial'; },
        set textContent(v) { /* ignore */ },
        get disabled() { return false; },
        set disabled(v) { /* ignore */ }
    };
    global.document = {
        getElementById: () => btn
    };

    try {
        let executed = false;
        await UI.withLoading('btn', 'Loading...', async () => {
            executed = true;
        });
        assert.strictEqual(executed, true);
    } finally {
        global.document = orig;
    }
});
