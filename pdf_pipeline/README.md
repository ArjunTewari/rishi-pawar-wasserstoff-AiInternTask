# PDF Summarization and Keyword Extraction Pipeline

## Project Overview
This project implements a dynamic pipeline that processes multiple PDF documents, generates domain-specific summaries, and extracts keywords. The processed data is stored in a MongoDB database. The system is designed to handle documents of varying lengths while ensuring concurrency and error handling.

## Features
- **PDF Ingestion**: Extracts text content from PDFs and stores it in MongoDB.
- **Text Summarization**: Summarizes the text content of PDFs using natural language processing techniques.
- **Keyword Extraction**: Extracts the most relevant keywords from each PDF.
- **Concurrency**: Processes multiple PDFs in parallel to enhance performance.
- **Error Handling & Logging**: Logs all the pipeline activities and handles errors gracefully to ensure uninterrupted processing.

## System Requirements
- **Python**: 3.9 or later
- **MongoDB**: Local or Atlas instance for storing processed data
- **Docker (Optional)**: For containerizing the project
- **OS**: Windows, macOS, or Linux

## Setup Instructions

### 1. Clone the Repository
First, clone the repository to your local machine:
`git clone https://github.com/yourusername/PDF_Summarization_Extraction.git
cd PDF_Summarization_Extraction`


2. Set Up a Python Virtual Environment
Create a virtual environment to isolate the project dependencies:
`python -m venv venv`

2.1. Activate the virtual environment:
Windows:
`.\venv\Scripts\activate`

3. Install Dependencies:
Install the necessary Python packages listed in the requirements.txt file:
`pip install -r requirements.txt`

4. Set Up MongoDB:
   You need to either have a MongoDB Atlas account or a local MongoDB instance running.
Update the MongoDB connection string in your src/connection.py or wherever it is used to match your database configuration.
Example MongoDB connection string (MongoDB Atlas):
python:
`client = pymongo.MongoClient("your-mongodb-connection-string")`

5. Download NLTK Data:
Ensure that the necessary NLTK resources (e.g., stopwords, tokenizer) are downloaded:
python
`import nltk
nltk.download('punkt')
nltk.download('stopwords')`

6. Running the Project
To run the project and start processing PDFs:
Place your PDF files in the appropriate folder (desktop).
Run the pipeline using the pipeline_manager.py:
`python src/pipeline_manager.py`


7. Logging
Logs for the pipeline (e.g., errors, status updates) will be stored in the `logs/pipeline`.log file.
The system will automatically create the log file and directory if they do not exist.
