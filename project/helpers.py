from flask import redirect, session, render_template, flash, url_for
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
        

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def give_message(message_text, type, redirect_to=None):

    flash(message_text, type)

    if redirect_to:
        return redirect(url_for(redirect_to))
    
