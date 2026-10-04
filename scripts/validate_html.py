from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
    
    def handle_starttag(self, tag, attrs):
        if tag not in ['meta', 'link', 'br', 'hr', 'img', 'input', 'path', 'line', 'circle', 'rect', 'polyline']:
            self.stack.append(tag)
            
    def handle_endtag(self, tag):
        if tag not in ['meta', 'link', 'br', 'hr', 'img', 'input', 'path', 'line', 'circle', 'rect', 'polyline']:
            if not self.stack:
                self.errors.append(f"Unexpected end tag: {tag}")
            elif self.stack[-1] == tag:
                self.stack.pop()
            else:
                self.errors.append(f"Mismatched end tag: expected {self.stack[-1]}, got {tag}")

parser = MyHTMLParser()
with open('os/comprehensive-report.html', 'r', encoding='utf-8') as f:
    parser.feed(f.read())

if parser.errors:
    print("Errors found:", parser.errors[:10])
else:
    print("No obvious unclosed tags.")
