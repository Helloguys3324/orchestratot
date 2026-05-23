const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderModelOptions handles empty models array', () => {
    const html = UI.renderModelOptions([]);
    assert.strictEqual(html, '');
});

test('UI.renderSkillCheckboxes handles empty skills array', () => {
    const html = UI.renderSkillCheckboxes([]);
    assert.strictEqual(html, '');
});

test('UI.renderEmptyState handles missing parameters with defaults', () => {
    const html = UI.renderEmptyState('icon', 'title', 'message');
    assert.ok(html.includes('<div class="empty-state">'));
    assert.ok(!html.includes('undefined'));
});
