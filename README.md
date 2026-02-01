# PHP Filter Chain Lesson (Red70)

## What is a PHP Filter Chain?
A **PHP Filter Chain** is a powerful technique that exploits the `php://filter` stream wrapper in PHP. 

By chaining together specific character encoding filters (like `convert.iconv.UTF8.UTF16`, `convert.base64-encode`, etc.), an attacker can manipulate the data stream byte-by-byte. This capability allows attackers to:
1.  **Bypass WAFs**: Obfuscate payloads to evade detection.
2.  **Achieve RCE**: Generate arbitrary PHP code to be executed.
3.  **Blind File Read**: Create "Error Oracles" to leak sensitive files (like `config.php`) even when the application produces no output.

This challenge demonstrates a **Blind File Read** vulnerability where you must use an error oracle to extract the flag from the server.

---

## Quick Start (Run from DockerHub)
You can run this challenge instantly without cloning the code.

**Docker Run Command:**
```bash
docker run -d --restart always --name flag-red67 -p 9051:80 joshbeck2024/ctf-php-filter-chain-lesson-flag-red70:latest
```

Once running, access the challenge at: **http://localhost:9051**

---

## Build from Source

### Prerequisites
*   Docker
*   Docker Compose

### Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/androidteacher/PHP-Filter-Chain-Lesson.git
    cd PHP-Filter-Chain-Lesson
    ```

2.  **Start the container:**
    ```bash
    docker-compose up -d --build
    ```

3.  **Access the Challenge:**
    Navigate to `http://localhost:9051` in your browser.

---

## Solution Guide
Solution Guide: https://humble-raptor-f30.notion.site/Red70-PHP-Filter-Chain-Lesson-2fa4c8e523768061bc1dfc42e70737b9?source=copy_link
