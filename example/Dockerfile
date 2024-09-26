FROM python:3.12.0-alpine

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml /app

RUN poetry install

COPY main.py /app/main.py

COPY code /app/code

ENTRYPOINT ["poetry", "run", "python", "main.py"]
