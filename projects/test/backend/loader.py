import os
import pdfplumber
from docx import Document
import markdown
import html2text
import email
from email import policy
import pandas as pd

def load_file(filepath):
    ext = filepath.lower().split(".")[-1]

    # TXT
    if ext == "txt":
        return open(filepath, "r", encoding="utf-8", errors="ignore").read()

    # Markdown → plain text
    if ext == "md":
        md = open(filepath, "r", encoding="utf-8", errors="ignore").read()
        return html2text.html2text(markdown.markdown(md))

    # HTML
    if ext in ["html", "htm"]:
        html = open(filepath, "r", encoding="utf-8", errors="ignore").read()
        return html2text.html2text(html)

    # PDF
    if ext == "pdf":
        text = ""
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except:
            pass
        return text

    # DOCX
    if ext == "docx":
        doc = Document(filepath)
        return "\n".join([p.text for p in doc.paragraphs])

    # EML
    if ext == "eml":
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            msg = email.message_from_file(f, policy=policy.default)
        body = msg.get_body(preferencelist=('plain'))
        if body:
            return body.get_content()
        return ""

    # CSV → chunk each row
    if ext == "csv":
        try:
            df = pd.read_csv(filepath, dtype=str, errors='ignore')
            rows = []
            for _, r in df.iterrows():
                row_text = f"[{os.path.basename(filepath)}] " + " | ".join(r.astype(str).tolist())
                rows.append(row_text)
            return "\n".join(rows)
        except:
            # fallback: raw CSV
            return open(filepath, "r", encoding="utf-8", errors="ignore").read()

    return None
