# PHP/MySQL: старт ПР 18–20

Версии выпуска: Open Server Panel 6.5.1, PHP 8.5 (проверяемая ветка; на дату сборки 8.5.11), MySQL 8.4 LTS (8.4.11).

1. В Open Server Panel создайте локальный домен для папки `public/`.
2. Создайте пустую базу `isrpo_course` в UTF-8 и выполните `database/schema.sql`, затем `database/seed.sql`.
3. Скопируйте `config.example.php` в `config.local.php` и укажите локальные реквизиты. `config.local.php` исключён из Git.
4. Запустите модули PHP и MySQL, откройте URL, выданный панелью.
5. На `/health.php` ожидается JSON `{"status":"ok"}`; секреты в ответ не входят.

Каркас уже использует PDO, подготовленные запросы, `password_hash`, `password_verify`, смену session id, CSRF и HTML-экранирование. Студент дополняет обработку по методичкам. Это учебный локальный проект, не готовая конфигурация публичного сервера.

