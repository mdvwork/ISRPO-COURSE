# Демонстрация: чтение HTTP

```http
POST /api/projects HTTP/1.1
Host: course.example
Content-Type: application/json

{"name":"Каталог","hours":12}
```

Вход: метод, путь, заголовок формата и JSON-тело. Успешное создание:

```http
HTTP/1.1 201 Created
Location: /api/projects/7
Content-Type: application/json

{"id":7,"name":"Каталог","hours":12}
```

`201` означает созданный ресурс, `Location` сообщает его адрес. Сам статус не доказывает корректность всех полей: клиент проверяет формат тела, сервер — вход и право пользователя.

