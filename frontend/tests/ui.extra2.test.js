const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderModelOptions formats correctly with null rpm', () => {
    const models = [
        { id: '1', name: 'Model 1', icon: 'M1', rate_limits: { rpm: null } }
    ];

    const html = UI.renderModelOptions(models);
    assert.ok(html.includes('(- RPM)'));
});

test('UI.renderModelOptions formats correctly with falsy rpm', () => {
    const models = [
        { id: '1', name: 'Model 1', icon: 'M1', rate_limits: { rpm: 0 } },
        { id: '2', name: 'Model 2', icon: 'M2', rate_limits: { rpm: false } },
        { id: '3', name: 'Model 3', icon: 'M3', rate_limits: { rpm: '' } }
    ];

    const html = UI.renderModelOptions(models);
    assert.ok(html.includes('(0 RPM)')); // Covers all falsy cases for fallback to 0
});
