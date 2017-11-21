// vonvert .csv to .xml
<?php

require("config.php");

// Start XML file, create parent node

$dom = new DOMDocument("1.0");
$node = $dom->createElement("AllgeoHops");
$parnode = $dom->appendChild($node);

// Opens a connection to a MySQL server

$connection=mysql_connect ('localhost', $username, $password);
if (!$connection) {  die('Not connected : ' . mysql_error());}

// Set the active MySQL database

$db_selected = mysql_select_db($database, $connection);
if (!$db_selected) {
  die ('Can\'t use db : ' . mysql_error());
}

// Select all the rows in the AllgeoHops table

$query = "SELECT * FROM AllgeoHops WHERE 1";
$result = mysql_query($query);
if (!$result) {
  die('Invalid query: ' . mysql_error());
}

header("Content-type: text/xml");

// Iterate through the rows, adding XML nodes for each

while ($row = @mysql_fetch_assoc($result)){
  // Add to XML document node
  $node = $dom->createElement("marker");
  $newnode = $parnode->appendChild($node);
  $newnode->setAttribute("idHop",$row['idHop']);
  $newnode->setAttribute("ipSrc",$row['ipSrc']);
  $newnode->setAttribute("country", $row['country']);
  $newnode->setAttribute("city", $row['city']);
  $newnode->setAttribute("latitude", $row['latitude']);
  $newnode->setAttribute("longitude", $row['longitude']);
}

echo $dom->saveXML();

?>