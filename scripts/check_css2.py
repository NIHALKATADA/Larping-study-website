with open("shared/design-system.css", "r", encoding="utf-8") as f:
    text = f.read()

print("Final nesting level:", text.count('{') - text.count('}'))
