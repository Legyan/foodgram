# Foodgram

Продуктовый помощник

![workflow](https://github.com/legyan/foodgram-project-react/actions/workflows/main.yml/badge.svg)

[```foodgram.sytes.net```](http://foodgram.sytes.net)

[```Документация```](http://foodgram.sytes.net/api/docs/) на API c примерами запросов доступна на развёрнутом проекте по аресу http://localhost/api/docs/.


### Описание:

Сервис на котором пользователи могут делиться рецептами, добавлять рецепты в избранное и подписываться на публикации других авторов.
Рецепты могут быть отмечены тегами, которые используются для фильтрации на главной странице. 
Пользователи также могут добавлять рецепты в список покупок и создавать отчеты в формате PDF с перечнем ингредиентов и их 
количеством, необходимым для приготовления блюд из списка.



### Стек технологий 

![](https://img.shields.io/badge/Python-3.11-black?style=flat&logo=python) 
![](https://img.shields.io/badge/Django-4.1.3-black?style=flat&logo=django&logoColor=green)
![](https://img.shields.io/badge/Djangorestframework-3.14.0-black?style=flat&logo=django&logoColor=green) 
![](https://img.shields.io/badge/PostgreSQL-black?style=flat&logo=PostgreSQL&logoColor=orange)
![](https://img.shields.io/badge/Nginx-black?style=flat&logo=NGINX&logoColor=green)
![](https://img.shields.io/badge/Gunicorn-black?style=flat&logo=Gunicorn&logoColor=#499848)
![](https://img.shields.io/badge/Docker-black?style=flat&logo=Docker&logoColor=blue)

### Запуск проекта
- Клонировать репозиторий:
```
git clone https://github.com/Legyan/foodgram.git
```
- Перейти в директорию для разворачиания проекта:
```
cd foodgram/infra/
```
- Создать файл .env и заполнить его согласно примеру в infra/.env.example:
```
touch .env && nano .env
```

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=<DJANGO_SECRET_KEY>
HOST=<YOUR_HOST>
```

- Запустить проект в контейнере:
```
sudo docker-compose up -d --build
```
- Выполнить миграции:
```
sudo docker-compose exec backend python manage.py migrate
```
- Создать пользователя с правами администратора в django:
```
sudo docker-compose exec backend python manage.py createsuperuser
```
- Загрузить начальный список ингридиентов в базу данных:
```
sudo docker-compose exec backend python manage.py load_ingredients
```
- Подгрузить статические файлы для панели администратора:
```
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

Добавление новых тегов осуществляется через [```панель администратора Django```](http://localhost/api/admin/).
