FROM python:3.12.0-alpine

# Without this setting, Python never prints anything out.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml /app

RUN poetry install

COPY . /app

CMD ["poetry", "run", "python", "main.py"]
