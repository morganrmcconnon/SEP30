from flask import Flask, request
import time
import os
from features import sentiment_analysis_with_vader
from features import sentiment_analysis_with_roberta
from source import mySource
# from flask_vite import Vite

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


@app.route("/sentiment_vader", methods=["POST"])
def check_sentiment_with_vader():
    # Get content from client, process it on server, and return it
    data = request.get_json()
    text = data["text"]
    compound_score, sentiment_label = sentiment_analysis_with_vader.check_sentiment(text)
    return { 'compound_score': compound_score, 'sentiment_label': sentiment_label }


@app.route("/sentiment", methods=["POST"])
def check_sentiment_with_roberta():
    # Get content from client, process it on server, and return it
    data = request.get_json()
    text = data["text"]
    # Analyze the sentiment of text
    sentiment_result, confidence_probabilities = sentiment_analysis_with_roberta.classify_sentiment(text=text)

    return { 'sentiment_result': sentiment_result, 'confidence_probabilities': confidence_probabilities }

@app.route("/test", methods=["GET"])
def get_data_test():
    # Return content from server
    r = mySource()
    return {"topics": r[0], "\nnegative tweets": r[1][0], "\npositive tweets": r[1][1],"\nneutral tweets": r[1][2]}

# New endpoints/functions:
@app.route("/download_tweet", methods=["POST"])
def download_tweet():
    return {"message": "Download tweet endpoint"}

@app.route("/analyze_tweet", methods=["POST"])
def analyze_tweet():
    return {"message": "Analyze tweet endpoint"}

@app.route("/get_all_data", methods=["GET"])
def get_all_data():
    return {"message": "Get all data endpoint"}
