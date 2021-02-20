## Инструкция по запуску сервиса на docker

`git clone -b v2 https://github.com/Foxonn/iqtek_test_task/`

`cd iqtek_test_task`

`docker-compose up --build`

`docker restart iqtek_test_task_web_1`

> postgres запускается не сразу, потому потребуется перезагрузка

Подключаемся к контейнеру web:

`docker exec -it iqtek_test_task_web_1 bash`

и выполняем:

`python app/usermanager/init_table.py`  # создание таблиц для postgres и mysql

Документация
- http://localhost:8080/docs/

Сменить тип хранилища в `app/usermanager/settings.py`:

    STORAGE = [postgres, redis, mysql]
