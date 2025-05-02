from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer #type:ignore

analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        sentiment = "positive"
    elif compound <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    return {
        "text": text,
        "sentiment": sentiment,
        "score": compound
    }

# Test it with some sample headlines
if __name__ == "__main__":
    sample_texts = [
        "Microsoft announces massive layoffs.",
        "Apple's new device is a game changer!",
        "Google maintains steady profits this quarter."
    ]
    
    for text in sample_texts:
        result = get_sentiment(text)
        print(f"{result['text']} → {result['sentiment'].upper()} ({result['score']})")


