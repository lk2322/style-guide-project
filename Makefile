MARKDOWNLINT := npx --yes markdownlint-cli2@0.23.3

.PHONY: install serve build lint lint-md lint-style

install:
	pip install -r requirements.txt

serve:
	mkdocs serve

build:
	mkdocs build --strict

lint: lint-md lint-style

lint-md:
	$(MARKDOWNLINT)

lint-style:
	python3 scripts/check_style.py
