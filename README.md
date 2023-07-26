# REST API по работе с меню ресторана

Проект на FastAPI с использованием PostgreSQL в качестве БД

Реализованы 3 сущности: Меню, Подменю, Блюдо.

Зависимости:
+ У меню есть подменю
+ В подменю есть блюда


#### Запустить приложение

- Клонируйте репозиторий командой <code> git clone https://github.com/Hardcore-ov/ylab_testwork.git </code> , затем установите 
необходимые библиотеки <code> pip install -r requirements.txt </code>

- Перейдите в папку с репозиторием и в терминале запустите <code> python -m venv venv </code>

- После установки файлов виртуального окружения запустите команду <code> source venv/bin/activate </code>

- Когда запустится виртуальное окружение уже можно будет ввести последовательно команды для запуска сервера и приложения:

<code> alembic upgrade head </code>

<code> uvicorn src.main:app --reload </code>

Сервер запущен по адресу http://127.0.0.1:8000 и можно теперь посылать API запросы.

Документация доступна по адресу ```http://127.0.0.1:8000/docs```

### Menus
+ **POST**   ```/api/v1/menus```создание меню
+ **GET** ```/api/v1/menus``` просмотр списка меню
+ **PATCH** ```/api/v1/menus/{menu_id}``` обновление меню
+ **GET**    ```/api/v1/menus/{menu_id}```просмотр определенного меню
+ **DELETE**  ```/api/v1/menus/{menu_id}``` удаление меню

### Submenus
+ **POST** ```/api/v1/menus/{menu_id}/submenus/``` создание подменю
+ **GET**  ```/api/v1/menus/{menu_id}/submenus/``` просмотр списка подменю
+ **PATCH** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}``` обновление подменю
+ **GET**  ```/api/v1/menus/{menu_id}/submenus/{submenu_id}``` просмотр определенного подменю
+ **DELETE** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}``` удаление подменю

### Dishes
+ **POST** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes``` создание блюда
+ **GET**   ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes``` просмотр списка блюд
+ **PATCH** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}``` обновление блюда
+ **GET**   ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}``` просмотр определенного блюда
+ **DELETE** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}``` удаление блюда