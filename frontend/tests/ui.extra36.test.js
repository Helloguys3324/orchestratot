const test = require('node:test');
const assert = require('node:assert');

test('UI remaining functions coverage', () => {
    delete require.cache[require.resolve('../js/ui.js')];
    const UI = require('../js/ui.js');

    // Test renderModelOptions
    const models = [
        { id: 'm1', name: 'Model 1', icon: '🤖', rate_limits: { rpm: 10 } },
        { id: 'm2', name: 'Model 2', icon: '🧠', rate_limits: { rpm: null } },
        { id: 'm3', name: 'Model 3', icon: '⚡' }
    ];
    const modelOpts = UI.renderModelOptions(models, 'm2');
    assert.strictEqual(modelOpts.includes('value="m1" >'), true);
    assert.strictEqual(modelOpts.includes('value="m2" selected>'), true);
    assert.strictEqual(modelOpts.includes('value="m3" >'), true);

    // Test renderSkillCheckboxes
    const skills = [
        { id: 's1', name: 'Skill 1', icon: '🛠️' },
        { id: 's2', name: 'Skill 2', icon: '🔧' }
    ];
    const skillChecks = UI.renderSkillCheckboxes(skills, ['s1'], 'custom-class');
    assert.strictEqual(skillChecks.includes('value="s1" checked>'), true);
    assert.strictEqual(skillChecks.includes('value="s2" >'), true);
    assert.strictEqual(skillChecks.includes('class="custom-class"'), true);

    // Test renderEmptyState
    const emptyState = UI.renderEmptyState('🚀', 'Ready', 'Let\'s go!', '<button>Start</button>');
    assert.strictEqual(emptyState.includes('🚀'), true);
    assert.strictEqual(emptyState.includes('Ready'), true);
    assert.strictEqual(emptyState.includes('Let\'s go!'), true);
    assert.strictEqual(emptyState.includes('<button>Start</button>'), true);
});

test('UI DOM functions coverage', async () => {
    delete require.cache[require.resolve('../js/ui.js')];
    const UI = require('../js/ui.js');

    const mockDiv = { textContent: '', style: { display: 'none' } };
    const mockBtn = { textContent: 'Initial', disabled: false };

    global.document = {
        getElementById: (id) => {
            if (id === 'test-err') return mockDiv;
            if (id === 'test-btn') return mockBtn;
            return null;
        }
    };

    // showError
    UI.showError('test-err', 'Error msg');
    assert.strictEqual(mockDiv.textContent, 'Error msg');
    assert.strictEqual(mockDiv.style.display, 'block');

    UI.showError('missing-err', 'Error msg'); // handles null

    // hideError
    UI.hideError('test-err');
    assert.strictEqual(mockDiv.style.display, 'none');

    UI.hideError('missing-err'); // handles null

    // withLoading
    let actionRun = false;
    await UI.withLoading('test-btn', 'Loading...', async () => {
        actionRun = true;
        assert.strictEqual(mockBtn.textContent, 'Loading...');
        assert.strictEqual(mockBtn.disabled, true);
    });
    assert.strictEqual(actionRun, true);
    assert.strictEqual(mockBtn.textContent, 'Initial');
    assert.strictEqual(mockBtn.disabled, false);

    // withLoading error
    try {
        await UI.withLoading('test-btn', 'Loading...', async () => {
            throw new Error('Action failed');
        });
        assert.fail('Should have thrown');
    } catch (err) {
        assert.strictEqual(err.message, 'Action failed');
        assert.strictEqual(mockBtn.textContent, 'Initial');
        assert.strictEqual(mockBtn.disabled, false);
    }

    // withLoading missing button
    await UI.withLoading('missing-btn', 'Loading...', async () => {});

    delete global.document;
});

test('UI window fallback module trick', () => {
    delete require.cache[require.resolve('../js/ui.js')];
    const backupModule = global.module;
    const backupWindow = global.window;

    global.window = {}; // Set window

    // To hit `typeof window !== 'undefined'` check
    // If we require it normally, `typeof module !== 'undefined' && module.exports` hits first.
    // However, in our Node.js environment, `module` is always defined.
    // The only way to hit the `window.UI = UI` line is if the module executes it.
    // The code does:
    // if (typeof module !== 'undefined' && module.exports) { module.exports = UI; }
    // if (typeof window !== 'undefined') { window.UI = UI; } else if (typeof global !== 'undefined') { global.UI = UI; }
    // Both if blocks run!

    require('../js/ui.js');

    assert.ok(global.window.UI);

    global.window = backupWindow;
});
