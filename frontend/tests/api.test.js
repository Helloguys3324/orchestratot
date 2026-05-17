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
