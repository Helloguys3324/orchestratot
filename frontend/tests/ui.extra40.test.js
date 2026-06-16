const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderModelOptions formats correctly when rate_limits is null or undefined', () => {
    const models = [
        { id: '1', name: 'Model 1', icon: 'M1', rate_limits: null },
        { id: '2', name: 'Model 2', icon: 'M2' }
    ];

    const html = UI.renderModelOptions(models, '2');

    assert.ok(html.includes('<option value="1" >M1 Model 1 (0 RPM)</option>'));
    assert.ok(html.includes('<option value="2" selected>M2 Model 2 (0 RPM)</option>'));
});

test('UI.renderSkillCheckboxes formats correctly without passing selectedIds as an array', () => {
    const skills = [
        { id: 's1', name: 'Skill 1', icon: 'S1' }
    ];

    const html = UI.renderSkillCheckboxes(skills, null, 'my-class');

    assert.ok(html.includes('<input type="checkbox" class="my-class" value="s1" > S1 Skill 1'));
});
