import time
import requests

CHANNEL_ID = "3169156"
READ_API_KEY = "D6G87GC56AN3CSSO"

def get_latest_data():
    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?results=1&api_key={READ_API_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
        try:
            data = r.json()['feeds'][0]
            print("Temp:", data['field1'], "°C")
            print("Humidity:", data['field2'], "%")
            print("Soil:", data['field3'], "%\n")
        except:
            print("Invalid data")
    else:
        print("Error fetching data")

while True:
    get_latest_data()
    time.sleep(5)    # read every 5 sec
