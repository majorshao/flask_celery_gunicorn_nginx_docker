FROM python:3.7.3 as base

WORKDIR /flask_app

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

############ CELERY WORKER ############
FROM base as celery_worker

CMD celery -A app.celery worker -l info

