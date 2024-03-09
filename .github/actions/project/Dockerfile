FROM python:3.12-slim

WORKDIR /app

COPY ./app/requirements.txt .

RUN pip install -r /app/requirements.txt --no-cache-dir

COPY ./app /app

ENTRYPOINT ["python", "/app/main2.py"]
