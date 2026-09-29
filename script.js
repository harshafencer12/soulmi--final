// ============================================
// STICKY NAVBAR
// ============================================
const header = document.getElementById('navbar');
if (header) {
    window.addEventListener('scroll', () => {
        header.classList.toggle('scrolled', window.scrollY > 50);
    });
}
 
// ============================================
// LOGGED-IN NAV STATE
// Public pages (Home, Therapists, About, Resources, Community, Blog) all
// ship a hardcoded "Get Started" -> register.html button with no idea
// whether the visitor is already logged in. Swap it to "Go to Dashboard"
// whenever they are, so navigating around the site doesn't look like you
// got logged out.
// ============================================
(function updateNavForLoggedInUser() {
    let user = null;
    try {
        user = JSON.parse(localStorage.getItem('soulmi-user') || 'null');
    } catch { /* ignore malformed cache */ }
    if (!user || !user.email) return;
 
    document.querySelectorAll('a[href="register.html"]').forEach((btn) => {
        btn.href = 'dashboard.html';
        btn.textContent = btn.textContent.includes('Free') ? "Go to Dashboard" : "Dashboard";
    });
})();
 
// ============================================
// MOBILE HAMBURGER MENU
// ============================================
const hamburger = document.getElementById('nav-hamburger');
const mobileMenu = document.getElementById('nav-mobile-menu');
const mobileClose = document.getElementById('nav-mobile-close');
 
if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
        mobileMenu.classList.add('open');
        document.body.style.overflow = 'hidden';
    });
 
    const closeMobileMenu = () => {
        mobileMenu.classList.remove('open');
        document.body.style.overflow = '';
    };
 
    if (mobileClose) mobileClose.addEventListener('click', closeMobileMenu);
 
    mobileMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });
 
    mobileMenu.addEventListener('click', (e) => {
        if (e.target === mobileMenu) closeMobileMenu();
    });
}
 
// ============================================
// SCROLL REVEAL ANIMATIONS
// ============================================
const reveals = document.querySelectorAll('.reveal');
const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('active');
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
 
reveals.forEach(el => revealObserver.observe(el));
 
window.addEventListener('load', () => {
    reveals.forEach(el => {
        if (el.getBoundingClientRect().top < window.innerHeight - 40) {
            el.classList.add('active');
        }
    });
});
 
// ============================================
// ZEN MODE (THEME) TOGGLE
// ============================================
const themeToggle = document.getElementById('theme-toggle');
const html = document.documentElement;
 
if (themeToggle) {
    const saved = localStorage.getItem('soulmi-theme');
    if (saved) html.setAttribute('data-theme', saved);
 
    themeToggle.addEventListener('click', () => {
        const next = html.getAttribute('data-theme') === 'zen' ? 'light' : 'zen';
        html.setAttribute('data-theme', next);
        localStorage.setItem('soulmi-theme', next);
    });
}
 
// ============================================
// MOOD SLIDER
// ============================================
const moodSlider = document.getElementById('mood-slider');
if (moodSlider) {
    moodSlider.addEventListener('input', (e) => {
        const val = Number(e.target.value);
        const label = moodSlider.closest('.mood-widget')?.querySelector('label');
        if (!label) return;
        if (val < 35) label.textContent = 'How is your mind feeling right now? — Quite anxious';
        else if (val < 65) label.textContent = 'How is your mind feeling right now? — Getting there';
        else label.textContent = 'How is your mind feeling right now? — Feeling calm';
    });
}
 
// ============================================
// BREATHING MODAL
// ============================================
const breatheBtn = document.getElementById('open-breathe');
const breatheModal = document.getElementById('breathing-modal');
const closeBreathe = document.getElementById('close-breathe');
const breatheText = document.getElementById('breathe-text');
const breatheCircle = document.querySelector('.breathe-circle');
let breatheInterval = null;
 
if (breatheBtn && breatheModal) {
    breatheBtn.addEventListener('click', () => {
        breatheModal.classList.add('active');
        breatheText.textContent = 'Breathe In…';
        breatheCircle.style.transform = 'scale(2)';
 
        breatheInterval = setInterval(() => {
            if (breatheText.textContent.startsWith('Breathe In')) {
                breatheText.textContent = 'Breathe Out…';
                breatheCircle.style.transform = 'scale(1)';
            } else {
                breatheText.textContent = 'Breathe In…';
                breatheCircle.style.transform = 'scale(2)';
            }
        }, 4000);
    });
 
    const stopBreathing = () => {
        breatheModal.classList.remove('active');
        clearInterval(breatheInterval);
        breatheInterval = null;
        setTimeout(() => {
            breatheText.textContent = 'Ready?';
            breatheCircle.style.transform = 'scale(1)';
        }, 350);
    };
 
    if (closeBreathe) closeBreathe.addEventListener('click', stopBreathing);
    breatheModal.addEventListener('click', (e) => {
        if (e.target === breatheModal) stopBreathing();
    });
}
 
// ============================================
// DAILY AFFIRMATIONS
// ============================================
const affBtn = document.getElementById('new-affirmation');
const affText = document.getElementById('affirmation-text');
const affirmations = [
    'You are enough, exactly as you are.',
    'Every storm runs out of rain.',
    "It's okay to rest and reset.",
    'Your feelings are completely valid.',
    'Progress, not perfection.',
    'You are stronger than you think.',
    'Breathe. You\'ve got this.',
    'Healing is not linear — and that\'s okay.',
    'You deserve the same kindness you give others.',
    'One moment at a time is enough.',
];
 
if (affBtn && affText) {
    let current = affText.textContent.replace(/['"]/g, '').trim();
 
    affBtn.addEventListener('click', () => {
        affText.style.opacity = '0';
        setTimeout(() => {
            let next;
            do {
                next = affirmations[Math.floor(Math.random() * affirmations.length)];
            } while (next === current);
            current = next;
            affText.textContent = `"${next}"`;
            affText.style.opacity = '1';
        }, 400);
    });
}
 
// ============================================
// AI CHAT WIDGET — OpenRouter Integration
// ============================================
const chatToggle = document.getElementById('chat-toggle');
const chatWindow = document.getElementById('chat-window');
const closeChat = document.getElementById('close-chat');
const sendBtn = document.getElementById('send-btn');
const chatInput = document.getElementById('chat-input-field');
const chatBody = document.getElementById('chat-body');
const chatTooltip = document.querySelector('.chat-tooltip');
 
// Backend API base — the Flask server. Chat now goes through our own
// /api/chat proxy so no AI provider key ever lives in the browser.
const API_BASE = window.SOULMI_CONFIG?.API_BASE || 'http://127.0.0.1:5000';
 
// Conversation history for context (sent to our backend, not OpenRouter directly)
const conversationHistory = [];
 
if (chatToggle && chatWindow) {
    chatToggle.addEventListener('click', () => {
        const isActive = chatWindow.classList.toggle('active');
        if (chatTooltip) {
            if (isActive) chatTooltip.classList.add('hide');
            else chatTooltip.classList.remove('hide');
        }
    });
    if (closeChat) {
        closeChat.addEventListener('click', () => {
            chatWindow.classList.remove('active');
            if (chatTooltip) chatTooltip.classList.remove('hide');
        });
    }
 
    const appendMessage = (text, className) => {
        const msg = document.createElement('div');
        msg.classList.add('message', className);
        msg.textContent = text;
        chatBody.appendChild(msg);
        chatBody.scrollTop = chatBody.scrollHeight;
        return msg;
    };
 
    const showTyping = () => {
        const typing = document.createElement('div');
        typing.classList.add('typing-indicator');
        typing.innerHTML = '<span></span><span></span><span></span>';
        typing.id = 'typing-dots';
        chatBody.appendChild(typing);
        chatBody.scrollTop = chatBody.scrollHeight;
        return typing;
    };
 
    const sendToBackend = async (userText) => {
        conversationHistory.push({ role: 'user', content: userText });
 
        const typingEl = showTyping();
 
        // Whether the user allows their real (MySQL-stored) mood history
        // to be spliced into the system prompt — the server does the
        // fetching, the browser just passes the preference along.
        const shareMoodAI = localStorage.getItem("soulmi-share-mood-ai") !== "false";
 
        try {
            const response = await fetch(`${API_BASE}/api/chat`, {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    messages: conversationHistory.slice(-12),
                    include_mood_context: shareMoodAI,
                }),
            });
 
            if (typingEl.parentNode) typingEl.remove();
 
            if (!response.ok) {
                const errData = await response.json().catch(() => ({}));
                console.error('Chat API error:', response.status, errData);
                appendMessage("I'm having trouble connecting right now. Please try again in a moment. 💛", 'ai-msg');
                return;
            }
 
            const data = await response.json();
            const aiText = data.reply || "I'm here for you. Could you tell me more about what's on your mind?";
 
            conversationHistory.push({ role: 'assistant', content: aiText });
            appendMessage(aiText, 'ai-msg');
 
        } catch (err) {
            console.error('Chat fetch error:', err);
            if (typingEl.parentNode) typingEl.remove();
            appendMessage("I'm having a moment of silence — but I'm still here. Try sending your message again. 🌱", 'ai-msg');
        }
    };
 
    const sendMessage = () => {
        const text = chatInput.value.trim();
        if (!text) return;
 
        appendMessage(text, 'user-msg');
        chatInput.value = '';
 
        sendToBackend(text);
    };
 
    if (sendBtn) sendBtn.addEventListener('click', sendMessage);
    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    }
}
 
// ============================================
// THERAPIST DIRECTORY FILTERING
// ============================================
const gridContainer = document.getElementById('therapists-grid');
 
if (gridContainer) {
    const therapistsData = [
        {
            name: 'Mrs. Soujanya Yanamandra',
            spec: ['child', 'anxiety', 'relationships'],
            specLabel: 'Child & Adolescent Mental Health',
            location: 'hyderabad',
            locationLabel: 'Hyderabad & Remote',
            lang: ['english', 'telugu', 'hindi'],
            img: 'images/therapist 1.jpg',
            desc: 'Compassionate professional focusing on emotional balance, understanding, and long-term wellbeing for children and adolescents.',
        },
        {
            name: 'Mrs. Srinidhi Veldanda',
            spec: ['trauma', 'anxiety'],
            specLabel: 'Emotional Trauma Healing',
            location: 'remote',
            locationLabel: 'Remote (Online)',
            lang: ['english', 'hindi', 'telugu', 'kannada', 'tamil'],
            img: 'images/therapist 2.png',
            desc: 'Psychosomatic practitioner supporting individuals through emotional trauma and deep inner rewiring for lasting change.',
        },
    ];
 
    const filterLoc = document.getElementById('filter-location');
    const filterSpec = document.getElementById('filter-spec');
    const filterLang = document.getElementById('filter-lang');
    const resetBtn = document.getElementById('reset-filters');
 
    const renderTherapists = (data) => {
        gridContainer.innerHTML = '';
 
        if (!data.length) {
            gridContainer.innerHTML = '<p style="color:var(--text-muted); text-align:center; grid-column:1/-1; padding:60px 0;">No therapists match your filters. Try adjusting your criteria.</p>';
            return;
        }
 
        data.forEach(t => {
            const card = document.createElement('div');
            card.classList.add('therapist-card-large');
            const langs = t.lang.map(l => l.charAt(0).toUpperCase() + l.slice(1)).join(' · ');
            card.innerHTML = `
                <div class="t-image-large" style="background-image:url('${t.img}')"></div>
                <h3>${t.name}</h3>
                <span class="t-spec">${t.specLabel}</span>
                <p style="font-size:0.9rem;color:var(--text-muted);margin-bottom:18px;line-height:1.6;">${t.desc}</p>
                <div class="t-details">
                    <span class="t-tag">📍 ${t.locationLabel}</span>
                    <span class="t-tag">🗣️ ${langs}</span>
                </div>
                <button class="btn btn-primary" style="width:100%;" onclick="window.location='register.html'">Book a Session</button>
            `;
            gridContainer.appendChild(card);
        });
    };
 
    const applyFilters = () => {
        const loc = filterLoc?.value || 'all';
        const spec = filterSpec?.value || 'all';
        const lang = filterLang?.value || 'all';
 
        const filtered = therapistsData.filter(t =>
            (loc === 'all' || t.location === loc) &&
            (spec === 'all' || t.spec.includes(spec)) &&
            (lang === 'all' || t.lang.includes(lang))
        );
        renderTherapists(filtered);
    };
 
    filterLoc?.addEventListener('change', applyFilters);
    filterSpec?.addEventListener('change', applyFilters);
    filterLang?.addEventListener('change', applyFilters);
    resetBtn?.addEventListener('click', () => {
        if (filterLoc) filterLoc.value = 'all';
        if (filterSpec) filterSpec.value = 'all';
        if (filterLang) filterLang.value = 'all';
        applyFilters();
    });
 
    renderTherapists(therapistsData);
}
 
// ============================================
// AUTH TABS (register page)
// ============================================
const authTabs = document.querySelectorAll('.auth-tab');
const registerForm = document.getElementById('register-form');
const loginForm = document.getElementById('login-form');
const authSwitchText = document.getElementById('auth-switch-text');
const authSwitchLink = document.getElementById('auth-switch-link');
 
if (authTabs.length && registerForm && loginForm) {
    const switchToTab = (tab) => {
        authTabs.forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
        if (tab === 'register') {
            registerForm.style.display = 'flex';
            loginForm.style.display = 'none';
            if (authSwitchText) authSwitchText.innerHTML = 'Already have an account? <a href="#" id="auth-switch-link">Sign in here</a>';
        } else {
            registerForm.style.display = 'none';
            loginForm.style.display = 'flex';
            if (authSwitchText) authSwitchText.innerHTML = "Don't have an account? <a href=\"#\" id=\"auth-switch-link\">Create one here</a>";
        }
        // Re-bind after innerHTML update
        document.getElementById('auth-switch-link')?.addEventListener('click', (e) => {
            e.preventDefault();
            switchToTab(tab === 'register' ? 'login' : 'register');
        });
    };
 
    const showAuthError = (form, message) => {
        let errEl = form.querySelector('.auth-error-msg');
        if (!errEl) {
            errEl = document.createElement('p');
            errEl.className = 'auth-error-msg';
            errEl.style.cssText = 'color:#c0392b; font-size:0.85rem; font-weight:600; margin:4px 0 0;';
            form.appendChild(errEl);
        }
        errEl.textContent = message;
    };
 
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const nameVal = document.getElementById('reg-name')?.value.trim() || '';
        const emailVal = document.getElementById('reg-email')?.value.trim() || '';
        const passwordVal = document.getElementById('reg-password')?.value || '';
        const submitBtn = registerForm.querySelector('[type="submit"]');
        if (submitBtn) submitBtn.disabled = true;
 
        try {
            const res = await fetch(`${API_BASE}/api/signup`, {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: nameVal, email: emailVal, password: passwordVal }),
            });
            const data = await res.json().catch(() => ({}));
            if (!res.ok) {
                showAuthError(registerForm, data.error || 'Could not create your account. Please try again.');
                return;
            }
            // Cache display info only (NOT credentials) for greeting the user in the UI
            localStorage.setItem('soulmi-user', JSON.stringify({ name: nameVal, email: emailVal }));
            window.location.href = 'dashboard.html';
        } catch (err) {
            console.error('Signup error:', err);
            showAuthError(registerForm, "Can't reach the server. Is the Flask backend running on port 5000?");
        } finally {
            if (submitBtn) submitBtn.disabled = false;
        }
    });
 
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const emailVal = document.getElementById('login-email')?.value.trim() || '';
        const passwordVal = document.getElementById('login-password')?.value || '';
        const submitBtn = loginForm.querySelector('[type="submit"]');
        if (submitBtn) submitBtn.disabled = true;
 
        try {
            const res = await fetch(`${API_BASE}/api/login`, {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: emailVal, password: passwordVal }),
            });
            const data = await res.json().catch(() => ({}));
            if (!res.ok) {
                showAuthError(loginForm, data.error || 'Invalid email or password.');
                return;
            }
            localStorage.setItem('soulmi-user', JSON.stringify({ name: data.name || 'there', email: emailVal }));
            window.location.href = 'dashboard.html';
        } catch (err) {
            console.error('Login error:', err);
            showAuthError(loginForm, "Can't reach the server. Is the Flask backend running on port 5000?");
        } finally {
            if (submitBtn) submitBtn.disabled = false;
        }
    });
 
    authTabs.forEach(tab => {
        tab.addEventListener('click', () => switchToTab(tab.dataset.tab));
    });
 
    authSwitchLink?.addEventListener('click', (e) => {
        e.preventDefault();
        const active = document.querySelector('.auth-tab.active');
        switchToTab(active?.dataset.tab === 'register' ? 'login' : 'register');
    });
}
 
// ============================================
// COMMUNITY TABS (community page)
// ============================================
const communityTabs = document.querySelectorAll('.community-tab');
 
if (communityTabs.length) {
    communityTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            communityTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
 
            document.querySelectorAll('.tab-panel').forEach(panel => {
                panel.style.display = 'none';
            });
            const target = document.getElementById(`tab-${tab.dataset.tab}`);
            if (target) target.style.display = 'block';
        });
    });
}
 
// ============================================
// RESOURCE FILTER CHIPS (resources page)
// ============================================
const filterChips = document.querySelectorAll('.filter-chip');
filterChips.forEach(chip => {
    chip.addEventListener('click', () => {
        filterChips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
    });
});