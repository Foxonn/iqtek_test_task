## Инструкция по запуску сервиса на docker

`git clone -b v2 https://github.com/Foxonn/iqtek_test_task/`

`cd iqtek_test_task`

`docker-compose up --build`

`docker restart iqtek_test_task_web_1`

> postgres страртует не сразу, из-за чего Django не может установить соединение, потому требуется перезагрузка

Подключаемся к контейнеру web, и выполняет:

`python app/usermanager/init_table.py`  # создание таблиц для postgres и mysql

Документация
- http://localhost:8080/docs/

Сменить тип хранилища в `app/usermanager/settings.py`:

    STORAGE = [postgres, redis, mysql]