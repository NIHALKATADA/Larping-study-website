<script>
        let assistantApp = null;
let assistantCloseTimer = null;
let isAssistantOpen = false;

async function openAssistant() {
    if (document.querySelector('.ask-ai-btn')?.getAttribute('data-dragged') === 'true') return;
    
    const modal = document.getElementById('assistantModal');
    
    // Toggle closed if already open
    if (isAssistantOpen) {
        closeAssistant();
        return;
    }

    // Cancel any pending close timer from rapid clicks
    if (assistantCloseTimer) {
        clearTimeout(assistantCloseTimer);
        assistantCloseTimer = null;
    }

    isAssistantOpen = true;
    modal.style.display = 'flex';
    
    // Removed FAB hide so it stays visible
    
    // Force DOM reflow so transition plays reliably
    void modal.offsetHeight;
    
    modal.style.opacity = '1';
    modal.style.transform = 'translateY(0)';
    if (window.innerWidth > 768) {
        document.getElementById('assistantInput').focus();
    }

    if (!assistantApp) {
                try {
                    const { initAssistant } = await import('../../shared/assistant-ui.js');
                    assistantApp = await initAssistant('{{ subject_id }}');
                    if (!assistantApp) throw new Error("App init failed");
                } catch (e) {
                    console.error('Assistant init failed:', e);
                    const msgs = document.getElementById('assistantMessages');
                    const isFileProtocol = window.location.protocol === 'file:';
                    msgs.innerHTML = `<div class="msg assistant" style="background:rgba(255,0,0,0.1); border-left:3px solid red; padding:1rem; margin-top:0.5rem; border-radius:8px;">${isFileProtocol ? 'I am blocked by your browser\'s security settings because you opened me directly as a local file (file:///). To chat with me, you MUST use the live website or the local web server (http://localhost:8000).' : 'Assistant failed to initialize: ' + e.message}</div>`;
                }
            }
        }
        function closeAssistant() {
    const modal = document.getElementById('assistantModal');
    isAssistantOpen = false;
    
    // FAB stays independent now
    
    modal.style.opacity = '0';
    modal.style.transform = 'translateY(20px)';
    
    if (assistantCloseTimer) clearTimeout(assistantCloseTimer);
    assistantCloseTimer = setTimeout(() => {
        modal.style.display = 'none';
        assistantCloseTimer = null;
    }, 300);
}
        function submitAssistantQuery(q) {
            const input = document.getElementById('assistantInput');
            const query = q || input.value.trim();
            if (!query) return;
            if (!assistantApp) {
                const msgs = document.getElementById('assistantMessages');
                msgs.innerHTML = `<div class="msg assistant" style="background:rgba(255,0,0,0.1); border-left:3px solid red; padding:1rem; margin-top:0.5rem; border-radius:8px;">I am blocked by your browser's security settings because you opened me directly as a local file (file:///). To chat with me, you MUST use the live website or the local web server (http://localhost:8000).</div>`;
                return;
            }
            input.value = '';
            assistantApp.handleQuery(query);
        }
    </script>