## Инструкция по запуску сервиса на docker

`git clone -b dev https://github.com/Foxonn/iqtek_test_task/`

`cd iqtek_test_task`

`docker-compose up --build`

Подключаемся к контейнеру django_app, и выполняет:
1. `python manage.py migrate`
2. `python manage.py loaddata usermanager/fixtures/data_initial.json`

Перезапустить все контейнеры

http://localhost:8080/api/v1/user/

Документация
- http://localhost:8080/swagger/
- http://localhost:8080/redoc/
