<?php
// serve_cocktails.php
header('Content-Type: application/json');

$filePath = 'recepies.json'; // Adjust the path as necessary

if (file_exists($filePath)) {
    readfile($filePath);
} else {
    echo json_encode(array("error" => "File not found"));
}
?>
