const test = require('node:test');
const assert = require('node:assert');

test('UI pure function extra utilities', () => {
    delete require.cache[require.resolve('../js/ui.js')];
    const UI = require('../js/ui.js');

    const models = [
        { id: 'm1', name: 'Model A', icon: 'A', rate_limits: { rpm: 50 } },
        { id: 'm2', name: 'Model B', icon: 'B', rate_limits: { rpm: null } },
        { id: 'm3', name: 'Model C', icon: 'C' }
    ];

    const html1 = UI.renderModelOptions(models, 'm2');
    assert.ok(html1.includes('value="m1"'));
    assert.ok(html1.includes('50 RPM'));
    assert.ok(html1.includes('value="m2" selected'));
    assert.ok(html1.includes('- RPM'));
    assert.ok(html1.includes('value="m3"'));
    assert.ok(html1.includes('0 RPM'));

    const skills = [
        { id: 's1', name: 'Skill 1', icon: '1' },
        { id: 's2', name: 'Skill 2', icon: '2' }
    ];

    const html2 = UI.renderSkillCheckboxes(skills, ['s1'], 'custom-class');
    assert.ok(html2.includes('value="s1" checked'));
    assert.ok(html2.includes('value="s2" >'));
    assert.ok(html2.includes('class="custom-class"'));

    const html3 = UI.renderEmptyState('E', 'Empty', 'Msg', '<a>Link</a>');
    assert.ok(html3.includes('<div class="empty-state">'));
    assert.ok(html3.includes('E'));
    assert.ok(html3.includes('Empty'));
    assert.ok(html3.includes('Msg'));
    assert.ok(html3.includes('<a>Link</a>'));
});
