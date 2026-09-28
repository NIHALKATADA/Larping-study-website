import { AssistantCore } from './assistant-core.js';

export async function initAssistant(subjectId) {
    let indexData = [];
    let aliases = {};
    
    try {
        const [indexRes, aliasesRes] = await Promise.all([
            fetch(`../../subjects/${subjectId}/assistant-index.json`),
            fetch(`../../shared/assistant-aliases.json`)
        ]);
        if (indexRes.ok) indexData = await indexRes.json();
        if (aliasesRes.ok) {
            const aliasData = await aliasesRes.json();
            aliases = aliasData.aliases || {};
        }
    } catch (e) {
        console.error("Assistant data load error:", e);
    }
    
    let core;
    try {
        const { AssistantLLM } = await import('./assistant-llm.js');
        core = new AssistantLLM(subjectId, aliases, indexData);
        window.assistantLLMInstance = core;
    } catch (e) {
        console.warn("Could not load AssistantLLM, falling back to Lite mode", e);
        core = new AssistantCore(subjectId, aliases, indexData);
        window.assistantLLMInstance = core;
        
        core.isDeepMode = false;
        core.setMode = function(mode) {
            if (mode === 'smart') {
                // Smart mode not available in fallback
                const sel = document.getElementById('aiModeSelect');
                if (sel) sel.value = this.isDeepMode ? 'deep' : 'lite';
                return;
            }
            this.isDeepMode = (mode === 'deep');
            const titleSpan = document.querySelector('#aiModalTitle span');
            const sel = document.getElementById('aiModeSelect');
            if (titleSpan) {
                if (this.isDeepMode) {
                    titleSpan.textContent = "(Deep Mode)";
                    titleSpan.style.color = "var(--primary-teal)";
                    if (sel) sel.value = 'deep';
                } else {
                    titleSpan.textContent = "(Lite)";
                    titleSpan.style.color = "var(--text-muted)";
                    if (sel) sel.value = 'lite';
                }
            }
        };
        core.toggleDeepMode = function(enabled) {
            this.setMode(enabled ? 'deep' : 'lite');
        };
        
        core.executeSmart = async function(text) {
            if (!this.isDeepMode) {
                return this.execute(text);
            }
            
            const msgs = document.getElementById('assistantMessages');
            const div = document.createElement('div');
            div.className = 'msg assistant';
            div.style.padding = '1rem';
            div.style.borderRadius = '8px';
            div.style.marginTop = '0.5rem';
            div.style.background = 'rgba(255,255,255,0.05)';
            div.style.borderLeft = '3px solid var(--primary-teal)';
            div.style.marginRight = '2rem';
            div.innerHTML = '<span class="typing-indicator"><span>.</span><span>.</span><span>.</span></span>';
            msgs.appendChild(div);
            msgs.scrollTo({ top: msgs.scrollHeight, behavior: 'smooth' });
            
            try {
                let messages = [
                    { role: 'system', content: 'You are a helpful study assistant. Use provided context to answer questions. Format mathematically using LaTeX where appropriate.' }
                ];
                
                let { rewrittenQuery } = this.routeIntent(text);
                let searchRes = this.search(rewrittenQuery);
                let contextStr = "Context:\n";
                if (searchRes.length > 0) {
                    searchRes.slice(0,3).forEach(r => contextStr += `${r.doc.title}:\n${r.doc.chunks.join(" ")}\n\n`);
                }
                messages.push({ role: 'user', content: `${contextStr}\n\nQuestion: ${text}` });

                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ messages, temperature: 0.5, max_tokens: 1024 })
                });
                
                if (!res.ok) throw new Error('API failed');
                const data = await res.json();
                
                let escaped = String(data.text).replace(/[&<>'"]/g, tag => ({
                    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
                }[tag]));
                escaped = escaped.replace(/`(?:[a-z]*)\n([\s\S]*?)`/g, '<pre style="background:rgba(0,0,0,0.5); padding:1rem; border-radius:8px; overflow-x:auto;"></pre>');
                escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong></strong>');
                escaped = escaped.replace(/([^]+)/g, '<code style="background:rgba(0,0,0,0.3); padding:0.1rem 0.3rem; border-radius:4px;"></code>');
                
                div.innerHTML = escaped;
            } catch (err) {
                console.warn('Deep mode failed, falling back', err);
                this.setMode('lite');
                
                div.style.borderLeft = '3px solid var(--subject-color)';
                div.innerHTML = "<em>Deep Mode API failed. Falling back to Lite Mode.</em>";
            }
        };
    }
    
    const ui = {
        core,
        handleQuery(query) {
            this.appendMessage('user', query);
            if (core.isSmartMode || core.isDeepMode) {
                core.executeSmart(query);
            } else {
                const res = core.execute(query);
                this.renderResponse(res);
            }
        },
        appendMessage(role, text) {
            const msgs = document.getElementById('assistantMessages');
            const div = document.createElement('div');
            div.className = `msg ${role}`;
            div.style.padding = '1rem';
            div.style.borderRadius = '8px';
            div.style.marginTop = '0.5rem';
            
            if (role === 'user') {
                div.style.background = 'rgba(255,255,255,0.1)';
                div.style.alignSelf = 'flex-end';
                div.style.marginLeft = '2rem';
            } else {
                div.style.background = 'rgba(255,255,255,0.05)';
                div.style.borderLeft = '3px solid var(--subject-color)';
                div.style.marginRight = '2rem';
            }
            
            div.textContent = text;
            msgs.appendChild(div);
            msgs.scrollTo({ top: msgs.scrollHeight, behavior: 'smooth' });
        },
        renderResponse(res) {
            const msgs = document.getElementById('assistantMessages');
            const div = document.createElement('div');
            div.className = 'msg assistant';
            div.style.padding = '1rem';
            div.style.borderRadius = '8px';
            div.style.marginTop = '0.5rem';
            div.style.background = 'rgba(255,255,255,0.05)';
            div.style.borderLeft = '3px solid var(--subject-color)';
            div.style.marginRight = '2rem';
            
            const escapeHTML = str => String(str).replace(/[&<>'"]/g, tag => ({
                '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
            }[tag]));

            let html = '';
            
            if (res.introText) {
                html += `<p style="margin-bottom: 0.5rem;"><em>${escapeHTML(res.introText)}</em></p>`;
            }
            
            if (res.intent === 'quiz') {
                html += `<p>${res.result}</p>`;
            } else if (res.intent === 'progress') {
                html += `<p>You have reviewed <strong>${res.result.done}</strong> out of ${res.result.total} questions (${res.result.percent}%).</p>`;
            } else if (res.intent === 'getQuestion' && res.result) {
                html += `<p>Here is Q${res.result.q_num}: <strong>${escapeHTML(res.result.title)}</strong></p>
                <div style="background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 8px; margin-top: 0.5rem; font-size: 0.9em;">
                    <em>From your question bank:</em><br/>
                    ${res.result.chunks.slice(0,2).map(escapeHTML).join('<br/><br/>')}
                </div>
                <a href="${res.result.url}" onclick="return !appUtilsOpenCard('${res.result.id}');" style="display:inline-block; margin-top:0.5rem; color:var(--primary-teal);">Read full answer</a>`;
            } else if (res.result && Array.isArray(res.result) && res.result.length > 0) {
                if (res.intent === 'search') {
                    const topMatch = res.result[0];
                    if (topMatch.score < 4.0) {
                        html += `<p>I am an offline study assistant. I couldn't find any relevant study material for your query.</p>
                        <p style="color:var(--primary-teal);"><strong>Please enable Smart Mode or Deep Mode to ask general knowledge questions.</strong></p>`;
                    } else if (topMatch.score > 2.5) {
                        html += `<p>Here is the best match for your query:</p>
                        <div style="background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 8px; margin-top: 0.5rem; font-size: 0.9em; border: 1px solid rgba(255,255,255,0.05);">
                            <div style="font-weight: bold; margin-bottom: 0.5rem; color: var(--primary-teal);">${escapeHTML(topMatch.doc.title)}</div>
                            <em>From your question bank:</em><br/><br/>
                            ${topMatch.doc.chunks.slice(0,2).map(escapeHTML).join('<br/><br/>')}
                        </div>
                        <a href="${topMatch.doc.url}" onclick="return !appUtilsOpenCard('${topMatch.doc.id}');" style="display:inline-block; margin-top:0.5rem; color:var(--primary-teal); margin-bottom: 1rem;">Read full answer</a>
                        <p>Other related questions:</p>`;

                    } else {
                        html += `<p>I couldn't find a strong exact match in the question bank, but here are some related topics:</p>`;
                    }
                } else if (res.intent === 'topQuestions') html += `<p>Here are some top questions you should look at:</p>`;
                else if (res.intent === 'nextToRevise') html += `<p>Here is what I recommend revising next:</p>`;
                
                html += `<div style="display:flex; flex-direction:column; gap:0.5rem; margin-top:0.5rem;">`;
                res.result.forEach((qObj, index) => {
                    const q = qObj.doc || qObj; // Handle both direct array and BM25 score objects
                    if (res.intent === 'search' && index === 0 && qObj.score > 2.5) return; // Skip if already shown as top match
                    html += `
                    <div style="background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
                        <a href="${q.url}" onclick="return !appUtilsOpenCard('${q.id}');" style="color: white; text-decoration: none; font-weight: bold; display: block;">${q.type === 'question' ? 'Q'+q.q_num+'. ' : ''}${escapeHTML(q.title)}</a>
                        ${q.type === 'question' ? `<div style="font-size: 0.8em; color: var(--text-muted); margin-top:0.25rem;">Unit ${q.unit} &bull; ${q.marks} Marks ${q.reason ? `&bull; ${escapeHTML(q.reason)}` : ''}</div>` : ''}
                    </div>`;
                });
                html += `</div>`;
            } else {
                html += `<p>I couldn't find anything matching your request.</p>`;
            }
            
            div.innerHTML = html;
            msgs.appendChild(div);
            msgs.scrollTo({ top: msgs.scrollHeight, behavior: 'smooth' });
        }
    };
    
    // Attach helper to window for deep links
    window.appUtilsOpenCard = function(id) {
        const el = document.getElementById(id);
        if (el) {
            if (typeof closeAssistant === 'function') closeAssistant();
            el.open = true;
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            return true;
        }
        return false;
    };
    

    // --- History Persistence ---
    const msgsContainer = document.getElementById('assistantMessages');
    const historyKey = 'assistant_history_' + subjectId;
    if (msgsContainer) {
        const savedHistory = sessionStorage.getItem(historyKey);
        if (savedHistory) {
            msgsContainer.innerHTML = savedHistory;
        }
        
        const observer = new MutationObserver(() => {
            sessionStorage.setItem(historyKey, msgsContainer.innerHTML);
        });
        observer.observe(msgsContainer, { childList: true, subtree: true, characterData: true });
    }
    // ---------------------------
    
    // Set Deep Mode as default on open
    if (core.setMode) {
        core.setMode('deep');
        const sel = document.getElementById('aiModeSelect');
        if (sel) sel.value = 'deep';
    }
    
    return ui;
}
