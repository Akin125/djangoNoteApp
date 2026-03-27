# Base image: Python 3.12 on Alpine Linux (latest)
FROM python:3.12-alpine

LABEL maintainer="Your Name <your-email@example.com>"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt

COPY ./NoteApp /app

WORKDIR /app

EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
