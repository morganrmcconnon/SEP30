import os


def load_mental_health_keywords(file_path):
    keywords = set()

    # Read keywords from the file
    with open(file_path, "r") as keyword_file:
        for line in keyword_file:
            keywords.add(line.lower())

    #print(keywords)
    return keywords


def define_topics(topics):
    r = set()

    file_path = os.path.join(os.path.dirname(__file__), "../../data/keywords2.txt")  # Replace with the actual path to your file

    keywords = load_mental_health_keywords(file_path)

    for topic in topics:
        # print(topic[1])
        topicWords = topic[1].split('"')
        # print(topicWords)
        for i in range(1, len(topicWords), 2):
            for tp in keywords:
                if topicWords[i] in tp:
                    r.add(tp.replace("\n", ""))
                    break

    return r


