# Демонстрация: структура SQL и значения

Опасный вариант:

```php
$sql = "SELECT * FROM users WHERE email = '$email'";
```

Вход становится частью синтаксиса. Безопасный вариант:

```php
$stmt = $pdo->prepare(
    'SELECT id, email, password_hash FROM users WHERE email = :email'
);
$stmt->execute(['email' => $email]);
```

Структура запроса фиксирована, email передаётся как значение. Параметр нельзя использовать для имени таблицы или `ASC/DESC`: такие части выбираются сервером из разрешённого списка.

