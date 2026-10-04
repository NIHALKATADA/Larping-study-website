with open("shared/design-system.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

in_print = False
brace_count = 0
for i, line in enumerate(lines):
    if "@media print" in line:
        in_print = True
        print(f"Found at line {i+1}")
    if in_print:
        brace_count += line.count("{")
        brace_count -= line.count("}")
        if brace_count <= 0:
            print(f"Ends at line {i+1}")
            break
