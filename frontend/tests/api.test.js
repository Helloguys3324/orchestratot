const test = require('node:test');
const assert = require('node:assert');
const API = require('../js/api.js');

test('API client base path is correct', () => {
    assert.strictEqual(API.base, '');
});

test('API request handles successful fetch', async () => {
    global.fetch = async (url, opts) => {
        return {
            ok: true,
            json: async () => ({ success: true })
        };
    };

    const res = await API.request('GET', '/test');
    assert.deepStrictEqual(res, { success: true });
});

test('API request handles fetch with body', async () => {
    let capturedOpts;
    global.fetch = async (url, opts) => {
        capturedOpts = opts;
        return {
            ok: true,
            json: async () => ({ success: true })
        };
    };

    await API.request('POST', '/test', { key: 'value' });
    assert.strictEqual(capturedOpts.method, 'POST');
    assert.strictEqual(capturedOpts.body, '{"key":"value"}');
    assert.strictEqual(capturedOpts.headers['Content-Type'], 'application/json');
});

test('API request handles fetch error with standard detail', async () => {
    global.fetch = async (url, opts) => {
        return {
            ok: false,
            statusText: 'Bad Request',
            json: async () => ({ detail: 'Custom error message' })
        };
    };

    try {
        await API.request('GET', '/test');
        assert.fail('Should have thrown an error');
    } catch (e) {
        assert.strictEqual(e.message, 'Custom error message');
    }
});

test('API request handles fetch error with array detail (pydantic style)', async () => {
    global.fetch = async (url, opts) => {
        return {
            ok: false,
            statusText: 'Unprocessable Entity',
            json: async () => ({
                detail: [
                    { loc: ['body', 'name'], msg: 'Field required' },
                    { loc: ['body', 'age'], msg: 'Must be positive' }
                ]
            })
        };
    };

    try {
        await API.request('POST', '/test');
        assert.fail('Should have thrown an error');
    } catch (e) {
        assert.strictEqual(e.message, 'body.name: Field required\nbody.age: Must be positive');
    }
});

test('API request handles fetch error when json parsing fails', async () => {
    global.fetch = async (url, opts) => {
        return {
            ok: false,
            statusText: 'Internal Server Error',
            json: async () => { throw new Error('Invalid JSON'); }
        };
    };

    try {
        await API.request('GET', '/test');
        assert.fail('Should have thrown an error');
    } catch (e) {
        assert.strictEqual(e.message, 'Internal Server Error');
    }
});

// Clean up mock
test.afterEach(() => {
    delete global.fetch;
});

test('API request throws json detail properly', async () => {
    global.fetch = async (url, opts) => {
        return {
            ok: false,
            statusText: 'Bad Request',
            json: async () => ({ detail: { key: 'value' } })
        };
    };

    try {
        await API.request('GET', '/test');
        assert.fail('Should have thrown an error');
    } catch (e) {
        assert.strictEqual(e.message, '{"key":"value"}');
    }
});

test('API wrapper methods call request correctly', async () => {
    const calls = [];
    const originalRequest = API.request;
    API.request = async (method, path, body) => {
        calls.push({ method, path, body });
        return { success: true };
    };

    await API.getSettings();
    await API.saveSettings({ theme: 'dark' });
    await API.getTemplates();

    await API.getAgents();
    await API.getAgent('a1');
    await API.createAgent({ name: 'Agent1' });
    await API.updateAgent('a1', { name: 'Agent1 Updated' });
    await API.deleteAgent('a1');
    await API.duplicateAgent('a1');

    await API.getModels();
    await API.getModelsByCategory();
    await API.getChatModels();

    await API.getSkills();
    await API.getMarketplace();
    await API.createSkill({ name: 'Skill1' });
    await API.deleteSkill('s1');
    await API.installSkill('http://example.com', 'Skill2');

    await API.getSessions();
    await API.getSession('sess1');
    await API.createSession({ agent_id: 'a1' });
    await API.deleteSession('sess1');
    await API.sendMessage('sess1', 'hello');
    await API.clearSession('sess1');
    await API.getSessionFiles('sess1');

    assert.deepStrictEqual(calls[0], { method: 'GET', path: '/api/settings', body: undefined });
    assert.deepStrictEqual(calls[1], { method: 'POST', path: '/api/settings', body: { theme: 'dark' } });
    assert.deepStrictEqual(calls[2], { method: 'GET', path: '/api/templates', body: undefined });

    assert.deepStrictEqual(calls[3], { method: 'GET', path: '/api/agents', body: undefined });
    assert.deepStrictEqual(calls[4], { method: 'GET', path: '/api/agents/a1', body: undefined });
    assert.deepStrictEqual(calls[5], { method: 'POST', path: '/api/agents', body: { name: 'Agent1' } });
    assert.deepStrictEqual(calls[6], { method: 'PUT', path: '/api/agents/a1', body: { name: 'Agent1 Updated' } });
    assert.deepStrictEqual(calls[7], { method: 'DELETE', path: '/api/agents/a1', body: undefined });
    assert.deepStrictEqual(calls[8], { method: 'POST', path: '/api/agents/a1/duplicate', body: undefined });

    assert.deepStrictEqual(calls[9], { method: 'GET', path: '/api/models', body: undefined });
    assert.deepStrictEqual(calls[10], { method: 'GET', path: '/api/models/categories', body: undefined });
    assert.deepStrictEqual(calls[11], { method: 'GET', path: '/api/models/chat', body: undefined });

    assert.deepStrictEqual(calls[12], { method: 'GET', path: '/api/skills', body: undefined });
    assert.deepStrictEqual(calls[13], { method: 'GET', path: '/api/skills/marketplace', body: undefined });
    assert.deepStrictEqual(calls[14], { method: 'POST', path: '/api/skills', body: { name: 'Skill1' } });
    assert.deepStrictEqual(calls[15], { method: 'DELETE', path: '/api/skills/s1', body: undefined });
    assert.deepStrictEqual(calls[16], { method: 'POST', path: '/api/skills/install', body: { url: 'http://example.com', name: 'Skill2' } });

    assert.deepStrictEqual(calls[17], { method: 'GET', path: '/api/sessions', body: undefined });
    assert.deepStrictEqual(calls[18], { method: 'GET', path: '/api/sessions/sess1', body: undefined });
    assert.deepStrictEqual(calls[19], { method: 'POST', path: '/api/sessions', body: { agent_id: 'a1' } });
    assert.deepStrictEqual(calls[20], { method: 'DELETE', path: '/api/sessions/sess1', body: undefined });
    assert.deepStrictEqual(calls[21], { method: 'POST', path: '/api/sessions/sess1/chat', body: { message: 'hello' } });
    assert.deepStrictEqual(calls[22], { method: 'POST', path: '/api/sessions/sess1/clear', body: undefined });
    assert.deepStrictEqual(calls[23], { method: 'GET', path: '/api/sessions/sess1/files', body: undefined });

    API.request = originalRequest;
});

test('API request handles fetch error with array detail containing plain strings', async () => {
    global.fetch = async (url, opts) => {
        return {
            ok: false,
            statusText: 'Bad Request',
            json: async () => ({
                detail: ['Error 1', 'Error 2']
            })
        };
    };

    try {
        await API.request('POST', '/test');
        assert.fail('Should have thrown an error');
    } catch (e) {
        assert.strictEqual(e.message, 'Error 1\nError 2');
    }
});

test('API request handles fetch error without detail field', async () => {
    global.fetch = async (url, opts) => {
        return {
            ok: false,
            json: async () => ({ other_field: 'something' })
        };
    };

    try {
        await API.request('POST', '/test');
        assert.fail('Should have thrown an error');
    } catch (e) {
        assert.strictEqual(e.message, 'Request failed');
    }
});
