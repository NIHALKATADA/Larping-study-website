from pathlib import Path
import re

def fix_latex(content):
    # \t imes -> \times
    content = content.replace("\t" + "imes", "\\times")
    # \r ightarrow -> \rightarrow
    content = content.replace("\r\n" + "ightarrow", "\\rightarrow")
    content = content.replace("\r" + "ightarrow", "\\rightarrow")
    # \n eg -> \neg
    content = content.replace("\n" + "eg", "\\neg")
    # \f rac -> \frac
    content = content.replace("\x0c" + "rac", "\\frac")
    # \t ext -> \text
    content = content.replace("\t" + "ext", "\\text")
    # \n eq -> \neq
    content = content.replace("\n" + "eq", "\\neq")
    # \r floor -> \rfloor
    content = content.replace("\r" + "floor", "\\rfloor")
    content = content.replace("\r\n" + "floor", "\\rfloor")
    
    # Let's also check for \t heta? 
    content = content.replace("\t" + "heta", "\\theta")

    # In HTML, sometimes \r\n is used for newline, so \right might have become \r\night. 
    # But wait, \r gets swallowed if it's \r\n. If the original string was "\rightarrow", Python parses it as \r (CR) + "ightarrow". 
    # When written to file, it might become \r\nightarrow or just \rightarrow depending on the file mode.
    # We saw in the Select-String output:
    # \((p 
    # ightarrow q)
    # This implies there is a newline! 
    # Let's use regex to be safe.
    
    # Match any whitespace followed by 'ightarrow' that was supposed to be \rightarrow
    content = re.sub(r'[\r\n]+ightarrow', r'\\rightarrow', content)
    content = re.sub(r'[\r\n]+eg\b', r'\\neg', content)
    content = re.sub(r'\x0crac', r'\\frac', content)
    content = re.sub(r'\t+imes', r'\\times', content)
    content = re.sub(r'[\r\n]+ight\b', r'\\right', content)
    content = re.sub(r'[\r\n]+floor\b', r'\\rfloor', content)
    content = re.sub(r'[\r\n]+ceil\b', r'\\rceil', content)
    content = re.sub(r'\t+o\b', r'\\to', content)
    content = re.sub(r'\t+ext\b', r'\\text', content)
    content = re.sub(r'[\r\n]+eq\b', r'\\neq', content)

    return content

for p in Path('subjects').rglob('*.html'):
    original = p.read_text(encoding='utf-8')
    fixed = fix_latex(original)
    if original != fixed:
        p.write_text(fixed, encoding='utf-8')
        print(f"Fixed LaTeX corruptions in {p}")
