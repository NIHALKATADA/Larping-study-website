export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    const body = req.body;
    if (!body || !Array.isArray(body.messages)) {
        return res.status(400).json({ error: 'Missing or invalid messages array' });
    }

    // 1. Strictly grab the Groq API key from environment
    const GROQ_API_KEY = (process.env.GROQ_API_KEY || '').trim();
    
    // 2. The API STRICTLY requires a model string. Based on your dashboard limits, 
    // we will default to 'qwen/qwen3.8-27b' which you have access to.
    const GROQ_MODEL = (process.env.GROQ_MODEL || process.env.OPENAI_MODEL || 'qwen/qwen3.8-27b').trim();

    if (!GROQ_API_KEY) {
        return res.status(500).json({ error: 'Missing GROQ_API_KEY in Vercel Environment Variables.' });
    }

    const temperature = Math.max(0, Math.min(1, Number(body.temperature) || 0.3));
    const maxOutputTokens = Math.min(1024, Number(body.max_tokens) || 500);

    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000); 

        const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': Bearer 
            },
            body: JSON.stringify({
                model: GROQ_MODEL,
                messages: body.messages, 
                temperature: temperature,
                max_tokens: maxOutputTokens
            }),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            let errText = await response.text();
            return res.status(response.status).json({ error: 'Groq API error: ' + errText });
        }

        const data = await response.json();
        if (data && data.choices && data.choices[0].message && data.choices[0].message.content) {
            return res.status(200).json({ text: data.choices[0].message.content });
        } else {
            return res.status(500).json({ error: 'Unexpected API response format from Groq' });
        }

    } catch (e) {
        if (e.name === 'AbortError') {
            return res.status(504).json({ error: 'Request timeout' });
        }
        return res.status(500).json({ error: 'Internal server error: ' + e.message });
    }
}
