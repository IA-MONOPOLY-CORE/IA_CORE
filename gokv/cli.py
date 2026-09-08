"""Command-line entry points for the development-only GOKV vault."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from gokv.capture import append_execution_metric, append_learning_event
from gokv.compiler import compile_execution_pack
from gokv.schema import validate_knowledge_item
from gokv.storage import (
    default_paths,
    list_promoted,
    load_knowledge_item,
    rebuild_index,
    save_knowledge_item,
    validate_vault,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GOKV development-only vault tools")
    parser.add_argument("--repo-root", type=Path, help="repo root for isolated development storage")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate")
    commands.add_parser("rebuild-index")
    show = commands.add_parser("show-item")
    show.add_argument("knowledge_id")
    commands.add_parser("list-promoted")
    for name in ("append-event", "append-metric", "add-candidate", "compile-pack"):
        command = commands.add_parser(name)
        command.add_argument("json_path", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = default_paths(args.repo_root or Path.cwd())

    if args.command == "validate":
        result: Any = validate_vault(paths)
    elif args.command == "rebuild-index":
        result = rebuild_index(paths)
    elif args.command == "show-item":
        result = load_knowledge_item(args.knowledge_id, paths)
    elif args.command == "list-promoted":
        result = list_promoted(paths)
    elif args.command == "append-event":
        result = {"path": str(append_learning_event(_load_json(args.json_path), paths))}
    elif args.command == "append-metric":
        result = {"path": str(append_execution_metric(_load_json(args.json_path), paths))}
    elif args.command == "add-candidate":
        item = validate_knowledge_item(_load_json(args.json_path))
        if item["status"] != "CANDIDATE":
            raise ValueError("add-candidate solo acepta status CANDIDATE")
        destination = save_knowledge_item(item, paths)
        rebuild_index(paths)
        result = {"path": str(destination), "knowledge_id": item["knowledge_id"]}
    elif args.command == "compile-pack":
        result = compile_execution_pack(_load_json(args.json_path), paths)
    else:  # pragma: no cover - argparse enforces command choices
        raise ValueError(f"comando no soportado: {args.command}")

    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"JSON debe ser un objeto: {path}")
    return value


if __name__ == "__main__":
    raise SystemExit(main())
