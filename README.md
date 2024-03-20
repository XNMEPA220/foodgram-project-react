### О проекте:
Продуктовый помошник - сайт, на котором можно публиковать рецепты. Другие пользователи могут добавлять рецепты в избранное или список покупок. Список покупок в свою очередь можно скачать, чтобы удобно взять с собой в магазин.

### Использованные технологии:

Django, REST framework, nginx, docker, docker compose

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:XNMEPA220/foodgram-project-react.git
```

В корне проекта создаете .env
Пример:
SECRET_KEY=секретный ключ
DEBUG=False
ALLOWED_HOSTS=127.0.0.1,localhost
POSTGRES_USER=логин от базы данных
POSTGRES_PASSWORD=пароль от базы данных
POSTGRES_DB=имя базы данных
DB_HOST=db
DB_PORT=5432

Запустить проект

```
sudo docker compose up -d
```

Создать и выполнить миграции

```
sudo docker compose backend python manage.py makemigrations

sudo docker compose backend python manage.py migrate
```

Заполняем базу данных ингридиентами

```
sudo docker compose backend python manage.py load_data
```

Создаем администратора

```
sudo docker compose backend python manage.py createsuperuser
```

Приложение будет доступно по адресу - localhost:8000

### Примеры запросов и документация:

Получение списка пользователей(GET) или регистрация нового пользователя(POST):

```
/api/users/
```

Получение токена(POST):

```
/api/auth/token/login/
```

Получение списка рецептов(GET) или создание нового рецепта(POST):

```
/api/recipes/
```

Добавить рецепт в избранное(POST):

```
/api/recipes/{id}/favorite/
```

Подписаться на пользователя(POST):

```
/api/users/{id}/subscribe/
```

Добавить рецепт в список покупок(POST):

```
/api/recipes/{id}/shopping_cart/
```

Скачать список покупок(GET):

```
/api/recipes/downloan_shopping_cart/
```

### Данные для использования:

Сайт http://xnmepa.ddns.net/
Админ: почта egor@mail.ru пароль egor

### Автор:

Рындин Егор, обучающийся в 29 когорте Яндекс Практикума на программе Python-разработчик плюс
https://github.com/XNMEPA220