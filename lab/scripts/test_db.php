<?php
try {
  $pdo = new PDO("mysql:host=mysql;dbname=docker", "docker", "Your_D...w0rd", [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
  echo "OK\n";
  $tables = $pdo->query("SHOW TABLES")->fetchAll(PDO::FETCH_COLUMN);
  echo count($tables) . " tables\n";
  print_r(array_slice($tables, 0, 40));
} catch (Exception $e) {
  echo "ERR: " . $e->getMessage() . "\n";
  // Try without password
  try {
    $pdo2 = new PDO("mysql:host=mysql;dbname=docker", "docker", "");
    echo "Empty pwd OK\n";
  } catch (Exception $e2) {
    echo "Empty pwd ERR: " . $e2->getMessage() . "\n";
  }
}
