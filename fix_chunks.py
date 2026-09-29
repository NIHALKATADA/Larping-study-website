import re
with open('shared/assistant-llm.js', 'r', encoding='utf-8') as f:
    js = f.read()

bad_chunk_regex = r'let chunks = relevant\.slice\(0, 3\)\.map\(r => \[Q \| Score:  \| Important: \]: \);'
good_chunk = 'let chunks = relevant.slice(0, 3).map(r => `[Q${r.doc.q_num} | Score: ${r.doc.score || "N/A"} | Important: ${r.doc.important ? "Yes" : "No"}]: ${r.doc.chunks.join(" ").substring(0, 400)}`);'

js = re.sub(bad_chunk_regex, good_chunk, js)

with open('shared/assistant-llm.js', 'w', encoding='utf-8') as f:
    f.write(js)
print('Fixed chunks!')
