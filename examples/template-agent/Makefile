.PHONY: setup dev run

setup: ## Install dependencies
	uv sync

dev: ## Start LangGraph dev server
	uv run langgraph dev --allow-blocking

run: ## Run agent directly in CLI mode
	uv run python cli.py
