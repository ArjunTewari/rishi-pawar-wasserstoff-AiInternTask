
import nltk
import logging
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from pymongo import MongoClient

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Connect to MongoDB
client = MongoClient("mongodb+srv://arjuntewari0505:by3xJDiZXwvHkGN0@cluster0.gkth7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['pdf_pipeline_db']
collection = db['pdf_data']

def summarize_text(text, num_sentences=3):
    """
    Summarize the given text by extracting key sentences.
    :param text: The full text content of the PDF
    :param num_sentences: Number of sentences to return in the summary
    :return: Summary text
    """
    # Tokenize the text into sentences and words
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text.lower())
    sentences = sent_tokenize(text)

    # Compute word frequency (excluding stopwords)
    word_freq = {}
    for word in words:
        if word not in stop_words:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1

    # Rank sentences based on word frequency
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                if sentence in sentence_scores:
                    sentence_scores[sentence] += word_freq[word]
                else:
                    sentence_scores[sentence] = word_freq[word]

    # Select the top-ranked sentences for the summary
    summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    return " ".join(summarized_sentences)

def summarize_documents():
    """
    Summarize the content of each PDF stored in MongoDB and update the document with the summary.
    """
    documents = collection.find()  # Get all documents from MongoDB
    for doc in documents:
        try:
            text = doc.get('content', '')
            summary = summarize_text(text, num_sentences=5)  # Adjust sentence count for document length

            # Update MongoDB with the summary
            collection.update_one({'_id': doc['_id']}, {'$set': {'summary': summary}})
            logging.info(f"Summary for {doc['filename']} updated successfully.")
            print(f"Summary for {doc['filename']} updated successfully.")

        except Exception as e:
            logging.error(f"Failed to summarize {doc['filename']}: {e}")
            print(f"Failed to summarize {doc['filename']}: {e}")

if __name__ == "__main__":
    summarize_documents()
