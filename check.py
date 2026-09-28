def find_missing_brackets(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Simple stack to find missing brackets
    stack = []
    lines = text.split('\n')
    for i, line in enumerate(lines):
        for char in line:
            if char in '{[(': 
                stack.append((char, i+1))
            elif char in '}])':
                if not stack:
                    print(f"Extra closing {char} on line {i+1}")
                    return
                last = stack.pop()
                expected = {'}':'{', ']':'[', ')':'('}[char]
                if last[0] != expected:
                    print(f"Mismatched brackets: expected closing for {last[0]} from line {last[1]}, got {char} on line {i+1}")
                    return
    
    if stack:
        print(f"Unclosed brackets remaining:")
        for b, l in stack:
            print(f"  {b} on line {l}")
            
find_missing_brackets('shared/app-utils.js')
