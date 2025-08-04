FROM python:3.12-slim

ENV POETRY_VIRTUALENVS_CREATE=false
WORKDIR /app

# Copy only dependency-related files first for better caching
COPY pyproject.toml poetry.lock* /app/

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --without dev

# Copy rest of the application code
COPY . /app

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "api.app:app"]