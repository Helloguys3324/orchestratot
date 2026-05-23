const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderEmptyState covers the default actionHtml param', () => {
    const html = UI.renderEmptyState('I', 'T', 'M');
    assert.ok(html.includes('<div class="empty-state">'));
});

test('UI.showError covers missing element', () => {
    global.document = { getElementById: () => null };
    UI.showError('non-existent', 'msg'); // Should not throw
    delete global.document;
});

test('UI.hideError covers missing element', () => {
    global.document = { getElementById: () => null };
    UI.hideError('non-existent'); // Should not throw
    delete global.document;
});

test('UI.withLoading covers missing element', async () => {
    global.document = { getElementById: () => null };
    let called = false;
    await UI.withLoading('non-existent', 'loading', async () => { called = true; });
    assert.strictEqual(called, true);
    delete global.document;
});

test('UI fallback: typeof window !== "undefined" without UI defined', () => {
    const origWindow = global.window;
    delete require.cache[require.resolve('../js/ui.js')];
    global.window = {};
    const uiModule = require('../js/ui.js');
    assert.strictEqual(global.window.UI, uiModule);
    global.window = origWindow;
    delete require.cache[require.resolve('../js/ui.js')];
});
