const test = require('node:test');
const assert = require('node:assert');

test('App.js module.exports branch coverage', () => {
    // Clear cache to re-require app.js
    delete require.cache[require.resolve('../js/app.js')];

    // Test the typeof document !== 'undefined' branch with document = undefined
    const originalDocument = global.document;
    global.document = undefined;

    // Require app.js, which should NOT add an event listener because document is undefined
    const App = require('../js/app.js');

    assert.ok(App.init);

    global.document = originalDocument;
});
