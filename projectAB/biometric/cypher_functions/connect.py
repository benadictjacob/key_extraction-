from flask import Flask, request, jsonify
from threading import Thread, Lock
from .encription import data_to_token, token_to_data
import pyrebase
import time

app = Flask(__name__)

# Thread-safe shared data
class SharedData:
    def __init__(self):
        self.farm_id = 0
        self.matched_key = ""
        self.count = 0
        self.lock = Lock()

shared = SharedData()

# Firebase Configuration
config = {
    "apiKey": "AIzaSyBDbta51BTIhCXEq5xwWQA9l7HoobEsB1g",
    "authDomain": "newproject-2b8c0.firebaseapp.com",
    "databaseURL": "https://newproject-2b8c0-default-rtdb.firebaseio.com",
    "projectId": "newproject-2b8c0",
    "storageBucket": "newproject-2b8c0.appspot.com",
    "messagingSenderId": "201430695093",
    "appId": "1:201430695093:web:3206452e4bbf2fa49292fc",
    "measurementId": "G-83GCZQE8G3"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

@app.route('/from-esp', methods=['POST'])
def handle_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400

        print("\nReceived sensor data:")
        print(f"Temperature: {data.get('temperature')}°C")
        print(f"Humidity: {data.get('humidity')}%")
        print(f"Rain Status: {data.get('rain_status')}")
        print(f"Soil Moisture: {data.get('soil_moisture')}%")

        # Encrypt data
        with shared.lock:
            temp_enc = data_to_token(str(data.get('temperature')), shared.matched_key)
            humid_enc = data_to_token(str(data.get('humidity')), shared.matched_key)
            rain_enc = data_to_token(str(data.get('rain_status')), shared.matched_key)
            soil_enc = data_to_token(str(data.get('soil_moisture')), shared.matched_key)
            current_count = shared.count
            shared.count += 1

        sensor_data = {
            "temperature": temp_enc,
            "humidity": humid_enc,
            "RainStatus": rain_enc,
            "SoilMoisture": soil_enc,
            "timestamp": int(time.time())
        }

        print("Encrypted data:", sensor_data)

        # Store in Firebase
        base_path = f"farms/{shared.farm_id}/sensor_readings"
        db.child(f"{base_path}/readings/{current_count}").set(sensor_data)
        db.child(f"{base_path}/latest").set(sensor_data)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

def run_server():
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

def start_server(key, farm):
    with shared.lock:
        shared.matched_key = key
        shared.farm_id = farm
        shared.count = 0  # Reset counter when starting
    
    print(f"Starting Flask server on http://192.168.1.7:5000 for farm {shared.farm_id}")
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()