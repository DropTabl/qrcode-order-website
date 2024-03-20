<?php
header('content-type: application/json');
$avail_cocktails = array();
$avail_cocktails["Gin Tonic"] = true;
$avail_cocktails["Mai Tai"] = true;
$avail_cocktails["Mojito"] = true;
echo json_encode($avail_cocktails);
exit;
?>
