const test = require('node:test');
const assert = require('node:assert');

test('ModelsPage handles Node environment without module.exports', () => {
    const fs = require('fs');
    const path = require('path');
    let code = fs.readFileSync(path.join(__dirname, '../js/models.js'), 'utf8');

    // Make the locally scoped variable accessible on the context object
    code = code.replace('const ModelsPage =', 'ModelsPage =');

    const context = { module: undefined };
    require('vm').runInNewContext(code, context);

    assert.strictEqual(typeof context.ModelsPage.render, 'function');
});
