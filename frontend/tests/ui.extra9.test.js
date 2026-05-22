const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderModelOptions handles extreme RPM values', () => {
    const models = [
        { id: '1', name: 'M1', icon: 'I1', rate_limits: { rpm: Infinity } },
        { id: '2', name: 'M2', icon: 'I2', rate_limits: { rpm: NaN } },
        { id: '3', name: 'M3', icon: 'I3', rate_limits: { rpm: -1 } },
        { id: '4', name: 'M4', icon: 'I4', rate_limits: { rpm: '' } }
    ];
    const html = UI.renderModelOptions(models);
    assert.ok(html.includes('(Infinity RPM)'));
    assert.ok(html.includes('(0 RPM)'));
    assert.ok(html.includes('(-1 RPM)'));
    assert.ok(html.includes('(0 RPM)'));
});

test('UI.renderEmptyState handles undefined arguments safely', () => {
    const html = UI.renderEmptyState(undefined, undefined, undefined, undefined);
    assert.ok(html.includes('<div class="icon">undefined</div>'));
    assert.ok(html.includes('<h3>undefined</h3>'));
    assert.ok(html.includes('<p>undefined</p>'));
});

test('UI.withLoading handles button element with missing textContent and disabled properties', async () => {
    const orig = global.document;
    const btn = {};
    global.document = {
        getElementById: () => btn
    };

    try {
        let executed = false;
        await UI.withLoading('btn', 'Loading...', async () => {
            executed = true;
            assert.strictEqual(btn.textContent, 'Loading...');
            assert.strictEqual(btn.disabled, true);
        });
        assert.strictEqual(executed, true);
        assert.strictEqual(btn.textContent, undefined);
        assert.strictEqual(btn.disabled, false);
    } finally {
        global.document = orig;
    }
});

test('UI.showError throws TypeError when element is missing style object', () => {
    const orig = global.document;
    global.document = {
        getElementById: () => ({ textContent: '' })
    };

    try {
        assert.throws(() => UI.showError('err', 'msg'), TypeError);
    } finally {
        global.document = orig;
    }
});

test('UI.hideError throws TypeError when element is missing style object', () => {
    const orig = global.document;
    global.document = {
        getElementById: () => ({})
    };

    try {
        assert.throws(() => UI.hideError('err'), TypeError);
    } finally {
        global.document = orig;
    }
});

test('UI.renderSkillCheckboxes throws TypeError when selectedIds is explicitly null', () => {
    const skills = [{ id: 's1', name: 'S1', icon: 'I1' }];
    assert.throws(() => UI.renderSkillCheckboxes(skills, null), TypeError);
});
