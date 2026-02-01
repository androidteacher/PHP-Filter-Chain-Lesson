<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Source Code</title>
    <link rel="stylesheet" href="style.css">
    <style>
        /* Override container for code view */
        .container {
            max-width: 1000px;
            text-align: left;
        }

        .source-code {
            background: #fff;
            padding: 20px;
            border-radius: 5px;
            color: #333;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>Vulnerable Source Code</h1>
        <div class="source-code">
            <?php highlight_file('index.php'); ?>
        </div>
        <div style="text-align: center; margin-top: 20px;">
            <a href="?page=home.php" class="button">Back to Home</a>
        </div>
    </div>
</body>

</html>