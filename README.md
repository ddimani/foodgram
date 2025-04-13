## Foodgram
Foodgram - Проект представляет собой сервис, с помощью которого пользователи могут делиться своими любимыми рецептами,
сохранять понравившиеся рецепты в избранное, а также выгружать список необходимых ингредиентов для приготовления выбранных блюд. 

### Описание
*  Зарегистрированные пользователи имеют возможность публиковать свои рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов
*  При добавлении рецепта необходимо указать название, описание, время приготовления, а также прикрепить изображение. Обязательно нужно выбрать как минимум по одному ингредиенту и тегу. 
*  Пополнять список ингредиентов и тегов может только администратор.
*  Зарегистрированным пользователям доступен сервис «Список покупок». Он позволяет создавать список продуктов, которые нужно купить для приготовления выбранных блюд.
*  Имеется возможность скачать составленный список покупок в формате .txt.

### После запуска проект будет доступен по адресу:
https://foodgrame.duckdns.org/recipes

### Автор проекта:
*  [Губский Дмитрий](https://github.com/ddimani)

## Техно-стек проекта.

**Backend:**

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django Rest Framework](https://img.shields.io/badge/Django%20REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

**Frontend:**

![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

**Инфраструктура:**

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

**Языки программирования:**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

### Как запустить проект:
1. Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/ddimani/foodgram.git
```

```
cd foodgram
```

2. Создать файл .env:

```
touch .env
```

3. Указать переменные окружения в файле .env по примеру файла .env.example:

```
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=<Ваш_пароль>
POSTGRES_DB=foodgram
DB_HOST=foodgram-db
DB_PORT=5432
ALLOWED_HOSTS=127.0.0.1, localhost, <Ваш_хост>
DEBUG = False
BD_IS_SQLITE=False
SECRET_KEY='<Ваша_длинная_индивидуальная_страка>'
```

4. Запустить Docker Compose:

```
docker compose up
```

5. Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
    ```
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    
    DOCKER_PASSWORD=<пароль от DockerHub>
    DOCKER_USERNAME=<имя пользователя>

    USER=<username для подключения к серверу>
    SSH_PASSPHRASE=<пароль для сервера, если он установлен>
    SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

    TELEGRAM_TO=<ID чата, в который придет сообщение>
    TELEGRAM_TOKEN=<токен вашего бота>
    ```
    Workflow состоит из трёх шагов:
     - Проверка кода на соответствие PEP8
     - Сборка и публикация образа бекенда на DockerHub.
     - Автоматический деплой на удаленный сервер.
     - Отправка уведомления в телеграм-чат. 


6. Выполнить миграции:

```
docker compose exec foodgram-backend-1 python manage.py migrate
```

7. Собрать статику:

```
docker compose exec foodgram-backend-1 python manage.py collectstatic
```

8. Создать Суперпользователя:

```
sudo docker exec -it foodgram-backend-1 python manage.py createsuperuser

```

8. Загрузите ингредиенты в базу данных с помощью следующей команды:

```
sudo docker exec -it foodgram-backend-1 python manage.py load_db

```

### Запуск проекта на локальной машине:

1. Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/ddimani/foodgram.git
```

```
cd foodgram
```

2. Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
source env/bin/activate
```
3. Указать переменные окружения в файле .env по примеру файла .env.example:

```
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=<Ваш_пароль>
POSTGRES_DB=foodgram
DB_HOST=foodgram-db
DB_PORT=5432
ALLOWED_HOSTS=127.0.0.1, localhost, <Ваш_хост>
DEBUG = False
BD_IS_SQLITE=False
SECRET_KEY='<Ваша_длинная_индивидуальная_страка>'
```

4. Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

5. Выполнить миграции:
```
python3 manage.py migrate
```

6. Загрузите ингредиенты в базу данных с помощью следующей команды:
```
python3 manage.py load_data
```

7. Создать Суперпользователя:

```
python3 manage.py createsuperuser
```

8. Запустить проект:
```
python3 manage.py runserver
```


### Техническое описание проекта foodgram

* Перейдите в папку infra :
```
cd foodgram/infra
```
* находясь в папке infra, выполните в терминале команду:
```
docker compose up
```
* Теперь Вам доступна документация проекта по данной ссылке

http://localhost/api/docs/ 


### Ресурсы API Foodgram:
* Пользователи
* Теги
* Рецепты
* Список покупок
* Избранное
* Подписки
* Ингредиенты

### Примеры запросов к API:
* Регистрация нового пользователя.
```
POST /api/users/
```
* Получение токена авторизации.
```
POST /api/auth/token/login/
```
* Получение данных своей учетной записи.
```
GET /api/users/me/
```
* Получение списка всех тегов.
```
GET /api/tags/
```
* Получение списка всех рецептов.
```
GET /api/recipes/
```
* Добавление нового рецепта.
```
POST /api/recipes/
```
* Получение короткой ссылки на рецепт.
```
GET /api/recipes/{id}/get-link/
```
* Скачивание списка покупок.
```
GET /api/recipes/download_shopping_cart/
```
* Добавление рецепта в список покупок.
```
POST /api/recipes/shopping_cart/
```
* Добавление рецепта в избранное.
```
POST /api/recipes/{id}/favorite/
```