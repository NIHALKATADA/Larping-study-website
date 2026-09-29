import { prebuiltAppConfig, CreateWebWorkerMLCEngine, hasModelInCache, deleteModelAllInfoInCache } from "https://esm.run/@mlc-ai/web-llm@0.2.85";
import { AssistantCore } from "./assistant-core.js";

export class AssistantLLM extends AssistantCore {
    constructor(subjectId, aliases, indexData) {
        super(subjectId, aliases, indexData);
        this.engine = null;
        this.modelId = null;
        this.ui = null;
        this.isSmartMode = false;
        this.smartPending = false;
        this.isDeepMode = false;
        this.history = []; 
        this.contextWindow = 4096;
        this.modelTiers = {};
    }

    setMode(mode) {
        this.isDeepMode = (mode === 'deep');
        
        if (mode === 'lite' || mode === 'deep') {
            this.isSmartMode = false;
            this.smartPending = false;
        }

        if (mode === 'smart') {
            if (this.engine) {
                this.isSmartMode = true;
            } else {
                this.smartPending = true;
                localStorage.removeItem('smartModeDismissed');
                if (this.ui) {
                    this.initSmartMode(this.ui);
                }
            }
        }
        
        this._updateTitle();
    }

    toggleDeepMode(enabled) {
        this.setMode(enabled ? 'deep' : (this.isSmartMode ? 'smart' : 'lite'));
    }

    _updateTitle() {
        const titleSpan = document.querySelector('#aiModalTitle span');
        const sel = document.getElementById('aiModeSelect');
        
        let activeModel = this.isDeepMode ? "Qwen 2.5 27B (Cloud API)" : 
                         (this.isSmartMode ? (this.modelId || "Llama (Local WebGPU)") : "Offline Search (No AI)");
                         
        const msgsContainer = document.getElementById('assistantMessages');
        if (msgsContainer) {
            const firstMsg = msgsContainer.firstElementChild;
            if (firstMsg && firstMsg.classList.contains('assistant') && firstMsg.innerText.includes("Hi! I'm your study assistant.")) {
                firstMsg.innerHTML = `Hi! I'm your study assistant. I am currently powered by <strong>${activeModel}</strong>. Ask me to find questions, summarize concepts, or recommend what to revise next.`;
            }
        }

        if (titleSpan) {
            if (this.isDeepMode) {
                titleSpan.textContent = "(Deep Mode)";
                titleSpan.style.color = "var(--primary-teal)";
                if (sel) sel.value = 'deep';
            } else if (this.isSmartMode) {
                let tierLabel = "";
                if (this.modelId) {
                    if (this.modelId.match(/1[\.\d]*B/i)) tierLabel = " - 1B";
                    else if (this.modelId.match(/3[\.\d]*B/i)) tierLabel = " - 3B";
                    else if (this.modelId.match(/[78]B/i)) tierLabel = " - 8B";
                }
                titleSpan.textContent = "(Smart" + tierLabel + ")";
                titleSpan.style.color = "var(--primary-teal)";
                if (sel) sel.value = 'smart';
            } else if (this.smartPending) {
                titleSpan.textContent = "(Smart - Select Model)";
                titleSpan.style.color = "var(--primary-teal)";
                if (sel) sel.value = 'smart';
            } else {
                titleSpan.textContent = "(Lite)";
                titleSpan.style.color = "var(--text-muted)";
                if (sel) sel.value = 'lite';
            }
        }
    }


    async initSmartMode(uiObj) {
        this.ui = uiObj;
        if (localStorage.getItem('smartModeDismissed') === 'true') {
            return;
        }
        if (!navigator.gpu) {
            this.ui.appendMessage('assistant', "Smart Mode unavailable: Your browser doesn't support WebGPU. I'll stay in Lite mode.");
            return;
        }
        try {
            const adapter = await navigator.gpu.requestAdapter();
            if (!adapter) {
                this.ui.appendMessage('assistant', "Smart Mode unavailable: WebGPU adapter not found. I'll stay in Lite mode.");
                return;
            }

            // Estimate limits
            let maxBufferSize = adapter.limits ? adapter.limits.maxBufferSize : 0;
            let maxStorage = adapter.limits ? adapter.limits.maxStorageBufferBindingSize : 0;
            let maxVramGb = Math.max(maxBufferSize, maxStorage) / (1024*1024*1024);
            let devMem = navigator.deviceMemory || 0; // Caps at 8 on many browsers

            let sizeClass = '1b'; // default for safety
            
            // If device has >4GB system memory AND >2.5GB adapter limits, suggest 3B
            // maxVramGb will be 0 if the browser doesn't expose adapter limits
            if ((devMem > 4 && maxVramGb > 2.5) || maxVramGb >= 3.0) {
                sizeClass = '3b';
            }
            if (maxVramGb >= 6.0) {
                sizeClass = '7b';
            }

            let usedStats = [];
            if (devMem) usedStats.push(`${devMem}GB RAM (capped)`);
            if (maxVramGb) usedStats.push(`~${maxVramGb.toFixed(1)}GB adapter limit`);
            let limitsMsg = usedStats.length ? `Detected: ${usedStats.join(', ')}` : 'Could not detect memory limits accurately';

            const models = prebuiltAppConfig.model_list.filter(m => {
                const id = m.model_id.toLowerCase();
                if (!id.includes('instruct') && !id.includes('it')) return false;
                if (!id.includes('qwen') && !id.includes('llama') && !id.includes('phi') && !id.includes('gemma')) return false;
                if (!id.includes('q4f16_1') && !id.includes('q4f32_1')) return false;
                return true;
            });

            const rankModel = (m) => {
                let score = 0;
                const id = m.model_id.toLowerCase();
                if (id.includes('llama-3.2')) score += 10;
                else if (id.includes('llama-3.1')) score += 8;
                else if (id.includes('deepseek-r1')) score += 9;
                else if (id.includes('llama-3')) score += 5;
                if (id.includes('q4f16_1')) score += 2;
                return score;
            };

            const models1B = models.filter(m => m.model_id.match(/1[\.\d]*b/i) || m.model_id.match(/2b/i)).sort((a,b)=>rankModel(b)-rankModel(a));
            const models3B = models.filter(m => m.model_id.match(/3[\.\d]*b/i) || m.model_id.match(/4b/i) || m.model_id.includes('phi')).sort((a,b)=>rankModel(b)-rankModel(a));
            const models7B = models.filter(m => m.model_id.match(/7b/i) || m.model_id.match(/8b/i)).sort((a,b)=>rankModel(b)-rankModel(a));
            
            this.modelTiers = { '1b': models1B, '3b': models3B, '7b': models7B };

            const preferredModel = localStorage.getItem('preferredSmartModel');
            const preferredTier = localStorage.getItem('preferredSmartTier') || sizeClass;
            
            if (preferredModel) {
                this.downloadAndLoadModel(preferredModel, preferredTier);
                return;
            }

            this.showModelSelection(models1B, models3B, models7B, sizeClass, limitsMsg);
        } catch (e) {
            console.error("WebGPU check failed:", e);
            this.ui.appendMessage('assistant', "Smart Mode unavailable: Error checking WebGPU. I'll stay in Lite mode.");
        }
    }

    async showModelSelection(m1, m3, m7, recommendedClass, limitsMsg) {
        const div = document.createElement('div');
        div.className = 'msg assistant';
        div.style.padding = '1rem';
        div.style.borderRadius = '8px';
        div.style.marginTop = '0.5rem';
        div.style.background = 'rgba(255,255,255,0.05)';
        div.style.borderLeft = '3px solid var(--primary-teal)';
        div.style.marginRight = '2rem';
        div.id = 'model-selection-ui';

        let html = `<div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <h4 style="margin-top:0;">Enable Smart Mode (In-Browser LLM)</h4>
            <button onclick="localStorage.setItem('smartModeDismissed', 'true'); document.getElementById('model-selection-ui').style.display='none';" style="background:none; border:none; color:var(--text-muted); cursor:pointer; font-size:0.8em; text-decoration:underline;">Dismiss permanently</button>
        </div>
        <p style="font-size:0.9em; color:var(--text-muted);">${limitsMsg}. Recommended tier: ${recommendedClass.toUpperCase()}</p>
        <p style="font-size:0.8em; color:var(--text-muted);">Default Llama 3.2 3B is recommended for best balance of quality and performance on laptops. <strong>If your laptop does not have a dedicated GPU, use the 1B model.</strong></p>
        <div style="display:flex; flex-direction:column; gap:0.5rem; margin-top:1rem;">`;

        const renderOption = async (modelArray, label, isRec, tier) => {
            if (!modelArray.length) return '';
            const m = modelArray[0];
            let cached = false;
            try {
                cached = await hasModelInCache(m.model_id);
            } catch(e) {}
            
            return `
            <div style="background:rgba(0,0,0,0.3); padding:0.75rem; border-radius:8px; display:flex; justify-content:space-between; align-items:center; border: 1px solid ${isRec ? 'var(--primary-teal)' : 'transparent'}">
                <div>
                    <div style="font-weight:bold;">${label} ${isRec ? '<span style="color:var(--primary-teal); font-size:0.8em;">(Recommended)</span>' : ''} ${cached ? '<span style="color:#4caf50; font-size:0.8em; margin-left:8px;">[Downloaded \u2713]</span>' : ''}</div>
                    <div style="font-size:0.8em; color:var(--text-muted);">${m.model_id} (${Math.round(m.vram_required_MB || 0)} MB VRAM)</div>
                </div>
                <button class="btn btn-primary" onclick="window.assistantLLMInstance.downloadAndLoadModel('${m.model_id}', '${tier}')">${cached ? 'Load Model' : 'Download & Load'}</button>
            </div>`;
        };

        html += await renderOption(m1, "1B (Phones and iGPU Laptops)", recommendedClass === '1b', '1b');
        html += await renderOption(m3, "3B (Dedicated GPUs)", recommendedClass === '3b', '3b');

        html += `</div>`;
        div.innerHTML = html;
        const msgs = document.getElementById('assistantMessages');
        msgs.appendChild(div);
        msgs.scrollTo({ top: msgs.scrollHeight, behavior: 'smooth' });
    }

    async downloadAndLoadModel(modelId, tier) {
        this.modelId = modelId;
        localStorage.setItem('preferredSmartModel', modelId);
        if (tier) localStorage.setItem('preferredSmartTier', tier);
        
        let selUi = document.getElementById('model-selection-ui');
        if (!selUi) {
            selUi = document.createElement('div');
            selUi.className = 'msg assistant';
            selUi.style.padding = '1rem';
            selUi.style.borderRadius = '8px';
            selUi.style.marginTop = '0.5rem';
            selUi.style.background = 'rgba(255,255,255,0.05)';
            selUi.style.borderLeft = '3px solid var(--primary-teal)';
            selUi.style.marginRight = '2rem';
            selUi.id = 'model-selection-ui';
            const msgs = document.getElementById('assistantMessages');
            msgs.appendChild(selUi);
            msgs.scrollTo({ top: msgs.scrollHeight, behavior: 'smooth' });
        }
        
        selUi.innerHTML = `<h4>Loading Model: ${modelId}</h4><div id="model-progress">Starting engine...</div><div class="skel-line" style="height:4px; width:100%; border-radius:2px; margin-top:0.5rem; background:rgba(255,255,255,0.1);"><div id="model-progress-bar" style="height:100%; width:0%; background:var(--primary-teal); transition:width 0.2s;"></div></div>`;

        try {
            const workerUrl = new URL('./assistant-worker.js', import.meta.url);
            
            const modelRec = prebuiltAppConfig.model_list.find(m => m.model_id === this.modelId);
            if (modelRec && modelRec.overrides && modelRec.overrides.context_window_size) {
                this.contextWindow = modelRec.overrides.context_window_size;
            } else {
                this.contextWindow = 4096;
            }

            this.engine = await CreateWebWorkerMLCEngine(
                new Worker(workerUrl, { type: 'module' }),
                this.modelId,
                {
                    initProgressCallback: (progress) => {
                        const progressText = selUi ? selUi.querySelector('#model-progress') : document.getElementById('model-progress');
                        const progressBar = selUi ? selUi.querySelector('#model-progress-bar') : document.getElementById('model-progress-bar');
                        if (progressText) progressText.innerText = progress.text;
                        if (progressBar && progress.progress) progressBar.style.width = Math.round(progress.progress * 100) + '%';
                    }
                }
            );
            
            this.isSmartMode = true;
            this._updateTitle();
            if (selUi) {
                selUi.innerHTML = `<h4>Smart Mode Active</h4><p style="font-size:0.9em; color:var(--text-muted);">Model: ${this.modelId} (Ready / Cached)<br/>Context budget: ${this.contextWindow} tokens</p>
                <button class="btn btn-secondary" onclick="window.assistantLLMInstance.deleteModel()" style="margin-top:0.5rem; font-size:0.8em; padding:0.2rem 0.5rem;">Delete Model Data</button>`;
            }
        } catch (e) {
            console.error("Model load failed:", e);
            if (e.message.toLowerCase().includes('memory') || e.message.toLowerCase().includes('oom') || e.message.toLowerCase().includes('device lost') || e.message.toLowerCase().includes('buffer size')) {
                let nextTier = null;
                if (tier === '7b') nextTier = '3b';
                else if (tier === '3b') nextTier = '1b';

                if (nextTier && this.modelTiers[nextTier] && this.modelTiers[nextTier].length > 0) {
                    const fallbackModel = this.modelTiers[nextTier][0].model_id;
                    this.ui.appendMessage('assistant', `Device ran out of memory. Automatically retrying with a smaller tier: ${fallbackModel}`);
                    return this.downloadAndLoadModel(fallbackModel, nextTier);
                } else {
                    this.ui.appendMessage('assistant', "Device ran out of memory. No smaller tier available to retry. Staying in Lite mode.");
                    if (selUi) selUi.innerHTML = `<h4>Smart Mode Failed</h4><p style="font-size:0.9em; color:var(--text-muted);">Out of memory.</p>`;
                }
            } else {
                if (selUi) selUi.innerHTML = `<h4>Smart Mode Failed</h4><p style="font-size:0.9em; color:var(--text-muted);">Error loading model: ${e.message}</p>`;
            }
        }
    }

    async deleteModel() {
        const targetModel = this.modelId || localStorage.getItem('preferredSmartModel');
        if (!targetModel) {
            this.ui.appendMessage('assistant', "No model is currently cached or selected.");
            return;
        }
        try {
            await deleteModelAllInfoInCache(targetModel);
            localStorage.removeItem('preferredSmartModel');
            localStorage.removeItem('preferredSmartTier');
            this.modelId = null;
            this.engine = null;
            this.isSmartMode = false;
            
            // Also revert the UI to Deep Mode
            this.setMode('deep');
            const sel = document.getElementById('aiModeSelect');
            if (sel) sel.value = 'deep';

            this.ui.appendMessage('assistant', "Model data deleted from cache. The assistant has been reverted to Deep Mode.");
        } catch (e) {
            console.error("Cache deletion error", e);
            this.ui.appendMessage('assistant', "Failed to delete cache. See console for details.");
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
            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ messages, temperature: temp, max_tokens })
                });
                if (!res.ok) {
                    const errTxt = await res.text();
                    console.error("Deep Mode API error details:", res.status, errTxt);
                    throw new Error('API failed: ' + errTxt);
                }
                const data = await res.json();
                yield { choices: [{ delta: { content: data.text } }] };
                return;
            } catch (e) {
                console.warn('Deep mode failed, falling back', e);
                this.toggleDeepMode(false);
                const sel = document.getElementById('deepModeToggle');
                if (sel) sel.checked = false;
                this.ui.appendMessage('assistant', "Deep mode unavailable. Falling back to local model.");
            }
        }
        
        if (this.isSmartMode && this.engine) {
            try {
                const stream = await this.engine.chat.completions.create({
                    messages,
                    temperature: temp,
                    max_tokens: max_tokens,
                    stream: true
                });
                for await (const chunk of stream) {
                    yield chunk;
                }
                return;
            } catch (e) {
                console.error("Smart mode generate failed:", e);
                this.ui.appendMessage('assistant', "Smart mode failed. Falling back to Lite mode.");
            }
        }
        
        yield { choices: [{ delta: { content: "I am in Lite mode and cannot generate text, but I found some references." } }] };
    }

    async executeSmart(text) {
        if (!this.isDeepMode && (!this.isSmartMode || !this.engine)) {
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
            if (this.engine) this.engine.interruptGenerate().catch(() => {});
        };
        regenBtn.onclick = () => {
            div.remove();
            this.executeSmart(text);
        };

        let { intent, params } = this.routeIntent(text);
        
        // Removed slow LLM-based secondary intent extraction pass to improve responsiveness.

        if (['topQuestions', 'progress', 'nextToRevise'].includes(intent)) {
            let resObj = null;
            if (intent === 'topQuestions') resObj = this.topQuestions(params);
            else if (intent === 'progress') resObj = this.progress();
            else if (intent === 'nextToRevise') resObj = this.nextToRevise();
            
            let introText = "";
            if (intent === 'topQuestions') introText = "Here are the most important questions you requested:";
            else if (intent === 'progress') introText = "Here is your current progress overview:";
            else if (intent === 'nextToRevise') introText = "Based on your progress, I recommend focusing on these topics next:";
            
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
            let chunks = relevant.slice(0, 3).map(r => [Q | Score:  | Important: ]: );
            notesText = chunks.join("\n\n");
            referenceHtml = `<div style="margin-top:1rem; padding:0.75rem; background:rgba(0,0,0,0.3); border-radius:8px; font-size:0.85em; color:var(--text-muted);"><strong>References:</strong> ${relevant.slice(0,3).map(r => `<a href="?open=${r.doc.id}" onclick="appUtilsOpenCard('${r.doc.id}'); return false;" style="color:var(--primary-teal);">Q${r.doc.q_num}</a>`).join(", ")}</div>`;
        } else {
            referenceHtml = `<div style="margin-top:1rem; padding:0.75rem; background:rgba(0,0,0,0.3); border-radius:8px; font-size:0.85em; color:var(--text-muted);"><em>General answer (not from your question bank)</em><br/>Related links: ${searchResults.slice(0,3).map(r => `<a href="?open=${r.doc.id}" onclick="appUtilsOpenCard('${r.doc.id}'); return false;" style="color:var(--primary-teal);">Q${r.doc.q_num}</a>`).join(", ")}</div>`;
        }

        let activeModel = this.isDeepMode ? "Qwen 2.5 27B (Groq Cloud API)" : (this.modelId || "Llama 3.2 (Local WebGPU)");
        
        let sysPrompt = `You are a highly intelligent and helpful study assistant for ${this.subjectId.toUpperCase()} at a university B.Tech level.
You are currently powered by the ${activeModel} AI model. If the user asks who you are or what model you are, proudly tell them this!
You are integrated into "Revision Hub", a premium study portal with a Black Glass aesthetic.
You have the freedom to reason deeply and answer questions naturally.
Platform Knowledge:
- The user's question bank is stored locally in JSON files and indexed into a RAG database (assistant-index.json) that you can search.
- The "Important Only" toggle on the website uses a dynamic scoring algorithm that evaluates questions based on syllabus heuristics, midterm exams, and professor pedagogical patterns (e.g., favoring comparison or applied coding questions).
- Cheat sheets are generated dynamically by AI agents to provide dense, Markdown-style article layouts.
Guidelines:
- If the user asks for a specific mark weight (e.g., 2m, 5m), adjust your detail level accordingly.
- Keep your tone friendly, conversational, yet academically accurate.
- If reference notes are provided below, use them to inform your answer, citing [Q...] when helpful.`;

        if (notesText) {
            sysPrompt += "\n\nReference notes:\n" + notesText;
        }

        let messages = [{role: "system", content: sysPrompt}];
        
        // Count history in turns based on context window budget
        // Assume roughly 300 tokens per turn (user + assistant) and 500 tokens for system + notes
        const budgetTokens = this.contextWindow - 500;
        const maxTurns = Math.max(1, Math.floor(budgetTokens / 300));
        this.history.slice(-(maxTurns * 2)).forEach(m => messages.push(m));
        
        messages.push({role: "user", content: text});

        try {
            const stream = this.generate(messages, { temperature: 0.7, max_tokens: params.marks ? params.marks * 150 : 800 });
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
