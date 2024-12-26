# Makefile with simple commands

update-requirements:
	uv pip compile pyproject.toml -o requirements.txt

run:
	uv run uvicorn service.main:app --reload

docker-build:
	docker build --progress=plain -t algoteque-code-assessment .

docker-run:
	docker run -p 8000:8000 algoteque-code-assessment