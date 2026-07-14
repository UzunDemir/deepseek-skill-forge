#!/usr/bin/env python3
"""
codex2deepseek.py — Convert Codex subagent .toml definitions to DeepSeek TUI format.

Converts:
  - workspace-write agents  → skills/<category>/<name>/ (SKILL.md + contract.yaml + benchmark.yaml)
  - read-only agents        → spawn-templates/<category>/<name>.json

Usage:
  python scripts/codex2deepseek.py awesome-codex-subagents/categories/01-core-development/backend-developer.toml
  python scripts/codex2deepseek.py awesome-codex-subagents/categories/04-quality-security/security-auditor.toml --mode spawn
  python scripts/codex2deepseek.py --batch categories/04-quality-security/*.toml
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib
    except ModuleNotFoundError:
        print("ERROR: install tomli — `pip install tomli`", file=sys.stderr)
        sys.exit(1)


def classify_agent(toml_data: dict) -> str:
    """Determine output format: 'skill' for doer-agents, 'spawn' for reviewers."""
    sandbox = toml_data.get("sandbox_mode", "")
    if sandbox == "read-only":
        return "spawn"
    return "skill"


def extract_category(toml_path: Path) -> str:
    """Extract category directory name from path like .../categories/NN-name/agent.toml."""
    parts = toml_path.parts
    for i, p in enumerate(parts):
        if p == "categories" and i + 1 < len(parts):
            return parts[i + 1]
    return "00-uncategorized"


def slugify(name: str) -> str:
    """Normalize agent name to directory-safe slug."""
    return name.lower().replace(" ", "-").replace("_", "-")


def build_frontmatter(toml_data: dict, agent_name: str) -> str:
    """Build YAML frontmatter for SKILL.md."""
    desc = toml_data.get("description", f"DeepSeek {agent_name} skill")
    # Escape any YAML-special characters in description
    desc = desc.replace("'", "''")
    lines = ["---"]
    lines.append(f"name: {agent_name}")
    lines.append(f"description: \"{desc}\"")
    lines.append("---")
    return "\n".join(lines)


def build_skill_body(toml_data: dict) -> str:
    """Build SKILL.md body, preserving Codex's structure but dropping Codex-specific fields."""
    instructions = toml_data.get("developer_instructions", "")
    body = instructions.strip()

    # Prepend a note if no instructions found
    if not body:
        body = f"# {toml_data.get('name', 'unnamed-agent')}\n\nOwn this task with production-quality behavior.\n\n(TODO: add Working mode, Focus, Quality checks, Return, Do not)"

    # If body already has "Own" pattern — keep it.

    # Add conversion note
    return body


def extract_produces_type(instructions: str) -> str:
    """Heuristic: extract what the agent returns from the 'Return' section."""
    match = re.search(
        r"Return:\s*\n((?:\s*[-*]\s+.+\n?)+)",
        instructions,
        re.MULTILINE
    )
    if match:
        returns = match.group(1)
        if "finding" in returns.lower():
            return "finding[]"
        elif "file" in returns.lower() or "change" in returns.lower():
            return "change-set"
        elif "analysis" in returns.lower() or "report" in returns.lower():
            return "report"
        elif "plan" in returns.lower():
            return "plan"
        else:
            return "report"
    return "report"


def build_contract(toml_data: dict, agent_name: str, instructions: str) -> dict:
    """Build contract.yaml content."""
    produces_type = extract_produces_type(instructions)
    return {
        "name": agent_name,
        "version": 1,
        "produces": {
            "type": produces_type,
            "description": "See SKILL.md Return section for full structure"
        },
        "consumes": {
            "type": "task-context",
            "required": True,
            "description": "The task scope, codebase state, and expected outcome"
        },
        "parallel_compatible": [],
        "conflicts_with": []
    }


def build_benchmark(toml_data: dict, agent_name: str) -> dict:
    """Build benchmark.yaml from description."""
    desc = toml_data.get("description", "")
    prompt = f"Perform your role as {agent_name}. Context: {desc}"
    return {
        "name": agent_name,
        "version": 1,
        "tests": [
            {
                "id": "default",
                "prompt": prompt,
                "expected": {
                    "return_contract": True,
                    "checks": [
                        "returns structured output matching SKILL.md Return section",
                        "validates at least one success path",
                        "validates at least one failure path",
                        "does not exceed scope boundaries"
                    ]
                },
                "eval": {
                    "method": "llm-as-judge",
                    "pass_threshold": 0.8
                }
            }
        ]
    }


def write_skill_files(toml_data: dict, output_dir: Path, agent_name: str):
    """Write SKILL.md + contract.yaml + benchmark.yaml."""
    skill_dir = output_dir / agent_name
    skill_dir.mkdir(parents=True, exist_ok=True)

    instructions = toml_data.get("developer_instructions", "")
    frontmatter = build_frontmatter(toml_data, agent_name)
    body = build_skill_body(toml_data)

    # Write SKILL.md
    skill_content = f"{frontmatter}\n\n{body}\n"
    (skill_dir / "SKILL.md").write_text(skill_content, encoding="utf-8")
    sys.stdout.write(f"  OK {skill_dir / 'SKILL.md'}\n")

    # Write contract.yaml
    contract = build_contract(toml_data, agent_name, instructions)
    contract["version"] = 1
    yaml_lines = ["---", f"name: {contract['name']}", f"version: {contract['version']}", "",
                  "produces:", f"  type: {contract['produces']['type']}",
                  f"  description: \"{contract['produces']['description']}\"", "",
                  "consumes:", f"  type: {contract['consumes']['type']}",
                  f"  required: {str(contract['consumes']['required']).lower()}",
                  f"  description: \"{contract['consumes']['description']}\"", "",
                  "parallel_compatible: []",
                  "conflicts_with: []", "---"]
    (skill_dir / "contract.yaml").write_text("\n".join(yaml_lines) + "\n", encoding="utf-8")
    sys.stdout.write(f"  OK {skill_dir / 'contract.yaml'}\n")

    # Write benchmark.yaml
    benchmark = build_benchmark(toml_data, agent_name)
    bm_lines = ["---", f"name: {benchmark['name']}", f"version: {benchmark['version']}", "",
                "tests:"]
    for t in benchmark["tests"]:
        bm_lines.append(f"  - id: {t['id']}")
        bm_lines.append(f"    prompt: \"{t['prompt']}\"")
        bm_lines.append("    expected:")
        bm_lines.append(f"      return_contract: {str(t['expected']['return_contract']).lower()}")
        bm_lines.append("      checks:")
        for c in t["expected"]["checks"]:
            bm_lines.append(f"        - \"{c}\"")
        bm_lines.append("    eval:")
        bm_lines.append(f"      method: {t['eval']['method']}")
        bm_lines.append(f"      pass_threshold: {t['eval']['pass_threshold']}")
    bm_lines.append("---")
    (skill_dir / "benchmark.yaml").write_text("\n".join(bm_lines) + "\n", encoding="utf-8")
    sys.stdout.write(f"  OK {skill_dir / 'benchmark.yaml'}\n")


def write_spawn_template(toml_data: dict, output_dir: Path, agent_name: str):
    """Write JSON spawn template."""
    output_dir.mkdir(parents=True, exist_ok=True)
    instructions = toml_data.get("developer_instructions", "").strip()
    desc = toml_data.get("description", "")
    model = toml_data.get("model", "gpt-5.4")  # kept as metadata hint

    template = {
        "name": agent_name,
        "description": desc,
        "model_hint": model,
        "spawn_prompt": instructions,
        "expected_output": extract_produces_type(instructions),
        "parallel_safe": True
    }

    template_path = output_dir / f"{agent_name}.json"
    template_path.write_text(json.dumps(template, indent=2, ensure_ascii=False), encoding="utf-8")
    sys.stdout.write(f"  OK {template_path}\n")


def convert_one(toml_path: Path, mode_override: str = None, base_dir: Path = Path(".")):
    """Convert a single .toml file."""
    print(f"\n=== Converting: {toml_path}")

    try:
        with open(toml_path, "rb") as f:
            data = tomllib.load(f)
    except Exception as e:
        sys.stderr.write(f"  ERROR parsing TOML: {e}\n")
        return False

    agent_name = data.get("name", "")
    if not agent_name:
        sys.stderr.write(f"  ERROR: no 'name' field in {toml_path}\n")
        return False

    agent_name = slugify(agent_name)
    category = extract_category(toml_path)
    mode = mode_override or classify_agent(data)

    print(f"  Name: {agent_name}")
    print(f"  Category: {category}")
    print(f"  Mode: {mode}")

    if mode == "skill":
        output_dir = base_dir / "skills" / category
        write_skill_files(data, output_dir, agent_name)
    else:
        output_dir = base_dir / "spawn-templates" / category
        write_spawn_template(data, output_dir, agent_name)

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Convert Codex .toml subagent definitions to DeepSeek TUI format"
    )
    parser.add_argument("paths", nargs="+", help="Path(s) to .toml file(s)")
    parser.add_argument("--mode", choices=["skill", "spawn"], default=None,
                        help="Override mode (default: auto from sandbox_mode)")
    parser.add_argument("--base", default=".",
                        help="Base output directory (default: current dir)")
    parser.add_argument("--batch", action="store_true",
                        help="Batch mode: continue on error")

    args = parser.parse_args()

    base_dir = Path(args.base).resolve()
    success = 0
    failed = 0

    for pattern in args.paths:
        p = Path(pattern)
        if not p.exists():
            sys.stderr.write(f"File not found: {p}\n")
            failed += 1
            continue
        ok = convert_one(p.resolve(), args.mode, base_dir)
        if ok:
            success += 1
        else:
            failed += 1
            if not args.batch:
                sys.exit(1)

    print(f"\n{'=' * 40}")
    print(f"Done: {success} converted, {failed} failed")

    if success > 0:
        print(f"\nNext steps:")
        print(f"  - For skills: cp -r skills/* ~/.deepseek/skills/")
        print(f"  - Validate: python scripts/validate_skills.py")


if __name__ == "__main__":
    main()
