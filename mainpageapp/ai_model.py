
from transformers import pipeline


import logging
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Singleton summarizer model
class SummarizerModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SummarizerModel, cls).__new__(cls)
            cls._instance.summarizer = pipeline(
                "summarization", 
                model="sshleifer/distilbart-cnn-12-6", 
                revision="a4f8f3e", 
                device=0
            )
        return cls._instance

summarizer_model = SummarizerModel().summarizer