const test = require('node:test');
const assert = require('node:assert');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const UI = require('../js/ui.js');

test('ui.js fallback: module is not defined', () => {
    const uiJsPath = path.join(__dirname, '../js/ui.js');
    const code = fs.readFileSync(uiJsPath, 'utf8');

    // Create a sandbox without 'module'
    const sandbox = {
        console: console,
        document: {}, global: {} // Minimal mock if needed, though ui.js logic mostly defines functions
    };

    vm.createContext(sandbox);

    // Evaluate the code in the sandbox. This should not throw if the fallback is correct.
    vm.runInContext(code, sandbox);

    // Verify UI is available in the sandbox
    assert.ok(sandbox.UI !== undefined || sandbox.global.UI !== undefined);
    assert.strictEqual(typeof (sandbox.UI || sandbox.global.UI).renderModelOptions, 'function');
});

test('UI.renderSkillCheckboxes ignores irrelevant values in selectedIds array', () => {
    const skills = [
        { id: '1', name: 'S1', icon: 'I1' },
        { id: '2', name: 'S2', icon: 'I2' }
    ];

    // selectedIds contains numbers, booleans, objects which shouldn't throw but also shouldn't match '1' or '2'
    const html = UI.renderSkillCheckboxes(skills, [1, true, {}, null, undefined, '3']);

    assert.ok(!html.includes('checked'));
    assert.ok(html.includes('value="1"'));
    assert.ok(html.includes('value="2"'));
});
