const test = require('node:test');
const assert = require('node:assert');

test('ui.js fallback: cover line 70 via require mocking window', () => {
  const origWindow = global.window;
  delete require.cache[require.resolve('../js/ui.js')];

  // Create window object
  global.window = {};

  // Require triggers module.exports AND window.UI = UI
  const UI = require('../js/ui.js');

  assert.ok(global.window.UI === UI);

  // Cleanup
  global.window = origWindow;
  delete require.cache[require.resolve('../js/ui.js')];
});

test('ui.js fallback: cover line 72 via require mocking global (no window)', () => {
  const origWindow = global.window;
  delete require.cache[require.resolve('../js/ui.js')];

  // Ensure window is undefined
  global.window = undefined;

  // Require triggers module.exports AND global.UI = UI
  const UI = require('../js/ui.js');

  assert.ok(global.UI === UI);

  // Cleanup
  global.window = origWindow;
  delete require.cache[require.resolve('../js/ui.js')];
});
