with open("shared/design-system.css", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("@media print")
print(text[idx:idx+1500])
