from docx import Document

def read_word_table(file_path):
    doc = Document(file_path)
    tables = doc.tables
    
    if not tables:
        print("No tables found in the document.")
        return
    
    for table in tables:
        for row in table.rows:
            row_data = [cell.text.strip() for cell in row.cells]
            print(row_data)

if __name__ == "__main__":
    file_path = "your_word_document.docx"  # Provide the path to your Word document
    read_word_table(file_path)

