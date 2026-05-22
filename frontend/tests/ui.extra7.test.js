const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderModelOptions formats correctly with falsy but not null rpm', () => {
    const models = [
        { id: '1', name: 'Model 1', icon: 'M1', rate_limits: { rpm: 0 } },
        { id: '2', name: 'Model 2', icon: 'M2', rate_limits: { rpm: false } },
        { id: '3', name: 'Model 3', icon: 'M3', rate_limits: { rpm: '' } }
    ];

    const html = UI.renderModelOptions(models);

    assert.ok(html.includes('<option value="1" >M1 Model 1 (0 RPM)</option>'));
    assert.ok(html.includes('<option value="2" >M2 Model 2 (0 RPM)</option>'));
    assert.ok(html.includes('<option value="3" >M3 Model 3 (0 RPM)</option>'));
});
