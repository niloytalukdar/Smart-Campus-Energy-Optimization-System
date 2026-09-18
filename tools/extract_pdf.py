from pathlib import Path
from PyPDF2 import PdfReader

p = Path('ChatGPT - bhp.pdf')
if not p.exists():
    print('PDF not found at', p.resolve())
    raise SystemExit(1)

r = PdfReader(str(p))
for i, page in enumerate(r.pages, start=1):
    text = page.extract_text() or ''
    print('--- PAGE', i, '---')
    print(text)
    print('\n')
