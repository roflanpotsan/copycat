docker-compose -f ./database/docker-compose.yml up -d
sleep 10
cat ./database/migration-fix.sql | docker exec -i copycat_db /usr/bin/mysql -uroot -pinsecurepassword copycat_db
python manage.py fill_db 20
gunicorn -c ./configs/gunicorn_config.py copycat.wsgi --log-level debug