<?php
session_start();

$proxy_url = "http://localhost:5000/oauth";

if (isset($_GET['code'])) {
    $callback_url = "http://localhost:5000/callback?code=" . urlencode($_GET['code']);
    $response = file_get_contents($callback_url);
    $user_data = json_decode($response, true);
    
    if ($user_data && !isset($user_data['error'])) {
        echo "<h1>Bienvenue, " . htmlspecialchars($user_data['name']) . "</h1>";
        echo "<p>Email : " . htmlspecialchars($user_data['email']) . "</p>";
    } else {
        echo "<h1>Erreur d'authentification</h1>";
        echo "<pre>" . print_r($user_data, true) . "</pre>";
    }
} else {
    header("Location: $proxy_url");
    exit;
}

$context = stream_context_create([
    'http' => [
        'ignore_errors' => true
    ]
]);
$response = file_get_contents($callback_url, false, $context);

?>