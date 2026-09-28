import re

with open('shared/assistant-ui.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace('''html += <p>I am an offline study assistant. I couldn't find any relevant study material for your query.</p>
                        <p style="color:var(--primary-teal);"><strong>Please enable Smart Mode or Deep Mode to ask general knowledge questions.</strong></p>;''',
'''html += `<p>I am an offline study assistant. I couldn't find any relevant study material for your query.</p>
                        <p style="color:var(--primary-teal);"><strong>Please enable Smart Mode or Deep Mode to ask general knowledge questions.</strong></p>`;''')

with open('shared/assistant-ui.js', 'w', encoding='utf-8') as f:
    f.write(js)
