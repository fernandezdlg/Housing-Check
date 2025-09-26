import os
import openai
import pymupdf  # PyMuPDF
from pathlib import Path
import json

description_outputs = {}


# find all pdf paths within data/*/*Verkaufsdokumentation*
def find_pdfs(base_path, keyword="Verkaufsdokumentation"):
    matches = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".pdf") and keyword in file:
                matches.append(os.path.join(root, file))
    return matches


# Example usage
base_directory = "data"
pdf_files = find_pdfs(base_directory)
for f in pdf_files:
    print(f)


for file in pdf_files[:10]:
    # print(file)
    haus = file.split("/")[1]

    pdf_path = Path(file)

    all_text = []
    with pymupdf.open(pdf_path) as doc:
        # print(f"Pages: {doc.page_count}, Title: {doc.metadata.get('title')}")
        for i, page in enumerate(doc):
            text = page.get_text(
                "text"
            )  # "text", "blocks", "words", "json" also available
            all_text.append(text)
            # print(f"\n--- Page {i+1} ---\n{text}")  # preview

    full_text = "\n".join(all_text)

    client = openai.OpenAI(
        api_key="XCnfIu5iKUABB6YWUaIGsrwi91yz",  # api_key=os.getenv("SWISS_AI_PLATFORM_API_KEY"),
        base_url="https://api.swisscom.com/layer/swiss-ai-weeks/apertus-70b/v1",
    )

    stream = client.chat.completions.create(
        model="swiss-ai/Apertus-70B",
        messages=[
            {
                "role": "system",
                "content": "You are the world's best real estate expert. I need you to read the following description \
            text and give me an analysis in English. \
            Then, I need you to give me a detailed overview for potential real estate buyers. Do not \
            write it slide by slide, this should be a holistic analysis but also concentrated on \
            whether renovations would be needed, and whether or not they would be expensive or \
            worth doing them. The very first thing you need to tell me is \
            the year the building was constructed, and summarize all renovations performed in the property.",
            },
            {"role": "user", "content": full_text},
        ],
        stream=True,
    )

    output_chunks = []
    for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        output_chunks.append(content)
        print(content, end="", flush=True)

    # Join all chunks into a single string
    description_outputs[haus] = "".join(output_chunks)


with open("description_outputs.json", "w") as f:
    json.dump(description_outputs, f, indent=4, ensure_ascii=False)
