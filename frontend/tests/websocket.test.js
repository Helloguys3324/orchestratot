const test = require('node:test');
const assert = require('node:assert');
const { WS } = require('../js/websocket.js');

test('WS connects and handles messages', (t) => {
    // Mock location and WebSocket
    global.location = { protocol: 'http:', host: 'localhost:8000' };

    let wsInstance = null;
    class MockWebSocket {
        constructor(url) {
            this.url = url;
            wsInstance = this;
        }
        close() {}
    }
    global.WebSocket = MockWebSocket;

    const ws = new WS();
    ws.connect('session-123');

    assert.ok(wsInstance !== null);
    assert.strictEqual(wsInstance.url, 'ws://localhost:8000/ws/session-123');

    // Test onMessage listener
    let receivedData = null;
    const listener = (data) => { receivedData = data; };
    ws.onMessage(listener);

    // Simulate message event
    wsInstance.onmessage({ data: JSON.stringify({ message: 'hello' }) });

    assert.deepStrictEqual(receivedData, { message: 'hello' });

    // Test removeListener
    ws.removeListener(listener);
    receivedData = null;
    wsInstance.onmessage({ data: JSON.stringify({ message: 'hello again' }) });

    assert.strictEqual(receivedData, null); // Shouldn't be called after removed

    // Cleanup
    delete global.location;
    delete global.WebSocket;
});

test('WS handles disconnect correctly', (t) => {
    // Mock location and WebSocket
    global.location = { protocol: 'https:', host: 'example.com' };

    let closeCalled = false;
    class MockWebSocket {
        constructor(url) {
            this.url = url;
        }
        close() { closeCalled = true; }
    }
    global.WebSocket = MockWebSocket;

    const ws = new WS();
    ws.connect('session-123');
    ws.disconnect();

    assert.strictEqual(closeCalled, true);
    assert.strictEqual(ws.socket, null);
    assert.strictEqual(ws.sessionId, null);

    // Cleanup
    delete global.location;
    delete global.WebSocket;
});

test('WS auto-reconnects on close', (t) => {
    return new Promise((resolve) => {
        global.location = { protocol: 'http:', host: 'localhost:8000' };

        let connectCalls = 0;
        class MockWebSocket {
            constructor(url) {
                this.url = url;
                connectCalls++;
            }
            close() {}
        }
        global.WebSocket = MockWebSocket;

        const ws = new WS();
        // Mock the global setTimeout to trigger immediately
        const originalSetTimeout = global.setTimeout;
        global.setTimeout = (cb) => {
            cb();
            // Restore everything and resolve
            assert.strictEqual(connectCalls, 2);
            global.setTimeout = originalSetTimeout;
            delete global.location;
            delete global.WebSocket;
            resolve();
        };

        ws.connect('session-123');
        assert.strictEqual(connectCalls, 1);

        // Simulate close to trigger reconnect
        ws.socket.onclose();
    });
});

test('WS handles JSON parse errors silently', (t) => {
    global.location = { protocol: 'http:', host: 'localhost:8000' };

    let wsInstance = null;
    class MockWebSocket {
        constructor(url) {
            this.url = url;
            wsInstance = this;
        }
        close() {}
    }
    global.WebSocket = MockWebSocket;

    const ws = new WS();
    ws.connect('session-123');

    let listenerCalled = false;
    ws.onMessage(() => { listenerCalled = true; });

    const origConsoleError = console.error;
    let errorLogged = false;
    console.error = () => { errorLogged = true; };

    wsInstance.onmessage({ data: 'invalid json' });

    assert.strictEqual(listenerCalled, false);
    assert.strictEqual(errorLogged, true);

    console.error = origConsoleError;
    delete global.location;
    delete global.WebSocket;
});

test('WS handles onerror', (t) => {
    global.location = { protocol: 'http:', host: 'localhost:8000' };

    let wsInstance = null;
    class MockWebSocket {
        constructor(url) {
            this.url = url;
            wsInstance = this;
        }
        close() {}
    }
    global.WebSocket = MockWebSocket;

    const ws = new WS();
    ws.connect('session-123');

    const origConsoleError = console.error;
    let errorLogged = false;
    console.error = () => { errorLogged = true; };

    wsInstance.onerror(new Error('test error'));

    assert.strictEqual(errorLogged, true);

    console.error = origConsoleError;
    delete global.location;
    delete global.WebSocket;
});

test('WS handles onopen', (t) => {
    global.location = { protocol: 'http:', host: 'localhost:8000' };

    let wsInstance = null;
    class MockWebSocket {
        constructor(url) {
            this.url = url;
            wsInstance = this;
        }
        close() {}
    }
    global.WebSocket = MockWebSocket;

    const ws = new WS();
    ws.connect('session-123');

    const origConsoleLog = console.log;
    let logged = false;
    console.log = () => { logged = true; };

    wsInstance.onopen();

    assert.strictEqual(logged, true);

    console.log = origConsoleLog;
    delete global.location;
    delete global.WebSocket;
});
