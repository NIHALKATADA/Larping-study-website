import re

with open('C:/Users/nihal/OneDrive/Desktop/revision-hub/README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: "Your Google Groq API Key" -> "Your Groq API Key"
content = content.replace("Your Google Groq API Key", "Your Groq API Key")

# Fix 2: "GEMINI_MODEL" -> "GROQ_MODEL"
content = content.replace("GEMINI_MODEL", "GROQ_MODEL")

# Fix 3: "gemini-3.8-flash" -> "llama-3.1-70b-versatile"
content = content.replace("gemini-3.8-flash", "llama-3.1-70b-versatile")

# Fix 4: "query Gemini" -> "query Groq"
content = content.replace("query Gemini", "query Groq")

# Fix 5: "Google API" -> "Groq API"
content = content.replace("Google API", "Groq API")

# Any other mention of Gemini? Let's check
# "AI script (Gemini) to auto-generate quiz JSON" -> "AI script (Groq) to auto-generate quiz JSON"
content = content.replace("(Gemini)", "(Groq)")

with open('C:/Users/nihal/OneDrive/Desktop/revision-hub/README.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated README.md")
