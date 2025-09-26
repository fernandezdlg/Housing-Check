import unicodedata
import pymupdf
from pathlib import Path
import os
import json


# find all pdf paths within data/*/*IAZI*
def find_pdfs(base_path, keyword="IAZI"):
    matches = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".pdf") and keyword in file:
                matches.append(os.path.join(root, file))
    return matches


base_directory = "data"  # FIXME: adjust path
pdf_files = find_pdfs(base_directory)[2:]


# Initialize dictionary for zustand database
status_orig = dict()


# Determine the zustand keys to look for
keys = [
    "Fassaden / Fenster / Aussentüren",
    "Flachdach / Steildach",
    "Nebenräume (Untergeschoss / Estrich /\nTreppenhaus)",
    "Elektrotechnische Anlagen",
    "Sanitär­ und wärmetechnische Anlagen",
    # "Feuchtigkeitsprobleme",
    "Aufzüge",
    # "Wohn­ / Schlafräume",
    # "Küche / Nasszellen (Bad / sep. WC)"
]


# Save zustands for each haus in the dictionary
for file in pdf_files:
    haus_name = file.split("/")[1]
    status_orig[haus_name] = dict()  # initialize sub-dict
    pdf_path = Path(file)

    all_text = []
    with pymupdf.open(pdf_path) as doc:
        print(f"Pages: {doc.page_count}, Title: {doc.metadata.get('title')}")
        for i, page in enumerate(doc):
            text = page.get_text(
                "text"
            )  # "text", "blocks", "words", "json" also available
            all_text.append(text)

    full_text = "\n".join(all_text)

    for key in keys:
        start_idx = full_text.find(key)

        tmp_key = unicodedata.normalize(
            "NFKD", key.replace("\n", " ").replace("\xad", "").strip()
        )

        if start_idx != -1:
            start_idx += len(key)
            end_idx = full_text.find("\n", start_idx + 1)
            tmp_txt = unicodedata.normalize(
                "NFKD",
                full_text[start_idx:end_idx]
                .replace("\n", " ")
                .replace("\xad", "")
                .strip(),
            )
            status_orig[haus_name][tmp_key] = tmp_txt
        else:
            status_orig[haus_name][tmp_key] = ""


# Save the dictionary as json
with open("status_orig.json", "w") as f:
    json.dump(status_orig, f, indent=4, ensure_ascii=False)
