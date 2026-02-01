# PHP Filter Chain Lesson (Red70)

## Quick Start
Run the challenge instantly:

```bash
docker run -d \
  --restart always \
  --name flag-red67 \
  -p 9051:80 \
  joshbeck2024/ctf-php-filter-chain-lesson-flag-red70:latest
```

## Challenge Description
This challenge demonstrates a **Blind File Read** vulnerability using PHP Filter Chains. You must exploit an output-buffered `include()` call to leak the contents of `/flag/flag.txt`.

## Solution Guide
Solution Guide: https://humble-raptor-f30.notion.site/Red70-PHP-Filter-Chain-Lesson-2fa4c8e523768061bc1dfc42e70737b9?source=copy_link
