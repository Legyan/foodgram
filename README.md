# Foodgram

Продуктовый помощник

![workflow](https://github.com/legyan/foodgram-project-react/actions/workflows/main.yml/badge.svg)

[```Ссылка на развернутый проект```](http://158.160.13.152)

**Учетные данные для проверки панели администратора**

username:
```
admin
```
password:
```
qazwsxcvb321
```
[```Документация```](http://158.160.13.152/api/docs/) доступна на развёрнутом проекте по аресу [```http://localhost/api/docs/```](http://localhost/api/docs/)


### Описание:

Сервис на котором пользователи могут делиться рецептами, добавлять рецепты в избранное и подписываться на публикации других авторов.
Также есть возможность создавать список покупок,который содерит информацию об ингредиентах ,которые необходимо приобрести и в каких количествах для приготовления выбранных блюд


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
git clone https://github.com/Legyan/foodgram-project-react
```
- Перейти в директорию для разворачиания проекта:
```
cd infra/
```
- Запустить проект в контейнере:
```
docker-compose up -d --build
```
- Выполнить миграции:
```
sudo docker-compose exec backend python manage.py migrate
```
- Создать пользователя с правами администратора в django:
```
sudo docker-compose exec backend python manage.py createsuperuser
```
- Загрузить начальный список ингридиентов:
```
sudo docker-compose exec backend python manage.py load_ingredients
```
- Подгрузить статические файлы для панели администратора:
```
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
### Некоторые примеры запросов к API

#### Регистрация нового пользователя:
```
/api/users/
```
POST запрос
```python
{
    "email": "string",
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "password": "string"
}
```
Варианты ответов:
- удачное выполнение запроса: статус 201 
```python
{
    "email": "string",
    "id": "integer",
    "username": "string",
    "first_name": "string",
    "last_name": "string"
}
```
- запрос отклонен: статус 400
```python
{
  "field_name": [
    "Обязательное поле."
  ]
}
```
#### Получение токена:
```
/api/auth/token/login/
```
POST запрос
```
{
    "password": "string",
    "email": "string"
}
```
Варианты ответов:
- успешное выполнение запроса: статус 201
```python
{
    "token": "string"
}
```
* запрос отклонен: статус 400
```python
{
    "non_field_errors": [
        "Невозможно войти с предоставленными учетными данными."
    ]
}
```
#### Добавление нового рецепта
Права доступа: aвторизованный пользователь.
```
/api/recipes/
```
POST запрос
```python
{
    "ingredients": [
        {"id": "integer",
         "name": "string",
         "amount": "integer"}
    ],
    "tags": [
    1,
    3
    ],
    "image": "string <binary>",
    "name": "string",
    "text": "string",
    "cooking_time": "integer"
}
```
Варианты ответов:
- успешное выполнение запроса: статус 201 
```python
{
    "id": "integer",
    "name": "string",
    "image": "string <binary>",
    "text": "string",
    "ingredients": [
        {
            "id": "integer",
            "name": "string",
            "amount": "integer"
        }
    ],
    "tags": [
        {
            "id": "integer",
            "name": "string",
            "color": "string <HEX>",
            "slug": "string"
        }
    ],
    "cooking_time": "integer",
    "is_favorited": "bool",
    "is_in_shopping_cart": "bool",
    "author": {
        "first_name": "string",
        "username": "string",
        "last_name": "string",
        "email": "string",
        "password": "string",
        "id": "integer",
        "is_subscribed": "bool"
    }
}
```
- запрос отклонен: статус 400
```python
{
    "errors": [
    "string"
  ]
}
```
* запрос отклонен: статус 404 - объект не найден
```python
{
  "detail": "Страница не найдена."
}
```
#### Получение списка ингредиентов:
```
/api/ingredients/
```
GET запрос
```python
[
    {
    "id": 1,
    "name": "рис",
    "measurement_unit": "мг"
    }
]
```