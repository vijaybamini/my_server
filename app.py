from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import credentials, db
import os
import json

app = Flask(__name__)

# Load Firebase credentials from environment variable
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
    """Fetches the latest sensor values."""
    ref = db.reference("data")  # Reference to "data" node
    data = ref.get()

    if not data:
        return jsonify({"error": "No data found"}), 404  # Handle empty database

    # ✅ Get the latest timestamp (highest key)
    latest_timestamp = sorted(data.keys(), reverse=True)[0]  # Get the latest entry
    latest_entry = data[latest_timestamp]

    # ✅ Format the response
    latest_data = {
        "dustbin_no": latest_entry.get("dustbin_no", "No data"),
        "percentage": latest_entry.get("percentage", "No data")
    }

    return jsonify(latest_data)  # Return latest sensor data

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
