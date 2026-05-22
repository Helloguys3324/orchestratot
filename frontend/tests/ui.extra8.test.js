const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.showError gracefully handles null element without throwing', () => {
    const orig = global.document;
    global.document = {
        getElementById: () => null
    };

    try {
        UI.showError('nonexistent-error-id', 'Some message');
        assert.ok(true, 'Did not throw');
    } finally {
        global.document = orig;
    }
});

test('UI.hideError gracefully handles null element without throwing', () => {
    const orig = global.document;
    global.document = {
        getElementById: () => null
    };

    try {
        UI.hideError('nonexistent-error-id');
        assert.ok(true, 'Did not throw');
    } finally {
        global.document = orig;
    }
});

test('UI.withLoading gracefully handles null element without throwing', async () => {
    const orig = global.document;
    global.document = {
        getElementById: () => null
    };

    try {
        let actionExecuted = false;
        await UI.withLoading('nonexistent-btn', 'Wait...', async () => {
            actionExecuted = true;
        });
        assert.strictEqual(actionExecuted, true, 'Action was executed despite null element');
    } finally {
        global.document = orig;
    }
});

test('UI.renderModelOptions handles rate_limits being explicitly null', () => {
    const models = [
        { id: 'test-1', name: 'Model Null', icon: 'M', rate_limits: null }
    ];
    const html = UI.renderModelOptions(models);
    assert.ok(html.includes('(0 RPM)'));
});

test('UI.renderSkillCheckboxes handles empty selectedIds and empty arrays without throwing', () => {
    const html1 = UI.renderSkillCheckboxes([]);
    assert.strictEqual(html1, '');

    const html2 = UI.renderSkillCheckboxes([{id: 's1', name: 'S1', icon: 'I'}], undefined, 'test-class');
    assert.ok(html2.includes('value="s1"'));
});
