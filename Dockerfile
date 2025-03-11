ARG PYTHON_VERSION=3.13.1-alpine

FROM python:${PYTHON_VERSION} AS api

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LOG_LEVEL="INFO" \
    LISTEN_ADDR="0.0.0.0" \
    LISTEN_PORT=8080 \
    MANIFEST_FILE_PATH=manifest.json \
    WAIT_TIME=10 \
    LOG_FORMAT="json"

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apk add --no-cache libstdc++ && \
    apk add --no-cache --virtual .build-deps gcc g++ musl-dev linux-headers && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apk del .build-deps

COPY . /app/

EXPOSE 8080

CMD ["python3", "src/app.py"]

FROM api AS unit_tests

WORKDIR /app/src

CMD ["python", "-m", "unittest", "discover", "-s", "./tests", "-p", "test_*.py", "-v"]
