"""
Bootstrap CLI wrapper for portable setup operations.

Supports the flag-style commands requested for quick initialization on fresh machines:
  uv run agent --setup-init
  uv run agent --setup-status
  uv run agent --setup-show-architecture
  uv run agent --ci
  uv run agent --setup-list-skills

Also includes a Phase 2 setup agent mode (scaffold + verify only).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

import setup_agent
import phase2_setup_agent


def _load_handlers_module():
    root = Path(__file__).parent
    handlers_file = root / "1_interface" / "handlers.py"
    spec = importlib.util.spec_from_file_location("agent_handlers", handlers_file)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load handlers module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_ci() -> int:
    handlers = _load_handlers_module()
    result = handlers.handle_ci(stages=None, verbose=False)
    status = result.get("status", "failed")
    return 0 if status == "success" else 1


def _show_orchestration_plan(workflow: str) -> int:
    handlers = _load_handlers_module()
    result = handlers.handle_maestro_plan(workflow)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    status = result.get("status", "failed")
    return 0 if status == "success" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent",
        description="Portable setup bootstrap CLI for Mi Portafolio Agent",
    )

    parser.add_argument("--setup-init", action="store_true", help="Initialize portable ecosystem")
    parser.add_argument("--setup-status", action="store_true", help="Show setup and architecture status")
    parser.add_argument("--setup-show-architecture", action="store_true", help="Show detailed 7-layer architecture")
    parser.add_argument("--setup-list-skills", action="store_true", help="List all registered skills")
    parser.add_argument("--setup-validate", action="store_true", help="Validate infrastructure components")
    parser.add_argument("--setup-mcp-check", action="store_true", help="Validate MCP configuration")
    parser.add_argument("--ci", action="store_true", help="Run CI workflow through maestro handlers")
    parser.add_argument(
        "--orchestration-plan",
        action="store_true",
        help="Preview maestro orchestration plan by workflow",
    )
    parser.add_argument(
        "--workflow",
        default="full-pipeline",
        choices=["ci", "test", "deploy", "portfolio-update", "quality", "full-pipeline"],
        help="Workflow name for orchestration plan preview",
    )

    parser.add_argument("--setup-phase2-agent", action="store_true", help="Create scaffold + plan for Phase 2")
    parser.add_argument("--setup-phase2-verify", action="store_true", help="Verify scaffold for Phase 2")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.setup_init:
        setup_agent.init()
        return
    if args.setup_status:
        setup_agent.status()
        return
    if args.setup_show_architecture:
        setup_agent.show_architecture()
        return
    if args.setup_list_skills:
        setup_agent.list_skills()
        return
    if args.setup_validate:
        setup_agent.validate()
        return
    if args.setup_mcp_check:
        setup_agent.check_mcp()
        return
    if args.setup_phase2_agent:
        created, skipped = phase2_setup_agent.scaffold_phase2()
        print(f"Phase 2 scaffold prepared. Created: {created}, skipped existing: {skipped}")
        return
    if args.setup_phase2_verify:
        ok = phase2_setup_agent.verify_phase2()
        raise SystemExit(0 if ok else 1)
    if args.ci:
        code = _run_ci()
        raise SystemExit(code)
    if args.orchestration_plan:
        code = _show_orchestration_plan(args.workflow)
        raise SystemExit(code)

    parser.print_help()


if __name__ == "__main__":
    main()
