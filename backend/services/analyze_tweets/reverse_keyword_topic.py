import os
import json

if __name__ == "__main__":

    from analyze_tweets.topic_modelling import load_model, apply_lda

    current_dir = os.path.dirname(os.path.realpath(__file__))
    model_path = os.path.join(current_dir, '..', "topic_model", "lda_model.model")
    model = load_model(model_path)

    def get_topics(text):
        topics = apply_lda(text, model)
        # Serialize the topics
        topics = [[topic[0], float(topic[1])] for topic in topics]
        return topics

    word_list = []
    with open(os.path.join(current_dir, "data/keywords2.txt")) as f:
        for line in f:
            word_list.append(line.strip())

    topics = {word: get_topics(word) for word in word_list}
    with open(os.path.join(current_dir, "data/keywords2_topics.json"), "w") as f:
        json.dump(topics, f)
    predicts = {word: max(topics[word], key=lambda x: x[1]) for word in topics}
    with open(os.path.join(current_dir, "data/keywords2_predicts.json"), "w") as f:
        json.dump(predicts, f)