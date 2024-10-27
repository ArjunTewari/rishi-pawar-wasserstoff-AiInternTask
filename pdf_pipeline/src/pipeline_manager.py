import time
import logging
import psutil  # Import psutil for resource monitoring
from concurrent.futures import ThreadPoolExecutor
from pdf_ingestion import ingest_pdfs
from summarizer import summarize_documents
from keyword_extractor import extract_keywords_for_documents
from logging_setup import setup_logging

def log_resource_utilization(stage):
    """
    Logs CPU, memory, and I/O usage at a specific stage in the pipeline.
    """
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    io_counters = psutil.disk_io_counters()
    logging.info(f"{stage} - CPU: {cpu}%, Memory: {memory}%, Read Count: {io_counters.read_count}, Write Count: {io_counters.write_count}")
    print(f"{stage} - CPU: {cpu}%, Memory: {memory}%, Read Count: {io_counters.read_count}, Write Count: {io_counters.write_count}")

def process_pipeline(folder_path):
    """
    Main function to run the PDF pipeline concurrently. Ingest PDFs, summarize them,
    and extract keywords in parallel. Tracks time and memory usage.
    """
    setup_logging()  # Set up logging at the very start
    start_time = time.time()  # Track the start time

    try:
        # Step 1: Ingest PDFs
        logging.info("Starting PDF ingestion...")
        log_resource_utilization("Before Ingestion")
        ingest_pdfs(folder_path)
        log_resource_utilization("After Ingestion")

        # Step 2: Summarize and extract keywords concurrently
        with ThreadPoolExecutor() as executor:
            logging.info("Summarizing PDFs and extracting keywords in parallel...")
            log_resource_utilization("Before Summarization and Extraction")
            executor.submit(summarize_documents)
            executor.submit(extract_keywords_for_documents)
            log_resource_utilization("After Summarization and Extraction")

        total_time = time.time() - start_time  # Calculate total processing time
        logging.info(f"Pipeline completed in {total_time} seconds.")
        print(f"Pipeline completed in {total_time} seconds.")

    except Exception as e:
        logging.error(f"Error occurred during pipeline processing: {e}")
        print(f"Error occurred during pipeline processing: {e}")

if __name__ == "__main__":
    folder_path = "C:/Users/hp/OneDrive/Desktop"  # Replace with the correct path to your PDFs
    process_pipeline(folder_path)
