# Makefile with simple commands

activate:
	source .venv/bin/activate

update-requirements:
	uv pip compile pyproject.toml -o requirements.txt

install:
	uv sync

run:
	uv run uvicorn service.main:app --reload

docker-build:
	docker build -t algoteque-code-assessment .

test:
	uv run pytest -vvv -s

test-cov:
	uv run pytest --cov=service --cov-report=term-missing

test-snapshot-update:
	uv run pytest --snapshot-update
