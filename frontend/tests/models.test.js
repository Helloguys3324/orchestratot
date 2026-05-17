const test = require('node:test');
const assert = require('node:assert');
const ModelsPage = require('../js/models.js');

test('ModelsPage renders HTML based on data', async () => {
    // Mock the API dependency
    global.API = {
        getModelsByCategory: async () => ({
            'test-cat': {
                info: { label: 'Test Cat', icon: '🐱' },
                models: [
                    {
                        id: 'm1',
                        name: 'Model One',
                        icon: '1️⃣',
                        tier: 'premium',
                        description: 'A test model',
                        supports_vision: true,
                        supports_tools: false,
                        context_window: '8K',
                        max_output_tokens: 4000,
                        rate_limits: { rpm: 100, tpm: 100000, rpd: null }
                    }
                ]
            }
        })
    };

    let innerHTML = '';
    const container = {
        set innerHTML(val) { innerHTML = val; }
    };

    await ModelsPage.render(container);

    assert.ok(innerHTML.includes('🐱'), 'Should include category icon');
    assert.ok(innerHTML.includes('Test Cat'), 'Should include category label');
    assert.ok(innerHTML.includes('Model One'), 'Should include model name');
    assert.ok(innerHTML.includes('1️⃣'), 'Should include model icon');
    assert.ok(innerHTML.includes('premium'), 'Should include model tier');
    assert.ok(innerHTML.includes('A test model'), 'Should include model description');
    assert.ok(innerHTML.includes('👁️ Vision'), 'Should include vision tag');
    assert.ok(innerHTML.includes('8K ctx'), 'Should include context window');
    assert.ok(innerHTML.includes('4K out'), 'Should include max output tokens formatted');
    assert.ok(innerHTML.includes('100'), 'Should include RPM limit');
    assert.ok(innerHTML.includes('100K'), 'Should include TPM limit formatted');

    // Cleanup
    delete global.API;
});

test('ModelsPage renders null limits and missing features gracefully', async () => {
    // Mock the API dependency
    global.API = {
        getModelsByCategory: async () => ({
            'empty-cat': {
                info: { label: 'Empty Cat', icon: '🐾' },
                models: [
                    {
                        id: 'm2',
                        name: 'Model Two',
                        icon: '2️⃣',
                        tier: 'unknown-tier',
                        description: 'A simple model',
                        supports_vision: false,
                        supports_tools: false,
                        context_window: null,
                        max_output_tokens: null,
                        rate_limits: { rpm: null, tpm: null, rpd: null }
                    }
                ]
            }
        })
    };

    let innerHTML = '';
    const container = {
        set innerHTML(val) { innerHTML = val; }
    };

    await ModelsPage.render(container);

    assert.ok(innerHTML.includes('🐾'), 'Should include category icon');
    assert.ok(innerHTML.includes('Empty Cat'), 'Should include category label');
    assert.ok(innerHTML.includes('Model Two'), 'Should include model name');

    // Limits formatted as '-'
    // Note: The HTML output has '-' in multiple places (RPM, TPM, RPD)
    const dashCount = (innerHTML.match(/>-</g) || []).length;
    assert.ok(dashCount >= 3, 'Should render dashes for null limits');

    // Missing features should not render
    assert.strictEqual(innerHTML.includes('👁️ Vision'), false);
    assert.strictEqual(innerHTML.includes('🔧 Tools'), false);
    assert.strictEqual(innerHTML.includes('ctx'), false);
    assert.strictEqual(innerHTML.includes('out'), false);

    // Cleanup
    delete global.API;
});

test('ModelsPage renders specific limits correctly', async () => {
    global.API = {
        getModelsByCategory: async () => ({
            'test-limits': {
                info: { label: 'Limit Tests', icon: '⚡' },
                models: [
                    {
                        id: 'm3',
                        name: 'Model Three',
                        icon: '3️⃣',
                        tier: 'premium',
                        description: 'Notes and zero limits test',
                        notes: 'Important warning',
                        supports_vision: false,
                        supports_tools: true,
                        context_window: '128K',
                        max_output_tokens: 500,
                        rate_limits: { rpm: 0, tpm: 'Unlimited', rpd: 0 }
                    }
                ]
            }
        })
    };

    let innerHTML = '';
    const container = {
        set innerHTML(val) { innerHTML = val; }
    };

    await ModelsPage.render(container);

    assert.ok(innerHTML.includes('⚡'), 'Should include category icon');
    assert.ok(innerHTML.includes('Limit Tests'), 'Should include category label');
    assert.ok(innerHTML.includes('Model Three'), 'Should include model name');
    assert.ok(innerHTML.includes('Important warning'), 'Should include warning notes');
    assert.ok(innerHTML.includes('🔧 Tools'), 'Should include tools tag');
    assert.ok(innerHTML.includes('500 out'), 'Should include max output tokens unformatted');
    assert.ok(innerHTML.includes('>0<'), 'Should include RPM limit zero');
    assert.ok(innerHTML.includes('Unlimited'), 'Should include string TPM limit');

    delete global.API;
});
