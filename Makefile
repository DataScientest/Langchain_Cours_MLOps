api:
	uv run uvicorn src.api.main:app --reload

test:
	uv run pytest
