with open("shared/design-system.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

nesting = 0
for i, line in enumerate(lines):
    nesting += line.count('{')
    nesting -= line.count('}')
    if nesting < 0:
        print(f"ERROR: Negative nesting at line {i+1}: {line.strip()}")
        nesting = 0
