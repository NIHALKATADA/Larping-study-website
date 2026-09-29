import re
import sys

def remove_buttons(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The AI assistant modal has an id='assistantModal' which should KEEP the buttons.
    # The other modals are filterModal, jumpModal, studyModal.
    # It might be easier to just remove any clear-btn and pin-btn that are NOT inside the assistantModal header.
    # Actually, the user says "Delete these specific <button> tags from the .modal-header divs of all non-chat modals."
    
    # Let's find all headers: <div class="modal-header"...> ... </div>
    # A simple regex to find the button elements.
    
    # We can match the exact <button class="clear-btn"...</button><button class="pin-btn"...</button> block
    # and remove it if it's right before <button class="close-modal" onclick="closeModal
    
    pattern = re.compile(r'<button class="clear-btn"[^>]*>.*?</button><button class="pin-btn"[^>]*>.*?</button>', re.DOTALL)
    
    # But wait, some have whitespace between them, let's just match them individually if they are not in assistantModal.
    # Actually, it's safer to just replace them where they are followed by <button class="close-modal" onclick="closeModal
    
    def replacer(match):
        return ''
    
    # Let's find all <button class="clear-btn" ... </svg>\s*</button>
    clear_btn_pattern = re.compile(r'<button class="clear-btn".*?</button>', re.DOTALL)
    pin_btn_pattern = re.compile(r'<button class="pin-btn".*?</button>', re.DOTALL)
    
    # Split content by '<div id="assistantModal"' so we don't touch the assistant modal
    parts = content.split('<div id="assistantModal"')
    
    if len(parts) > 1:
        parts[0] = clear_btn_pattern.sub('', parts[0])
        parts[0] = pin_btn_pattern.sub('', parts[0])
        content = '<div id="assistantModal"'.join(parts)
    else:
        content = clear_btn_pattern.sub('', content)
        content = pin_btn_pattern.sub('', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleaned {file_path}")

remove_buttons('C:/Users/nihal/OneDrive/Desktop/revision-hub/templates/question-bank-template.html')
remove_buttons('C:/Users/nihal/OneDrive/Desktop/revision-hub/templates/quiz-template.html')
