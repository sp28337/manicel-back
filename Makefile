.DEFAULT_GOAL := help

run: ## Run the application
	## poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --env-file .local.env
	poetry run gunicorn app.main:app -c gunicorn.conf.py

migrate-create: ## Create migration
	alembic revision --autogenerate -m $(NAME)

pytests: ## Run tests
	poetry run docker-compose -f docker-compose.yml down
	poetry run docker-compose -f docker-compose.test.yml up -d
	poetry run pytest
	poetry run docker-compose -f docker-compose.test.yml down
	poetry run docker-compose -f docker-compose.yml up -d

db-images: ## Start docker-compose
	poetry run docker-compose -f docker-compose.test.yml down
	poetry run docker-compose -f docker-compose.yml up -d