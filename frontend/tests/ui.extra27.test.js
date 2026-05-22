const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderEmptyState gracefully renders null properties as strings', () => {
    const result = UI.renderEmptyState(null, null, null, null);
    assert.ok(result.includes('<div class="icon">null</div>'));
    assert.ok(result.includes('<h3>null</h3>'));
    assert.ok(result.includes('<p>null</p>'));
});

test('UI.renderModelOptions gracefully renders null properties', () => {
    const models = [{ id: null, name: null, icon: null, rate_limits: null }];
    const result = UI.renderModelOptions(models, null);
    assert.ok(result.includes('value="null"'));
    assert.ok(result.includes('selected>null null (0 RPM)'));
});

test('UI.renderSkillCheckboxes gracefully renders null properties', () => {
    const skills = [{ id: null, name: null, icon: null }];
    const result = UI.renderSkillCheckboxes(skills, [null], null);
    assert.ok(result.includes('value="null"'));
    assert.ok(result.includes('class="null"'));
    assert.ok(result.includes('checked> null null'));
});
