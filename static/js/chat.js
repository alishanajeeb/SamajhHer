// ── SamajhHer Chat Engine ──────────────────────────────────────────────────
// Used by all 3 flow pages: woman, family, doctor

requireAuth();
setNavUser();

let currentFlow         = 'woman';
let currentConversationId = null;
let currentLang         = getLang();
window.currentMessages  = [];
let isTyping            = false;

// ── Initialize chat ────────────────────────────────────────────────────────
async function initChat(flow) {
    currentFlow = flow;
    currentLang = getLang();
    await startNewChat();
}

// ── Start new conversation ─────────────────────────────────────────────────
async function startNewChat() {
    const messagesEl = document.getElementById('chatMessages');
    messagesEl.innerHTML = '';
    window.currentMessages = [];

    // Show loading
    messagesEl.innerHTML = `
      <div style="text-align:center;color:#c0b0d0;font-size:13px;padding:20px">
        <div class="typing-bubble" style="margin:0 auto">
          <div class="td"></div><div class="td"></div><div class="td"></div>
        </div>
        <div style="margin-top:10px">Tayari ho rahi hai...</div>
      </div>
    `;

    const res = await apiStartConversation(currentFlow, currentLang);

    if (!res || !res.ok) {
        messagesEl.innerHTML = '<div style="color:#c04060;font-size:13px;padding:20px">Connection error. Please refresh.</div>';
        return;
    }

    currentConversationId = res.data.conversation_id;
    messagesEl.innerHTML  = '';

    // Show welcome message
    const welcome = res.data.welcome_message;
    window.currentMessages = [{ role: 'ai', text: welcome }];
    appendMessage('ai', welcome);

    // Focus input
    document.getElementById('chatInput').focus();
}

// ── Send message ───────────────────────────────────────────────────────────
async function sendMessage() {
    const input   = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    const text    = input.value.trim();

    if (!text || isTyping) return;
    if (!currentConversationId) { await startNewChat(); return; }

    // Clear input
    input.value = '';
    input.style.height = 'auto';

    // Add user message to UI
    window.currentMessages.push({ role: 'user', text });
    appendMessage('user', text);

    // Show typing indicator
    isTyping = true;
    sendBtn.disabled = true;
    showTyping();

    // Send to API
    const res = await apiSendMessage(currentConversationId, text);

    // Remove typing indicator
    hideTyping();
    isTyping    = false;
    sendBtn.disabled = false;

    if (!res || !res.ok) {
        appendMessage('ai', 'Maafi chahti hun, connection mein masla aa gaya. Dobara koshish karein. 🙏');
        return;
    }

    const aiResponse = res.data.response;
    window.currentMessages.push({ role: 'ai', text: aiResponse });
    appendMessage('ai', aiResponse);
}

// ── Append message to UI ───────────────────────────────────────────────────
function appendMessage(role, text) {
    const messagesEl = document.getElementById('chatMessages');
    const msgDiv     = document.createElement('div');
    msgDiv.className = `msg ${role}`;

    const now     = new Date();
    const timeStr = now.toLocaleTimeString('en-PK', { hour:'2-digit', minute:'2-digit' });

    // Detect if text is Urdu script
    const isUrduScript = /[\u0600-\u06FF]/.test(text);
    const bubbleClass  = isUrduScript ? 'msg-bubble urdu-msg' : 'msg-bubble';

    // Format text — convert newlines to <br>
    const formatted = text.replace(/\n/g, '<br>');

    msgDiv.innerHTML = `
      <div class="${bubbleClass}">${formatted}</div>
      <div class="msg-time">${timeStr}</div>
    `;

    messagesEl.appendChild(msgDiv);
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

// ── Typing indicator ───────────────────────────────────────────────────────
function showTyping() {
    const messagesEl = document.getElementById('chatMessages');
    const typingDiv  = document.createElement('div');
    typingDiv.className = 'typing-wrap';
    typingDiv.id        = 'typingIndicator';
    typingDiv.innerHTML = `
      <div class="typing-bubble">
        <div class="td"></div>
        <div class="td"></div>
        <div class="td"></div>
      </div>
    `;
    messagesEl.appendChild(typingDiv);
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

function hideTyping() {
    const el = document.getElementById('typingIndicator');
    if (el) el.remove();
}

// ── Language switcher ──────────────────────────────────────────────────────
async function switchLang(lang, btn) {
    currentLang = lang;
    saveLang(lang);

    document.querySelectorAll('.lsb').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    // Update placeholder based on language
    const input       = document.getElementById('chatInput');
    const placeholders = {
        roman_urdu: 'Apni baat yahan likhein...',
        urdu:       'یہاں لکھیں...',
        english:    'Type your message here...'
    };
    input.placeholder = placeholders[lang] || placeholders.roman_urdu;

    // Start fresh conversation in new language
    await startNewChat();
}

// ── Handle Enter key ───────────────────────────────────────────────────────
function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

// ── Auto resize textarea ───────────────────────────────────────────────────
function autoResize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}