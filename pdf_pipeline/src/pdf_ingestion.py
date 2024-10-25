import logging
import fitz  # PyMuPDF
import os
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://arjuntewari0505:by3xJDiZXwvHkGN0@cluster0.gkth7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['pdf_pipeline_db']
collection = db['pdf_data']

def ingest_pdfs(folder_path):
    """
    Ingest all PDFs from the specified folder, extract text, and store metadata in MongoDB.
    :param folder_path: Path to the folder containing PDFs
    """
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            try:
                # Open and read PDF
                with fitz.open(file_path) as pdf_file:
                    text = ""
                    for page_num in range(len(pdf_file)):
                        text += pdf_file[page_num].get_text()

                # Get metadata
                file_metadata = {
                    "filename": filename,
                    "path": file_path,
                    "size": os.path.getsize(file_path),
                    "content": text  # You will summarize and extract keywords from this later
                }

                # Insert metadata into MongoDB
                collection.insert_one(file_metadata)
                logging.info(f"Successfully ingested: {filename}")
                print(f"Successfully ingested: {filename}")

            except Exception as e:
                logging.error(f"Failed to ingest {filename}: {e}")
                print(f"Failed to ingest {filename}: {e}")

if __name__ == "__main__":
    folder_path = "C:/Users/hp/OneDrive/Desktop"
    ingest_pdfs(folder_path)
