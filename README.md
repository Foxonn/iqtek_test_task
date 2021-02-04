## Инструкция по запуску сервиса на docker

`git clone -b dev https://github.com/Foxonn/iqtek_test_task/`

`cd iqtek_test_task`

`docker-compose up --build`

`docker restart iqtek_test_task_web_1`

Подключаемся к контейнеру web, и выполняет:
1. `python manage.py migrate`
2. `python manage.py loaddata usermanager/fixtures/data_initial.json`

`docker restart iqtek_test_task_web_1`

http://localhost:8080/api/v1/user/

Документация
- http://localhost:8080/swagger/
- http://localhost:8080/redoc/
