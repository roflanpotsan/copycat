<h1>@Copycat</h1>

Инициализация БД:
```
cd database/
docker-compose build
docker-compose up

cd ../
python manage.py makemigrations
python manage.py mirgate
```
Заполнение БД данными:
```
python manage.py fill_db [ratio]
```
Запуск приложения:
```
python manage.py runserver
```

<h2>Main Page</h2>
<img width="1512" alt="layout" src="https://github.com/roflanpotsan/copycat/assets/91660065/7fd27b6c-7fdf-42a6-8d21-38002fd1d8f2">
