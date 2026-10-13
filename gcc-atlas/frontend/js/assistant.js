/**
 * AI Research Assistant Module for GCC Atlas
 * Handles chat messaging, suggested prompt chips, citation rendering, and mode badges.
 */

const assistantModule = {
  chatHistory: [],
  isSubmitting: false,

  init() {
    this.setupListeners();
  },

  setupListeners() {
    // Form submit
    const form = document.getElementById('chat-input-form');
    const input = document.getElementById('chat-user-input');
    if (form && input) {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const msg = input.value.trim();
        if (!msg || this.isSubmitting) return;

        input.value = '';
        await this.sendMessage(msg);
      });
    }

    // Suggested prompt chips
    document.querySelectorAll('.prompt-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const prompt = chip.getAttribute('data-prompt');
        if (prompt && !this.isSubmitting) {
          const inputEl = document.getElementById('chat-user-input');
          if (inputEl) inputEl.value = prompt;
          this.sendMessage(prompt);
        }
      });
    });
  },

  formatMarkdown(text) {
    if (!text) return '';
    // Format bold headers
    let html = text
      .replace(/^### (.*$)/gim, '<h4 style="font-size: 15px; font-weight: 700; color: var(--navy-900); margin: 12px 0 6px;">$1</h4>')
      .replace(/^#### (.*$)/gim, '<h5 style="font-size: 14px; font-weight: 700; color: var(--navy-900); margin: 10px 0 4px;">$1</h5>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" class="evidence-link">$1 ↗</a>')
      .replace(/^\s*-\s+(.*$)/gim, '<div style="margin: 3px 0 3px 14px; line-height: 1.4;">• $1</div>')
      .replace(/^\s*\d+\.\s+(.*$)/gim, '<div style="margin: 3px 0 3px 14px; line-height: 1.4;">$1</div>')
      .replace(/\n\n/g, '<br><br>');
    return html;
  },

  async sendMessage(messageText) {
    this.isSubmitting = true;
    const historyBox = document.getElementById('chat-history-box');
    const sendBtn = document.getElementById('chat-send-btn');
    if (sendBtn) sendBtn.disabled = true;

    // 1. Append User Bubble
    const userBubble = document.createElement('div');
    userBubble.className = 'chat-bubble user';
    userBubble.innerHTML = `
      <div class="chat-avatar">U</div>
      <div class="bubble-content">
        ${messageText}
      </div>
    `;
    historyBox.appendChild(userBubble);
    historyBox.scrollTop = historyBox.scrollHeight;

    // 2. Append Loading Assistant Bubble
    const assistantBubble = document.createElement('div');
    assistantBubble.className = 'chat-bubble assistant';
    const loadingId = 'loading-' + Date.now();
    assistantBubble.id = loadingId;
    assistantBubble.innerHTML = `
      <div class="chat-avatar">AI</div>
      <div class="bubble-content" style="display: flex; align-items: center; gap: 8px;">
        <div class="spinner" style="width: 16px; height: 16px;"></div>
        <span style="font-size: 13px; color: var(--navy-600);">Retrieving verified database records...</span>
      </div>
    `;
    historyBox.appendChild(assistantBubble);
    historyBox.scrollTop = historyBox.scrollHeight;

    try {
      const payload = {
        message: messageText,
        history: this.chatHistory.slice(-6)
      };

      const res = await fetch('/api/assistant/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error('Assistant API returned error');
      const data = await res.json();

      // Update badge
      const isLive = !data.is_demo_mode;
      const badgePill = document.getElementById('assistant-badge-pill');
      if (badgePill) {
        badgePill.className = isLive ? 'badge badge-live' : 'badge badge-demo';
        badgePill.innerText = isLive ? 'Live Gemini AI' : 'Rule-Based Demo Mode';
      }

      // Format Citations
      let citationsHtml = '';
      if (data.citations && data.citations.length > 0) {
        citationsHtml = `
          <div class="citations-panel">
            <span class="citations-label">Verified Source Citations (${data.citations.length}):</span>
            <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px;">
              ${data.citations.map(c => `
                <a href="${c.url}" target="_blank" class="citation-chip" title="${c.relevant_fact}">
                  <span>🔗</span>
                  <span>${c.title}</span>
                  <span style="opacity: 0.7;">↗</span>
                </a>
              `).join('')}
            </div>
          </div>
        `;
      }

      // Mode note banner if demo mode
      let modeNoteBanner = '';
      if (data.is_demo_mode) {
        modeNoteBanner = `
          <div style="margin-bottom: 12px; font-size: 11px; background-color: #fff7ed; border: 1px solid #fed7aa; color: #9a3412; padding: 4px 8px; border-radius: 4px; display: inline-flex; align-items: center; gap: 6px;">
            <span>ℹ️</span>
            <span><strong>DEMO MODE:</strong> Synthesized locally from SQLite records. Grounded without external LLM API key.</span>
          </div>
        `;
      }

      // Replace loading bubble content
      assistantBubble.innerHTML = `
        <div class="chat-avatar">AI</div>
        <div class="bubble-content">
          ${modeNoteBanner}
          <div class="bubble-text">
            ${this.formatMarkdown(data.answer)}
          </div>
          ${citationsHtml}
        </div>
      `;

      // Save to conversation history
      this.chatHistory.push({ role: 'user', content: messageText });
      this.chatHistory.push({ role: 'assistant', content: data.answer });

    } catch (err) {
      console.error('Chat request error:', err);
      assistantBubble.innerHTML = `
        <div class="chat-avatar">AI</div>
        <div class="bubble-content" style="color: #dc2626;">
          An error occurred while connecting to the research intelligence engine. Please try again or check your local server status.
        </div>
      `;
    } finally {
      this.isSubmitting = false;
      if (sendBtn) sendBtn.disabled = false;
      historyBox.scrollTop = historyBox.scrollHeight;
    }
  }
};

window.assistantModule = assistantModule;
window.addEventListener('DOMContentLoaded', () => {
  assistantModule.init();
});
