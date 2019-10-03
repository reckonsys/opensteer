# FROM reckonsys/python:latest
FROM python:3.7-alpine
WORKDIR /app
COPY requirements.txt .
RUN \
 apk add --no-cache python3 postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev libffi-dev jpeg-dev zlib-dev && \
 pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
COPY . .
RUN python manage.py collectstatic --noinput
