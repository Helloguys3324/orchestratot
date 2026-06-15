const test = require('node:test');
const assert = require('node:assert');

test('UI globals fallback module trick', () => {
    delete require.cache[require.resolve('../js/ui.js')];
    delete global.UI;

    global.window = undefined; // Force undefined to ensure we hit branch
    delete global.window;

    require('../js/ui.js');

    assert.ok(global.UI, 'global.UI should be set by the fallback code');
    assert.strictEqual(typeof global.UI.renderModelOptions, 'function');

    delete global.UI;
});

test('UI window fallback module trick', () => {
    delete require.cache[require.resolve('../js/ui.js')];
    delete global.UI;

    global.window = {}; // Mock window environment

    require('../js/ui.js');

    assert.ok(global.window.UI, 'window.UI should be set when window is defined');
    assert.strictEqual(typeof global.window.UI.renderModelOptions, 'function');
    assert.strictEqual(global.UI, undefined);

    delete global.window;
});
