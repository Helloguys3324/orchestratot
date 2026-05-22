const test = require('node:test');
const assert = require('node:assert');
const UI = require('../js/ui.js');

test('UI.renderEmptyState correctly interpolates values and handles missing actionHtml', () => {
    const icon = '<svg>icon</svg>';
    const title = 'Empty state title';
    const message = 'There are no items to display.';
    const result = UI.renderEmptyState(icon, title, message);

    assert.ok(result.includes('<div class="empty-state">'));
    assert.ok(result.includes('<div class="icon"><svg>icon</svg></div>'));
    assert.ok(result.includes('<h3>Empty state title</h3>'));
    assert.ok(result.includes('<p>There are no items to display.</p>'));
});

test('UI.hideError throws TypeError when element lacks style property', () => {
    const orig = global.document;
    const errDiv = { }; // no style property
    global.document = {
        getElementById: () => errDiv
    };
    try {
        assert.throws(() => {
            UI.hideError('err-id');
        }, TypeError);
    } finally {
        global.document = orig;
    }
});

test('UI.withLoading handles button disabled property correctly when resolving', async () => {
    const orig = global.document;
    const btn = { textContent: 'Initial', disabled: false };
    global.document = {
        getElementById: () => btn
    };

    let isCalled = false;

    try {
        await UI.withLoading('btn-id', 'Loading...', async () => {
            assert.strictEqual(btn.disabled, true);
            assert.strictEqual(btn.textContent, 'Loading...');
            isCalled = true;
        });
        assert.strictEqual(btn.disabled, false);
        assert.strictEqual(btn.textContent, 'Initial');
        assert.strictEqual(isCalled, true);
    } finally {
        global.document = orig;
    }
});
