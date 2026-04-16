/* ═══════════════════════════════════════════════════════════════════════════
   Bharat Legal AI — Frontend Application
   Chat logic, Speech-to-Text, Text-to-Speech, Language switching
   ═══════════════════════════════════════════════════════════════════════════ */

(() => {
    'use strict';

    // ─── Configuration ───────────────────────────────────────────────────────
    const API_BASE = window.location.origin;

    const LANG_CONFIG = {
        en: { name: 'English',   native: 'English',  speechCode: 'en-IN',  welcomeText: 'Ask any question about Indian law...' },
        hi: { name: 'Hindi',     native: 'हिन्दी',    speechCode: 'hi-IN',  welcomeText: 'भारतीय कानून के बारे में पूछें...' },
        te: { name: 'Telugu',    native: 'తెలుగు',    speechCode: 'te-IN',  welcomeText: 'భారతీయ చట్టం గురించి అడగండి...' },
        ta: { name: 'Tamil',     native: 'தமிழ்',     speechCode: 'ta-IN',  welcomeText: 'இந்திய சட்டம் பற்றி கேளுங்கள்...' },
        kn: { name: 'Kannada',   native: 'ಕನ್ನಡ',     speechCode: 'kn-IN',  welcomeText: 'ಭಾರತೀಯ ಕಾನೂನಿನ ಬಗ್ಗೆ ಕೇಳಿ...' },
        ml: { name: 'Malayalam', native: 'മലയാളം',   speechCode: 'ml-IN',  welcomeText: 'ഇന്ത്യൻ നിയമത്തെക്കുറിച്ച് ചോദിക്കൂ...' },
        bn: { name: 'Bengali',   native: 'বাংলা',     speechCode: 'bn-IN',  welcomeText: 'ভারতীয় আইন সম্পর্কে জিজ্ঞাসা করুন...' },
        mr: { name: 'Marathi',   native: 'मराठी',     speechCode: 'mr-IN',  welcomeText: 'भारतीय कायद्याबद्दल विचारा...' },
        pa: { name: 'Punjabi',   native: 'ਪੰਜਾਬੀ',    speechCode: 'pa-IN',  welcomeText: 'ਭਾਰਤੀ ਕਾਨੂੰਨ ਬਾਰੇ ਪੁੱਛੋ...' },
        gu: { name: 'Gujarati',  native: 'ગુજરાતી',   speechCode: 'gu-IN',  welcomeText: 'ભારતીય કાયદા વિશે પૂછો...' },
    };

    // ─── State ───────────────────────────────────────────────────────────────
    let currentLang = 'en';
    let isRecording = false;
    let isSending = false;
    let currentAudio = null;
    let recognition = null;

    // ─── DOM Elements ────────────────────────────────────────────────────────
    const $ = (sel) => document.querySelector(sel);
    const $$ = (sel) => document.querySelectorAll(sel);

    const elements = {
        chatMessages:   $('#chat-messages'),
        chatInput:      $('#chat-input'),
        sendBtn:        $('#send-btn'),
        micBtn:         $('#mic-btn'),
        voiceIndicator: $('#voice-indicator'),
        voiceLabel:     $('#voice-label'),
        voiceStop:      $('#voice-stop'),
        inputBar:       $('#input-bar'),
        sidebar:        $('#sidebar'),
        sidebarOverlay: $('#sidebar-overlay'),
        menuToggle:     $('#menu-toggle'),
        languageGrid:   $('#language-grid'),
        topicChips:     $('#topic-chips'),
        headerLang:     $('#header-lang-select'),
        statusText:     $('#status-text'),
        audioPlayer:    $('#audio-player'),
    };

    // ─── Initialize ──────────────────────────────────────────────────────────
    function init() {
        setupEventListeners();
        setupSpeechRecognition();
        updatePlaceholder();
        autoResizeTextarea();
        console.log('[Bharat Legal AI] Initialized with', Object.keys(LANG_CONFIG).length, 'languages');
    }

    // ─── Event Listeners ─────────────────────────────────────────────────────
    function setupEventListeners() {
        // Send message
        elements.sendBtn.addEventListener('click', sendMessage);
        elements.chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        // Input validation — enable/disable send button
        elements.chatInput.addEventListener('input', () => {
            const hasText = elements.chatInput.value.trim().length > 0;
            elements.sendBtn.disabled = !hasText || isSending;
            autoResizeTextarea();
        });

        // Voice input
        elements.micBtn.addEventListener('click', toggleVoiceInput);
        elements.voiceStop.addEventListener('click', stopVoiceInput);

        // Sidebar toggle
        elements.menuToggle.addEventListener('click', toggleSidebar);
        elements.sidebarOverlay.addEventListener('click', closeSidebar);

        // Language selection — sidebar buttons
        $$('.lang-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                switchLanguage(btn.dataset.lang);
            });
        });

        // Language selection — header dropdown
        elements.headerLang.addEventListener('change', (e) => {
            switchLanguage(e.target.value);
        });

        // Topic chips
        $$('.chip').forEach(chip => {
            chip.addEventListener('click', () => {
                const query = chip.dataset.query;
                elements.chatInput.value = query;
                elements.sendBtn.disabled = false;
                autoResizeTextarea();
                closeSidebar();
                sendMessage();
            });
        });

        // Close sidebar on Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeSidebar();
                if (isRecording) stopVoiceInput();
            }
        });
    }

    // ─── Language Switching ───────────────────────────────────────────────────
    function switchLanguage(lang) {
        if (!LANG_CONFIG[lang]) return;
        currentLang = lang;

        // Update sidebar buttons
        $$('.lang-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.lang === lang);
        });

        // Update header dropdown
        elements.headerLang.value = lang;

        // Update placeholder
        updatePlaceholder();

        // Update status
        setStatus(`Language: ${LANG_CONFIG[lang].native}`);
        setTimeout(() => setStatus('Ready'), 2000);

        console.log(`[Lang] Switched to ${LANG_CONFIG[lang].name} (${lang})`);
    }

    function updatePlaceholder() {
        const config = LANG_CONFIG[currentLang];
        elements.chatInput.placeholder = config.welcomeText;
    }

    // ─── Sidebar ─────────────────────────────────────────────────────────────
    function toggleSidebar() {
        elements.sidebar.classList.toggle('open');
        elements.sidebarOverlay.classList.toggle('visible');
    }

    function closeSidebar() {
        elements.sidebar.classList.remove('open');
        elements.sidebarOverlay.classList.remove('visible');
    }

    // ─── Status ──────────────────────────────────────────────────────────────
    function setStatus(text) {
        elements.statusText.textContent = text;
    }

    // ─── Auto-resize Textarea ────────────────────────────────────────────────
    function autoResizeTextarea() {
        const textarea = elements.chatInput;
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    // ─── Send Message ────────────────────────────────────────────────────────
    async function sendMessage() {
        const query = elements.chatInput.value.trim();
        if (!query || isSending) return;

        isSending = true;
        elements.sendBtn.disabled = true;
        elements.chatInput.value = '';
        autoResizeTextarea();

        // Add user message
        addMessage('user', query);

        // Show typing indicator
        const typingEl = showTypingIndicator();
        setStatus('Thinking...');

        try {
            const response = await fetch(`${API_BASE}/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    query: query,
                    language: currentLang,
                }),
            });

            if (!response.ok) {
                const errData = await response.json().catch(() => ({}));
                throw new Error(errData.detail || `Server error (${response.status})`);
            }

            const data = await response.json();

            // Remove typing indicator
            removeTypingIndicator(typingEl);

            // Add bot response
            addMessage('bot', data.response, {
                sources: data.sources || [],
                status: data.status,
            });

            setStatus('Ready');

        } catch (error) {
            console.error('[Chat Error]', error);
            removeTypingIndicator(typingEl);
            addMessage('bot', `❌ **Error:** ${error.message}\n\nPlease check if the server is running and try again.`, {
                isError: true,
            });
            setStatus('Error — check connection');
        }

        isSending = false;
    }

    // ─── Add Message to Chat ─────────────────────────────────────────────────
    function addMessage(role, text, options = {}) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}-message`;

        // Avatar
        const avatarDiv = document.createElement('div');
        avatarDiv.className = `message-avatar ${role}-avatar`;
        if (role === 'bot') {
            avatarDiv.innerHTML = `<svg viewBox="0 0 32 32" width="24" height="24" fill="none">
                <circle cx="16" cy="16" r="14" stroke="#FF9933" stroke-width="1.5"/>
                <circle cx="16" cy="16" r="3" fill="#FF9933"/>
                <path d="M16 6v20M8 10h16M8 22h16" stroke="#138808" stroke-width="1.2" stroke-linecap="round"/>
            </svg>`;
        } else {
            avatarDiv.textContent = '👤';
        }

        // Content
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        textDiv.innerHTML = formatMessage(text);
        contentDiv.appendChild(textDiv);

        // Actions (for bot messages)
        if (role === 'bot' && !options.isError) {
            const actionsDiv = document.createElement('div');
            actionsDiv.className = 'message-actions';

            // Listen button
            const listenBtn = document.createElement('button');
            listenBtn.className = 'action-btn listen-btn';
            listenBtn.innerHTML = '🔊 Listen';
            listenBtn.addEventListener('click', () => playAudioResponse(text, listenBtn));
            actionsDiv.appendChild(listenBtn);

            // Copy button
            const copyBtn = document.createElement('button');
            copyBtn.className = 'action-btn copy-btn';
            copyBtn.innerHTML = '📋 Copy';
            copyBtn.addEventListener('click', () => copyText(text, copyBtn));
            actionsDiv.appendChild(copyBtn);

            contentDiv.appendChild(actionsDiv);

            // Sources
            if (options.sources && options.sources.length > 0) {
                const sourcesDiv = document.createElement('div');
                sourcesDiv.className = 'message-sources';
                options.sources.forEach(source => {
                    if (source.title) {
                        const tag = document.createElement('span');
                        tag.className = 'source-tag';
                        tag.textContent = `📖 ${source.title}`;
                        sourcesDiv.appendChild(tag);
                    }
                });
                contentDiv.appendChild(sourcesDiv);
            }
        }

        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        elements.chatMessages.appendChild(messageDiv);

        // Scroll to bottom
        scrollToBottom();
    }

    // ─── Format Message ──────────────────────────────────────────────────────
    function formatMessage(text) {
        if (!text) return '';

        let html = text;

        // Escape HTML
        html = html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

        // Bold: **text**
        html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

        // Italic: *text*
        html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

        // Headers: ### text
        html = html.replace(/^### (.+)$/gm, '<h4>$1</h4>');
        html = html.replace(/^## (.+)$/gm, '<h3>$1</h3>');

        // Bullet lists
        html = html.replace(/^[•\-]\s+(.+)$/gm, '<li>$1</li>');

        // Numbered lists
        html = html.replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>');

        // Wrap consecutive <li> in <ul>
        html = html.replace(/(<li>.*?<\/li>\n?)+/gs, (match) => `<ul>${match}</ul>`);

        // Paragraphs
        html = html.replace(/\n{2,}/g, '</p><p>');
        html = html.replace(/\n/g, '<br>');
        html = `<p>${html}</p>`;

        // Clean up empty paragraphs
        html = html.replace(/<p>\s*<\/p>/g, '');
        html = html.replace(/<p>\s*(<h[34]>)/g, '$1');
        html = html.replace(/(<\/h[34]>)\s*<\/p>/g, '$1');
        html = html.replace(/<p>\s*(<ul>)/g, '$1');
        html = html.replace(/(<\/ul>)\s*<\/p>/g, '$1');

        return html;
    }

    // ─── Typing Indicator ────────────────────────────────────────────────────
    function showTypingIndicator() {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message typing-message';
        messageDiv.id = 'typing-indicator-msg';

        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar bot-avatar';
        avatarDiv.innerHTML = `<svg viewBox="0 0 32 32" width="24" height="24" fill="none">
            <circle cx="16" cy="16" r="14" stroke="#FF9933" stroke-width="1.5"/>
            <circle cx="16" cy="16" r="3" fill="#FF9933"/>
            <path d="M16 6v20M8 10h16M8 22h16" stroke="#138808" stroke-width="1.2" stroke-linecap="round"/>
        </svg>`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        textDiv.innerHTML = `
            <div class="typing-indicator">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
            </div>
        `;

        contentDiv.appendChild(textDiv);
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        elements.chatMessages.appendChild(messageDiv);

        scrollToBottom();
        return messageDiv;
    }

    function removeTypingIndicator(el) {
        if (el && el.parentNode) {
            el.remove();
        }
    }

    // ─── Scroll to Bottom ────────────────────────────────────────────────────
    function scrollToBottom() {
        requestAnimationFrame(() => {
            elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
        });
    }

    // ─── Speech-to-Text (Web Speech API) ─────────────────────────────────────
    function setupSpeechRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            console.warn('[STT] Web Speech API not supported in this browser');
            elements.micBtn.title = 'Voice input not supported in this browser';
            elements.micBtn.style.opacity = '0.3';
            elements.micBtn.style.cursor = 'not-allowed';
            return;
        }

        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.maxAlternatives = 1;

        recognition.onstart = () => {
            isRecording = true;
            elements.micBtn.classList.add('recording');
            elements.voiceIndicator.classList.remove('hidden');
            elements.voiceLabel.textContent = `Listening in ${LANG_CONFIG[currentLang].native}...`;
            setStatus('🎤 Listening...');
        };

        recognition.onresult = (event) => {
            let transcript = '';
            let isFinal = false;

            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    isFinal = true;
                }
            }

            // Show interim results in input
            elements.chatInput.value = transcript;
            autoResizeTextarea();
            elements.sendBtn.disabled = !transcript.trim();

            if (isFinal) {
                stopVoiceInput();
                // Auto-send after a short delay
                setTimeout(() => {
                    if (elements.chatInput.value.trim()) {
                        sendMessage();
                    }
                }, 500);
            }
        };

        recognition.onerror = (event) => {
            console.error('[STT Error]', event.error);
            stopVoiceInput();

            if (event.error === 'not-allowed') {
                addMessage('bot', '🎤 **Microphone access denied.** Please allow microphone access in your browser settings and try again.', { isError: true });
            } else if (event.error === 'no-speech') {
                setStatus('No speech detected — try again');
            } else {
                setStatus(`Voice error: ${event.error}`);
            }
        };

        recognition.onend = () => {
            stopVoiceInput();
        };
    }

    function toggleVoiceInput() {
        if (!recognition) {
            addMessage('bot', '🎤 **Voice input is not supported** in this browser. Please use Chrome, Edge, or Safari for voice input.', { isError: true });
            return;
        }

        if (isRecording) {
            stopVoiceInput();
        } else {
            startVoiceInput();
        }
    }

    function startVoiceInput() {
        if (!recognition || isRecording) return;

        try {
            // Set recognition language
            const langConfig = LANG_CONFIG[currentLang];
            recognition.lang = langConfig.speechCode;

            recognition.start();
        } catch (err) {
            console.error('[STT] Failed to start:', err);
            setStatus('Failed to start voice input');
        }
    }

    function stopVoiceInput() {
        isRecording = false;
        elements.micBtn.classList.remove('recording');
        elements.voiceIndicator.classList.add('hidden');

        if (recognition) {
            try {
                recognition.stop();
            } catch (e) {
                // Ignore — may already be stopped
            }
        }

        setStatus('Ready');
    }

    // ─── Text-to-Speech (Server-side gTTS) ───────────────────────────────────
    async function playAudioResponse(text, button) {
        // If currently playing, stop
        if (currentAudio && !currentAudio.paused) {
            currentAudio.pause();
            currentAudio.currentTime = 0;
            $$('.action-btn.playing').forEach(b => {
                b.classList.remove('playing');
                b.innerHTML = '🔊 Listen';
            });
            currentAudio = null;
            return;
        }

        button.classList.add('playing');
        button.innerHTML = '⏳ Loading...';
        setStatus('Generating audio...');

        try {
            const response = await fetch(`${API_BASE}/api/tts`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: text,
                    language: currentLang,
                }),
            });

            if (!response.ok) {
                throw new Error(`TTS server error (${response.status})`);
            }

            const data = await response.json();

            if (data.status !== 'success' || !data.audio_base64) {
                // Fallback to browser TTS
                fallbackBrowserTTS(text, button);
                return;
            }

            // Play the audio
            const audioSrc = `data:${data.mime_type};base64,${data.audio_base64}`;
            const audio = new Audio(audioSrc);
            currentAudio = audio;

            audio.onplay = () => {
                button.innerHTML = '⏸️ Pause';
                setStatus('🔊 Playing audio...');
            };

            audio.onended = () => {
                button.classList.remove('playing');
                button.innerHTML = '🔊 Listen';
                currentAudio = null;
                setStatus('Ready');
            };

            audio.onerror = () => {
                console.warn('[TTS] Audio playback failed, trying browser TTS');
                fallbackBrowserTTS(text, button);
            };

            audio.play().catch(() => {
                fallbackBrowserTTS(text, button);
            });

        } catch (error) {
            console.error('[TTS Error]', error);
            // Fallback to browser TTS
            fallbackBrowserTTS(text, button);
        }
    }

    // ─── Browser TTS Fallback ────────────────────────────────────────────────
    function fallbackBrowserTTS(text, button) {
        if (!window.speechSynthesis) {
            button.classList.remove('playing');
            button.innerHTML = '🔊 Listen';
            setStatus('TTS unavailable');
            return;
        }

        // Clean text for speech
        let cleanText = text
            .replace(/\*\*(.+?)\*\*/g, '$1')
            .replace(/\*(.+?)\*/g, '$1')
            .replace(/#{1,6}\s*/g, '')
            .replace(/[📋💡📝📌📚⚠️✅❌🔍🏛️🎤🔊📜📢💻🏠💰🛡️💍]/g, '')
            .replace(/```[\s\S]*?```/g, '')
            .replace(/`(.+?)`/g, '$1')
            .replace(/\n+/g, '. ')
            .replace(/\s+/g, ' ')
            .trim();

        if (cleanText.length > 500) {
            cleanText = cleanText.substring(0, 500) + '... For more details, please refer to the text response.';
        }

        const utterance = new SpeechSynthesisUtterance(cleanText);
        const langConfig = LANG_CONFIG[currentLang];
        utterance.lang = langConfig.speechCode;
        utterance.rate = 0.95;
        utterance.pitch = 1;

        utterance.onstart = () => {
            button.innerHTML = '⏸️ Pause';
            setStatus('🔊 Playing (browser)...');
        };

        utterance.onend = () => {
            button.classList.remove('playing');
            button.innerHTML = '🔊 Listen';
            currentAudio = null;
            setStatus('Ready');
        };

        utterance.onerror = () => {
            button.classList.remove('playing');
            button.innerHTML = '🔊 Listen';
            setStatus('TTS failed');
        };

        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utterance);

        // Store reference for stopping
        currentAudio = { pause: () => window.speechSynthesis.cancel(), paused: false, currentTime: 0 };
    }

    // ─── Copy Text ───────────────────────────────────────────────────────────
    async function copyText(text, button) {
        try {
            // Strip markdown for clean copy
            const cleanText = text
                .replace(/\*\*(.+?)\*\*/g, '$1')
                .replace(/\*(.+?)\*/g, '$1')
                .replace(/#{1,6}\s*/g, '');

            await navigator.clipboard.writeText(cleanText);
            const original = button.innerHTML;
            button.innerHTML = '✅ Copied!';
            setTimeout(() => { button.innerHTML = original; }, 1500);
        } catch (err) {
            // Fallback
            const textarea = document.createElement('textarea');
            textarea.value = text;
            textarea.style.position = 'fixed';
            textarea.style.left = '-9999px';
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);

            const original = button.innerHTML;
            button.innerHTML = '✅ Copied!';
            setTimeout(() => { button.innerHTML = original; }, 1500);
        }
    }

    // ─── Start App ───────────────────────────────────────────────────────────
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
