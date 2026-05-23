const test = require('node:test');
const assert = require('node:assert');
const AgentsPage = require('../js/agents.js');
const UI = require('../js/ui.js');

test('AgentsPage missing enabled truthiness check', async () => {
    global.API = {
        getAgent: async () => ({ id: 'a1', name: 'Agent 1', enabled: false, skills: [] }),
        getChatModels: async () => [],
        getSkills: async () => []
    };

    global.document = {
        getElementById: () => null,
        body: { insertAdjacentHTML: () => {} }
    };
    global.UI = UI;

    let htmlContent = '';
    global.document.body.insertAdjacentHTML = (pos, html) => {
        htmlContent = html;
    };

    await AgentsPage.showEditModal('a1');
    assert.ok(htmlContent.includes('class="toggle "'));

    delete global.API;
    delete global.document;
    delete global.UI;
});
