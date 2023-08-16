# REST API по работе с меню ресторана

Проект на FastAPI с использованием PostgreSQL в качестве БД

Реализованы 3 сущности: Меню, Подменю, Блюдо.

Зависимости:
- У меню есть подменю
- В подменю есть блюда


#### Запустить приложение в Docker

- Клонируйте репозиторий командой <code> git clone https://github.com/Hardcore-ov/ylab_testwork.git </code>
- В папке проекта, где находится Dockerfile и docker-compose.yml в терминале введите команду <code> docker-compose up -d </code>

После запуска контейнеров сервер запустится по адресу http://127.0.0.1:8000 и можно посылать API запросы.

#### Запустить контейнер с тестами в Docker

```
docker-compose -f docker-compose-tests.yml up
```

- Результат тестов будет выведен в терминале запуска докера и в самом терминале запущеного контейнера

#### Запустить приложение БЕЗ использования Docker

- Клонируйте репозиторий командой <code> git clone https://github.com/Hardcore-ov/ylab_testwork.git </code> , затем установите
необходимые библиотеки <code> pip install -r requirements.txt </code>

- - Перейдите в папку с репозиторием

- В файле .env измените поле **POSTGRES_HOST** с **db** на **localhost**

- В терминале запустите <code> python -m venv venv </code>

- После установки файлов виртуального окружения запустите команду:

<code> venv\Scripts\activate.bat </code> для Windows

<code> source venv/bin/activate </code> для Mac и Linux

- Когда запустится виртуальное окружение уже можно будет ввести последовательно команды для запуска сервера и приложения:

<code> alembic upgrade head </code>

<code> uvicorn src.main:app --reload </code>

Сервер запущен по адресу http://127.0.0.1:8000 и можно теперь посылать API запросы.

<a name="headers"><h2>Документация</h2></a>

Документация доступна по адресу http://127.0.0.1:8000/docs и http://127.0.0.1:8000/redoc

База изначально пустая для запуска тестов Postman.

Для того чтобы наполнить базу воспользуйтесь эндпоинтом:
```
/api/v1/update_from_file/manual
```

После загрузки данных из excel-файла все изменения в файле **Menu.xlsx** в папке **admin**
будут автоматически внесены в базу данных с помощью фоновой задачи Celery.

## Эндпоинты:

### Menus
- **POST**   ```/api/v1/menus```создание меню
- **GET** ```/api/v1/menus``` просмотр списка меню
- **PATCH** ```/api/v1/menus/{menu_id}``` обновление меню
- **GET**    ```/api/v1/menus/{menu_id}```просмотр определенного меню
- **DELETE**  ```/api/v1/menus/{menu_id}``` удаление меню

### Submenus
- **POST** ```/api/v1/menus/{menu_id}/submenus/``` создание подменю
- **GET**  ```/api/v1/menus/{menu_id}/submenus/``` просмотр списка подменю
- **PATCH** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}``` обновление подменю
- **GET**  ```/api/v1/menus/{menu_id}/submenus/{submenu_id}``` просмотр определенного подменю
- **DELETE** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}``` удаление подменю

### Dishes
- **POST** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes``` создание блюда
- **GET**   ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes``` просмотр списка блюд
- **PATCH** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}``` обновление блюда
- **GET**   ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}``` просмотр определенного блюда
- **DELETE** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}``` удаление блюда


### Заданя со звездочкой:

ДЗ 2:

\* Реализовать вывод количества подменю и блюд для Меню через один (сложный) ORM запрос. 

[Реализация меню](src/menu/models.py)

[Реализация подменю](src/submenu/models.py)

ДЗ 3:

\* Описать ручки API в соответствий c OpenAPI [Документация тут](#headers)