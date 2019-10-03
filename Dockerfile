# FROM reckonsys/python:latest
FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt .
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
COPY . .
RUN python manage.py collectstatic
