const test = require('node:test');
const assert = require('node:assert');

test('ui.js fallback: window fallback properly sets window.UI', () => {
    delete require.cache[require.resolve('../js/ui.js')];

    // We want to verify line 70 is covered.
    // The issue is `vm` doesn't register with coverage.
    // So we must manipulate global environment.

    // We need `typeof module !== 'undefined'` to be true (it is).
    // We need `typeof window !== 'undefined'` to be true.

    const originalWindow = global.window;

    // Fake a window object
    global.window = {};

    // In ui.js:
    // if (typeof window !== 'undefined') { window.UI = UI; }
    require('../js/ui.js');

    assert.strictEqual(typeof global.window.UI, 'object');

    global.window = originalWindow;
});

test('ui.js fallback: cover line 72 via require mocking global (no window)', () => {
    delete require.cache[require.resolve('../js/ui.js')];

    // We want to verify line 72 is covered.
    // In ui.js:
    // } else if (typeof global !== 'undefined') { global.UI = UI; }

    // So `window` must be undefined.
    // `global` is already defined in Node.
    const originalWindow = global.window;
    global.window = undefined;

    // global.UI is not defined
    delete global.UI;

    require('../js/ui.js');

    assert.strictEqual(typeof global.UI, 'object');

    global.window = originalWindow;
    delete global.UI;
});

test('ui.js fallback: module is not defined', () => {
    // This is tricky because we can't easily make `module` undefined in Node
    // using normal requires. We'll use vm but it won't trigger coverage correctly
    // However, maybe we don't need it for coverage since the if checks `typeof module !== 'undefined'` which is true,
    // and the `&& module.exports` which is true. Both branches are technically covered for line 66 (the truthy path).
    // What if we test that ui.js doesn't crash in vm?
    const vm = require('vm');
    const fs = require('fs');
    const uiCode = fs.readFileSync('frontend/js/ui.js', 'utf8');
    const sandbox = { window: {} };
    vm.createContext(sandbox);
    vm.runInContext(uiCode, sandbox);
    assert.strictEqual(typeof sandbox.window.UI, 'object');
});
