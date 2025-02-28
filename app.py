from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import credentials, db
import os
import json

app = Flask(__name__)

# Load Firebase credentials from Render environment variable
firebase_credentials = os.environ.get("FIREBASE_CREDENTIALS")

if firebase_credentials:
    cred_dict = json.loads(firebase_credentials)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://dustbinmonitor-c5e71-default-rtdb.firebaseio.com/"
    })
else:
    raise ValueError("Firebase credentials not found in environment variables.")

@app.route("/")
def index():
    return render_template("index.html")  # Your HTML file

@app.route("/get-data")
def get_data():
    """Fetches the latest distance value from Firebase."""
    ref = db.reference("data")  # Reference to the "data" node
    data = ref.get()

    if not data:
        return jsonify({"error": "No data found"}), 404  # Handle empty database

    # ✅ Get the latest key (Firebase keys are unordered, so we get the last one)
    latest_key = max(data.keys())  
    latest_distance = data[latest_key].get("distance", "No distance data")

    return jsonify({"distance": latest_distance})  # Return only the latest distance

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
