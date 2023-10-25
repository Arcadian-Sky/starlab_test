#Тестовое задание.

##Стек:
python, aiohttp, postgres, sqlachemy

##Описание:
Делаем API сервис, в рамках которого будем давать пользователю доступ к различным литературным произведениям.

##Требования:
1. Файл книги можно сохранять по своему усмотрению;
1. Создать для хранения структуры данных в бд, которые в будущем позволит получать доступ к книгам по (name, author, date\_published, genre);
1. Создать create/read endpoints, которые могу позволять пользователю загружать книги, 
   получать список книг по одному из параметров (name, author, date\_published, genre) 
   и получать доступ к нужной книге по id (ее можно скачать или можно просмотреть в онлайне);
1. Для create добавить валидацию, чтобы проверять, что пользователь указал обязательные поля, такие как (name, author, date\_published).

#Оформление:
1. Создать репозиторий на гитлаб, загрузить туда код;
1. Функции должны быть аннотированы;
1. API должно покрываться тестами;
1. Будет плюсом добавить поддержку docker, 
   чтобы приложение могло быть запущено локально. 
   А так же инструкцию к нему.


_Будет плюсом, если получится реализовать дополнительный фукнционал._

##Расширение задачи:
Добавить endpoint для принятия и парсинга xls файла (пример файла в приложении), который будет хранить две страницы. Первая из которых содержит name, а вторая author книги. Этот файл присылается издательским домом и содержит те указатели на книгу которая должна быть включена в denied list, то есть стать недоступной для скачивания, но остаться доступной для просмотра.

#Инструкции:
Докер:
1. Установите и запустите докер.
2. Клонируйте репозиторий.
3. Из папки проекта запустите командой `docker-compose up --build`.

Приложение запустится по адресу http://0.0.0.0:8080/.

Миграция демо данных:
`docker-compose exec app alembic upgrade head`

## API Endpoints
- `GET /`: Индексная публичная страница со всеми интерфейсами.
- `POST /author/create`: Создание нового автора
  - `id`: Ид автора
  - `name`: Имя автора
  - `second_name`: Фамилия автора
- `POST /book/create`: Создание новой книги
  - `id`: Ид книги
  - `name`: Наименование книги
  - `author_id`: Автор книги
  - `genre`: Жанр книги
  - `date_published_start`: Период (от) в котором книга выпускалась в формате "YYYY-MM-DD"
  - `date_published_end`: Период (до) в котором книга выпускалась в формате "YYYY-MM-DD"
- `POST /book/list`: Получить список книг с учетом фильтров.
- `GET /author/list`: Получить список авторов.
- `POST /decline_by_file`: Закрытие из файла (xlsx)
    - `первый лист` - содержит книги, обрабаываемые колонки:
        - `name`: Наименование книги
        - `author`: Автор книги (поиск по совпадению по имени или фамилии в базе)
        - `genre`: Жанр книги
        - `date_published`: Период (от) в котором книга выпускалась в формате "YYYY-MM-DD"
    - `второй лист` - содержит авторов, обрабаываемые колонки:
        - `name`: Имя автора
        - `second_name`: Фамилия автора
    
