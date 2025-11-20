import requests
from twilio.rest import Client
import time
import sys

# ---------------- Twilio credentials ----------------
ACCOUNT_SID = "ACaa2fa6b1d38ad241d20b9e85887301f2"
AUTH_TOKEN = "60777c114ab55ca3279940052e7f32fb"
FROM_NUMBER = "+19047504962"   # Twilio number
TO_NUMBER = "+919488848836"    # Your verified phone number

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# ---------------- ThingSpeak credentials ----------------
CHANNEL_ID = "3169156"
READ_API_KEY = "D6G87GC56AN3CSSO"

# ---------------- Thresholds ----------------
SOIL_THRESHOLD = 40  # percentage
CHECK_INTERVAL = 60  # seconds

# ---------------- Functions ----------------
def send_alert(message):
    try:
        msg = client.messages.create(
            body=message,
            from_=FROM_NUMBER,
            to=TO_NUMBER
        )
        print(f"[ALERT SENT] {msg.sid} | {message}")
    except Exception as e:
        print(f"[ERROR] Failed to send SMS: {e}")

def fetch_latest_thingspeak():
    try:
        url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?results=1&api_key={READ_API_KEY}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        feed = data['feeds'][0]
        return {
            'temperature': float(feed['field1']),
            'humidity': float(feed['field2']),
            'soil': float(feed['field3']),
            'timestamp': feed['created_at']
        }
    except Exception as e:
        print(f"[ERROR] Failed to fetch ThingSpeak data: {e}")
        return None

def predict_irrigation(latest_soil, crop_type="rice", soil_type="loamy"):
    # Simple predictive logic: trigger if soil below min threshold
    min_soil = 50 if crop_type=="rice" else 40
    return latest_soil < min_soil

# ---------------- Main Loop ----------------
print("=== SmartAgri SMS Alert System Started ===")
print("Fetching data every", CHECK_INTERVAL, "seconds...\n")

try:
    while True:
        latest = fetch_latest_thingspeak()
        if latest:
            print(f"[DATA] {latest['timestamp']} | Temp: {latest['temperature']}°C | Humidity: {latest['humidity']}% | Soil: {latest['soil']}%")

            # Soil moisture alert
            if latest['soil'] < SOIL_THRESHOLD:
                send_alert(f"⚠️ Soil moisture low: {latest['soil']}%! Irrigation needed.")

            # Predicted irrigation alert
            if predict_irrigation(latest['soil']):
                send_alert(f"📅 Predicted irrigation needed soon for crop based on soil and crop type!")

        time.sleep(CHECK_INTERVAL)
except KeyboardInterrupt:
    print("\n[INFO] Script terminated by user.")
except Exception as e:
    print(f"[ERROR] Unexpected exception: {e}")
finally:
    print("[INFO] Exiting script. Press Enter to close.")
    input()
