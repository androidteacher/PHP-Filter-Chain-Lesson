# PHP Filter Chain Oracle: Deep Dive Explanation

## 1. The Attack Concept: The "Safe = Hex" Oracle

We are blindly reading a file. We can't see the output, but we can measure **Server Stress**.
Our Oracle uses a **Logic Gate** based on the file's content.

### The Gate Components
1.  **Dechunk Filter**: Acts as the gatekeeper.
    *   **Behavior**: It looks at the **very first character** of the stream.
    *   **If Hex (0-9, A-F)**: It tries to process the data as "Chunked", FAILS (because it's not valid chunked data), and **DISCARDS** the rest. Result: **Empty Stream**.
    *   **If Non-Hex**: It ignores the data and **PASSES** it through. Result: **Full Stream**.

2.  **Size Bomb**: The punishment.
    *   A chain of filters that multiplies data size.
    *   **If Input is Empty**: Output is Empty. **(Safe - 200 OK)**
    *   **If Input is Full**: Output is Massive. **(Crash - 500/Timeout)**

### The Logic Table
| First Char | Is it Hex? | Dechunk Action | Bomb Input | Server Result | Deduction |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`A`** | YES | Drop Data | Empty | **Fast Response** | It was Hex! |
| **`G`** | NO | Pass Data | Huge Data | **Crash/Timeout** | It was NOT Hex. |

---

## 2. Step-by-Step Deduction Example (3 Characters)

Target String: `f` `l` `a` ... (Start of "flag")

### Deduction 1: Character 1 (`f`)
**Goal:** Determine if Char 1 is Hex.
1.  **Current Stream:** `f l a g ...`
2.  **Check:** Apply `dechunk|bomb`.
3.  **Dechunk sees:** `f`.
4.  **Is `f` Hex?** YES.
5.  **Action:** Dechunk tries to parse, fails, destroys data.
6.  **Bomb:** Receives nothing.
7.  **Result:** **Fast Response**.
8.  **Conclusion:** The first character is one of `[0-9, a-f]`. (We essentially "know" it's hex, narrowing it down significantly. We can then binary search the specific hex digit).

### Deduction 2: Character 2 (`l`) - The Non-Hex Case
**Goal:** We've shifted the stream. Now Char 2 is at the front.
1.  **Shift Operation:** (Detailed below).
2.  **Current Stream:** `l a g ...`
3.  **Check:** Apply `dechunk|bomb`.
4.  **Dechunk sees:** `l`.
5.  **Is `l` Hex?** NO.
6.  **Action:** Dechunk ignores it. Passes `l a g ...` to the bomb.
7.  **Bomb:** Explodes.
8.  **Result:** **CRASH**.
9.  **Conclusion:** The character is **NOT Hex**.

**"How do we find out what it IS then?"**
We must **Map** it to Hex.
We construct a filter chain that says: *"If the character is 'l', turn it into 'A'. If it's anything else, turn it into '?'"*

1.  **Apply Transformation:** `Map(l -> A)`.
2.  **Current Stream:** `A ...` (Because it *was* `l`).
3.  **Check:** Apply `dechunk|bomb`.
4.  **Dechunk sees:** `A`.
5.  **Is `A` Hex?** YES.
6.  **Action:** Drop Data -> **Fast Response**.
7.  **Conclusion:** Since we got a Fast Response, our input *must* have successfully mapped to 'A'. Therefore, the input *must* have been `l`.

---

## 3. Deep Dive: The Shifting & Conversion ("0s and 1s")

The user asked: *"Show how it is converted and interpreted as hex even though it is not."*

Let's look at the **Shift** operation for the second character (`l`).
We use `convert.iconv.UTF16.UTF16`.

**Initial Bytes (ASCII):**
`66 6C 61 67` (`f l a g`)

**Step A: Convert to UTF-16**
*Expands 8-bit bytes to 16-bit.*
`00 66 00 6C 00 61 00 67` (`.f.l.a.g`)

**Step B: The "Shift" (The 0s and 1s Trick)**
We apply a filter usually used for re-encoding, but we abuse the **Byte Order Mark (BOM)**.
When converting TO UTF-16, PHP prepends `FE FF` (or `FF FE`).

**Transformation:**
Input: `00 66 00 6C 00 61 00 67`
Output: `FE FF 00 66 00 6C 00 61 00 67`

**The "Misinterpretation" (The Bit Shift)**
Now, we convert back or treat this stream as a different encoding (like UCS-2 or just reading it offset).
Crucially, look at the alignment.
Original Index 0: `66` ('f')
Original Index 1: `6C` ('l')

After adding 2 bytes (`FE FF`) at the start:
New Index 0: `FE`
New Index 1: `FF`
New Index 2: `00`
New Index 3: `66`
...
By adding specific garbage bytes at the start, we change alignment.
Advanced chains use combinations like `UTF-16LE` (Little Endian) vs `UTF-16BE` (Big Endian) to **swap** bytes.
`00 6C` (Big Endian 'l') -> `6C 00` (Little Endian).

**Making 'l' resemble 'A' (Transformation)**
We don't shift bits of 'l' (`01101100`) to make `A` (`01000001`).
We use a **Lookup Table** (Charset).
Filter: `convert.iconv.CP1046.UTF8` (Example hypothetic chain).
*   In CP1046, byte `0x6C` might verify as a letter that, when converted to UTF-8, becomes `0x41` ('A').
*   It's a "dictionary attack" on the character sets. We find a path through the dictionaries that leads `l` -> `A`.

---

## 4. Using the Tool: `php_filter_chains_oracle_exploit`

**Correction:** The `php_filter_chain_generator` tool *only* generates the raw filter string. It does not run the attack loop.
The tool you need for the "Blind File Read" attack is a separate script, often found in a related repository or as a standalone exploit.

**Recommended Tool:** `php_filter_chains_oracle_exploit` (by Synacktiv).

### Step 1: Download
```bash
git clone https://github.com/synacktiv/php_filter_chains_oracle_exploit.git
cd php_filter_chains_oracle_exploit
```

### Step 2: Run the Attack
This tool effectively runs the "Explanation.md" logic loop for you.

```bash
# Example Command (Corrected)
python3 filters_chain_oracle_exploit.py \
    --target "http://localhost:9051/index.php" \
    --parameter "page" \
    --file "/flag/flag.txt"
```

*   `--target`: The URL of the vulnerable page.
*   `--parameter`: The GET parameter susceptible to `include`.
*   `--file`: The remote file you want to read.

### Custom Python Implementation
If you were writing your own `oracle_solver.py` (like the demo provided), you would need to:
1.  Import the `filters` (chains) from a library.
2.  Implement the `check_oracle` function (as shown in `oracle_solver.py`).
3.  Loop through every character position.
4.  Loop through every possible character.

### Custom Python Implementation
If you were writing your own `oracle_solver.py` (like the demo provided), you would need to:
1.  Import the `filters` (chains) from a library.
2.  Implement the `check_oracle` function (as shown in `oracle_solver.py`).
3.  Loop through every character position.
4.  Loop through every possible character.

The `php_filter_chains_oracle_exploit` tool bundles all of this (the thousands of chain maps) into its database.

## 5. Critical Server Configuration
For this "Blind Oracle" to work reliably, the server needs specific tuning. If the server is "too strong" or "too verbose", the oracle fails.

### A. Memory Limit
The "Bomb" works by exhausting memory.
-   **Standard (128M)**: Often too resilient for the default bomb payload.
-   **Tuned (8M - 64M)**: Ensures the bomb causes a crash reliability.
-   **Config:** `memory_limit = 8M` in `php.ini`.

### B. Error Handling
The tool relies on distinguishing a **Crash** (500 Error) from a **Success** (200 OK).
-   **display_errors = On**: The server returns 200 OK even on Fatal Errors (printing the error text). The tool sees "200" and thinks "Safe", leading to false negatives.
-   **display_errors = Off**: The server returns **500 Internal Server Error** on Fatal Errors. This provides the clean boolean signal the tool needs.


