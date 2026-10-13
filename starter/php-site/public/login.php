<?php
declare(strict_types=1);
require dirname(__DIR__) . '/src/bootstrap.php';

$message = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = strtolower(trim((string)($_POST['email'] ?? '')));
    $password = (string)($_POST['password'] ?? '');
    if (!verify_csrf((string)($_POST['csrf'] ?? ''))) {
        http_response_code(400);
        $message = 'Форма устарела. Обновите страницу.';
    } else {
        $stmt = $pdo->prepare('SELECT id, email, password_hash FROM users WHERE email = :email');
        $stmt->execute(['email' => $email]);
        $user = $stmt->fetch();
        if ($user && password_verify($password, $user['password_hash'])) {
            session_regenerate_id(true);
            $_SESSION['user_id'] = (int)$user['id'];
            $message = 'Вход выполнен.';
        } else {
            http_response_code(401);
            $message = 'Неверная почта или пароль.';
        }
    }
}
?>
<!doctype html><html lang="ru"><meta charset="utf-8"><title>Вход</title>
<h1>Вход</h1><p role="status"><?= h($message) ?></p>
<form method="post">
  <input type="hidden" name="csrf" value="<?= h(csrf_token()) ?>">
  <label>Email <input name="email" type="email" required autocomplete="email"></label>
  <label>Пароль <input name="password" type="password" required autocomplete="current-password"></label>
  <button type="submit">Войти</button>
</form></html>

