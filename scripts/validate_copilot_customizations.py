#!/usr/bin/env python3
"""Copilotカスタマイズ一式の構造と参照関係を検証する。"""

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

GROUP_LABELS = {
    "agents": "エージェント",
    "skills": "スキル",
    "prompts": "プロンプト",
    "instructions": "指示ファイル",
    "templates": "テンプレート",
}


def parse_frontmatter(path: Path) -> tuple[dict[str, object], list[str]]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, [f"{path}: YAMLフロントマターがありません"]
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, [f"{path}: YAMLフロントマターが正しく終了していません"]

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
            errors.append(f"{path}:{number}: 対応していないフロントマター構文です")
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
                errors.append(f"{path}: 相対リンクの参照先がありません: {target}")
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
            errors.append(f"必須ファイルがありません: {path}")

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
            label = GROUP_LABELS[name]
            errors.append(f"{label}: 想定{expected}件に対して{actual}件見つかりました")

    agent_names: set[str] = set()
    for path in groups["agents"]:
        data, parse_errors = parse_frontmatter(path)
        errors.extend(parse_errors)
        if not data.get("description"):
            errors.append(f"{path}: エージェントにはdescriptionが必要です")
        name = str(data.get("name") or path.name.removesuffix(".agent.md"))
        if name in agent_names:
            errors.append(f"{path}: エージェント名が重複しています: {name}")
        agent_names.add(name)
        tools = data.get("tools")
        if not isinstance(tools, list) or not tools:
            warnings.append(f"{path}: エージェントのtoolsが明示的に制限されていません")

    skill_names: set[str] = set()
    for path in groups["skills"]:
        data, parse_errors = parse_frontmatter(path)
        errors.extend(parse_errors)
        name = str(data.get("name") or "")
        description = str(data.get("description") or "")
        if not name or not description:
            errors.append(f"{path}: スキルにはnameとdescriptionが必要です")
        if name in skill_names:
            errors.append(f"{path}: スキル名が重複しています: {name}")
        skill_names.add(name)

    prompt_names: set[str] = set()
    for path in groups["prompts"]:
        data, parse_errors = parse_frontmatter(path)
        errors.extend(parse_errors)
        name = str(data.get("name") or path.name.removesuffix(".prompt.md"))
        if name in prompt_names:
            errors.append(f"{path}: プロンプト名が重複しています: {name}")
        prompt_names.add(name)
        if not data.get("description"):
            errors.append(f"{path}: プロンプトにはdescriptionが必要です")
        agent = str(data.get("agent") or "")
        if agent and agent not in agent_names and agent not in {"ask", "agent", "plan"}:
            errors.append(f"{path}: 未定義のエージェントを参照しています: {agent}")

    for path in groups["instructions"]:
        data, parse_errors = parse_frontmatter(path)
        errors.extend(parse_errors)
        if not data.get("applyTo"):
            errors.append(f"{path}: 指示ファイルにはapplyToが必要です")

    settings_path = root / ".vscode/settings.json"
    if settings_path.is_file():
        try:
            json.loads(settings_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{settings_path}: JSONの形式が正しくありません: {exc}")

    errors.extend(check_markdown_links(root))

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="カスタマイズ一式のルートディレクトリ",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="警告がある場合も終了コードを0以外にする",
    )
    args, unknown = parser.parse_known_args()

    if args.help:
        print(
            "使用方法: python validate_copilot_customizations.py "
            "[--root ルートディレクトリ] [--strict]\n\n"
            "オプション:\n"
            "  -h, --help    この説明を表示する\n"
            "  --root       カスタマイズ一式のルートディレクトリ\n"
            "  --strict     警告がある場合も終了コードを0以外にする"
        )
        return 0

    if unknown:
        print(f"エラー: 未知の引数です: {' '.join(unknown)}")
        return 2

    errors, warnings = validate(args.root.resolve())
    for message in errors:
        print(f"エラー: {message}")
    for message in warnings:
        print(f"警告: {message}")
    print(f"エラー: {len(errors)}件、警告: {len(warnings)}件")

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
