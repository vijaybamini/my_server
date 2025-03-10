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
    """Fetches the latest sensor values for three dustbins (32, 35, 36)."""
    ref = db.reference("data")  # Reference to "data" node
    data = ref.get()

    if not data:
        return jsonify({"error": "No data found"}), 404  # Handle empty database

    dustbins_to_fetch = ["32", "35", "36"]  # Only fetch these dustbins
    latest_data = {}

    # ✅ Extract latest entry for each dustbin
    for dustbin_id in dustbins_to_fetch:
        dustbin_entries = data.get(dustbin_id, {})  # Get dustbin entries
        if isinstance(dustbin_entries, dict) and dustbin_entries:
            latest_entry_key = max(dustbin_entries.keys())  # Get latest timestamp
            latest_entry = dustbin_entries[latest_entry_key]

            # Get percentage and apply the new condition
            percentage = latest_entry.get("percentage", "No data")
            if isinstance(percentage, (int, float)):  # Ensure it's a number
                if percentage > 100 or percentage < 0:  
                    percentage = 100  # If out of range, set to 100
            else:
                percentage = "No data"  # If data is invalid

            latest_data[dustbin_id] = {
                "dustbin_no": latest_entry.get("dustbin_no", dustbin_id),
                "percentage": percentage  # Send modified percentage
            }

    return jsonify(latest_data)  # Returns data for three dustbins

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
