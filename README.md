# demobaza

## Запуск
Так как sqlite так и не пашет ставим postgreSQL 11.
Для отладки устанавливаем в локалхост на порт 5432.
Создаем базу данных и даем нашей демобазе права на нее:

```
CREATE DATABASE demobaza; CREATE USER demobaza;
ALTER USER demobaza PASSWORD 'demobaza';
GRANT ALL ON DATABASE demobaza TO demobaza;
```
Далее, ничего неожиданного:

```
./manage.py migrate
./manage.py runserver
```
