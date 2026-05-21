const test = require('node:test');
const assert = require('node:assert');
const { SkillsPage, MarketplacePage } = require('../js/skills.js');

test('SkillsPage.remove handles unconfirmed prompt', async () => {
    let navigatedTo = null;
    let deletedId = null;
    global.App = { navigate: async (path) => { navigatedTo = path; } };
    global.API = { deleteSkill: async (id) => { deletedId = id; } };
    global.confirm = () => false;

    await SkillsPage.remove('s1');

    assert.strictEqual(deletedId, null);
    assert.strictEqual(navigatedTo, null);

    delete global.App;
    delete global.API;
    delete global.confirm;
});

test('MarketplacePage.install handles errors', async () => {
    let alertMsg = null;
    global.alert = (msg) => { alertMsg = msg; };
    global.API = {
        installSkill: async () => { throw new Error('API Error'); }
    };

    await MarketplacePage.install('http://bad.com', 'Bad');

    assert.ok(alertMsg.includes('API Error'));

    delete global.alert;
    delete global.API;
});

test('MarketplacePage.installFromUrl handles empty input', async () => {
    let alertMsg = null;
    global.alert = (msg) => { alertMsg = msg; };
    global.document = {
        getElementById: () => ({ value: '   ' })
    };

    await MarketplacePage.installFromUrl();

    assert.ok(alertMsg.includes('Enter a URL'));

    delete global.alert;
    delete global.document;
});
