from transformers import AutoModelForSequenceClassification

# from transformers import  TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import expit


MODEL_NAME = f"cardiffnlp/tweet-topic-latest-multi"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
class_mapping = model.config.id2label


def detect_topic_cardiffnlp_tweet_topic(text: str):
    """
    Detects the topic of a tweet using cardiffnlp/tweet-topic-latest-multi pretrained using RoBERTa.
    """

    tokens = tokenizer(
        text,
        add_special_tokens=True,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=1024,
    )
    output = model(**tokens)

    scores = output[0][0].detach().numpy()
    scores = expit(scores)

    # Map to classes
    return [
        {"topic_id": i, "topic_name": class_mapping[i], "topic_score": float(scores[i])}
        for i in range(len(scores))
    ]


# # TF
# tf_model = TFAutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
# class_mapping = tf_model.config.id2label
# text = "It is great to see athletes promoting awareness for climate change."
# tokens = tokenizer(text, return_tensors="tf")
# output = tf_model(**tokens)
# scores = output[0][0]
# scores = expit(scores)
# predictions = (scores >= 0.5) * 1

# # Map to classes
# for i in range(len(predictions)):
#     if predictions[i]:
#         print(class_mapping[i])
