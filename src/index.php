<?php
// Simulate a blind file read vulnerability
// The attacker controls $_GET['page']
// We use output buffering to make it 'blind' - the user sees no output regardless of what is included
// UNLESS they crash the process or cause a timeout (side-channel oracle)

$file = $_REQUEST['page'] ?? 'home.php';

if ($file === 'home.php' || $file === 'source.php') {
    // Normal mode: Display instructions or source
    include($file);
} else {
    // Challenge mode: Blind include
    ob_start();
    include($file);
    ob_get_clean(); // Discard output
    echo "Request processed.";
}
?>