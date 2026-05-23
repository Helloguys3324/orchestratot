const test = require('node:test');
const assert = require('node:assert');

test('AgentsPage.showEditModal works and handles empty agent properties', async () => {
    const AgentsPage = require('../js/agents.js');
    const UI = require('../js/ui.js');

    global.API = {
        getAgent: async () => ({
            id: '1',
            name: 'Agent 1',
            icon: 'A',
            model: 'm1',
            system_prompt: 'prompt',
            temperature: 0.5,
            enabled: true,
            // skills is missing
        }),
        getSkills: async () => [{ id: 's1', name: 'Skill 1', icon: 'S' }],
        getChatModels: async () => [{ id: 'm1', name: 'Model 1' }]
    };

    global.UI = UI;
    global.App = { navigate: () => {} };
    global.window = {
        models: [{ id: 'm1', name: 'Model 1' }]
    };

    const originalDocument = global.document;

    let modalHtml = '';
    global.document = {
        body: {
            insertAdjacentHTML: (position, html) => {
                modalHtml = html;
            }
        }
    };

    await AgentsPage.showEditModal('1');

    assert.ok(modalHtml.includes('value="m1" selected>'));

    global.document = originalDocument;
    delete global.API;
    delete global.UI;
    delete global.App;
    delete global.window;
});
