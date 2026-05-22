const test = require('node:test');
const assert = require('node:assert');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');

test('UI module exports correctly when module is defined', () => {
    const code = fs.readFileSync(path.join(__dirname, '../js/ui.js'), 'utf8');
    const sandbox = { module: { exports: {} } };
    vm.createContext(sandbox);
    vm.runInContext(code, sandbox);
    assert.ok(sandbox.module.exports);
    assert.strictEqual(typeof sandbox.module.exports.renderModelOptions, 'function');
});

test('UI module does not error when module is undefined', () => {
    const code = fs.readFileSync(path.join(__dirname, '../js/ui.js'), 'utf8');
    const sandbox = { module: undefined };
    vm.createContext(sandbox);
    assert.doesNotThrow(() => {
        vm.runInContext(code, sandbox);
    });
    // For some reason, variable declaration `const UI` might not become a property of sandbox directly.
    // We can evaluate it inside.
    const hasUI = vm.runInContext('typeof UI === "object"', sandbox);
    assert.strictEqual(hasUI, true);
});
