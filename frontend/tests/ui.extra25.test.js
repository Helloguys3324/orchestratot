const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderModelOptions handles explicitly null, 0, and undefined rpm for edge cases', () => {
    const models = [
        { id: '1', name: 'M1', icon: 'I1', rate_limits: { rpm: null } },
        { id: '2', name: 'M2', icon: 'I2', rate_limits: { rpm: 0 } },
        { id: '3', name: 'M3', icon: 'I3', rate_limits: { rpm: undefined } },
        { id: '4', name: 'M4', icon: 'I4', rate_limits: null }
    ];
    const result = UI.renderModelOptions(models);

    assert.ok(result.includes('(- RPM)'));
    const matches = result.match(/\(0 RPM\)/g);
    assert.ok(matches && matches.length === 3);
});

test('UI.renderSkillCheckboxes gracefully handles edge case type mismatches in selectedIds', () => {
    const skills = [
        { id: '12', name: 'S1', icon: 'I1' },
        { id: '1', name: 'S2', icon: 'I2' }
    ];
    // string instead of array
    const result1 = UI.renderSkillCheckboxes(skills, '12');

    const checkedMatches1 = result1.match(/checked/g);
    assert.ok(checkedMatches1 && checkedMatches1.length === 2);

    // empty string
    const result2 = UI.renderSkillCheckboxes(skills, '');
    assert.ok(!result2.includes('checked'));
});

test('UI.showError edge case missing elements', () => {
    const orig = global.document;
    global.document = {
        getElementById: () => null
    };
    try {
        assert.doesNotThrow(() => {
            UI.showError('non-existent', 'msg');
        });
    } finally {
        global.document = orig;
    }
});

test('UI.hideError edge case missing elements', () => {
    const orig = global.document;
    global.document = {
        getElementById: () => null
    };
    try {
        assert.doesNotThrow(() => {
            UI.hideError('non-existent');
        });
    } finally {
        global.document = orig;
    }
});

test('UI.withLoading edge case gracefully handling rejected promises in finally blocks', async () => {
    const orig = global.document;
    const btn = { textContent: 'Initial', disabled: false };
    global.document = {
        getElementById: () => btn
    };

    try {
        await assert.rejects(
            async () => {
                await UI.withLoading('btn-id', 'Loading...', async () => {
                    throw new Error('Action failed edge case');
                });
            },
            Error,
            'Action failed edge case'
        );
        assert.strictEqual(btn.disabled, false);
        assert.strictEqual(btn.textContent, 'Initial');
    } finally {
        global.document = orig;
    }
});
