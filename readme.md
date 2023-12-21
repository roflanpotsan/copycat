<h1>@Copycat</h1>

Запуск приложения выполняется одним скриптом, который инициализирует БД и заполнит ее 20 пользователями, запускает WSGI сервер:
```
. ./run_app.sh
```
Дополнительно добавить пользователей можно с помощью managment команды fill_db:
```
python manage.py fill_db [ratio: int]
```
Все команды выполняются из корневой директории.

Креды администратора: admin:insecurepassword

<h2>Main Page</h2>
<img width="1512" alt="layout" src="https://github.com/roflanpotsan/copycat/assets/91660065/7fd27b6c-7fdf-42a6-8d21-38002fd1d8f2">
