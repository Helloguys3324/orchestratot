const test = require('node:test');
const assert = require('node:assert');

test('ModelsPage handles Node environment without module.exports', () => {
    const originalModule = global.module;
    global.module = undefined; // Force the if condition to fail

    // Evaluate the code using eval
    const fs = require('fs');
    const path = require('path');
    const code = fs.readFileSync(path.join(__dirname, '../js/models.js'), 'utf8');

    eval(code);

    assert.strictEqual(typeof ModelsPage.render, 'function');

    global.module = originalModule;
});
