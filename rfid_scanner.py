import time
import requests

RFID_API_ENDPOINT = "http://192.168.178.47:8080/rfid"

def simulate_rfid_scan(rfid_code):
    response = requests.post(RFID_API_ENDPOINT, data={'rfid': rfid_code})
    return response

if __name__ == "__main__":
    while True:
        rfid_code = input("Enter RFID code to simulate scan: ")
        response = simulate_rfid_scan(rfid_code)
        print(f"Response: {response.text}")
        time.sleep(2)
