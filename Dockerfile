FROM python:3.12-alpine

RUN apk --no-cache add curl

WORKDIR /app

COPY pyproject.toml .
RUN pip install -e .

COPY main/ ./main/

VOLUME ["/app"]

CMD ["python", "/app/main/main.py"]
