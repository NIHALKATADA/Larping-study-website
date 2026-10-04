with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Add display none for desktop, block for mobile
new_css = """

/* Mobile-only FAB for Reports */
.mobile-only-fab {
    display: none !important;
}

@media (max-width: 768px) {
    .mobile-only-fab {
        display: flex !important;
    }
}
"""

with open('shared/design-system.css', 'a', encoding='utf-8') as f:
    f.write(new_css)
