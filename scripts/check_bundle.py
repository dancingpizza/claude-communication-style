#!/usr/bin/env python3
"""Проверяет папку скилла claude-communication-style без сети.

Что проверяется:
  1. Frontmatter основного SKILL.md по спецификации Agent Skills.
  2. Длина тела SKILL.md (не больше 500 строк).
  3. Во всей папке нет вложенных файлов SKILL.md.
  4. Все относительные ссылки в Markdown ведут на существующие файлы,
     а якоря на существующие заголовки.
  5. Пути в обратных кавычках из основного SKILL.md существуют.
  6. Файлы vendor/ совпадают с scripts/vendor.sha256.
  7. В пакете кроме vendor/ только инструкция и рабочие справочники.

Запуск из любого каталога:
  python3 scripts/check_bundle.py            проверить
  python3 scripts/check_bundle.py --update   пересчитать scripts/vendor.sha256
Код выхода 0, если ошибок нет, иначе 1.
"""

import hashlib
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ROOT = REPO_ROOT / "skills/claude-communication-style"
VENDOR = ROOT / "vendor"
SUMS = REPO_ROOT / "scripts/vendor.sha256"

ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
CODE_PATH_RE = re.compile(r"`((?:vendor|references|scripts)/[^`\s]+)`")
SKIPPED_DIRS = {".git", "__pycache__", "__pypackages__"}
PACKAGE_FILES = {
    "SKILL.md",
    "references/decisions.md",
    "references/examples.md",
    "references/sources.md",
}


def bundle_files():
    for path in sorted(ROOT.rglob("*")):
        if path.is_file() and not SKIPPED_DIRS.intersection(path.relative_to(ROOT).parts):
            yield path


def check_package_files(errors):
    actual = {
        path.relative_to(ROOT).as_posix()
        for path in bundle_files()
        if not path.is_relative_to(VENDOR)
    }
    for path in sorted(PACKAGE_FILES - actual):
        errors.append(f"в пакете отсутствует: {path}")
    for path in sorted(actual - PACKAGE_FILES):
        errors.append(f"лишний файл в пакете: {path}")


def parse_frontmatter(text):
    """Разбирает простой YAML frontmatter без внешних зависимостей."""
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return None, text
    data, current = {}, None
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        if line.startswith("  ") and current == "metadata":
            key, _, value = line.strip().partition(":")
            data["metadata"][key.strip()] = value.strip().strip('"')
            continue
        key, _, value = line.partition(":")
        current = key.strip()
        data[current] = {} if current == "metadata" and not value.strip() else value.strip()
    return data, text[match.end():]


def check_frontmatter(errors):
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    data, body = parse_frontmatter(text)
    if data is None:
        errors.append("SKILL.md: нет frontmatter")
        return
    unknown = set(data) - ALLOWED_KEYS
    if unknown:
        errors.append(f"SKILL.md: лишние поля frontmatter: {', '.join(sorted(unknown))}")
    name = data.get("name", "")
    if not NAME_RE.match(name) or len(name) > 64:
        errors.append(f"SKILL.md: недопустимое имя {name!r}")
    if name != ROOT.name:
        errors.append(f"SKILL.md: имя {name!r} не совпадает с каталогом {ROOT.name!r}")
    description = data.get("description", "")
    if not 1 <= len(description) <= 1024:
        errors.append(f"SKILL.md: длина description {len(description)}, допустимо 1–1024")
    if "<" in description or ">" in description:
        errors.append("SKILL.md: в description есть угловые скобки")
    if len(data.get("compatibility", "")) > 500:
        errors.append("SKILL.md: compatibility длиннее 500 символов")
    if not isinstance(data.get("metadata", {}), dict):
        errors.append("SKILL.md: metadata должно быть словарём")
    body_lines = body.count("\n")
    if body_lines > 500:
        errors.append(f"SKILL.md: тело занимает {body_lines} строк, рекомендуется не больше 500")
    print(f"frontmatter: name={name}, description={len(description)} симв., тело {body_lines} строк")


def check_nested_skill_files(errors):
    extra = [p for p in bundle_files() if p.name == "SKILL.md" and p != ROOT / "SKILL.md"]
    for path in extra:
        errors.append(f"вложенный SKILL.md будет зарегистрирован как отдельный скилл: {path.relative_to(ROOT)}")


def github_slug(heading):
    slug = re.sub(r"[^\w\- ]", "", heading.strip().lower())
    return slug.replace(" ", "-")


def headings(path):
    slugs, in_fence = set(), False
    for line in path.read_text(encoding="utf-8").splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
        elif not in_fence and line.startswith("#"):
            slugs.add(github_slug(line.lstrip("#")))
    return slugs


def prose_lines(path):
    """Строки Markdown вне блоков кода, без инлайн-кода."""
    in_fence = False
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield number, INLINE_CODE_RE.sub("", line)


def check_links(errors):
    checked = 0
    for path in bundle_files():
        if path.suffix != ".md":
            continue
        for number, line in prose_lines(path):
            for target in LINK_RE.findall(line):
                if re.match(r"^[a-z]+:", target):
                    continue
                checked += 1
                file_part, _, anchor = target.partition("#")
                resolved = (path.parent / file_part).resolve() if file_part else path
                where = f"{path.relative_to(ROOT)}:{number}"
                if not resolved.exists():
                    errors.append(f"{where}: ссылка никуда не ведёт: {target}")
                elif anchor and resolved.suffix == ".md" and anchor not in headings(resolved):
                    errors.append(f"{where}: нет заголовка для якоря: {target}")
    print(f"ссылки: проверено {checked}")


def check_code_paths(errors):
    main = ROOT / "SKILL.md"
    for number, line in enumerate(main.read_text(encoding="utf-8").splitlines(), 1):
        for target in CODE_PATH_RE.findall(line):
            path = ROOT / target
            if not path.exists():
                errors.append(f"SKILL.md:{number}: путь не найден: {target}")
            elif path.is_file():
                path.read_bytes()


def vendor_digests():
    lines = []
    for path in bundle_files():
        if path.is_relative_to(VENDOR):
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            lines.append(f"{digest}  {path.relative_to(VENDOR).as_posix()}")
    return lines


def check_vendor(errors):
    if not SUMS.exists():
        errors.append("нет scripts/vendor.sha256, запустите с --update")
        return
    expected = set(SUMS.read_text(encoding="utf-8").splitlines())
    actual = set(vendor_digests())
    for line in sorted(expected - actual):
        errors.append(f"vendor: файл изменён или пропал: {line.split('  ', 1)[1]}")
    for line in sorted(actual - expected):
        name = line.split("  ", 1)[1]
        if not any(e.endswith("  " + name) for e in expected):
            errors.append(f"vendor: файл не учтён в SHA256SUMS: {name}")
    print(f"vendor: {len(actual)} файлов")


def main():
    if "--update" in sys.argv[1:]:
        SUMS.write_text("\n".join(vendor_digests()) + "\n", encoding="utf-8")
        print(f"записан {SUMS.relative_to(REPO_ROOT)}")
        return 0
    errors = []
    check_package_files(errors)
    check_frontmatter(errors)
    check_nested_skill_files(errors)
    check_links(errors)
    check_code_paths(errors)
    check_vendor(errors)
    for error in errors:
        print("ОШИБКА:", error)
    print("готово: ошибок нет" if not errors else f"готово: ошибок {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
