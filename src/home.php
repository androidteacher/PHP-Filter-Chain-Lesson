<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PHP Filter Chain Blind Oracle</title>
    <link rel="stylesheet" href="style.css">
</head>

<body>
    <div class="container">
        <h1>PHP Filter Chain Attack</h1>

        <p>
            Welcome to the <strong>Blind Oracle</strong> challenge.
            This application allows you to include files via the <code class="highlight">?page=</code> parameter,
            but the output is suppressed (blind).
        </p>

        <p>
            <strong>What is a Filter Chain?</strong><br>
            It is a technique that uses <code>php://filter</code> to manipulate data streams.
            By chaining specific character encodings (like UTF-16, Base64, etc.), an attacker can
            generate arbitrary content or, in this case, create an <strong>Error Oracle</strong> to leak files
            bit-by-bit.
        </p>

        <div class="code-block">
            Target Flag: <span class="highlight">/flag/flag.txt</span>
        </div>

        <p>
            Use this technique to bypass WAFs, achieve RCE, or read sensitive files when you have no direct output.
        </p>

        <a href="?page=source.php" class="button">View Source Code</a>
    </div>
</body>

</html>