import spacy
from nltk.stem import WordNetLemmatizer
from spacy.matcher import Matcher
import json

lemmatizer = WordNetLemmatizer()

# Load spaCy language model
nlp = spacy.load("en_core_web_sm")

# Initialize Matcher
matcher = Matcher(nlp.vocab)

file_path = "D:\Swinburne\S2 2023\Capstone\keywords.txt"  # Replace with the actual path to your file
keywords = set()
# Read keywords from the file
with open(file_path, "r") as keyword_file:
    for line in keyword_file:
        #print(len(line.split()))
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
            patterns.append({"LOWER": x})
    keyword_patterns.append(patterns)

matcher.add("KeywordPattern", keyword_patterns)

print(keyword_patterns)
print(len(keyword_patterns))
# Example text
text = "autism, kill"



# Print match details
file_path = "D:\Swinburne\S2 2023\Capstone\\test.json"  # Replace with the actual path to your file
cnt = 0
with open(file_path, "r") as json_file:
    for line in json_file:
        text = (json.loads(line))["text"]
        doc = nlp(text)
        matches = matcher(doc)

        if len(matches) > 0:
            print(f"Matched in '{text}':")
            for match_id, start, end in matches:
                matched_text = doc[start:end].text
                print(f"  - '{matched_text}' at position {start}-{end}")
            cnt += 1
            print(cnt)
        #else:
            #print(f"No matches in '{text}'")

