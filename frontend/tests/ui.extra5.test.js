const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderModelOptions handles extreme rate limit values', () => {
    const models = [
        { id: '1', name: 'M1', icon: 'i', rate_limits: { rpm: Number.MAX_SAFE_INTEGER } },
        { id: '2', name: 'M2', icon: 'i', rate_limits: { rpm: -100 } }
    ];
    const html = UI.renderModelOptions(models);
    assert.ok(html.includes(`(${Number.MAX_SAFE_INTEGER} RPM)`));
    assert.ok(html.includes(`(-100 RPM)`));
});

test('UI.renderSkillCheckboxes handles number as className', () => {
    const skills = [
        { id: '1', name: 'S1', icon: 'I' }
    ];
    const html = UI.renderSkillCheckboxes(skills, [], 12345);
    assert.ok(html.includes('class="12345"'));
});

test('UI.renderEmptyState handles number as actionHtml', () => {
    const html = UI.renderEmptyState('I', 'T', 'M', 999);
    assert.ok(html.includes('999'));
});

test('UI.withLoading restores state when actionFn throws string', async () => {
    let btnState = { textContent: 'Initial', disabled: false };
    global.document = {
        getElementById: () => btnState
    };

    let caughtErr = null;
    try {
        await UI.withLoading('btn', 'Load...', async () => {
            throw "String Error";
        });
    } catch(e) {
        caughtErr = e;
    }

    assert.strictEqual(caughtErr, "String Error");
    assert.strictEqual(btnState.textContent, 'Initial');
    assert.strictEqual(btnState.disabled, false);

    delete global.document;
});

test('UI.showError handles array as message', () => {
    let errDiv = { textContent: '', style: { display: '' } };
    global.document = {
        getElementById: () => errDiv
    };

    UI.showError('err', ['A', 'B']);
    assert.deepStrictEqual(errDiv.textContent, ['A', 'B']);
    assert.strictEqual(errDiv.style.display, 'block');

    delete global.document;
});
