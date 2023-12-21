<h1>@Copycat</h1>

Запуск приложения выполняется одним скриптом, который инициализирует БД и заполнит ее 20 пользователями, запустит WSGI сервер:
```
. ./run_app.sh
```
Дополнительно добавить множество фейковых пользователей можно с помощью managment команды fill_db:
```
python manage.py fill_db [ratio: int]
```
Все команды выполняются из корневой директории.

Отчет о нагрузочном тестировании находится в файле 
```
./ab_test_results.txt
```
Конфиги gunicorn и nginx находятся в папке
```
./configs
```
Простой WSGI скрипт находится в папке
```
./extras
```
Креды администратора: admin:insecurepassword

<h2>Main Page</h2>
<img width="1512" alt="layout" src="https://github.com/roflanpotsan/copycat/assets/91660065/7fd27b6c-7fdf-42a6-8d21-38002fd1d8f2">
