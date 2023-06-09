### Ответ на вопрос

Сделать колонку с датой индексом, это ускорит фильтрацию по дате. А так же можно применить партицирование таблиц.


## О чем этот проект

Проект делится на 3 основные части: 
1) сервер с REST API для получения информации из БД о рейсах за определенную дату
2) Консольное приложение, которое запускает обработчик поступающих файлов
3) Консольное приложение, которое генерирует файл и отдает команду приложению номер 2 на обработку данных
Второе приложение и третье взаимодействую посредством брокера очередей

### Дисклеймер

Я не успел настроить докер + селери, для того, чтобы генерировать задачи каждые 150 секунд,
а так же для простоты запуска приложений оставил некоторые секреты в докер файле + конфиге приложения.
Разумеется, так делать нельзя, для докера нужно использовать .env 


# Запуск
Первое, что необходимо сделать, это запустить докер контейнер с необходимыми сервисами

`docker compose build`

`docker compose up`

Далее, пока контейнеры собираются, устанавливаем виртуальное окружение и необходимые зависимости

`python3.10 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

После сборки контейнеров, применить миграцию 

`alembic upgrade head`

После успешно применненной миграции, можно запустить сам обработчик файлов

`python main.py`

Данное приложение начнет прослушку брокера сообщений

И чтоб запустить генератор файла, прописываем во второй консоли 

`python script.py`

У нас сгенерируется файл, оправится сообщение в кролика с названием файла, обработчик подхватит его и дальше все в соответствии ТЗ.


Чтобы запустить серверную часть приложения, вводим 

`uvicorn server:app`

Запустится сервер на 8000 порту, со спецификацией API можно будет ознакомиться по адресу http://localhost:8000/docs

