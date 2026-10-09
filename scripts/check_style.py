#!/usr/bin/env python3
"""Линтер стиля документации «Сальдо».

Проверяет то, чего не видит markdownlint: термины из глоссария, канцелярит,
букву «ё», кавычки, тире и формат денежных сумм.

Код (блоки и `инлайн`), ссылки и строки врезок не проверяются.
Примеры «как не надо» оборачивайте в комментарии:

    <!-- style-check: off -->
    ...плохой пример...
    <!-- style-check: on -->

Запуск: python scripts/check_style.py [путь ...]   (по умолчанию docs/)
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TERMS_FILE = ROOT / "scripts" / "terms.yml"

OFF = "<!-- style-check: off -->"
ON = "<!-- style-check: on -->"

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"(`+)(.+?)\1")
LINK_TARGET_RE = re.compile(r"\]\([^)]*\)")
URL_RE = re.compile(r"https?://\S+")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->")

# Типографика и формат чисел: (регулярное выражение, сообщение)
TYPO_RULES = [
    (re.compile(r'"[^"\n]+"'), "прямые кавычки в тексте: используйте «ёлочки»"),
    (re.compile(r"(?<=[\w»)])\s-\s(?=[\w«(])"), "дефис вместо тире: ставьте « — »"),
    (re.compile(r"(?<![\w.-])\d+-\d+(?![\w.-])"), "диапазон через дефис: ставьте короткое тире «–»"),
    (re.compile(r"\d\s?(р\.?|руб\.?|рублей|рубля)(?!\w)", re.IGNORECASE), "сумма в рублях: пишите знак «₽» после числа"),
    (re.compile(r"\$\s?\d"), "знак валюты ставится после суммы: «250 $»"),
    (re.compile(r"(?<![\w-])-\d"), "отрицательная сумма: используйте знак минус «−», а не дефис"),
    (re.compile(r"\d%"), "между числом и «%» нужен неразрывный пробел"),
]


@dataclass
class Finding:
    path: Path
    line: int
    col: int
    rule: str
    message: str
    excerpt: str

    def __str__(self) -> str:
        rel = self.path.relative_to(ROOT) if self.path.is_relative_to(ROOT) else self.path
        return f"{rel}:{self.line}:{self.col}: [{self.rule}] {self.message} → «{self.excerpt}»"


def load_rules() -> list[tuple[str, re.Pattern[str], str]]:
    data = yaml.safe_load(TERMS_FILE.read_text(encoding="utf-8"))
    rules: list[tuple[str, re.Pattern[str], str]] = []
    for item in data.get("terms", []):
        rules.append(("термин", re.compile(item["pattern"], re.IGNORECASE), item["message"]))
    for item in data.get("kanceliarit", []):
        rules.append(("канцелярит", re.compile(item["pattern"], re.IGNORECASE), item["message"]))
    for item in data.get("yo", []):
        pattern = re.compile(rf"(?<!\w){item['word']}(?!\w)", re.IGNORECASE)
        rules.append(("ё", pattern, f"пишите «{item['right']}»"))
    for pattern, message in TYPO_RULES:
        rules.append(("типографика", pattern, message))
    return rules


def mask(text: str) -> str:
    """Заменяет код, ссылки и комментарии пробелами, сохраняя позиции символов."""
    for regex in (HTML_COMMENT_RE, INLINE_CODE_RE, LINK_TARGET_RE, URL_RE):
        text = regex.sub(lambda m: " " * len(m.group(0)), text)
    return text


def check_file(path: Path, rules) -> list[Finding]:
    findings: list[Finding] = []
    in_fence = False
    fence_marker = ""
    enabled = True

    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = raw.strip()

        if stripped == OFF:
            enabled = False
            continue
        if stripped == ON:
            enabled = True
            continue

        fence = FENCE_RE.match(raw)
        if fence:
            marker = fence.group(1)
            if not in_fence:
                in_fence, fence_marker = True, marker[0] * len(marker)
            elif marker.startswith(fence_marker):
                in_fence = False
            continue

        if in_fence or not enabled:
            continue
        # Заголовки врезок MkDocs используют прямые кавычки по синтаксису.
        if stripped.startswith(("!!!", "???")):
            continue

        text = mask(raw)
        for rule, pattern, message in rules:
            for match in pattern.finditer(text):
                findings.append(
                    Finding(path, lineno, match.start() + 1, rule, message, match.group(0).strip())
                )
    return findings


def collect(paths: list[str]) -> list[Path]:
    targets = [Path(p) for p in paths] or [ROOT / "docs"]
    files: list[Path] = []
    for target in targets:
        target = target.resolve()
        files.extend(sorted(target.rglob("*.md")) if target.is_dir() else [target])
    return files


def main(argv: list[str]) -> int:
    rules = load_rules()
    files = collect(argv)
    findings = [f for path in files for f in check_file(path, rules)]

    for finding in findings:
        print(finding)

    if findings:
        print(f"\nНайдено замечаний: {len(findings)} в {len({f.path for f in findings})} файлах.")
        return 1
    print(f"Проверено файлов: {len(files)}. Замечаний нет.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
