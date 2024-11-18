.DEFAULT_GOAL := help

run: ## Run the application using uvicorn with provided arguments or defaults
	poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload --env-file .local.env

migrate-create: ## Create migration
	alembic revision --autogenerate -m $(NAME)
