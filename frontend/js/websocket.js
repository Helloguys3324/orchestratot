// WebSocket client for real-time agent messages
class WS {
  constructor() {
    this.socket = null;
    this.sessionId = null;
    this.listeners = [];
    this.reconnectTimer = null;
  }

  connect(sessionId) {
    this.disconnect();
    this.sessionId = sessionId;
    const proto = location.protocol === 'https:' ? 'wss' : 'ws';
    this.socket = new WebSocket(`${proto}://${location.host}/ws/${sessionId}`);

    this.socket.onopen = () => console.log('[WS] Connected to', sessionId);

    this.socket.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);
        this.listeners.forEach(fn => fn(data));
      } catch (err) {
        console.error('[WS] Parse error:', err);
      }
    };

    this.socket.onclose = () => {
      console.log('[WS] Disconnected');
      this.reconnectTimer = setTimeout(() => {
        if (this.sessionId) this.connect(this.sessionId);
      }, 3000);
    };

    this.socket.onerror = (err) => console.error('[WS] Error:', err);
  }

  disconnect() {
    clearTimeout(this.reconnectTimer);
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
    this.sessionId = null;
  }

  onMessage(fn) {
    this.listeners.push(fn);
  }

  removeListener(fn) {
    this.listeners = this.listeners.filter(l => l !== fn);
  }
}

const ws = new WS();

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { WS, ws };
}
