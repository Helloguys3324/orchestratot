const test = require('node:test');
const assert = require('node:assert');
const ModelsPage = require('../js/models.js');

test('ModelsPage renders with missing optional properties', async () => {
    global.API = {
        getModelsByCategory: async () => ({
            'missing-props': {
                info: { label: 'Missing Props', icon: '❓' },
                models: [
                    {
                        id: 'm4',
                        name: 'Model Four',
                        icon: '4️⃣',
                        tier: 'standard',
                        description: 'A model with missing properties'
                        // No rate_limits, supports_vision, context_window, etc.
                    }
                ]
            }
        })
    };

    let innerHTML = '';
    const container = { set innerHTML(val) { innerHTML = val; } };

    await ModelsPage.render(container);

    assert.ok(innerHTML.includes('Model Four'));
    assert.ok(innerHTML.includes('0</div>')); // Default rpm=0, tpm=0, rpd=0
    assert.ok(innerHTML.includes('0</div>'));
    assert.ok(innerHTML.includes('0</div>'));

    delete global.API;
});

test('ModelsPage renders TPM correctly when numeric', async () => {
    global.API = {
        getModelsByCategory: async () => ({
            'numeric-tpm': {
                info: { label: 'Numeric TPM', icon: '🔢' },
                models: [
                    {
                        id: 'm5',
                        name: 'Model Five',
                        icon: '5️⃣',
                        tier: 'standard',
                        description: 'Numeric TPM',
                        rate_limits: { rpm: 10, tpm: 500, rpd: 100 }
                    }
                ]
            }
        })
    };

    let innerHTML = '';
    const container = { set innerHTML(val) { innerHTML = val; } };

    await ModelsPage.render(container);

    assert.ok(innerHTML.includes('500</div>')); // tpm=500 -> 500

    delete global.API;
});
