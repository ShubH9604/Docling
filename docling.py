from docling.document_converter import DocumentConverter 

# Step 1: Initialize the converter
converter = DocumentConverter()

# Step 2: Convert the PDF
result = converter.convert("canara.pdf")

# Step 3: Access the document
doc = result.document

# Step 4: Export to Markdown
markdown_output = doc.export_to_markdown()
with open("canara.md", "w", encoding="utf-8") as md_file:
    md_file.write(markdown_output)
print("✅ Saved as 'canara.md'")

# Step 5: Export to plain text
plain_text_output = doc.export_to_text()
with open("canara.txt", "w", encoding="utf-8") as txt_file:
    txt_file.write(plain_text_output)
print("✅ Saved as 'canara.txt'")
