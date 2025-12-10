.DEFAULT_GOAL := help

run: ## Run the application
	## poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --env-file .local.env
	poetry run gunicorn app.main:app -c gunicorn.conf.py

docker: ## Run docker
	poetry run docker-compose -f docker-compose.yml up db -d

migrate-create: ## Create migration
	alembic revision --autogenerate -m $(NAME)
