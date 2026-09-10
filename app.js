(function () {
    const recentKey = 'sanskritisetu-recent-explorations';

    function getRecentExplorations() {
        try {
            return JSON.parse(localStorage.getItem(recentKey) || '[]');
        } catch (error) {
            return [];
        }
    }

    function saveRecentExploration(title) {
        const recent = [title, ...getRecentExplorations().filter(item => item !== title)].slice(0, 4);
        localStorage.setItem(recentKey, JSON.stringify(recent));
        renderRecentExplorations();
    }

    function renderRecentExplorations() {
        const container = document.getElementById('recentExplorations');
        const recent = getRecentExplorations();
        if (!container || !recent.length) return;

        container.hidden = false;
        container.innerHTML = '<span>Recently explored</span>';
        recent.forEach(title => {
            const button = document.createElement('button');
            button.type = 'button';
            button.textContent = title;
            button.addEventListener('click', () => {
                const input = document.getElementById('heritageSearchInput');
                input.value = title;
                updateHeritageView(title);
                document.querySelector('.immersive-card').scrollIntoView({ behavior: 'smooth', block: 'center' });
            });
            container.appendChild(button);
        });
    }

    function setupGuidePrompts() {
        document.querySelectorAll('[data-guide-prompt]').forEach(button => {
            button.addEventListener('click', () => {
                const input = document.getElementById('userInput');
                input.value = button.dataset.guidePrompt;
                input.focus();
            });
        });
    }

    function setupVoiceInput() {
        const button = document.getElementById('voiceInputBtn');
        const input = document.getElementById('userInput');
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!button || !SpeechRecognition) {
            if (button) button.hidden = true;
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.lang = 'en-IN';
        recognition.interimResults = false;

        button.addEventListener('click', () => {
            recognition.start();
            button.classList.add('listening');
            button.setAttribute('aria-label', 'Listening');
        });

        recognition.addEventListener('result', event => {
            input.value = event.results[0][0].transcript;
            input.focus();
        });

        recognition.addEventListener('end', () => {
            button.classList.remove('listening');
            button.setAttribute('aria-label', 'Ask by voice');
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        setupGuidePrompts();
        setupVoiceInput();
        renderRecentExplorations();

        document.getElementById('heritageSearchBtn').addEventListener('click', () => {
            const title = document.getElementById('heritageSearchInput').value.trim();
            if (title) saveRecentExploration(title);
        });
    });
})();