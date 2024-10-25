import nltk
import logging
nltk.download('punkt_tab')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pymongo import MongoClient
import re

# Connect to MongoDB
client = MongoClient("mongodb+srv://arjuntewari0505:by3xJDiZXwvHkGN0@cluster0.gkth7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['pdf_pipeline_db']
collection = db['pdf_data']

def extract_keywords(text, top_n=10):
    """
    Extract keywords from the given text based on word frequency.
    :param text: The full text content of the PDF
    :param top_n: Number of top keywords to extract
    :return: List of keywords
    """
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(re.sub(r'\W+', ' ', text.lower()))  # Tokenize and remove special characters

    # Compute word frequency, ignoring stopwords
    word_freq = {}
    for word in words:
        if word not in stop_words and len(word) > 3:  # Exclude short words
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1

    # Sort words by frequency and return the top N keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [word for word, freq in sorted_words]

def extract_keywords_for_documents():
    """
    Extract keywords for each PDF stored in MongoDB and update the document with keywords.
    """
    documents = collection.find()  # Get all documents from MongoDB
    for doc in documents:
        try:
            text = doc.get('content', '')
            keywords = extract_keywords(text, top_n=10)  # Extract top 10 keywords

            # Update MongoDB with keywords
            collection.update_one({'_id': doc['_id']}, {'$set': {'keywords': keywords}})
            logging.info(f"Keywords for {doc['filename']} updated successfully.")
            print(f"Keywords for {doc['filename']} updated successfully.")

        except Exception as e:
            logging.error(f"Failed to extract keywords for {doc['filename']}: {e}")
            print(f"Failed to extract keywords for {doc['filename']}: {e}")

if __name__ == "__main__":
    extract_keywords_for_documents()
