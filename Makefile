MARKDOWNLINT := npx --yes markdownlint-cli2@0.23.3

.PHONY: install serve build lint lint-md lint-style lint-fixture

install:
	pip install -r requirements.txt

serve:
	mkdocs serve

build:
	mkdocs build --strict

lint: lint-md lint-style lint-fixture

lint-md:
	$(MARKDOWNLINT)

lint-style:
	python3 scripts/check_style.py

# Тестовый текст с намеренными нарушениями: линтер должен найти ровно 10 замечаний.
lint-fixture:
	@found=$$(python3 scripts/check_style.py tests/fixtures/violations.md | grep -c '^tests/'); \
	if [ "$$found" -ne 10 ]; then echo "lint-fixture: ожидали 10 замечаний, найдено $$found"; exit 1; fi; \
	echo "lint-fixture: найдено 10 замечаний, как ожидалось"
