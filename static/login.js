const email = document.getElementById('email');
const remember = document.getElementById('remember-email');
const storageKey = 'darb.login.email';

try {
    const savedEmail = localStorage.getItem(storageKey);
    if (savedEmail) {
        email.value = savedEmail;
        remember.checked = true;
    }
} catch (_) {
    // Login remains available when browser storage is disabled.
}

remember.addEventListener('change', () => {
    if (!remember.checked) {
        try { localStorage.removeItem(storageKey); } catch (_) {}
    }
});

email.form.addEventListener('submit', () => {
    try {
        if (remember.checked) localStorage.setItem(storageKey, email.value);
        else localStorage.removeItem(storageKey);
    } catch (_) {}
});

const forgotPassword = document.getElementById('forgot-password');
const recoveryHelp = document.getElementById('recovery-help');
forgotPassword.addEventListener('click', () => {
    recoveryHelp.hidden = !recoveryHelp.hidden;
    forgotPassword.setAttribute('aria-expanded', String(!recoveryHelp.hidden));
});

if (new URLSearchParams(window.location.search).get('role') === 'teacher') {
    document.getElementById('teacher-help').hidden = false;
    email.focus();
}
