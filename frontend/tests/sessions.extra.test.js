const test = require('node:test');
const assert = require('node:assert');
const SessionsPage = require('../js/sessions.js');

test('SessionsPage.render handles missing properties', async () => {
    let headerActions = { innerHTML: '' };
    let container = { innerHTML: '' };
    global.API = {
        getSessions: async () => [{
            id: 'sess1',
            name: 'Session 1',
            strategy: 'test',
            agent_ids: ['a1'],
            status: 'running',
            created_at: new Date().toISOString()
        }, {
            id: 'sess2',
            name: 'Session 2',
            strategy: 'test',
            agent_ids: ['a1'],
            status: 'completed',
            created_at: new Date().toISOString()
        }]
    };

    await SessionsPage.render(container, headerActions);
    assert.ok(container.innerHTML.includes('0 msgs'));
    assert.ok(container.innerHTML.includes('tag-warning'));
    assert.ok(container.innerHTML.includes('tag-success'));
    delete global.API;
});
