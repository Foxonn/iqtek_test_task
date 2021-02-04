FROM python:3.8

EXPOSE 80:80

RUN python -m pip install --upgrade pip

RUN pip install pipenv

RUN mkdir -p /application/

COPY Pipfile Pipfile.lock /var/app/

WORKDIR /var/app/

RUN pipenv install --deploy --system --ignore-pipfile
