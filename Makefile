.PHONY: lint
lint:
	docker compose run --rm --entrypoint=pylint test /src/gmsa

.PHONY: typecheck
typecheck:
	docker compose run --rm test --mypy /src/gmsa

.PHONY: dist
dist:
	pip install wheel build
	python -m build
