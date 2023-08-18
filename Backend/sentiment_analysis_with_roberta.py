
#Using a json file from Google Drive as the data source
#pip install transformers scipy pandas torch

from transformers import RobertaTokenizer, RobertaForSequenceClassification
from scipy.special import softmax
import json
import numpy as np
import torch


# Load tokenizer and RoBERTa model
TOKENIZER = RobertaTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
MODEL = RobertaForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest", num_labels=3)


# Data pre-processing function
def preprocess_text(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

# Sentiment classification function
def classify_sentiment(text):
    inputs = TOKENIZER.encode_plus(
        text,
        add_special_tokens=True,
        return_tensors="pt",
        truncation=True,
        padding='max_length',
        max_length=128
    )

    with torch.no_grad():
        outputs = MODEL(**inputs)
        logits = outputs.logits
        probs = softmax(logits.numpy(), axis=1)[0]

    print([type(d) for d in probs])

    sentiment = np.argmax(probs)

    return sentiment
