<?php
declare(strict_types=1);

$configPath = dirname(__DIR__) . '/config.local.php';
if (!is_file($configPath)) {
    throw new RuntimeException('Создайте config.local.php по примеру.');
}
$config = require $configPath;

$pdo = new PDO($config['dsn'], $config['user'], $config['password'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);

session_set_cookie_params([
    'httponly' => true,
    'secure' => !empty($_SERVER['HTTPS']),
    'samesite' => 'Lax',
]);
session_start();

function csrf_token(): string
{
    if (!isset($_SESSION['csrf'])) {
        $_SESSION['csrf'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf'];
}

function verify_csrf(string $value): bool
{
    return isset($_SESSION['csrf']) && hash_equals($_SESSION['csrf'], $value);
}

function h(string $value): string
{
    return htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

