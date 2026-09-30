from pathlib import Path

mathjax_script = """
<!-- MathJax for rendering LaTeX -->
<script>
  window.MathJax = {
    tex: {
      inlineMath: [['\\\\(', '\\\\)'], ['$', '$']],
      displayMath: [['\\\\[', '\\\\]'], ['$$', '$$']]
    }
  };
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
"""

def inject(path):
    content = path.read_text(encoding='utf-8')
    if 'MathJax' in content:
        print(f"Skipping {path} (MathJax already present)")
        return
        
    # Inject before </head>
    if '</head>' in content:
        content = content.replace('</head>', mathjax_script + '\n</head>')
        path.write_text(content, encoding='utf-8')
        print(f"Injected into {path}")

# Inject into all HTML files in subjects/ and templates/
for p in Path('.').rglob('*.html'):
    if 'node_modules' in p.parts:
        continue
    inject(p)
