from flask import redirect, session
from functools import wraps
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def get_tone(text):
    '''Get the tone of the text'''

    if (not text) or (text == ''):
        return None
    
    sent = SentimentIntensityAnalyzer()
    scores = sent.polarity_scores(text)
    tone = max(scores, key=scores.get)

    match tone:
        
        case "pos":
            return "Mostly Positive"
        
        case "neg":
            return "Mostly Negative"
        
        case _:
            return "Neutral"