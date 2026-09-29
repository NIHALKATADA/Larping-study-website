import re

with open('C:/Users/nihal/OneDrive/Desktop/revision-hub/README.md', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("qwen3.8-27b", "qwen2.5-32b")

with open('C:/Users/nihal/OneDrive/Desktop/revision-hub/README.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated README.md for qwen")
