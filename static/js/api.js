// ── SamajhHer — Central API Layer ─────────────────────────────────────────
const API = '/api';

// ── Token & user helpers ───────────────────────────────────────────────────
const getToken  = ()      => localStorage.getItem('sh_token');
const getUser   = ()      => { const u = localStorage.getItem('sh_user'); return u ? JSON.parse(u) : null; };
const getLang   = ()      => localStorage.getItem('sh_lang') || 'roman_urdu';
const saveAuth  = (t, u)  => {
    localStorage.setItem('sh_token', t);
    localStorage.setItem('sh_user', JSON.stringify(u));
    localStorage.setItem('sh_lang', u.language);
};
const clearAuth = ()      => {
    localStorage.removeItem('sh_token');
    localStorage.removeItem('sh_user');
};
const saveLang  = (lang)  => localStorage.setItem('sh_lang', lang);

function logout() { clearAuth(); window.location.href = '/'; }
function requireAuth() { if (!getToken()) window.location.href = '/login'; }

// ── Core request ───────────────────────────────────────────────────────────
async function req(method, endpoint, body = null, auth = true) {
    const headers = { 'Content-Type': 'application/json' };
    if (auth) {
        const t = getToken();
        if (!t) { logout(); return null; }
        headers['Authorization'] = `Bearer ${t}`;
    }
    const opts = { method, headers };
    if (body) opts.body = JSON.stringify(body);
    try {
        const res  = await fetch(`${API}${endpoint}`, opts);
        const data = await res.json();
        if (res.status === 401) { logout(); return null; }
        return { ok: res.ok, status: res.status, data };
    } catch (e) {
        console.error('API Error:', e);
        return { ok: false, data: { error: 'Cannot connect to server. Is Flask running?' } };
    }
}

// ── Auth ───────────────────────────────────────────────────────────────────
const apiRegister = (name, email, password, language) =>
    req('POST', '/auth/register', { name, email, password, language }, false);
const apiLogin = (email, password) =>
    req('POST', '/auth/login', { email, password }, false);

// ── Chat ───────────────────────────────────────────────────────────────────
const apiStartConversation = (flow, language) =>
    req('POST', '/chat/start', { flow, language });
const apiSendMessage = (conversation_id, message) =>
    req('POST', '/chat/message', { conversation_id, message });
const apiGetConversations = (flow = null) =>
    req('GET', `/chat/conversations${flow ? '?flow=' + flow : ''}`);
const apiGetConversation = (id) =>
    req('GET', `/chat/conversations/${id}`);
const apiDeleteConversation = (id) =>
    req('DELETE', `/chat/conversations/${id}`);

// ── Doctor cards ───────────────────────────────────────────────────────────
const apiGenerateCard = (symptoms, duration, severity, language) =>
    req('POST', '/card/generate', { symptoms, duration, severity, language });
const apiGetMyCards = () =>
    req('GET', '/card/my-cards');
const apiGetCard = (id) =>
    req('GET', `/card/${id}`);

// ── History ────────────────────────────────────────────────────────────────
const apiGetAllHistory = () =>
    req('GET', '/history/all');

// ── Helpers ────────────────────────────────────────────────────────────────
function showAlert(id, msg, type = 'error') {
    const el = document.getElementById(id);
    if (!el) return;
    el.className = `alert alert-${type} show`;
    el.textContent = msg;
    if (type === 'success') setTimeout(() => el.classList.remove('show'), 4000);
}

function setNavUser() {
    const u  = getUser();
    const el = document.getElementById('nav-user');
    if (el && u) el.textContent = u.name;
}

function formatDate(isoString) {
    return new Date(isoString).toLocaleDateString('en-PK', {
        day: 'numeric', month: 'short', year: 'numeric'
    });
}