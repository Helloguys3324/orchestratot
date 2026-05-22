const test = require('node:test');
const assert = require('node:assert');

test('api.js fallback module export branch', () => {
    // Delete from cache
    delete require.cache[require.resolve('../js/api.js')];

    // Mock module global var state
    const origModule = global.module;
    global.module = undefined;

    // Attempt require and expect it to NOT fail, even if module exports is skipped
    assert.doesNotThrow(() => {
        require('../js/api.js');
    });

    // restore
    global.module = origModule;
    delete require.cache[require.resolve('../js/api.js')];
});
