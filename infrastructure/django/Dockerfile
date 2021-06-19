FROM python:3.8.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /tmp

COPY Pipfile .
COPY Pipfile.lock .
RUN python -m pip install --upgrade pip pipenv
RUN pipenv lock -r --dev > requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

WORKDIR /opt

CMD python manage.py runserver 0.0.0.0:5000
