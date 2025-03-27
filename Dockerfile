FROM python:3.9-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY ./app /app

ENV DB_URL=${DB_URL:-postgresql://user:password@db:5432/mydb}
ENV APP_ENV=production

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]