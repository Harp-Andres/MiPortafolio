"""
CLI & MCP Command Handlers

Handlers for CLI commands and MCP tool invocations.
Routes to actual skill implementations.

Dual-mode operation:
  - Sync handlers for CLI (handle_*)
  - Async handlers for MCP (handle_*_async)

Both modes use the same underlying skill registry and routing logic.
"""

import logging
import sys
import asyncio
import json
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from datetime import datetime
from rich.console import Console

# Numbered directories (4_skills, 3_memory, 7_state) are not valid Python identifiers.
# We resolve them by inserting their parent (agent/) into sys.path and using importlib.
_AGENT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_AGENT_ROOT))

import importlib.util as _ilu


def _load_module(rel_path: str, attr: str = None):
    """Load a module from a file path relative to agent root, bypassing numbered-dir restrictions."""
    full_path = _AGENT_ROOT / rel_path
    spec = _ilu.spec_from_file_location(rel_path.replace("/", ".").replace("\\", "."), full_path)
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, attr) if attr else mod


# Lazy-loaded module references
_skills_mod = None
_routing_mod = None
_base_mod = None
_checkpoint_mod = None
_state_mod = None


def _load_deps():
    global _skills_mod, _routing_mod, _base_mod, _checkpoint_mod, _state_mod
    if _skills_mod is None:
        _base_mod = _load_module("4_skills/base_skill.py")
        _skills_mod = _load_module("4_skills/skill_registry.py")
        _routing_mod = _load_module("4_skills/skill_routing.py")
        _checkpoint_mod = _load_module("3_memory/checkpoint.py")
        _state_mod = _load_module("7_state/state_manager.py")


from config.constants import get_logger  # config/ has no number prefix, normal import works

logger = get_logger(__name__)
console = Console()

# Cache registry and router
_skill_registry = None
_skill_router = None


# Explicit ownership used by maestro for cross-agent orchestration visibility.
SKILL_SPECIALIZED_OWNER: Dict[str, str] = {
    "dependency_resolver": "devops-cicd-manager",
    "type_checker": "software-architecture-manager",
    "linter_checker": "sdet-quality-manager",
    "build_orchestrator": "devops-cicd-manager",
    "quality_gate_runner": "devops-cicd-manager",
    "unit_test_runner": "sdet-quality-manager",
    "e2e_test_runner": "portfolio-test-manager",
    "coverage_analyzer": "sdet-quality-manager",
    "test_aggregator": "sdet-quality-manager",
    "github_pages_deployer": "portfolio-deployment-manager",
    "release_orchestrator": "github-cicd-manager",
    "git_workflow_manager": "github-cicd-manager",
    "git_branch_creator": "github-cicd-manager",
    "cv_data_validator": "portfolio-cv-manager",
    "pdf_generator": "portfolio-cv-manager",
    "docx_generator": "portfolio-cv-manager",
    "excel_generator": "portfolio-cv-manager",
    "sync_verifier": "portfolio-cv-manager",
    "portfolio_updater": "portfolio-cv-manager",
    "skills_manager": "software-architecture-manager",
    "certificate_manager": "portfolio-cv-manager",
    "experience_tracker": "portfolio-cv-manager",
    "api_validator": "sdet-quality-manager",
    "backend_server": "platform-architecture-manager",
    "backend_test_runner": "sdet-quality-manager",
    "code_formatter": "software-architecture-manager",
    "performance_monitor": "devops-cicd-manager",
}


WORKFLOW_AGENT_PRIORITY: Dict[str, List[str]] = {
    "ci": [
        "setup-portability-manager",
        "devops-cicd-manager",
        "software-architecture-manager",
        "sdet-quality-manager",
    ],
    "test": [
        "setup-portability-manager",
        "sdet-quality-manager",
        "portfolio-test-manager",
    ],
    "deploy": [
        "devops-cicd-manager",
        "platform-architecture-manager",
        "github-cicd-manager",
        "portfolio-deployment-manager",
    ],
    "portfolio-update": [
        "software-architecture-manager",
        "portfolio-cv-manager",
        "portfolio-test-manager",
    ],
    "quality": [
        "software-architecture-manager",
        "sdet-quality-manager",
        "devops-cicd-manager",
    ],
    "full-pipeline": [
        "setup-portability-manager",
        "devops-cicd-manager",
        "software-architecture-manager",
        "sdet-quality-manager",
        "portfolio-test-manager",
        "platform-architecture-manager",
        "github-cicd-manager",
        "portfolio-deployment-manager",
        "portfolio-cv-manager",
        "os-platform-manager",
    ],
}


def _get_registry():
    """Get skill registry (lazy load)"""
    global _skill_registry
    _load_deps()
    if _skill_registry is None:
        _skill_registry = _skills_mod.get_skill_registry()
    return _skill_registry


def _get_router():
    """Get skill router (lazy load)"""
    global _skill_router
    _load_deps()
    if _skill_router is None:
        _skill_router = _routing_mod.get_skill_router()
    return _skill_router


def _get_specialized_agent_for_skill(skill_name: str) -> str:
    """Resolve specialized manager owner for a skill (maestro visibility layer)."""
    return SKILL_SPECIALIZED_OWNER.get(skill_name, "agent-master-portfolio")


def _build_orchestration_plan(workflow: str) -> List[Dict[str, Any]]:
    """Build ordered plan: specialized agent -> owned skills for a workflow."""
    workflow_name = workflow.lower()
    workflow_skills = _get_workflow_skills(workflow_name)
    if not workflow_skills:
        return []

    by_agent: Dict[str, List[str]] = {}
    for skill in workflow_skills:
        agent_name = _get_specialized_agent_for_skill(skill)
        by_agent.setdefault(agent_name, []).append(skill)

    ordered_plan: List[Dict[str, Any]] = []
    for agent_name in WORKFLOW_AGENT_PRIORITY.get(workflow_name, []):
        skills = by_agent.pop(agent_name, [])
        if skills:
            ordered_plan.append({"agent": agent_name, "skills": skills})

    # Append any unmapped agents at the end to avoid hiding work.
    for agent_name, skills in by_agent.items():
        ordered_plan.append({"agent": agent_name, "skills": skills})

    return ordered_plan


# ============================================================================
# MAESTRO ORCHESTRATOR HANDLER - Master Workflow Coordinator
# ============================================================================

def handle_maestro(
    workflow: str,
    options: Optional[Dict[str, Any]] = None,
    verbose: bool = False,
) -> Dict[str, Any]:
    """
    Handle maestro command - Master orchestrator for complex workflows.

    Maestro coordinates multiple skills across multiple agents to execute
    complete workflows like CI/CD pipelines, deployments, portfolio updates.

    Available workflows:
    - ci: Full CI/CD pipeline (lint → type-check → build → test)
    - deploy: Deploy to GitHub Pages (quality-gate → build → deploy)
    - test: Run all tests (unit + E2E + coverage)
    - portfolio-update: Update portfolio (validate → generate → sync)
    - full-pipeline: Complete workflow (ci → test → deploy → portfolio)
    - quality: Run quality gates (lint, types, tests, build)

    Args:
        workflow: Workflow name to execute
        options: Workflow-specific options (skip_tests, dry_run, verbose, etc.)
        verbose: Enable verbose logging

    Returns:
        Dict with execution results
    """
    if options is None:
        options = {}

    logger.info(f"Maestro orchestrating workflow: {workflow}")
    logger.debug(f"Options: {options}")

    start_time = datetime.now()
    results = {
        "workflow": workflow,
        "status": "pending",
        "stages": [],
        "errors": [],
        "warnings": [],
        "timestamp": start_time.isoformat(),
        "orchestration_plan": [],
    }

    try:
        console.print(f"\n[bold cyan][MAESTRO] Maestro Orchestrator - {workflow.upper()}[/bold cyan]")
        console.print("=" * 70)

        # Map workflows to skill sequences
        workflow_skills = _get_workflow_skills(workflow)
        if not workflow_skills:
            error_msg = f"Unknown workflow: {workflow}"
            logger.error(error_msg)
            results["status"] = "failed"
            results["errors"].append(error_msg)
            return results

        orchestration_plan = _build_orchestration_plan(workflow)
        results["orchestration_plan"] = orchestration_plan
        if orchestration_plan:
            console.print("[bold]Orchestration plan:[/bold]")
            for stage in orchestration_plan:
                console.print(f"  - {stage['agent']}: {', '.join(stage['skills'])}")
            console.print()

        # Execute skills in sequence
        _load_deps()
        state = _state_mod.StateManager.get_instance()
        state.start_workflow(workflow, workflow_skills)

        for i, skill_name in enumerate(workflow_skills, 1):
            console.print(f"  [{i}/{len(workflow_skills)}] {skill_name}... ", end="")
            logger.info(f"Executing skill: {skill_name} ({i}/{len(workflow_skills)})")

            try:
                # Get routing for skill
                router = _get_router()
                agent = router.route_skill(
                    skill_name,
                    _routing_mod.RoutingContext(skill_name=skill_name, execution_order=i),
                )
                logger.debug(f"Routed {skill_name} to agent: {agent}")

                # Instantiate skill
                skill = _skills_mod.instantiate_skill(skill_name)
                if not skill:
                    raise RuntimeError(f"Failed to instantiate skill: {skill_name}")

                # Execute skill (real execution with checkpoint + state tracking)
                checkpoint = _checkpoint_mod.CheckpointManager.get_instance()
                state = _state_mod.StateManager.get_instance()
                state.mark_step_running(skill_name)

                skill_request = _base_mod.SkillRequest(verbose=verbose)
                skill_result = asyncio.run(skill.execute(skill_request))

                # Save to feedback loop
                checkpoint.save(skill_name, skill_result)
                state.mark_step_done(skill_name, skill_result)

                stage_result = {
                    "skill": skill_name,
                    "agent": agent.value if hasattr(agent, "value") else str(agent),
                    "specialized_agent": _get_specialized_agent_for_skill(skill_name),
                    "status": "success" if skill_result.success else "failed",
                    "duration_seconds": skill_result.duration_seconds,
                    "message": skill_result.message,
                    "output": skill_result.output,
                }

                results["stages"].append(stage_result)
                console.print("[green][OK][/green]")

            except Exception as e:
                error_msg = f"Skill '{skill_name}' failed: {str(e)}"
                logger.error(error_msg, exc_info=True)
                results["errors"].append(error_msg)
                console.print("[red][FAIL][/red]")

                if not options.get("continue_on_error", False):
                    break

        _load_deps()
        state = _state_mod.StateManager.get_instance()
        state.finish_workflow()

        if not results["errors"]:
            results["status"] = "success"
            console.print("=" * 70)
            console.print(f"[green][OK] Workflow completed successfully[/green]")
        else:
            results["status"] = "failed"
            console.print("=" * 70)
            console.print(f"[red][FAIL] Workflow failed with {len(results['errors'])} errors[/red]")
            checkpoint = _checkpoint_mod.CheckpointManager.get_instance()
            results["feedback_context"] = checkpoint.get_feedback_context()
            results["recovery_plan"] = state.get_recovery_plan()

        results["duration_seconds"] = (
            (datetime.now() - start_time).total_seconds()
        )
        logger.info(f"Maestro workflow complete: {workflow} ({results['status']})")

        return results

    except Exception as e:
        logger.error(f"Maestro orchestration failed: {str(e)}", exc_info=True)
        results["status"] = "failed"
        results["errors"].append(f"Maestro orchestration failed: {str(e)}")
        return results


async def handle_maestro_async(arguments: Dict[str, Any]) -> str:
    """
    Async handler for maestro tool (used by MCP server).

    Args:
        arguments: MCP tool arguments dict

    Returns:
        JSON string with results
    """
    workflow = arguments.get("workflow", "")
    options = arguments.get("options", {})
    verbose = arguments.get("verbose", False)

    if not workflow:
        return json.dumps({
            "status": "error",
            "error": "Missing required parameter: workflow"
        })

    # Call sync handler (maestro is synchronous)
    result = handle_maestro(workflow=workflow, options=options, verbose=verbose)
    return json.dumps(result)


def handle_maestro_plan(workflow: str) -> Dict[str, Any]:
    """Return the agent-level orchestration plan without executing skills."""
    workflow_skills = _get_workflow_skills(workflow)
    if not workflow_skills:
        return {
            "status": "failed",
            "error": f"Unknown workflow: {workflow}",
            "workflow": workflow,
            "orchestration_plan": [],
        }

    return {
        "status": "success",
        "workflow": workflow,
        "workflow_skills": workflow_skills,
        "orchestration_plan": _build_orchestration_plan(workflow),
    }


async def handle_maestro_plan_async(arguments: Dict[str, Any]) -> str:
    """Async handler for plan-only orchestration preview."""
    workflow = arguments.get("workflow", "")
    if not workflow:
        return json.dumps({
            "status": "error",
            "error": "Missing required parameter: workflow"
        })
    return json.dumps(handle_maestro_plan(workflow))


# ============================================================================
# SKILL-SPECIFIC HANDLERS - For individual skill invocation via MCP
# ============================================================================

async def _run_skill_handler(skill_name: str, arguments: Dict[str, Any]) -> str:
    """Generic skill handler: loads skill via file-path registry, executes, returns JSON."""
    _load_deps()
    try:
        skill = _skills_mod.instantiate_skill(skill_name)
        if not skill:
            return json.dumps({"status": "error", "error": f"Skill '{skill_name}' not found in registry"})
        request = _base_mod.SkillRequest(
            timeout_seconds=arguments.get("timeout_seconds", 120),
            verbose=arguments.get("verbose", False),
        )
        result = await skill.execute(request)
        # save to feedback loop
        _checkpoint_mod.CheckpointManager.get_instance().save(skill_name, result)
        return json.dumps({
            "status": "success" if result.success else "failed",
            "message": result.message,
            "output": result.output,
            "errors": result.errors,
            "duration_seconds": result.duration_seconds,
        })
    except Exception as e:
        logger.error(f"Skill '{skill_name}' error: {e}", exc_info=True)
        return json.dumps({"status": "error", "error": str(e)})


async def handle_type_checker_async(arguments: Dict[str, Any]) -> str:
    return await _run_skill_handler("type_checker", arguments)


async def handle_build_orchestrator_async(arguments: Dict[str, Any]) -> str:
    return await _run_skill_handler("build_orchestrator", arguments)


async def handle_quality_gate_runner_async(arguments: Dict[str, Any]) -> str:
    return await _run_skill_handler("quality_gate_runner", arguments)


async def handle_unit_test_runner_async(arguments: Dict[str, Any]) -> str:
    return await _run_skill_handler("unit_test_runner", arguments)


async def handle_e2e_test_runner_async(arguments: Dict[str, Any]) -> str:
    return await _run_skill_handler("e2e_test_runner", arguments)


async def handle_coverage_analyzer_async(arguments: Dict[str, Any]) -> str:
    return await _run_skill_handler("coverage_analyzer", arguments)


async def handle_pdf_generator_async(arguments: Dict[str, Any]) -> str:
    return await _run_skill_handler("pdf_generator", arguments)


async def handle_docx_generator_async(arguments: Dict[str, Any]) -> str:
    return await _run_skill_handler("docx_generator", arguments)


async def handle_excel_generator_async(arguments: Dict[str, Any]) -> str:
    return await _run_skill_handler("excel_generator", arguments)


async def handle_github_pages_deployer_async(arguments: Dict[str, Any]) -> str:
    return await _run_skill_handler("github_pages_deployer", arguments)


async def handle_release_orchestrator_async(arguments: Dict[str, Any]) -> str:
    return await _run_skill_handler("release_orchestrator", arguments)


async def handle_git_workflow_manager_async(arguments: Dict[str, Any]) -> str:
    return await _run_skill_handler("git_workflow_manager", arguments)


# ============================================================================
# CLI HANDLERS - for command-line interface
# ============================================================================

def handle_ci(
    stages: Optional[str] = None,
    verbose: bool = False,
) -> Dict[str, Any]:
    """
    Handle 'ci' command - Full CI/CD pipeline.

    Orchestrates full CI/CD pipeline.
    Delegates to maestro with 'ci' workflow.

    Args:
        stages: Specific stages to run (comma-separated)
        verbose: Enable verbose logging

    Returns:
        Dict with execution results
    """
    logger.info("Handling CI command")
    return handle_maestro(workflow="ci", options={"stages": stages} if stages else {}, verbose=verbose)


def handle_deploy(
    environment: str = "production",
    force: bool = False,
    verbose: bool = False,
) -> Dict[str, Any]:
    """
    Handle 'deploy' command - Deployment to GitHub Pages.

    Args:
        environment: deployment environment
        force: Skip confirmations
        verbose: Enable verbose logging

    Returns:
        Dict with execution results
    """
    logger.info(f"Handling deploy command for environment: {environment}")
    return handle_maestro(workflow="deploy", options={"environment": environment}, verbose=verbose)


def handle_test(
    suite: str = "all",
    coverage: bool = True,
    verbose: bool = False,
) -> Dict[str, Any]:
    """
    Handle 'test' command - Run all tests.

    Args:
        suite: Test suite to run
        coverage: Generate coverage reports
        verbose: Enable verbose logging

    Returns:
        Dict with execution results
    """
    logger.info(f"Handling test command for suite: {suite}")
    return handle_maestro(workflow="test", options={"suite": suite, "coverage": coverage}, verbose=verbose)


def handle_docs(
    format: str = "all",
    output_dir: Optional[str] = None,
    sync_verify: bool = True,
) -> Dict[str, Any]:
    """
    Handle 'docs' command - Generate documents.

    Args:
        format: Document format (all, docx, pdf, excel)
        output_dir: Output directory for documents
        sync_verify: Verify synchronization between formats

    Returns:
        Dict with execution results
    """
    logger.info(f"Handling docs command for format: {format}")
    return handle_maestro(workflow="portfolio-update", options={"format": format}, verbose=False)


def handle_add_project(
    name: str,
    description: Optional[str] = None,
    tech: Optional[str] = None,
    link: Optional[str] = None,
    github: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Handle 'add-project' command - Add project to portfolio.

    Args:
        name: Project name
        description: Project description
        tech: Technologies
        link: Project URL
        github: GitHub repository URL

    Returns:
        Dict with execution results
    """
    logger.info(f"Handling add-project command for: {name}")
    return handle_maestro(workflow="portfolio-update", options={"project_name": name}, verbose=False)


# ============================================================================
# WORKFLOW DEFINITION - Maps workflow names to skill sequences
# ============================================================================

def _get_workflow_skills(workflow: str) -> List[str]:
    """
    Map workflow name to list of skills to execute.

    Args:
        workflow: Workflow name

    Returns:
        List of skill names in execution order
    """
    workflows = {
        "ci": [
            "dependency_resolver",
            "type_checker",
            "linter_checker",
            "build_orchestrator",
            "unit_test_runner",
            "coverage_analyzer",
        ],
        "deploy": [
            "quality_gate_runner",
            "build_orchestrator",
            "github_pages_deployer",
        ],
        "test": [
            "unit_test_runner",
            "e2e_test_runner",
            "coverage_analyzer",
            "test_aggregator",
        ],
        "portfolio-update": [
            "cv_data_validator",
            "pdf_generator",
            "docx_generator",
            "excel_generator",
            "sync_verifier",
        ],
        "quality": [
            "linter_checker",
            "type_checker",
            "unit_test_runner",
            "build_orchestrator",
            "quality_gate_runner",
        ],
        "full-pipeline": [
            "dependency_resolver",
            "type_checker",
            "linter_checker",
            "build_orchestrator",
            "unit_test_runner",
            "e2e_test_runner",
            "coverage_analyzer",
            "github_pages_deployer",
            "cv_data_validator",
            "pdf_generator",
            "docx_generator",
            "sync_verifier",
        ],
    }
    return workflows.get(workflow.lower(), [])
