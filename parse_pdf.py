import fitz  # PyMuPDF
import os

def parse_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")
    
    doc = fitz.open(pdf_path)
    full_text = []

    for i, page in enumerate(doc):
        text_dict = page.get_text("dict")
        lines = []

        for block in text_dict["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    line_text = " ".join(span["text"] for span in line["spans"]).strip()
                    if line_text:
                        lines.append((line["bbox"][1], line_text))

        lines.sort(key=lambda x: x[0])
        page_text = "\n".join(line[1] for line in lines)
        full_text.append(f"--- Page {i + 1} ---\n{page_text}\n")

    return "\n".join(full_text)

if __name__ == "__main__":
    input_pdf_path = "../input_files/standard_chartered_unlocked.pdf"
    output_txt_path = "sc_unlocked.txt"

    full_text = parse_pdf(input_pdf_path)

    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"PDF parsed and saved as plain text to {output_txt_path}.")