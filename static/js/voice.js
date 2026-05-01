// ── SamajhHer Voice Input ──────────────────────────────────────────────────
// Uses browser Web Speech API — no installation needed

let recognition  = null;
let isRecording  = false;

function initVoice() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        const hint = document.getElementById('voiceHint');
        if (hint) hint.textContent = '⚠️ Voice not supported in this browser. Use Chrome.';
        const btn = document.getElementById('voiceBtn');
        if (btn) btn.style.opacity = '0.4';
        return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous     = false;
    recognition.interimResults = true;

    // Set language based on user preference
    const lang = getLang();
    recognition.lang = lang === 'english' ? 'en-US' : 'ur-PK';

    recognition.onstart = () => {
        isRecording = true;
        const btn  = document.getElementById('voiceBtn');
        const hint = document.getElementById('voiceHint');
        if (btn)  { btn.classList.add('recording'); btn.textContent = '⏹'; }
        if (hint) hint.textContent = '🔴 Sun rahi hun... Bolein';
    };

    recognition.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
        }
        const input = document.getElementById('chatInput');
        if (input) {
            input.value = transcript;
            autoResize(input);
        }
    };

    recognition.onend = () => {
        isRecording = false;
        const btn  = document.getElementById('voiceBtn');
        const hint = document.getElementById('voiceHint');
        if (btn)  { btn.classList.remove('recording'); btn.textContent = '🎤'; }
        if (hint) hint.textContent = '🎤 Press mic to speak';
    };

    recognition.onerror = (e) => {
        isRecording = false;
        const btn  = document.getElementById('voiceBtn');
        const hint = document.getElementById('voiceHint');
        if (btn)  { btn.classList.remove('recording'); btn.textContent = '🎤'; }
        if (hint) hint.textContent = '⚠️ Error: ' + e.error;
    };
}

function toggleVoice() {
    if (!recognition) { initVoice(); }
    if (!recognition)  return;

    if (isRecording) {
        recognition.stop();
    } else {
        // Update language before starting
        const lang = getLang();
        recognition.lang = lang === 'english' ? 'en-US' : 'ur-PK';
        recognition.start();
    }
}

// Initialize voice on page load
document.addEventListener('DOMContentLoaded', initVoice);