# Руководство по стилю документации «Сальдо»

[![CI](https://github.com/lk2322/style-guide-project/actions/workflows/ci.yml/badge.svg)](https://github.com/lk2322/style-guide-project/actions/workflows/ci.yml)
[![Deploy](https://github.com/lk2322/style-guide-project/actions/workflows/deploy.yml/badge.svg)](https://github.com/lk2322/style-guide-project/actions/workflows/deploy.yml)

Правила написания и оформления документации «Сальдо», мобильного приложения для учёта доходов, расходов и инвестиций. Руководство ведётся по принципу Docs as Code: Markdown в Git, проверка линтерами в CI, публикация на GitHub Pages после слияния в `main`.

Сайт: <https://lk2322.github.io/style-guide-project/>

## Быстрый старт

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Сайт откроется на <http://127.0.0.1:8000>. Страницы обновляются при сохранении файла.

## Проверки

```bash
make lint    # markdownlint и линтер стиля
make build   # сборка в режиме --strict
```

Для `markdownlint-cli2` нужен Node.js 20 или новее.

## Структура

```text
docs/                  страницы руководства
  style/               тон, язык, числа
  format/              структура, Markdown, интерфейс
  doc-templates/       шаблоны документов
  examples/            документы, написанные по руководству
scripts/check_style.py линтер терминов и типографики
scripts/terms.yml      словарь линтера
.github/workflows/     CI и деплой
```

## Как внести изменения

Читайте [CONTRIBUTING.md](CONTRIBUTING.md).

## Автор

Владзиевский Евгений, НИУ ИТМО, 2026.
