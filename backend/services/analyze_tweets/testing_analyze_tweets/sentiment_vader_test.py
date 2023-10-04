from ..sentiment_vader import check_sentiment

# Test cases
test_cases = [
    {
        "text": "Psilocybin containing shrooms can help to reduce addiction, depression, anxiety\nPTSD when microdosed with a professional supervision, I know cause l'm undergoing it now, by doctor (Myco_durk on Instagram), I'm feeling better than ever. He helped me during my dark times",
        "expected_compound_score": 0.8016,
        "expected_sentiment_label": "Positive",
    },
    {
        "text": "Skyrocketing costs have Americans choosing between:\n\n-Food and Fuel\n\n-Fuel and Medications\n\n-Medications and Rent \n\nJoe Biden",
        "expected_compound_score": -0.5994,
        "expected_sentiment_label": "Negative",
    },
    {
        "text": "Hi! Good morning! Don't be so hard to yourself, you're doing great job! Your mental health is just as important as your physical health, be kind to your mind! Fighting!!",
        "expected_compound_score": 0.8085,
        "expected_sentiment_label": "Positive",
    },
    {
        "text": "Already getting anxiety about running out of candy 😖 I don’t want to be the Scrooge neighbor!",
        "expected_compound_score": -0.4019,
        "expected_sentiment_label": "Negative",
    },
    {
        "text": "i deserve to have my therapy expenses paid for these",
        "expected_compound_score": 0.4404,
        "expected_sentiment_label": "Positive",
    },
]

# Run test cases
for idx, test_case in enumerate(test_cases):
    text = test_case["text"]
    expected_compound_score = test_case["expected_compound_score"]
    expected_sentiment_label = test_case["expected_sentiment_label"]

    compound_score, sentiment_label = check_sentiment(text)

    if (
        round(compound_score, 4) == round(expected_compound_score, 4)
        and sentiment_label == expected_sentiment_label
    ):
        print(f"Test case {idx + 1}: PASS")
    else:
        print(f"Test case {idx + 1}: FAIL")
        print(f"Expected Compound Score: {expected_compound_score}")
        print(f"Expected Sentiment Label: {expected_sentiment_label}")
        print(f"Actual Compound Score: {compound_score}")
        print(f"Actual Sentiment Label: {sentiment_label}")

