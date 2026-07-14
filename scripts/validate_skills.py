#!/usr/bin/env python3
"""
validate_skills.py — CI-валидатор для DeepSeek Subagents.

Проверяет:
  - YAML-фронтматер всех SKILL.md (name, description)
  - Уникальность имён скиллов
  - Все contract.yaml парсятся (YAML)
  - Все benchmark.yaml содержат минимум 1 тест
  - Все spawn-templates.json валидны (JSON)
  - Ссылки в README.md указывают на существующие файлы

Usage:
  python scripts/validate_skills.py
  python scripts/validate_skills.py --verbose
"""

import os
import sys
import json
import re
from pathlib import Path
from collections import Counter

BASE_DIR = Path(".").resolve()
SKILLS_DIR = BASE_DIR / "skills"
SPAWN_DIR = BASE_DIR / "spawn-templates"
README = BASE_DIR / "README.md"


def log(msg: str, level: str = "INFO"):
    """Log with colorized level."""
    markers = {"OK": "  OK", "WARN": " WARN", "ERROR": "ERROR"}
    m = markers.get(level, "INFO")
    sys.stdout.write(f"[{m}] {msg}\n")


def validate_yaml_frontmatter(filepath: Path) -> bool:
    """Validate YAML frontmatter has name + description."""
    content = filepath.read_text(encoding="utf-8", errors="replace")
    # Extract between --- markers
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        log(f"{filepath}: missing YAML frontmatter", "ERROR")
        return False

    frontmatter = match.group(1)
    has_name = bool(re.search(r"^name:\s*\S", frontmatter, re.MULTILINE))
    has_desc = bool(re.search(r"^description:\s*\S", frontmatter, re.MULTILINE))

    if not has_name:
        log(f"{filepath}: missing 'name' in frontmatter", "ERROR")
        return False
    if not has_desc:
        log(f"{filepath}: missing 'description' in frontmatter", "ERROR")
        return False

    return True


def validate_contract_yaml(filepath: Path) -> bool:
    """Validate contract.yaml exists and has basic structure."""
    if not filepath.exists():
        log(f"{filepath}: missing", "ERROR")
        return False

    content = filepath.read_text(encoding="utf-8", errors="replace")
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        log(f"{filepath}: not valid YAML (missing --- markers)", "ERROR")
        return False

    front = match.group(1)
    has_name = bool(re.search(r"^name:\s*\S", front, re.MULTILINE))
    has_produces = bool(re.search(r"^produces:", front, re.MULTILINE))

    if not has_name:
        log(f"{filepath}: missing 'name'", "ERROR")
        return False
    if not has_produces:
        log(f"{filepath}: missing 'produces'", "WARN")
    return True


def validate_benchmark_yaml(filepath: Path) -> bool:
    """Validate benchmark.yaml has at least one test."""
    if not filepath.exists():
        log(f"{filepath}: missing", "WARN")
        return False  # not required for all skills

    content = filepath.read_text(encoding="utf-8", errors="replace")
    has_tests = bool(re.search(r"^tests:", content, re.MULTILINE))
    has_test_id = bool(re.search(r"^\s*- id:", content, re.MULTILINE))

    if not has_tests:
        log(f"{filepath}: no 'tests:' section", "ERROR")
        return False
    if not has_test_id:
        log(f"{filepath}: no test entries with 'id'", "ERROR")
        return False
    return True


def validate_spawn_json(filepath: Path) -> bool:
    """Validate spawn template JSON has required fields."""
    if not filepath.exists():
        log(f"{filepath}: missing", "ERROR")
        return False

    try:
        data = json.loads(filepath.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        log(f"{filepath}: invalid JSON: {e}", "ERROR")
        return False

    required = ["name", "description", "spawn_prompt"]
    for field in required:
        if field not in data:
            log(f"{filepath}: missing required field '{field}'", "ERROR")
            return False

    return True


def check_unique_names() -> list:
    """Check for duplicate skill/spawn template names."""
    names = []

    for cat_dir in sorted(SKILLS_DIR.iterdir()):
        if not cat_dir.is_dir():
            continue
        for skill_dir in cat_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                names.append(("skill", skill_dir.name))

    for cat_dir in sorted(SPAWN_DIR.iterdir()):
        if not cat_dir.is_dir():
            continue
        for json_file in cat_dir.glob("*.json"):
            names.append(("spawn", json_file.stem))

    counter = Counter(n for _, n in names)
    duplicates = [name for name, count in counter.items() if count > 1]

    if duplicates:
        for dup in duplicates:
            types = [t for t, n in names if n == dup]
            log(f"duplicate name '{dup}': {types}", "ERROR")
    return duplicates


def check_readme_links() -> list:
    """Verify that links in README point to existing files."""
    if not README.exists():
        log("README.md not found", "WARN")
        return []

    broken = []
    content = README.read_text(encoding="utf-8")
    # Match markdown links: [text](path) and badge images
    links = re.findall(r"\]\(([^)]+)\)", content)

    for link in links:
        if link.startswith("http://") or link.startswith("https://"):
            continue
        link_path = (BASE_DIR / link).resolve()
        if not link_path.exists():
            broken.append(link)
            log(f"README.md: broken link '{link}' -> {link_path}", "WARN")

    return broken


def main():
    verbose = "--verbose" in sys.argv
    errors = 0
    warnings = 0
    skill_count = 0
    spawn_count = 0

    log("=" * 50, "INFO")
    log("Validating DeepSeek Subagents project...", "INFO")
    log("=" * 50, "INFO")

    # Validate skills
    log("\n--- SKILLS ---", "INFO")
    for cat_dir in sorted(SKILLS_DIR.iterdir()):
        if not cat_dir.is_dir():
            continue
        for skill_dir in sorted(cat_dir.iterdir()):
            if not skill_dir.is_dir():
                continue

            skill_md = skill_dir / "SKILL.md"
            contract = skill_dir / "contract.yaml"
            benchmark = skill_dir / "benchmark.yaml"

            if not skill_md.exists():
                log(f"{skill_dir}: missing SKILL.md", "ERROR")
                errors += 1
                continue

            skill_count += 1
            if verbose:
                log(f"  Checking: {skill_dir.name}")

            if not validate_yaml_frontmatter(skill_md):
                errors += 1
            if not validate_contract_yaml(contract):
                errors += 1
            if not validate_benchmark_yaml(benchmark):
                warnings += 1  # benchmark is optional

    # Validate spawn templates
    log("\n--- SPAWN TEMPLATES ---", "INFO")
    for cat_dir in sorted(SPAWN_DIR.iterdir()):
        if not cat_dir.is_dir():
            continue
        for json_file in sorted(cat_dir.glob("*.json")):
            spawn_count += 1
            if verbose:
                log(f"  Checking: {json_file.name}")
            if not validate_spawn_json(json_file):
                errors += 1

    # Cross-cutting checks
    log("\n--- CROSS-CUTTING ---", "INFO")

    duplicates = check_unique_names()
    errors += len(duplicates)

    broken_links = check_readme_links()
    warnings += len(broken_links)

    # Summary
    log("=" * 50, "INFO")
    log(f"Skills: {skill_count} | Spawn templates: {spawn_count}", "INFO")
    log(f"Errors: {errors} | Warnings: {warnings}", "INFO")
    log("=" * 50, "INFO")

    if errors:
        log("VALIDATION FAILED", "ERROR")
    else:
        log("ALL CHECKS PASSED", "OK")

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
