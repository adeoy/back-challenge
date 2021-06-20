FROM python:3.8.10-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /tmp

COPY Pipfile .
COPY Pipfile.lock .
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev
RUN python -m pip install --upgrade pip pipenv
RUN pipenv lock -r --dev > requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

WORKDIR /opt

CMD python manage.py runserver 0.0.0.0:5000
