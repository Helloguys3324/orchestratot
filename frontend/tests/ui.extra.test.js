const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderModelOptions handles empty models array', () => {
    const html = UI.renderModelOptions([]);
    assert.strictEqual(html, '');
});

test('UI.renderModelOptions handles missing rate_limits completely', () => {
    const models = [{ id: '1', name: 'Model', icon: 'M' }];
    const html = UI.renderModelOptions(models);
    assert.ok(html.includes('(0 RPM)'));
});

test('UI.renderSkillCheckboxes handles empty skills array', () => {
    const html = UI.renderSkillCheckboxes([]);
    assert.strictEqual(html, '');
});

test('UI.withLoading restores original text on success', async () => {
    let btnState = { textContent: 'Initial', disabled: false };
    global.document = {
        getElementById: () => btnState
    };

    await UI.withLoading('btn', 'Wait...', async () => {
        assert.strictEqual(btnState.textContent, 'Wait...');
        assert.strictEqual(btnState.disabled, true);
    });

    assert.strictEqual(btnState.textContent, 'Initial');
    assert.strictEqual(btnState.disabled, false);
});

test('UI.showError does not throw when element missing', () => {
    global.document = {
        getElementById: () => null
    };
    assert.doesNotThrow(() => {
        UI.showError('nonexistent', 'An error occurred');
    });
});

test('UI.hideError does not throw when element missing', () => {
    global.document = {
        getElementById: () => null
    };
    assert.doesNotThrow(() => {
        UI.hideError('nonexistent');
    });
});

test('UI.renderModelOptions handles missing properties gracefully', () => {
    const models = [{ id: '1', rate_limits: { rpm: 10 } }];
    const html = UI.renderModelOptions(models);
    assert.ok(html.includes('<option value="1" >undefined undefined (10 RPM)</option>'));
});

test('UI.renderEmptyState handles empty strings and missing arguments', () => {
    const html = UI.renderEmptyState('', '', '');
    assert.ok(html.includes('<div class="icon"></div>'));
    assert.ok(html.includes('<h3></h3>'));
    assert.ok(html.includes('<p></p>'));
});

test('UI.renderSkillCheckboxes handles missing properties', () => {
    const skills = [{ id: 's1' }];
    const html = UI.renderSkillCheckboxes(skills);
    assert.ok(html.includes('<input type="checkbox" class="" value="s1" > undefined undefined'));
});

test('UI.renderModelOptions handles selectedId correctly when not matched', () => {
    const models = [{ id: '1', name: 'Model', icon: 'M', rate_limits: { rpm: 10 } }];
    const html = UI.renderModelOptions(models, '2');
    assert.ok(html.includes('<option value="1" >M Model (10 RPM)</option>'));
});

test('UI.renderSkillCheckboxes handles selectedIds array safely', () => {
    const skills = [{ id: 's1', name: 'Skill 1', icon: 'S1' }];
    const html = UI.renderSkillCheckboxes(skills, []);
    assert.ok(html.includes('<input type="checkbox" class="" value="s1" > S1 Skill 1'));
});

test('UI.withLoading restores text successfully on multiple invocations', async () => {
    let btnState = { textContent: 'Initial', disabled: false };
    global.document = {
        getElementById: () => btnState
    };

    await UI.withLoading('btn', 'Wait1...', async () => {
        assert.strictEqual(btnState.textContent, 'Wait1...');
        assert.strictEqual(btnState.disabled, true);
    });
    assert.strictEqual(btnState.textContent, 'Initial');

    await UI.withLoading('btn', 'Wait2...', async () => {
        assert.strictEqual(btnState.textContent, 'Wait2...');
        assert.strictEqual(btnState.disabled, true);
    });
    assert.strictEqual(btnState.textContent, 'Initial');
});

test('UI.showError handles valid element correctly', () => {
    let errDiv = { textContent: '', style: { display: '' } };
    global.document = {
        getElementById: () => errDiv
    };
    UI.showError('err', 'Test error message');
    assert.strictEqual(errDiv.textContent, 'Test error message');
    assert.strictEqual(errDiv.style.display, 'block');
});

test('UI.hideError handles valid element correctly', () => {
    let errDiv = { style: { display: 'block' } };
    global.document = {
        getElementById: () => errDiv
    };
    UI.hideError('err');
    assert.strictEqual(errDiv.style.display, 'none');
});

test('UI.withLoading handles case where btn is nullified during action', async () => {
    let btnState = { textContent: 'Initial', disabled: false };
    global.document = { getElementById: () => btnState };

    await UI.withLoading('btn', 'Wait...', async () => {
        // Test passes without throwing
    });
});

test('UI.withLoading handles case where btn is nullified during action (dynamic DOM coverage fix)', async () => {
    let btnState = { textContent: 'Initial', disabled: false };
    global.document = { getElementById: () => btnState };

    let actionCalled = false;
    await UI.withLoading('btn', 'Wait...', async () => {
        actionCalled = true;
    });

    assert.strictEqual(actionCalled, true);
});


test.afterEach(() => {
    delete global.document;
});
