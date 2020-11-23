from flask import Flask
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)
# cors = CORS(app)
vader = SentimentIntensityAnalyzer()

# cred = credentials.Certificate("cubstart-final-lecture-firebase-adminsdk-nisl0-a7faef9ae6.json")
# firebase_admin.initialize_app(cred)
# db = firestore.client()

@app.route("/")
def home():
    return "Welcome to cubstart!"

@app.route('/api/signup/<name>')
def signup_user(name):
    # Add a new line to the database in the following order:
    # ID, username, interests

    return "Hello " + name + "!"

@app.route('/api/delete/<id>')
def delete_user(id):
    # Delete the user with ID from the database

    return "Removed " + id + "!"

@app.route('/api/update/<new_update>')
def update_profile(new_update):
    # Updates the account with ID the updates in UPDATES
    return "Updated a user's " + new_update + "!"

# @app.route("/api/analyze_sentiment/<document_id>", )
# def analyze_text(document_id):
#     text = request.args.get("sentence")
#     sentiment = vader.polarity_scores(text)["compound"]
#     result = {"sentiment": sentiment}

#     doc = db.collection("sentiment-data").document(document_id)
#     doc.set(result, merge=True)

#     return {"success": "true"}




if __name__ == "__main__":
    app.run(debug=True, port=3000)

