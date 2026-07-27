#!/usr/bin/env python3
"""Validate the structure and references of this Copilot customization pack."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


EXPECTED_COUNTS = {
    "agents": 7,
    "skills": 3,
    "prompts": 25,
    "instructions": 4,
    "templates": 8,
}


def parse_frontmatter(path: Path) -> tuple[dict[str, object], list[str]]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, [f"{path}: missing YAML frontmatter"]
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, [f"{path}: unterminated YAML frontmatter"]

    data: dict[str, object] = {}
    current_list: str | None = None
    for number, raw_line in enumerate(text[4:end].splitlines(), start=2):
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        list_match = re.match(r"^\s+-\s+(.+)$", line)
        if list_match and current_list:
            value = list_match.group(1).strip().strip("'\"")
            cast_list = data.setdefault(current_list, [])
            if isinstance(cast_list, list):
                cast_list.append(value)
            continue
        field_match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$", line)
        if not field_match:
            errors.append(f"{path}:{number}: unsupported frontmatter syntax")
            continue
        key, value = field_match.groups()
        value = (value or "").strip()
        if value:
            data[key] = value.strip("'\"")
            current_list = None
        else:
            data[key] = []
            current_list = key
    return data, errors


def check_markdown_links(root: Path) -> list[str]:
    errors: list[str] = []
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in link_pattern.findall(text):
            clean = target.split("#", 1)[0].strip()
            if not clean or re.match(r"^[a-z]+://", clean):
                continue
            if clean.startswith(("mailto:", "oai-")):
                continue
            resolved = (path.parent / clean).resolve()
            if not resolved.exists():
                errors.append(f"{path}: broken relative link: {target}")
    return errors


def validate(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    github = root / ".github"

    required = [
        root / "README.md",
        root / "AGENTS.md",
        github / "copilot-instructions.md",
        root / ".vscode/settings.json",
        root / "docs/how-to/use-cases.md",
        root / "docs/reference/customizations.md",
        root / "docs/templates/project-context.md",
    ]
    for path in required:
        if not path.is_file():
            errors.append(f"missing required file: {path}")

    groups = {
        "agents": sorted((github / "agents").glob("*.agent.md")),
        "skills": sorted((github / "skills").glob("*/SKILL.md")),
        "prompts": sorted((github / "prompts").glob("*.prompt.md")),
        "instructions": sorted((github / "instructions").glob("*.instructions.md")),
        "templates": sorted((root / "docs/templates").glob("*.md")),
    }
    groups["templates"] = [
        path for path in groups["templates"] if path.name != "README.md"
    ]

    for name, expected in EXPECTED_COUNTS.items():
        actual = len(groups[name])
        if actual != expected:
            errors.append(f"{name}: expected {expected}, found {actual}")

    agent_names: set[str] = set()
    for path in groups["agents"]:
        data, parse_errors = parse_frontmatter(path)
        errors.extend(parse_errors)
        if not data.get("description"):
            errors.append(f"{path}: agent requires description")
        name = str(data.get("name") or path.name.removesuffix(".agent.md"))
        if name in agent_names:
            errors.append(f"{path}: duplicate agent name: {name}")
        agent_names.add(name)
        tools = data.get("tools")
        if not isinstance(tools, list) or not tools:
            warnings.append(f"{path}: agent tools are not explicitly restricted")

    skill_names: set[str] = set()
    for path in groups["skills"]:
        data, parse_errors = parse_frontmatter(path)
        errors.extend(parse_errors)
        name = str(data.get("name") or "")
        description = str(data.get("description") or "")
        if not name or not description:
            errors.append(f"{path}: skill requires name and description")
        if name in skill_names:
            errors.append(f"{path}: duplicate skill name: {name}")
        skill_names.add(name)

    prompt_names: set[str] = set()
    for path in groups["prompts"]:
        data, parse_errors = parse_frontmatter(path)
        errors.extend(parse_errors)
        name = str(data.get("name") or path.name.removesuffix(".prompt.md"))
        if name in prompt_names:
            errors.append(f"{path}: duplicate prompt name: {name}")
        prompt_names.add(name)
        if not data.get("description"):
            errors.append(f"{path}: prompt requires description")
        agent = str(data.get("agent") or "")
        if agent and agent not in agent_names and agent not in {"ask", "agent", "plan"}:
            errors.append(f"{path}: unknown agent reference: {agent}")

    for path in groups["instructions"]:
        data, parse_errors = parse_frontmatter(path)
        errors.extend(parse_errors)
        if not data.get("applyTo"):
            errors.append(f"{path}: instruction requires applyTo")

    settings_path = root / ".vscode/settings.json"
    if settings_path.is_file():
        try:
            json.loads(settings_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{settings_path}: invalid JSON: {exc}")

    errors.extend(check_markdown_links(root))

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Customization pack root",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as a non-zero exit status",
    )
    args = parser.parse_args()

    errors, warnings = validate(args.root.resolve())
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
