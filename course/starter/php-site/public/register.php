<?php
declare(strict_types=1);
require dirname(__DIR__) . '/src/bootstrap.php';

$message = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = strtolower(trim((string)($_POST['email'] ?? '')));
    $password = (string)($_POST['password'] ?? '');
    $csrf = (string)($_POST['csrf'] ?? '');

    if (!verify_csrf($csrf)) {
        http_response_code(400);
        $message = 'Форма устарела. Обновите страницу.';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL) || strlen($password) < 12) {
        http_response_code(422);
        $message = 'Проверьте email; пароль должен быть не короче 12 символов.';
    } else {
        try {
            $stmt = $pdo->prepare('INSERT INTO users (email, password_hash) VALUES (:email, :hash)');
            $stmt->execute(['email' => $email, 'hash' => password_hash($password, PASSWORD_DEFAULT)]);
            $message = 'Пользователь создан. Пароль в базе хранится как хеш.';
        } catch (PDOException $error) {
            error_log($error->getMessage());
            http_response_code(409);
            $message = 'Не удалось создать пользователя. Проверьте введённые данные.';
        }
    }
}
?>
<!doctype html><html lang="ru"><meta charset="utf-8"><title>Регистрация</title>
<h1>Регистрация</h1><p role="status"><?= h($message) ?></p>
<form method="post">
  <input type="hidden" name="csrf" value="<?= h(csrf_token()) ?>">
  <label>Email <input name="email" type="email" required autocomplete="email"></label>
  <label>Пароль <input name="password" type="password" required minlength="12" autocomplete="new-password"></label>
  <button type="submit">Создать пользователя</button>
</form></html>

