from transformers import RobertaTokenizer, RobertaForSequenceClassification
from scipy.special import softmax
import numpy as np
import torch

# Load tokenizer and RoBERTa model
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = RobertaTokenizer.from_pretrained(MODEL_NAME)
SENTIMENT_MODEL = RobertaForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=3)

# Classify the sentiment of a string of text
def classify_sentiment(text):
    '''
    Classify the sentiment of a string of text
    '''
    inputs = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        return_tensors="pt",
        truncation=True,
        padding='max_length',
        max_length=min(len(text), 512)
    )

    with torch.no_grad():
        outputs = SENTIMENT_MODEL(**inputs)
        logits = outputs.logits
        probs = softmax(logits.numpy(), axis=1)[0]

    confidence_probabilities = {
        'negative': float(probs[0]),
        'neutral': float(probs[1]),
        'positive': float(probs[2])
    }

    sentiment = np.argmax(probs)

    sentiment_result = 'negative' if sentiment == 0 else 'neutral' if sentiment == 1 else 'positive'

    return sentiment_result, confidence_probabilities