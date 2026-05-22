const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('ui.js fallback: cover line 70 via require mocking window with global fallback', () => {
  const origWindow = global.window;
  const origGlobalUI = global.UI;
  delete require.cache[require.resolve('../js/ui.js')];

  // We want to test the `if (typeof global !== 'undefined')` branch
  // without `typeof window !== 'undefined'`.
  // `global` is an object in Node.
  global.window = undefined;

  const UI = require('../js/ui.js');

  assert.ok(global.UI === UI);

  // Cleanup
  global.window = origWindow;
  global.UI = origGlobalUI;
  delete require.cache[require.resolve('../js/ui.js')];
});

test('ui.js fallback: window fallback properly sets window.UI', () => {
    const origWindow = global.window;
    delete require.cache[require.resolve('../js/ui.js')];

    global.window = {};
    const UI = require('../js/ui.js');

    assert.ok(global.window.UI === UI);

    global.window = origWindow;
    delete require.cache[require.resolve('../js/ui.js')];
});
