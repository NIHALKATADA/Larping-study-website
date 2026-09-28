import { AssistantCore } from "./assistant-core.js";

export class AssistantLLM extends AssistantCore {
    constructor(subjectId, aliases, indexData) {
        super(subjectId, aliases, indexData);
        this.ui = null;
        this.isDeepMode = false;
        this.history = []; 
    }

    toggleDeepMode(enabled) {
        this.isDeepMode = enabled;
        const titleSpan = document.querySelector('#aiModalTitle span');
        if (titleSpan) {
            if (this.isDeepMode) {
                titleSpan.textContent = "(Deep Mode)";
                titleSpan.style.color = "var(--primary-teal)";
            } else {
                titleSpan.textContent = "(Lite)";
                titleSpan.style.color = "var(--text-muted)";
            }
        }
    }

    renderSafeMarkdown(text) {
        let escaped = String(text).replace(/[&<>'"]/g, tag => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
        }[tag]));
        escaped = escaped.replace(/```(?:[a-z]*)\n([\s\S]*?)```/g, '<pre style="background:rgba(0,0,0,0.5); padding:1rem; border-radius:8px; overflow-x:auto;">$1</pre>');
        escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        escaped = escaped.replace(/`([^`]+)`/g, '<code style="background:rgba(0,0,0,0.3); padding:0.1rem 0.3rem; border-radius:4px;">$1</code>');
        escaped = escaped.replace(/\n/g, '<br/>');
        return escaped;
    }

    async *generate(messages, opts = {}) {
        const temp = opts.temperature !== undefined ? opts.temperature : 0.3;
        const max_tokens = opts.max_tokens || 300;
        
        if (this.isDeepMode) {
            let retries = 3;
            let delay = 1000;
            while (retries > 0) {
                try {
                    const res = await fetch('/api/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ messages, temperature: temp, max_tokens })
                    });
                    
                    if (res.status === 503 || res.status === 502) {
                        retries--;
                        if (retries === 0) throw new Error(`API overloaded after retries (${res.status})`);
                        console.warn(`Deep mode API overloaded (${res.status}), retrying in ${delay}ms...`);
                        await new Promise(r => setTimeout(r, delay));
                        delay *= 2;
                        continue;
                    }
                    
                    if (!res.ok) throw new Error(`API failed with status ${res.status}`);
                    const data = await res.json();
                    yield { choices: [{ delta: { content: data.text } }] };
                    return;
                } catch (e) {
                    if (retries > 0 && e.message.includes('overloaded')) {
                        continue;
                    }
                    console.warn('Deep mode failed, falling back', e);
                    this.toggleDeepMode(false);
                    const sel = document.getElementById('deepModeToggle');
                    if (sel) sel.checked = false;
                    this.ui.appendMessage('assistant', "Deep mode unavailable. Falling back to Lite mode.");
                    break;
                }
            }
        }
        
        yield { choices: [{ delta: { content: "I am in Lite mode and cannot generate text, but I found some references." } }] };
    }

    async executeSmart(text) {
        if (!this.isDeepMode) {
            return super.execute(text);
        }

        const msgs = document.getElementById('assistantMessages');
        const div = document.createElement('div');
        div.className = 'msg assistant';
        div.style.padding = '1rem';
        div.style.borderRadius = '8px';
        div.style.marginTop = '0.5rem';
        div.style.background = 'rgba(255,255,255,0.05)';
        div.style.borderLeft = '3px solid var(--subject-color)';
        div.style.marginRight = '2rem';
        
        let containerHtml = `<div class="llm-response-content" style="white-space:pre-wrap; line-height:1.5;">Thinking...</div>
        <div style="margin-top:1rem; display:flex; gap:0.5rem;">
            <button class="btn btn-secondary stop-btn" style="font-size:0.8em; padding:0.3rem 0.6rem;">Stop</button>
            <button class="btn btn-secondary regen-btn" style="display:none; font-size:0.8em; padding:0.3rem 0.6rem;">Regenerate</button>
        </div>`;
        div.innerHTML = containerHtml;
        msgs.appendChild(div);
        msgs.scrollTo({ top: msgs.scrollHeight, behavior: 'smooth' });

        const contentDiv = div.querySelector('.llm-response-content');
        const stopBtn = div.querySelector('.stop-btn');
        const regenBtn = div.querySelector('.regen-btn');

        let isStopped = false;
        stopBtn.onclick = () => { 
            isStopped = true; 
            stopBtn.style.display = 'none'; 
        };
        regenBtn.onclick = () => {
            div.remove();
            this.executeSmart(text);
        };

        let { intent, params } = this.routeIntent(text);
        
        if (intent === 'search' && !params.unit && !params.marks && !params.qId && text.length < 50 && !text.includes('?')) {
            try {
                contentDiv.innerHTML = '<em>Analyzing intent...</em>';
                const jsonPrompt = `Extract intent, subject, unit, marks, n, query from: "${text}". Valid intents: search, getQuestion, progress, topQuestions, nextToRevise, quiz. Output valid JSON only.`;
                let outText = '';
                const stream = this.generate([{role: "user", content: jsonPrompt}], { temperature: 0, max_tokens: 150 });
                for await (const chunk of stream) {
                    outText += chunk.choices[0]?.delta?.content || "";
                }
                const parsed = JSON.parse(outText.replace(/```json/g, '').replace(/```/g, '').trim());
                if (parsed) {
                    if (parsed.intent) intent = parsed.intent;
                    Object.assign(params, parsed);
                }
            } catch (e) {
                console.error("JSON mode extraction failed", e);
            }
        }

        if (['topQuestions', 'progress', 'nextToRevise'].includes(intent)) {
            let resObj = null;
            if (intent === 'topQuestions') resObj = this.topQuestions(params);
            else if (intent === 'progress') resObj = this.progress();
            else if (intent === 'nextToRevise') resObj = this.nextToRevise();
            
            let introText = "";
            try {
                const introPrompt = `Generate a brief, friendly one-line introduction for the user's request: "${text}". The intent is ${intent}.`;
                const stream = this.generate([{role: "user", content: introPrompt}], { temperature: 0.3, max_tokens: 50 });
                for await (const chunk of stream) {
                    introText += chunk.choices[0]?.delta?.content || "";
                }
                introText = introText.trim();
            } catch(e) {}
            
            div.remove();
            this.ui.renderResponse({ intent, params, result: resObj, introText });
            return;
        }

        if (intent === 'quiz') {
            div.remove();
            this.ui.renderResponse({ intent, params, result: "Ready for a quiz? Go to the interactive quiz page from the dashboard!" });
            return;
        }

        const searchResults = this.bm25Search(text);
        let notesText = "";
        let referenceHtml = "";
        
        let relevant = searchResults.filter(r => r.score > 2.0);
        
        if (relevant.length > 0) {
            let chunks = relevant.slice(0, 3).map(r => `[Q${r.doc.q_num}]: ${r.doc.chunks.join(" ").substring(0, 400)}`);
            notesText = chunks.join("\n\n");
            referenceHtml = `<div style="margin-top:1rem; padding:0.75rem; background:rgba(0,0,0,0.3); border-radius:8px; font-size:0.85em; color:var(--text-muted);"><strong>References:</strong> ${relevant.slice(0,3).map(r => `<a href="?open=${r.doc.id}" onclick="appUtilsOpenCard('${r.doc.id}'); return false;" style="color:var(--primary-teal);">Q${r.doc.q_num}</a>`).join(", ")}</div>`;
        } else {
            referenceHtml = `<div style="margin-top:1rem; padding:0.75rem; background:rgba(0,0,0,0.3); border-radius:8px; font-size:0.85em; color:var(--text-muted);"><em>General answer (not from your question bank)</em><br/>Related links: ${searchResults.slice(0,3).map(r => `<a href="?open=${r.doc.id}" onclick="appUtilsOpenCard('${r.doc.id}'); return false;" style="color:var(--primary-teal);">Q${r.doc.q_num}</a>`).join(", ")}</div>`;
        }

        let sysPrompt = `You are an expert exam tutor for ${this.subjectId.toUpperCase()} at university B.Tech level.
Format answers based on marks (if asked):
- 2m: 2-3 lines
- 3m: definition + points + example
- 5m: definition, explanation, diagram (ASCII or description), example, exam tip.
Keep runnable code/SQL minimal. Say "I'm not sure" rather than bluff.
If reference notes are provided, cite question numbers like [Q12].`;

        let messages = [{role: "system", content: sysPrompt}];
        if (notesText) {
            messages.push({role: "system", content: "Reference notes:\n" + notesText});
        }
        
        // Keep last few conversation turns for context
        const maxTurns = 4;
        this.history.slice(-(maxTurns * 2)).forEach(m => messages.push(m));
        
        messages.push({role: "user", content: text});

        try {
            const stream = this.generate(messages, { temperature: 0.3, max_tokens: params.marks ? params.marks * 100 : 300 });
            contentDiv.innerHTML = '';
            let fullText = '';
            
            for await (const chunk of stream) {
                if (isStopped) break;
                const content = chunk.choices[0]?.delta?.content || "";
                fullText += content;
                contentDiv.innerHTML = this.renderSafeMarkdown(fullText);
            }
            
            if (referenceHtml) {
                contentDiv.insertAdjacentHTML('beforeend', referenceHtml);
            }
            
            this.history.push({role: "user", content: text});
            this.history.push({role: "assistant", content: fullText});
            
            stopBtn.style.display = 'none';
            regenBtn.style.display = 'block';

        } catch (e) {
            contentDiv.innerHTML = "<em>Error generating response.</em>";
            console.error(e);
        }
    }
}
