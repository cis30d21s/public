import time
import requests

while True:
    requests.get('http://localhost:5000/ping')
    time.sleep(1)
