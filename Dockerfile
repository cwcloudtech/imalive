FROM python:3-alpine AS api

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LISTEN_ADDR="0.0.0.0" \
    LISTEN_PORT=8080 \
    WERKZEUG_RUN_MAIN=true \
    MANIFEST_FILE_PATH=manifest.json \
    WAIT_TIME=10 \
    HEART_BIT_LOG_JSON=no

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apk add --no-cache --virtual .build-deps gcc musl-dev linux-headers && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apk del .build-deps

COPY . /app/

EXPOSE 8080

CMD ["python3", "src/app.py"]