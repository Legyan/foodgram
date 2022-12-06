# Foodgram

Продуктовый помощник

![workflow](https://github.com/legyan/foodgram-project-react/actions/workflows/main.yml/badge.svg)

[```Ссылка на развернутый проект```](http://158.160.13.152)

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
