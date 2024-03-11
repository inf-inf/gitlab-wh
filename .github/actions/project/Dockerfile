FROM python:3.12-slim

WORKDIR /app

COPY ./pyproject.toml .

RUN pip install . --no-cache-dir && pip uninstall -y project-action

COPY ./app /app

ENTRYPOINT ["python", "/app/main.py"]
