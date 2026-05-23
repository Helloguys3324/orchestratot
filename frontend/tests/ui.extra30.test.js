const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderModelOptions handles extreme parameter types', () => {
    const models = [
        { id: 'test1', name: 'No RL', icon: 'X' },
        { id: 'test2', name: 'Undefined RPM', icon: 'Y', rate_limits: { rpm: undefined } }
    ];
    const html = UI.renderModelOptions(models);
    assert.ok(html.includes('(0 RPM)'));
    assert.ok(html.includes('value="test1"'));
});

test('UI.renderSkillCheckboxes defaults to unchecked when selectedIds is not passed', () => {
    const skills = [{ id: 's1', name: 'Skill 1', icon: 'S1' }];
    const html = UI.renderSkillCheckboxes(skills);
    assert.ok(html.includes('value="s1"'));
    assert.ok(!html.includes('checked'));
});

test('UI fallback: typeof window !== "undefined"', () => {
    const origWindow = global.window;
    delete require.cache[require.resolve('../js/ui.js')];
    global.window = {};
    const uiModule = require('../js/ui.js');
    assert.strictEqual(global.window.UI, uiModule);
    global.window = origWindow;
    delete require.cache[require.resolve('../js/ui.js')];
});

test('UI fallback: typeof global !== "undefined"', () => {
    const origWindow = global.window;
    const origGlobalUI = global.UI;
    delete require.cache[require.resolve('../js/ui.js')];
    global.window = undefined;
    const uiModule = require('../js/ui.js');
    assert.strictEqual(global.UI, uiModule);
    global.window = origWindow;
    global.UI = origGlobalUI;
    delete require.cache[require.resolve('../js/ui.js')];
});
