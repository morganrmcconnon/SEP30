
#Using a json file from Google Drive as the data source
#pip install transformers scipy pandas torch

from transformers import RobertaTokenizer, RobertaForSequenceClassification
from scipy.special import softmax
import json
import numpy as np
from google.colab import drive
import torch

# Mount Google Drive
drive.mount('/content/drive')

# Load tokenizer and RoBERTa model
tokenizer = RobertaTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
model = RobertaForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest", num_labels=3)

# Data pre-processing function
def preprocess_text(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

# Sentiment classification function
def classify_sentiment(model, tokenizer, text):
    inputs = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        return_tensors="pt",
        truncation=True,
        padding='max_length',
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = softmax(logits.numpy(), axis=1)[0]

    sentiment = np.argmax(probs)

    return sentiment


# Load data from tweet.json and process each line separately
with open("/content/drive/MyDrive/ML_Data/tweet.json", "r") as f:
    lines = f.readlines()
    data = [json.loads(line) for line in lines]

# Extract tweet "text" data
texts = [entry["text"] for entry in data]

# Preprocess texts
processed_texts = [preprocess_text(text) for text in texts]

# Perform sentiment analysis
sentiments = [classify_sentiment(model, tokenizer, text) for text in processed_texts]

# Print the results
for text, sentiment in zip(texts, sentiments):
    print(f"Tweet: {text}")
    print(f"Predicted Sentiment: {sentiment} (Negative: 0, Neutral: 1, Positive: 2)")
    print("=" * 50)
