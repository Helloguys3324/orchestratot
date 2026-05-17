const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderModelOptions formats correctly', () => {
    const models = [
        { id: '1', name: 'Model 1', icon: 'M1', rate_limits: { rpm: 10 } },
        { id: '2', name: 'Model 2', icon: 'M2', rate_limits: { rpm: null } },
        { id: '3', name: 'Model 3', icon: 'M3' }
    ];

    const html = UI.renderModelOptions(models, '2');

    assert.ok(html.includes('<option value="1" >M1 Model 1 (10 RPM)</option>'));
    assert.ok(html.includes('<option value="2" selected>M2 Model 2 (- RPM)</option>'));
    assert.ok(html.includes('<option value="3" >M3 Model 3 (0 RPM)</option>'));
});

test('UI.renderSkillCheckboxes formats correctly', () => {
    const skills = [
        { id: 's1', name: 'Skill 1', icon: 'S1' },
        { id: 's2', name: 'Skill 2', icon: 'S2' }
    ];

    const html = UI.renderSkillCheckboxes(skills, ['s2'], 'my-class');

    assert.ok(html.includes('<input type="checkbox" class="my-class" value="s1" > S1 Skill 1'));
    assert.ok(html.includes('<input type="checkbox" class="my-class" value="s2" checked> S2 Skill 2'));
});

test('UI.renderEmptyState formats correctly', () => {
    const html = UI.renderEmptyState('ICON', 'Title', 'Message', '<button>Action</button>');

    assert.ok(html.includes('<div class="icon">ICON</div>'));
    assert.ok(html.includes('<h3>Title</h3>'));
    assert.ok(html.includes('<p>Message</p>'));
    assert.ok(html.includes('<button>Action</button>'));
});

test('UI.showError manipulates DOM correctly', () => {
    let textContent = '';
    let display = '';
    global.document = {
        getElementById: (id) => {
            if (id === 'err') {
                return {
                    set textContent(val) { textContent = val; },
                    style: {
                        set display(val) { display = val; }
                    }
                };
            }
            return null;
        }
    };

    UI.showError('err', 'An error occurred');
    assert.strictEqual(textContent, 'An error occurred');
    assert.strictEqual(display, 'block');

    UI.showError('nonexistent', 'Error');
});

test('UI.hideError manipulates DOM correctly', () => {
    let display = 'block';
    global.document = {
        getElementById: (id) => {
            if (id === 'err') {
                return {
                    style: {
                        set display(val) { display = val; }
                    }
                };
            }
            return null;
        }
    };

    UI.hideError('err');
    assert.strictEqual(display, 'none');

    UI.hideError('nonexistent');
});

test('UI.withLoading handles button state and awaits action', async () => {
    let textContent = 'Submit';
    let disabled = false;
    global.document = {
        getElementById: (id) => {
            if (id === 'btn') {
                return {
                    get textContent() { return textContent; },
                    set textContent(val) { textContent = val; },
                    get disabled() { return disabled; },
                    set disabled(val) { disabled = val; }
                };
            }
            return null;
        }
    };

    let actionCalled = false;
    const actionFn = async () => {
        actionCalled = true;
        assert.strictEqual(textContent, 'Loading...');
        assert.strictEqual(disabled, true);
    };

    await UI.withLoading('btn', 'Loading...', actionFn);

    assert.strictEqual(global.document.getElementById('other'), null);

    assert.strictEqual(actionCalled, true);
    assert.strictEqual(textContent, 'Submit');
    assert.strictEqual(disabled, false);
});

test('UI.withLoading handles button state and awaits action even with errors', async () => {
    let textContent = 'Submit';
    let disabled = false;
    global.document = {
        getElementById: (id) => {
            if (id === 'btn') {
                return {
                    get textContent() { return textContent; },
                    set textContent(val) { textContent = val; },
                    get disabled() { return disabled; },
                    set disabled(val) { disabled = val; }
                };
            }
            return null;
        }
    };

    let actionCalled = false;
    const actionFn = async () => {
        actionCalled = true;
        assert.strictEqual(textContent, 'Loading...');
        assert.strictEqual(disabled, true);
        throw new Error('Test error');
    };

    await assert.rejects(
        UI.withLoading('btn', 'Loading...', actionFn),
        { message: 'Test error' }
    );

    assert.strictEqual(global.document.getElementById('other'), null);

    assert.strictEqual(actionCalled, true);
    assert.strictEqual(textContent, 'Submit');
    assert.strictEqual(disabled, false);
});

test('UI.withLoading handles non-existent button safely', async () => {
    global.document = {
        getElementById: () => null
    };

    let actionCalled = false;
    const actionFn = async () => {
        actionCalled = true;
    };

    await UI.withLoading('btn', 'Loading...', actionFn);

    assert.strictEqual(actionCalled, true);
});

// Restore document object just in case
test.afterEach(() => {
    delete global.document;
});

test('UI.renderEmptyState formats correctly without actionHtml', () => {
    const html = UI.renderEmptyState('ICON', 'Title', 'Message');
    assert.ok(html.includes('<div class="icon">ICON</div>'));
    assert.ok(html.includes('<h3>Title</h3>'));
    assert.ok(html.includes('<p>Message</p>'));
});

test('UI.renderSkillCheckboxes formats correctly without selectedIds or className', () => {
    const skills = [
        { id: 's1', name: 'Skill 1', icon: 'S1' }
    ];

    const html = UI.renderSkillCheckboxes(skills);

    assert.ok(html.includes('<input type="checkbox" class="" value="s1" > S1 Skill 1'));
});

test('UI.renderModelOptions formats correctly without selectedId', () => {
    const models = [
        { id: '1', name: 'Model 1', icon: 'M1', rate_limits: { rpm: 10 } }
    ];

    const html = UI.renderModelOptions(models);

    assert.ok(html.includes('<option value="1" >M1 Model 1 (10 RPM)</option>'));
});
