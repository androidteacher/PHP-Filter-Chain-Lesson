<?php
// Simulate a blind file read vulnerability
// The attacker controls $_GET['page']
// We use output buffering to make it 'blind' - the user sees no output regardless of what is included
// UNLESS they crash the process or cause a timeout (side-channel oracle)

$file = $_REQUEST['page'] ?? 'home.php';

ob_start();
include($file);
$content = ob_get_contents();
ob_end_clean();

echo "Request processed.";
// echo $content;
?>