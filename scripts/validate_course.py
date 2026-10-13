"""Структурная проверка первого выпуска курса без внешних зависимостей."""

from __future__ import annotations

import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_LABS = {
    "01-visual-studio.md", "02-program-skeleton.md", "03-radiobutton.md",
    "04-debugging.md", "05-dynamic-controls.md", "06-data-models.md",
    "07-data-views.md", "08-domain-data.md", "09-domain-classes.md",
    "10-mvvm-part-1.md", "10-mvvm-part-2.md", "11-json-part-1.md",
    "11-json-part-2.md", "12-edm-part-1.md", "12-edm-part-2.md",
    "13-unit-testing.md", "14-html-part-1.md", "14-html-part-2.md",
    "15-css.md", "16-bootstrap.md", "17-javascript.md", "18-database.md",
    "19-php-registration.md", "19-php-login.md", "20-dynamic-pages.md",
    "21-react-part-1.md", "21-react-part-2.md", "22-wordpress-part-1.md",
    "22-wordpress-part-2.md",
}

EXPECTED_LECTURE_COUNTS = {
    "01-tools": 10,
    "02-wpf": 9,
    "03-web": 9,
}

errors: list[str] = []
checks: list[str] = []


class StrictEnoughHTML(HTMLParser):
    def error(self, message: str) -> None:  # pragma: no cover - compatibility hook
        errors.append(message)


def check_counts() -> None:
    for folder, expected in EXPECTED_LECTURE_COUNTS.items():
        actual = len(list((ROOT / "modules" / folder).glob("*.md")))
        checks.append(f"Лекции {folder}: {actual}/{expected}")
        if actual != expected:
            errors.append(f"{folder}: ожидалось {expected} лекций, найдено {actual}")

    actual_labs = {path.name for path in (ROOT / "labs").glob("*.md") if path.name != "README.md"}
    checks.append(f"Лабораторные: {len(actual_labs)}/29")
    if actual_labs != EXPECTED_LABS:
        errors.append(f"Набор лабораторных отличается: missing={sorted(EXPECTED_LABS-actual_labs)}, extra={sorted(actual_labs-EXPECTED_LABS)}")


def check_lab_sections() -> None:
    required = [
        "Цель", "Результат", "ПО", "Самостоятельная часть",
        "Проверка и диагностика", "Сдача и критерии", "Вопросы", "Критические ошибки",
    ]
    for name in sorted(EXPECTED_LABS):
        text = (ROOT / "labs" / name).read_text(encoding="utf-8")
        missing = [item for item in required if item.lower() not in text.lower()]
        question_count = len(re.findall(r"(?m)^\d+\. ", text.split("## Вопросы", 1)[-1]))
        if missing:
            errors.append(f"{name}: нет разделов/меток {missing}")
        if question_count < 5:
            errors.append(f"{name}: вопросов меньше пяти ({question_count})")
    checks.append("Структура 29 лабораторных проверена")


def check_lecture_sections() -> None:
    required = ["Связь с программой", "Цель", "Результат", "Лекция", "Упражнение", "Вопросы", "Чек-лист"]
    lectures = sorted((ROOT / "modules").rglob("*.md"))
    for path in lectures:
        text = path.read_text(encoding="utf-8")
        missing = [item for item in required if item.lower() not in text.lower()]
        question_count = len(re.findall(r"(?m)^\d+\. ", text.split("## Вопросы", 1)[-1].split("## Чек-лист", 1)[0]))
        if missing:
            errors.append(f"{path.relative_to(ROOT)}: нет разделов/меток {missing}")
        if not re.search(r"(?mi)^## Связь с (практикой|ПР|лабораторн)", text):
            errors.append(f"{path.relative_to(ROOT)}: нет отдельной связи с практикой")
        if question_count < 5:
            errors.append(f"{path.relative_to(ROOT)}: вопросов меньше пяти ({question_count})")
        if text.count("```") % 2:
            errors.append(f"{path.relative_to(ROOT)}: незакрытый блок кода")
    checks.append(f"Структура лекций: проверено {len(lectures)}")


def check_markdown_links() -> None:
    pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    count = 0
    for md in ROOT.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        for raw in pattern.findall(text):
            parts = raw.strip().split("#", 1)
            target = parts[0]
            fragment = unquote(parts[1]) if len(parts) == 2 else ""
            if not target or re.match(r"^(https?://|mailto:)", target):
                if not target and fragment:
                    resolved = md
                else:
                    continue
            else:
                target = unquote(target).replace("\\", "/")
                resolved = (md.parent / target).resolve()
                count += 1
                if not resolved.exists():
                    errors.append(f"{md.relative_to(ROOT)}: не найдена ссылка {raw}")
                    continue
            if fragment and resolved.suffix.lower() == ".md":
                heading_slugs = set()
                for heading in re.findall(r"(?m)^#{1,6}\s+(.+?)\s*$", resolved.read_text(encoding="utf-8")):
                    value = "".join(ch for ch in heading.casefold() if unicodedata.category(ch)[0] in {"L", "N"} or ch in " -_")
                    heading_slugs.add(re.sub(r"\s+", "-", value.strip()))
                if fragment.casefold() not in heading_slugs:
                    errors.append(f"{md.relative_to(ROOT)}: не найден раздел #{fragment} в {resolved.relative_to(ROOT)}")
    checks.append(f"Относительные Markdown-ссылки: проверено {count}")


def check_data_and_markup() -> None:
    json_count = 0
    for path in ROOT.rglob("*.json"):
        if {"bin", "obj", "node_modules", "dist"}.intersection(path.parts):
            continue
        if path.name == "json-broken.json":
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
            json_count += 1
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: JSON: {exc}")

    xml_count = 0
    for pattern in ("*.xaml", "*.csproj", "*.slnx"):
        for path in ROOT.rglob(pattern):
            if {"bin", "obj", "node_modules", "dist"}.intersection(path.parts):
                continue
            try:
                ET.parse(path)
                xml_count += 1
            except Exception as exc:
                errors.append(f"{path.relative_to(ROOT)}: XML: {exc}")

    html_count = 0
    for path in ROOT.rglob("*.html"):
        if {"bin", "obj", "node_modules", "dist"}.intersection(path.parts):
            continue
        parser = StrictEnoughHTML()
        try:
            parser.feed(path.read_text(encoding="utf-8"))
            parser.close()
            html_count += 1
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: HTML parse: {exc}")
    checks.append(f"Данные/разметка: JSON {json_count}, XML {xml_count}, HTML {html_count}")


def check_pins_and_security() -> None:
    package = json.loads((ROOT / "starter/react-projects/package.json").read_text(encoding="utf-8"))
    pins = {
        package["dependencies"]["react"],
        package["dependencies"]["react-dom"],
        package["devDependencies"]["vite"],
        package["devDependencies"]["@vitejs/plugin-react"],
    }
    if pins != {"19.3.0", "8.3.4", "6.1.2"}:
        errors.append(f"React/Vite версии не закреплены ожидаемо: {pins}")

    php = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "starter/php-site").rglob("*.php"))
    for marker in ("password_hash", "password_verify", "prepare(", "session_regenerate_id", "hash_equals"):
        if marker not in php:
            errors.append(f"PHP: отсутствует защитный механизм {marker}")
    if re.search(r"password\s*=\s*['\"]\$", php):
        errors.append("PHP: обнаружена вероятная SQL-конкатенация пароля")
    checks.append("Закрепление React/Vite и защитные механизмы PHP проверены")


def check_placeholders() -> None:
    forbidden = re.compile(r"\b(TODO|TBD|FIXME)\b|заглушк", re.IGNORECASE)
    for area in (ROOT / "modules", ROOT / "labs", ROOT / "starter"):
        for path in area.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".cs", ".xaml", ".js", ".jsx", ".php", ".html"}:
                text = path.read_text(encoding="utf-8")
                if forbidden.search(text):
                    errors.append(f"{path.relative_to(ROOT)}: найдена заглушка/TODO")
    checks.append("Студенческие материалы проверены на TODO/FIXME/заглушки")


def main() -> int:
    check_counts()
    check_lab_sections()
    check_lecture_sections()
    check_markdown_links()
    check_data_and_markup()
    check_pins_and_security()
    check_placeholders()
    print("COURSE VALIDATION")
    for item in checks:
        print(f"PASS: {item}")
    for item in errors:
        print(f"FAIL: {item}")
    print(f"RESULT: {'FAIL' if errors else 'PASS'} ({len(errors)} errors)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

