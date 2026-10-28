FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY tests ./tests
COPY data ./data

RUN pip install --upgrade pip && pip install ".[dev]"

CMD ["python", "-m", "trading_lab.main", "--csv", "data/sample_prices.csv"]
