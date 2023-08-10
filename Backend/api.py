from flask import Flask, request
import time
import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from flask_vite import Vite

# Download the required data (run this only once)
nltk.download('vader_lexicon')

# Create a SentimentIntensityAnalyzer object
analyzer = SentimentIntensityAnalyzer()


# # Get and set directory for static files (ie. index.html, css, and bundled JS)
# # defaults to 'dist', the default name of Parcel's build directory
# build_dir = os.getenv("BUILD_DIR", "dist")
# print("Build dir:", build_dir)

# app = Flask(__name__, static_folder=f"../{build_dir}", static_url_path="/")

app = Flask(__name__)    
# vite = Vite(app)

# # or
# vite = Vite()
# vite.init_app(app)


@app.route("/")
def hello_world():
    return "<p>Hello, there!</p>"


@app.route("/data", methods=["GET"])
def get_data():
    # Return content from server
    return {"greeting": "Hello!!!!!!"}


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


@app.route("/sentiment", methods=["POST"])
def check_sentiment():
    # Get content from client, process it on server, and return it
    data = request.get_json()
    text = data["text"]
    # Analyze the sentiment of each text
    scores = analyzer.polarity_scores(text)
    compound_score = scores['compound']

    # Determine the sentiment label based on the compound score
    if compound_score >= 0.05:
        sentiment_label = 'Positive'
    elif compound_score <= -0.05:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'

    return {"sentiment_label": sentiment_label, "compound_score": compound_score, "text": text}