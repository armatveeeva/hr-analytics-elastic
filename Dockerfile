FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 POETRY_VIRTUALENVS_CREATE=false
WORKDIR /app
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock ./
COPY src ./src
RUN poetry install --only main
COPY config ./config
COPY data ./data
ENTRYPOINT ["python", "-m", "hr_analytics"]
