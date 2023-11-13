<h1>@Copycat</h1>

Инициализация БД:
```
В папке /database
docker-compose build
docker-compose up
. ./setup_tables.sh

(Если нужно обновить модели)
В папке / 
python manage.py makemigrations
python manage.py migrate
```
Заполнение БД данными:
```
python manage.py fill_db [ratio]
```
Запуск приложения:
```
python manage.py runserver [ip]:[port]
```

Войти в профиль пока можно только через /admin

Креды: admin:insecurepassword

<h2>Main Page</h2>
<img width="1512" alt="layout" src="https://github.com/roflanpotsan/copycat/assets/91660065/7fd27b6c-7fdf-42a6-8d21-38002fd1d8f2">
