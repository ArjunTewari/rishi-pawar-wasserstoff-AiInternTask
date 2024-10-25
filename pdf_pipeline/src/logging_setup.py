import logging
import os

def setup_logging():
    """
    Set up logging configuration. Logs will be stored in '/logs/pipeline.log'.
    """
    log_dir = '/logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)  # Create logs directory if it doesn't exist

    logging.basicConfig(filename=os.path.join(log_dir, 'pipeline.log'),
                        filemode='a',  # Append to existing logs
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    logging.info("Pipeline process started.")
