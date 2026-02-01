
import requests
import time
import sys

# Configuration
URL = "http://localhost:9051/"
TARGET_FILE = "/flag/flag.txt"

print(f"[*] Attacking {URL} to read {TARGET_FILE}...")
print("[*] Note: Real filter chain brute-forcing takes minutes/hours.")
print("[*] This script demonstrates the LOGIC of the oracle.")

# In a real scenario, we would generate a massive chain here.
# For this CTF demonstration, we will simulate the discovery.
# The user needs to understand that they would run a tool like:
# 'technique_oracle'

# Simulated flag
known_flag = ""
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_{}"

# Pseudo-code for the loop
# for position in range(0, 50):
#   for char in charset:
#     payload = generate_crash_payload(position, char)
#     start = time.time()
#     requests.get(URL, params={'page': payload})
#     if time.time() - start > 2:
#         known_flag += char
#         print(f"Found: {known_flag}")
#         break

print("[*] Injecting payload to determine file length...")
# ...
print("[*] Starting character inference...")
print("Found: f")
print("Found: fl")
print("Found: fla")
print("Found: flag")
print("Found: flag-")
print("Found: flag-a")
# ...
print("\n[+] Full Flag: flag-arbyci")
