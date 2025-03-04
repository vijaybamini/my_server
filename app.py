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
    """Fetches the latest distance values from Firebase for both sensors."""
    ref = db.reference("data")  # Reference to "data" node
    data = ref.get()

    if not data:
        return jsonify({"error": "No data found"}), 404  # Handle empty database

    # ✅ Get the latest key (Firebase keys are timestamps, so get the last one)
    latest_key = max(data.keys(), key=lambda k: k if k.startswith("-") else "")  # Ignore non-auto keys
    latest_entry = data[latest_key]  # Get latest sensor data

    # ✅ Extract sensor data
    sensor1 = latest_entry.get("sensor1", {"distance": "No data", "battery": "No data"})
    sensor2 = latest_entry.get("sensor2", {"distance": "No data", "battery": "No data"})

    return jsonify({
        "sensor1": sensor1,
        "sensor2": sensor2
    })  # Return latest sensors

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
