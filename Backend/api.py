from flask import Flask, request
import time
import os
# from flask_vite import Vite

import sentiment_analysis_with_vader
import sentiment_analysis_with_roberta




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
    print(data)
    text = data["text"]
    compound_score, sentiment_label = sentiment_analysis_with_vader.check_sentiment(text)
    return { 'compound_score': compound_score, 'sentiment_label': sentiment_label }


@app.route("/sentiment", methods=["POST"])
def check_sentiment_with_roberta():
    # Get content from client, process it on server, and return it
    data = request.get_json()
    print(data)
    text = data["text"]
    # Analyze the sentiment of text
    result = sentiment_analysis_with_roberta.classify_sentiment(text=text)

    return { "sentiment_result": int(result) }