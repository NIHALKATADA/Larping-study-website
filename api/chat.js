export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    // 1. Exact origin check
    const origin = req.headers.origin || req.headers.referer;
    if (!origin) {
        return res.status(403).json({ error: 'Missing origin' });
    }
    try {
        const originUrl = new URL(origin).origin;
        const allowedOriginsStr = process.env.ALLOWED_ORIGINS || '';
        const allowedOrigins = allowedOriginsStr.split(',').map(s => {
            try { return new URL(s.trim()).origin; } catch(e) { return s.trim(); }
        }).filter(Boolean);
        if (allowedOrigins.length > 0 && !allowedOrigins.includes(originUrl)) {
            return res.status(403).json({ error: 'Forbidden origin' });
        }
    } catch(e) {
        return res.status(403).json({ error: 'Invalid origin format' });
    }

    // 2. Request size cap
    const contentLength = parseInt(req.headers['content-length'] || '0');
    if (contentLength > 1024 * 10) { 
        return res.status(413).json({ error: 'Payload too large' });
    }

    // 3. Rate limiting (in-memory, per-instance/best-effort)
    const ip = req.headers['x-forwarded-for'] || req.socket?.remoteAddress || 'unknown';
    if (!global.rateLimits) global.rateLimits = new Map();
    const now = Date.now();
    const limitWindow = 60000; // 1 minute
    const maxRequests = 10;
    
    let userLimit = global.rateLimits.get(ip) || { count: 0, startTime: now };
    if (now - userLimit.startTime > limitWindow) {
        userLimit = { count: 1, startTime: now };
    } else {
        userLimit.count++;
        if (userLimit.count > maxRequests) {
            return res.status(429).json({ error: 'Rate limit exceeded' });
        }
    }
    global.rateLimits.set(ip, userLimit);

    // 4. Extract and strictly validate body
    const body = req.body;
    if (!body || !Array.isArray(body.messages)) {
        return res.status(400).json({ error: 'Missing or invalid messages array' });
    }
    if (body.messages.length > 8) {
        return res.status(400).json({ error: 'Too many messages (max 8)' });
    }

    const validRoles = ['user', 'assistant', 'system'];
    for (const msg of body.messages) {
        if (!validRoles.includes(msg.role)) {
            return res.status(400).json({ error: 'Invalid role' });
        }
        if (typeof msg.content !== 'string' || msg.content.length > 4000) {
            return res.status(400).json({ error: 'Invalid or too long content (max 4000 chars)' });
        }
    }

    const GEMINI_API_KEY = (process.env.GEMINI_API_KEY || '').trim();
    const GEMINI_MODEL = (process.env.GEMINI_MODEL || '').trim();
    const OPENAI_API_KEY = (process.env.OPENAI_API_KEY || process.env.GROQ_API_KEY || process.env.OPENROUTER_API_KEY || '').trim();
    const OPENAI_BASE_URL = (process.env.OPENAI_BASE_URL || (process.env.GROQ_API_KEY ? 'https://api.groq.com/openai/v1' : 'https://openrouter.ai/api/v1')).trim();
    const OPENAI_MODEL = (process.env.OPENAI_MODEL || 'llama3-8b-8192').trim(); // Default Groq model

    if (!GEMINI_API_KEY && !OPENAI_API_KEY) {
        return res.status(500).json({ error: 'Server configuration error: No API key provided (Gemini or OpenAI-compatible)' });
    }

    // Clamp parameters
    const temperature = Math.max(0, Math.min(1, Number(body.temperature) || 0.3));
    const maxOutputTokens = Math.min(1024, Number(body.max_tokens) || 500);

    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000); // 30s timeout
        
        let response, data, text;

        if (OPENAI_API_KEY) {
            // --- OPENAI-COMPATIBLE ROUTE (Groq, OpenRouter, Together, OpenAI) ---
            response = await fetch(`${OPENAI_BASE_URL}/chat/completions`, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${OPENAI_API_KEY}`,
                    'HTTP-Referer': 'https://larping-study.vercel.app', // For OpenRouter
                    'X-Title': 'Revision Hub'
                },
                body: JSON.stringify({
                    model: OPENAI_MODEL,
                    messages: body.messages, // Already in standard {role, content} format
                    temperature: temperature,
                    max_tokens: maxOutputTokens
                }),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                let errText = await response.text();
                return res.status(502).json({ error: 'Upstream OpenAI-compatible API error: ' + errText });
            }

            data = await response.json();
            if (data && data.choices && data.choices[0].message && data.choices[0].message.content) {
                text = data.choices[0].message.content;
            } else {
                return res.status(500).json({ error: 'Unexpected API response format from OpenAI-compatible endpoint' });
            }

        } else {
            // --- GEMINI ROUTE ---
            const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent`;
            
            const formattedMessages = body.messages.map(msg => ({
                role: msg.role === 'assistant' ? 'model' : 'user', 
                parts: [{ text: msg.content }]
            }));

            let mergedMessages = [];
            formattedMessages.forEach(msg => {
                if (mergedMessages.length > 0 && mergedMessages[mergedMessages.length - 1].role === msg.role) {
                    mergedMessages[mergedMessages.length - 1].parts[0].text += '\n\n' + msg.parts[0].text;
                } else {
                    mergedMessages.push(msg);
                }
            });

            response = await fetch(geminiUrl, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'x-goog-api-key': GEMINI_API_KEY
                },
                body: JSON.stringify({
                    systemInstruction: {
                        parts: [{ text: "You are an educational study assistant." }]
                    },
                    contents: mergedMessages,
                    generationConfig: {
                        temperature: temperature,
                        maxOutputTokens: maxOutputTokens
                    }
                }),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                let errText = await response.text();
                return res.status(502).json({ error: 'Upstream Gemini API error: ' + errText });
            }

            data = await response.json();
            if (data && data.candidates && data.candidates[0].content && data.candidates[0].content.parts) {
                text = data.candidates[0].content.parts[0].text;
            } else {
                return res.status(500).json({ error: 'Unexpected API response format from Gemini' });
            }
        }

        return res.status(200).json({ text });

    } catch (e) {
        if (e.name === 'AbortError') {
            return res.status(504).json({ error: 'Request timeout' });
        }
        return res.status(500).json({ error: 'Internal server error: ' + e.message });
    }
}
