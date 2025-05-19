FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV ENVIRONMENT=prod

WORKDIR /app

RUN pip install --upgrade pip wheel "poetry==1.8.3"

# RUN apt-get update && apt-get install -y curl

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-root

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "gunicorn", "app.main:app", "-c", "gunicorn.conf.py"]
