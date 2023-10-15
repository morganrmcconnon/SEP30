import os
from gensim.models.ldamodel import LdaModel
import json

CURRENT_DIR = os.path.dirname(__file__)
TOPIC_MODEL_FILE = os.path.join(CURRENT_DIR, "../topic_model/lda_model.model")
TOPIC_VALUES_FILE = os.path.join(CURRENT_DIR, "../topic_model/topics.json")

def load_pretrained_model():
    """
    Loads a pretrained model from the file system.
    """

    # Load the model
    lda_model = LdaModel.load(TOPIC_MODEL_FILE)

    # Load the topics
    with open(TOPIC_VALUES_FILE, "r") as f:
        topics_values = json.load(f)

    return lda_model, topics_values