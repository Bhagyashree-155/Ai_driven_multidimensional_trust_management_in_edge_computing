import requests
import time

def probe(url):
    try:
        start = time.time()
        r = requests.get(url, timeout=2)

        latency = (time.time() - start) * 1000
        success = 1 if r.status_code == 200 else 0

    except:
        latency = 2000
        success = 0

    return latency, success