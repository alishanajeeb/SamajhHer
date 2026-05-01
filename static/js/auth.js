// Redirect if already logged in
if (getToken()) window.location.href = '/woman';

async function handleLogin() {
    const email    = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const btn      = document.getElementById('loginBtn');

    if (!email || !password) {
        showAlert('alert', 'Please enter email and password.'); return;
    }

    btn.disabled  = true;
    btn.innerHTML = '<span class="spinner"></span> Signing in...';

    const res = await apiLogin(email, password);

    btn.disabled  = false;
    btn.innerHTML = 'Sign In';

    if (!res || !res.ok) {
        showAlert('alert', res?.data?.error || 'Login failed.'); return;
    }

    saveAuth(res.data.access_token, res.data.user);
    // Redirect to landing so user can pick their flow
    window.location.href = '/';
}

document.addEventListener('keydown', e => {
    if (e.key === 'Enter') handleLogin();
});