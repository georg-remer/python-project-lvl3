install:
	poetry install

selfcheck:
	poetry check

lint:
	poetry run flake8 page_loader
	poetry run flake8 tests

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml tests

check: selfcheck lint test

build: check
	poetry build

publish:
	poetry publish --dry-run

package-install:
	pip install --user dist/*.whl