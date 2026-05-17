const test = require('node:test');
const assert = require('node:assert');
const { SkillsPage, MarketplacePage } = require('../js/skills.js');

test('SkillsPage.render generates correct HTML', async () => {
    global.API = {
        getSkills: async () => [
            { id: '1', name: 'Skill 1', icon: '🔧', source: 'user', description: 'Desc 1', builtin: false },
            { id: '2', name: 'Skill 2', icon: '⚙️', source: 'system', description: 'Desc 2', builtin: true }
        ]
    };

    let containerHtml = '';
    const container = {
        set innerHTML(val) { containerHtml = val; }
    };

    let headerHtml = '';
    const headerActions = {
        set innerHTML(val) { headerHtml = val; }
    };

    await SkillsPage.render(container, headerActions);

    assert.ok(headerHtml.includes('New Skill'));
    assert.ok(containerHtml.includes('Skill 1'));
    assert.ok(containerHtml.includes('Desc 1'));
    assert.ok(containerHtml.includes('Skill 2'));
    assert.ok(containerHtml.includes('Desc 2'));
    assert.ok(containerHtml.includes('tag-success'));
    assert.ok(containerHtml.includes('Delete'));

    delete global.API;
});

test('MarketplacePage.render generates correct HTML', async () => {
    global.API = {
        getMarketplace: async () => [
            { name: 'Market Skill', icon: '📦', category: 'tools', description: 'Cool skill', author: 'Dev', downloads: 10, url: 'http://example.com' }
        ]
    };

    let containerHtml = '';
    const container = {
        set innerHTML(val) { containerHtml = val; }
    };

    let headerHtml = '';
    const headerActions = {
        set innerHTML(val) { headerHtml = val; }
    };

    await MarketplacePage.render(container, headerActions);

    assert.ok(headerHtml.includes('Install'));
    assert.ok(containerHtml.includes('Market Skill'));
    assert.ok(containerHtml.includes('tools'));
    assert.ok(containerHtml.includes('Dev'));
    assert.ok(containerHtml.includes('10'));

    delete global.API;
});

test('SkillsPage.remove prompts and deletes', async () => {
    let deletedId = null;
    global.API = {
        deleteSkill: async (id) => { deletedId = id; }
    };
    global.confirm = () => true;
    let navigatedTo = null;
    global.App = {
        navigate: (path) => { navigatedTo = path; }
    };

    await SkillsPage.remove('123');

    assert.strictEqual(deletedId, '123');
    assert.strictEqual(navigatedTo, 'skills');

    // Cancel prompt
    global.confirm = () => false;
    deletedId = null;
    await SkillsPage.remove('456');
    assert.strictEqual(deletedId, null);

    delete global.API;
    delete global.confirm;
    delete global.App;
});

test('MarketplacePage.install works', async () => {
    let installedUrl = null;
    global.API = {
        installSkill: async (url, name) => { installedUrl = url; }
    };
    let alertMsg = null;
    global.alert = (msg) => { alertMsg = msg; };

    await MarketplacePage.install('http://test.com', 'Test');
    assert.strictEqual(installedUrl, 'http://test.com');
    assert.strictEqual(alertMsg, 'Skill installed!');

    // Test error
    global.API.installSkill = async () => { throw new Error('fail'); };
    await MarketplacePage.install('http://bad.com', 'Bad');
    assert.strictEqual(alertMsg, 'Install failed: fail');

    delete global.API;
    delete global.alert;
});

test('MarketplacePage.installFromUrl works', async () => {
    global.document = {
        getElementById: (id) => {
            if (id === 'mp-url') return { value: 'http://foo.com' };
            return null;
        }
    };

    let installedUrl = null;
    MarketplacePage.install = async (url) => { installedUrl = url; };

    await MarketplacePage.installFromUrl();
    assert.strictEqual(installedUrl, 'http://foo.com');

    global.document.getElementById = () => ({ value: '' });
    let alertMsg = null;
    global.alert = (msg) => { alertMsg = msg; };

    await MarketplacePage.installFromUrl();
    assert.strictEqual(alertMsg, 'Enter a URL');

    delete global.document;
    delete global.alert;
});

test('SkillsPage.showCreateModal injects modal HTML', () => {
    let insertedHtml = '';
    global.document = {
        body: {
            insertAdjacentHTML: (pos, html) => { insertedHtml = html; }
        }
    };

    SkillsPage.showCreateModal();
    assert.ok(insertedHtml.includes('id="skill-modal"'));
    assert.ok(insertedHtml.includes('Create Skill'));

    delete global.document;
});

test('SkillsPage.create handles validation errors', async () => {
    global.UI = {
        hideError: () => {},
        showError: (id, msg) => { throw new Error(msg); },
        withLoading: async (id, text, fn) => { await fn(); }
    };

    global.document = {
        getElementById: (id) => ({ value: '' })
    };

    try {
        await SkillsPage.create();
        assert.fail('Should have thrown validation error');
    } catch (e) {
        assert.strictEqual(e.message, 'Name, Description, and Python Code are required.');
    }

    delete global.UI;
    delete global.document;
});

test('SkillsPage.create successfully creates skill', async () => {
    let createdData = null;
    let errorHidden = false;
    let loadingCalled = false;
    global.API = {
        createSkill: async (data) => { createdData = data; }
    };
    global.UI = {
        hideError: () => { errorHidden = true; },
        showError: () => {},
        withLoading: async (id, text, fn) => { loadingCalled = true; await fn(); }
    };

    global.document = {
        getElementById: (id) => {
            const vals = {
                'sk-name': { value: 'My Skill' },
                'sk-desc': { value: 'Desc' },
                'sk-code': { value: 'print("hello")' },
                'sk-icon': { value: '✨' },
                'skill-modal': { remove: () => {} }
            };
            return vals[id] || null;
        }
    };

    let navigatedTo = null;
    global.App = {
        navigate: (path) => { navigatedTo = path; }
    };

    await SkillsPage.create();

    assert.strictEqual(errorHidden, true);
    assert.strictEqual(loadingCalled, true);
    assert.deepStrictEqual(createdData, {
        name: 'My Skill',
        icon: '✨',
        description: 'Desc',
        code: 'print("hello")'
    });
    assert.strictEqual(navigatedTo, 'skills');

    delete global.API;
    delete global.UI;
    delete global.document;
    delete global.App;
});

test('SkillsPage.create handles API errors', async () => {
    let errorShown = null;
    global.API = {
        createSkill: async () => { throw new Error('API failed'); }
    };
    global.UI = {
        hideError: () => {},
        showError: (id, msg) => { errorShown = msg; },
        withLoading: async (id, text, fn) => { await fn(); }
    };

    global.document = {
        getElementById: (id) => {
            const vals = {
                'sk-name': { value: 'My Skill' },
                'sk-desc': { value: 'Desc' },
                'sk-code': { value: 'print("hello")' },
                'sk-icon': { value: '' }, // test default fallback
                'skill-modal': null
            };
            return vals[id] || null;
        }
    };

    await SkillsPage.create();

    assert.strictEqual(errorShown, 'API failed');

    delete global.API;
    delete global.UI;
    delete global.document;
});
