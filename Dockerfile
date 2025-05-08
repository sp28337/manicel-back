FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV ENVIRONMENT=local

WORKDIR /app

RUN pip install --upgrade pip wheel "poetry==1.8.3"

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-root

COPY . .

EXPOSE 8000

# CMD ["python", "main.py"]
# CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["poetry", "run", "gunicorn", "app.main:app", "-c", "gunicorn.conf.py"]