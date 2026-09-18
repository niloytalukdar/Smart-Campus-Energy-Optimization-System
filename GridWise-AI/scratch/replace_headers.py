import os
import glob
import re

new_header = """<div class="w-full sticky top-0 z-50 bg-surface-container-lowest">
  <div class="max-w-[1720px] mx-auto px-margin py-2 flex items-center">
    <!-- Logo only header -->
    <img alt="GridWise AI Logo" src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='40'><rect rx='6' ry='6' width='40' height='40' fill='%230b1220'/><g transform='translate(6,6)'><circle cx='14' cy='14' r='10' fill='%2341b3ff'/></g><text x='54' y='26' font-family='Verdana' font-size='14' fill='%23e2e2e9'>GridWise</text><text x='118' y='26' font-family='Verdana' font-size='12' fill='%2388c3ff'>AI</text></svg>" class="h-8 w-auto object-contain">
  </div>
</div>"""

files = glob.glob('system_ui/**/code.html', recursive=True)
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Remove the large header
    content = re.sub(r'<header class="fixed top-0 left-0 right-0 w-full z-50 bg-surface-container border-b border-surface-container-highest">.*?</header>', new_header, content, flags=re.DOTALL)
    
    # Also remove the "Minimal Sticky Header" block if it exists (like in ai_interpretation) to avoid duplicates
    # Since we just added new_header, it will be duplicated if it was already there.
    # Actually, let's just do a string replace of the old minimal header to empty string.
    old_minimal = """<!-- Minimal Sticky Header: logo only -->
<div class="w-full sticky top-0 z-50 bg-surface-container-lowest">
  <div class="max-w-[1720px] mx-auto px-margin py-2 flex items-center">
    <!-- Logo only header. Replace the data URL below with your exact logo path if desired. -->
    <img alt="GridWise AI Logo" src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='40'><rect rx='6' ry='6' width='40' height='40' fill='%230b1220'/><g transform='translate(6,6)'><circle cx='14' cy='14' r='10' fill='%2341b3ff'/></g><text x='54' y='26' font-family='Verdana' font-size='14' fill='%23e2e2e9'>GridWise</text><text x='118' y='26' font-family='Verdana' font-size='12' fill='%2388c3ff'>AI</text></svg>" class="h-8 w-auto object-contain">
  </div>
</div>"""
    content = content.replace(old_minimal, "")
    
    # Clean up any leftover comments
    content = content.replace("<!-- Header section removed; minimal sticky logo header above -->", "")
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Updated {f}")
