const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

test('App handles Node environment without module.exports', () => {
    const code = fs.readFileSync(path.join(__dirname, '../js/app.js'), 'utf8');

    // Create a new context with module undefined and module.exports undefined
    const sandbox = {
        document: {
            addEventListener: () => {}
        },
        module: undefined
    };

    vm.createContext(sandbox);
    vm.runInContext(code, sandbox);

    // In vm context, const definitions block the global object but they can be evaluated
    const result = vm.runInContext('typeof App.init === "function"', sandbox);

    assert.strictEqual(result, true);
});
