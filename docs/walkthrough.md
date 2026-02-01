# PHP Filter Chain Blind Oracle Walkthrough

## The Challenge
We have a **Blind File Read** vulnerability:
```php
include($_GET['page']); // Output is buffered and discarded
```
We cannot see the content. We need an **Oracle**—a way to ask "Is the first character 'A'?" and get a yes/no answer based on a side-channel (time or error).

## The Oracle Strategy
The most robust method for this (popularized by Synacktiv) is the **Error-Based Oracle** or **Memory Exhaustion Oracle**, but optimized to be a "Boolean Oracle".

We use `php://filter` to transform the file content.
Crucially, we can **Base64 encode** the file content first:
`php://filter/codert.base64-encode/resource=/flag/flag.txt`
Now the content is `ZmxhZy...` (alphanumeric + `+`/`/`).

### Step 1: Align the Target Character (Shifting)
We want to guess the $N$-th character. We apply filters to **shift** or **delete** the first $N-1$ characters.

**Deep Dive: `convert.iconv.UTF16.UTF16` for Shifting**
This filter is often used to "prepend" bytes, effectively shifting the string.
Why? Because `iconv` adds a **BOM (Byte Order Mark)** when converting *to* UTF-16, even if the input is already UTF-16.

**Hex Dump Visualization:**
Let's see what happens to the string "ABCD".

**Initial State (ASCII/UTF-8):**
`41 42 43 44`  ("ABCD")

**Action 1: Convert UTF-8 to UTF-16BE (Big Endian)**
`00 41 00 42 00 43 00 44`
*(Every character is now 2 bytes)*

**Action 2: Apply `convert.iconv.UTF16.UTF16`**
Ideally this does nothing? NO. It sees the input as "UTF-16" and converts it to "UTF-16".
Crucially, when writing UTF-16, it often **prepends the BOM (`FE FF` or `FF FE`)**.

**Transformation:**
Input (from step 1): `00 41 00 42 00 43 00 44`
Output: `FE FF 00 41 00 42 00 43 00 44`

**Result:**
The string has grown by 2 bytes at the start!
If we interpret this later as something else, "A" (`41`) is now at offset 3 instead of offset 1 (0-indexed).

| Step | Hex Bytes | ASCII/Representation | Note |
| :--- | :--- | :--- | :--- |
| **Original** | `41 42 43 44` | `A B C D` | Target 'A' at index 0 |
| **UTF16BE** | `00 41 00 42 00 43 00 44` | `.A.B.C.D` | Expanded |
| **+Filter** | `FE FF 00 41 00 42 00 43 00 44` | `.. .A.B.C.D` | **Shifted Right by 2 bytes!** |

By repeating this, we can push the original text to the right.
Conversely, we can use specific encodings (like `UTF-7`) to consume/delete bytes or shift left.

### Step 2: The "Magic" Encoding Oracle (Dechunk + Size Bomb)

This challenge uses a robust **"Yes/No" Oracle** to identify characters.
The core mechanism involves two components: the **Dechunk Filter** and the **Size Bomb**.

#### 1. The "Bomb" (The Potential Crash)
We use a chain of `iconv` filters (specifically `UCS-4` or similar) to multiply the data size exponentially.
*   **Normal**: "A" -> (filters) -> Huge String (GBs) -> **CRASH** (Memory Limit Exceeded).
*   **Empty**: "" -> (filters) -> "" -> **NO CRASH**.

#### 2. The "Switch" (Why Hex Avoids the Crash)
We use the `dechunk` filter *before* the bomb.
Its job is to parse the input as "Chunked Transfer Encoding" (like HTTP).
`dechunk` expects a hexadecimal length at the start (e.g. `A` or `3`).

*   **If First Char IS Hex (0-9, a-f, A-F):**
    *   `dechunk` sees 'A', thinks "Ah, a chunk of length 10!".
    *   It tries to read the chunk. But the file format is wrong (no CRLF).
    *   **Crucial Mechanism:** `dechunk` FAILS to parse and **discards the data**.
    *   **Result:** The stream becomes EMPTY. The logic proceeds to the "Bomb", which receives nothing. 0 * 1000 = 0. **NO CRASH**.

*   **If First Char IS NOT Hex (e.g., 'G', 'Z'):**
    *   `dechunk` sees 'G', thinks "Not a hex digit. Not a chunk."
    *   It passes the data through UNCHANGED.
    *   **Result:** The full string reaches the "Bomb". 1 * 1000 = HUGE. **CRASH**.

#### Summary of the Oracle Logic

| First Character | Dechunk Action | Input to Bomb | Result | Conclusion |
| :--- | :--- | :--- | :--- | :--- |
| **Hex (e.g. 'A')** | Discards Data | Empty String | **NO Error** | Character IS Hex |
| **Non-Hex (e.g. 'G')** | Passes Data | Full String | **FATAL Error** | Character IS NOT Hex |

By shifting different characters to the "First Position" (Step 1) and checking if they cause a crash or not, we can deduce if they are Hexadecimal.
To find specific letters, we use *other* encodings to map our target letter (like 'Z') into a Hex letter (like 'A') while mapping everything else to Non-Hex.

**Visualizing the "Hex Dump" Interaction:**
Suppose we want to check if the char is 'A' (Hex 0x41).
1.  **Shift:** Move 'A' to the front. Stream starts with `41 ...`.
2.  **Dechunk:** Reads `41` (A). Valid Hex? YES.
3.  **Action:** Tries to dechunk -> Fails -> **Empties Stream**.
4.  **Bomb:** Receives nothing. **Safe.**
5.  **Oracle says:** "Safe response" means "It was Hex".

This is how we "read" the file blindly.

### The Encoding Chart
The user specifically asked for "ASCII to a-f" conversion breakdown.
While we don't convert `A` to `4` `1`, we effectively map `A` to a "index" in our oracle.

| Original Char | ASCII Hex | Filter Chain Transformation (Conceptual) | Resulting Byte | Behavior |
| :--- | :--- | :--- | :--- | :--- |
| **A** | `0x41` | `UTF8` -> `CP037` -> `IBM...` -> `ISO...` | `0x51` ('Q') | **CRASH** (Match) |
| **B** | `0x42` | `UTF8` -> `CP037` -> `IBM...` -> `ISO...` | `0x00` (Null) | **OK** (No Match) |
| **C** | `0x43` | `UTF8` -> `CP037` -> `IBM...` -> `ISO...` | `0x00` (Null) | **OK** (No Match) |
| ... | ... | ... | ... | ... |

*Note: The actual chains are auto-generated and look like `convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|...` repeated hundreds of times.*

## Exploit POC

Refer to the `solver.py` (to be created) for the automation of this logic.
We will use a pre-generated chain logic or a simplified version for demonstration.
For the purpose of this "Lesson", user should use a tool like `php_filter_chain_generator` to generate the payloads for reading files.

**Command to generate payload:**
```bash
python3 php_filter_chain_generator.py --chain "<?php system('ls'); ?>"
```
*Wait, that's for RCE (writing files).*
For **Reading Files** blindly, we need the Oracle mode.
```bash
# Example Oracle Logic
# 1. Base64 encode the file content twice.
# 2. Use a filter chain that crashes if the Nth character is 'X'.
```
