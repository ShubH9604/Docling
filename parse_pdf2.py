import fitz  # PyMuPDF
import os
import re

# Detect if a line begins with a transaction date
def is_transaction_start(line):
    return bool(re.match(r'^\d{2}-\d{2}-\d{4}$', line))  # e.g., 13-12-2021

# Label columns based on X-position (horizontal alignment)
def label_by_position(x_pos):
    if x_pos < 120:
        return "Date"
    elif 120 <= x_pos < 200:
        return "Cheque No"
    elif 200 <= x_pos < 375:
        return "Description"
    elif 380 <= x_pos < 390:
        return "Debit"
    elif 400 <= x_pos < 470:
        return "Credit"
    elif 470 <= x_pos < 550:
        return "Balance"
    else:
        return "Other"

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
                    row_data = []
                    for span in line["spans"]:
                        text = span["text"].strip()
                        x_pos = span["bbox"][0]  # left X-position
                        label = label_by_position(x_pos)

                        # If it's a number, label it by its column
                        if re.match(r'^[\d,]+\.\d{2}$', text):
                            if label == "Debit":
                                text += " -> Debit"
                            elif label == "Credit":
                                text += " -> Credit"
                            elif label == "Balance":
                                text += " -> Balance"

                        row_data.append(text)

                    # Append the whole row as a string
                    if row_data:
                        lines.append(" ".join(row_data))

        # Add blank line before each transaction for readability
        content_lines = []
        for text in lines:
            if is_transaction_start(text) and content_lines:
                content_lines.append("")  # blank line before new transaction
            content_lines.append(text)

        # Append page content
        page_text = "\n".join(content_lines)
        full_text.append(f"--- Page {i + 1} ---\n{page_text}\n")

    return "\n".join(full_text)

if __name__ == "__main__":
    input_pdf_path = "../input_files/axisstatement.pdf"  # update if path is different
    output_txt_path = "axisstatement.txt"

    full_text = parse_pdf(input_pdf_path)

    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"✅ PDF parsed and saved with labeled Debit/Credit/Balance values to '{output_txt_path}'.")
