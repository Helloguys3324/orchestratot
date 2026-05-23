const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderModelOptions handles extreme parameter types', () => {
    // Falsy inputs, NaN, Arrays
    const result1 = UI.renderModelOptions([{}], NaN);
    assert.ok(result1.includes('value="undefined"'));
});

test('UI.renderSkillCheckboxes handles extreme parameter types', () => {
    const result = UI.renderSkillCheckboxes([{id: NaN}], [NaN], false);
    assert.ok(result.includes('class="false"'));
});

test('UI.renderEmptyState handles extreme parameter types', () => {
    const result = UI.renderEmptyState(false, 0, NaN, []);
    assert.ok(result.includes('<div class="icon">false</div>'));
    assert.ok(result.includes('<h3>0</h3>'));
    assert.ok(result.includes('<p>NaN</p>'));
});
