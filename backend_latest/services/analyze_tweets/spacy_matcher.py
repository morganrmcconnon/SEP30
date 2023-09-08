import spacy
from nltk.stem import WordNetLemmatizer
from spacy.matcher import Matcher
import os


def filter_tweet(json_data):
    lemmatizer = WordNetLemmatizer()

    # Load spaCy language model
    nlp = spacy.load("en_core_web_sm")

    # Initialize Matcher
    matcher = Matcher(nlp.vocab)

    keywords_file_path = "data\keywords2.txt"  # Replace with the actual path to your file
    keywords = set()

    with open(keywords_file_path, "r") as keyword_file:
        for line in keyword_file:
            # print(len(line.split()))
            line = line.lower()
            if len(line.split()) == 1:
                line = lemmatizer.lemmatize(line)
            else:
                doc = nlp(line)
                filtered_tokens = [token.text for token in doc if not token.is_stop]
                filtered_tokens.pop()
                cnt = len(filtered_tokens)
                if cnt == 0:
                    continue
                elif cnt == 1:
                    line = lemmatizer.lemmatize(filtered_tokens[0])
                else:
                    line = " ".join(filtered_tokens)
            keywords.add(line.strip())

    keyword_patterns = []

    for keyword in keywords:
        words = keyword.split()
        patterns = []
        if len(words) == 1:
            patterns.append({"LEMMA": lemmatizer.lemmatize(keyword)})
        else:
            for x in words:
                patterns.append({"LEMMA": x})
        keyword_patterns.append(patterns)

    matcher.add("KeywordPattern", keyword_patterns)

    #print(keyword_patterns)
    #print(len(keyword_patterns))

    # file_path = "D:\Swinburne\S2 2023\Capstone\\test.json"  # Replace with the actual path to your file

    cnt = 0
    result = []
    # with open(file_path, "r") as json_file:
    for line in json_data:
        #print(999, line)
        text = line["text"]
        doc = nlp(text)
        matches = matcher(doc)

        if len(matches) > 0:
            # print(f"Matched in '{text}':")
            # for match_id, start, end in matches:
            #  matched_text = doc[start:end].text
            #  print(f"  - '{matched_text}' at position {start}-{end}")
            cnt += 1
            #print(cnt)
            result.append(line)

    return result



def create_matcher_model():
    lemmatizer = WordNetLemmatizer()

    # Load spaCy language model
    NLP = spacy.load("en_core_web_sm")

    keywords_file_path = "data/keywords2.txt"  # Replace with the actual path to your file

    with open(keywords_file_path, "r") as keyword_file:
        lines = keyword_file.readlines()

    keywords = set()
    for line in lines:
        line = line.lower()
        if len(line.split()) == 1:
            line = lemmatizer.lemmatize(line)
        else:
            doc = NLP(line) # tokenize
            filtered_tokens = [token.text for token in doc if not token.is_stop] # remove stop words
            filtered_tokens.pop() # remove last word
            cnt = len(filtered_tokens) # count number of tokens
            if cnt == 0:
                continue
            elif cnt == 1:
                line = lemmatizer.lemmatize(filtered_tokens[0])
            else:
                line = " ".join(filtered_tokens)
        keywords.add(line.strip())

    keyword_patterns = []

    for keyword in keywords:
        
        words = keyword.split()
        
        if len(words) == 1:
            patterns = [{"LEMMA": lemmatizer.lemmatize(keyword)}]
        else:
            patterns = [{"LEMMA": x} for x in words]

        keyword_patterns.append(patterns)

    # Initialize Matcher
    matcher = Matcher(NLP.vocab)

    matcher.add("KeywordPattern", keyword_patterns)

    return matcher, NLP



def text_is_related_to_mental_health(text, matcher : Matcher, nlp : spacy.language.Language):
    
    doc = nlp(text)
    
    matches = matcher(doc)

    return len(matches) > 0