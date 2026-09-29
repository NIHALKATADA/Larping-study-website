import re

with open('shared/assistant-llm.js', 'r', encoding='utf-8') as f:
    js = f.read()

new_chunks = r'let chunks = relevant.slice(0, 3).map(r => [Q | Score:  | Important: ]: );'

js = re.sub(r'let chunks = relevant\.slice\(0, 3\)\.map\(r => \[Q\$\{r\.doc\.q_num\}\]: \$\{r\.doc\.chunks\.join\(" "\)\.substring\(0, 400\)\}\);', new_chunks, js)

with open('shared/assistant-llm.js', 'w', encoding='utf-8') as f:
    f.write(js)
print('Updated chunks injection')
