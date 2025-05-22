from flask import Flask, jsonify
from data_collector import fetch_headlines
from sentiment import get_sentiment

app = Flask(__name__)

@app.route("/analyze", methods=["GET"])
def analyze_headlines():
    try:
        headlines = fetch_headlines()
        results = [get_sentiment(headline) for headline in headlines]
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
