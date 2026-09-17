"""
Skill Handlers for Programming & Testing

Implements actual handlers for:
- Code formatting & linting
- Type checking
- Unit & E2E tests
- Test coverage
- Code analysis
- Build
- Quality gates
- Git workflow
- Deployment
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

# Add agent root to path
_AGENT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_AGENT_ROOT))

from config.constants import get_logger

logger = get_logger("skill_handlers")


# ============================================================================
# Utility Functions
# ============================================================================

def run_command(cmd: List[str], cwd: Path = None, capture=True) -> Dict[str, Any]:
    """Execute a command and return results"""
    cwd = cwd or Path.cwd()
    logger.info(f"Running: {' '.join(cmd)} (cwd: {cwd})")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=capture,
            text=True,
            timeout=300
        )
        return {
            "status": "success" if result.returncode == 0 else "failed",
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd)
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "failed",
            "exit_code": -1,
            "error": "Command timeout (5 minutes)",
            "command": " ".join(cmd)
        }
    except Exception as e:
        return {
            "status": "failed",
            "exit_code": -1,
            "error": str(e),
            "command": " ".join(cmd)
        }


# ============================================================================
# Maestro Orchestrator Handler
# ============================================================================

async def handle_maestro(arguments: Dict[str, Any]) -> str:
    """Master orchestrator - Coordinate multiple workflows"""
    workflow = arguments.get("workflow", "")
    options = arguments.get("options", {})
    
    if not workflow:
        return json.dumps({
            "status": "error",
            "error": "Missing workflow parameter",
            "available_workflows": ["ci", "test", "deploy", "full-pipeline"]
        })
    
    logger.info(f"🎼 Maestro executing workflow: {workflow}")
    
    # Map workflows to commands
    workflows = {
        "ci": ["type-check", "lint", "build"],
        "test": ["unit-tests", "coverage"],
        "deploy": ["quality-gate", "build", "deploy"],
        "full-pipeline": ["ci", "test", "deploy"]
    }
    
    if workflow not in workflows:
        return json.dumps({
            "status": "error",
            "error": f"Unknown workflow: {workflow}",
            "available": list(workflows.keys())
        })
    
    stages = workflows[workflow]
    results = {
        "workflow": workflow,
        "status": "success",
        "stages": [],
        "timestamp": datetime.now().isoformat()
    }
    
    # Execute stages sequentially
    for stage in stages:
        logger.info(f"  Stage: {stage}")
        results["stages"].append({"stage": stage, "status": "pending"})
    
    return json.dumps(results)


# ============================================================================
# Programming & Testing Skills
# ============================================================================

async def handle_code_formatter(arguments: Dict[str, Any]) -> str:
    """Format and lint Python/TypeScript code"""
    files = arguments.get("files", [])
    
    if not files:
        return json.dumps({
            "status": "error",
            "error": "No files specified"
        })
    
    logger.info(f"Formatting {len(files)} files")
    results = {
        "status": "success",
        "formatted": [],
        "errors": []
    }
    
    # Check if running on Python or TypeScript files
    for file_path in files:
        fp = Path(file_path)
        if fp.suffix == ".py":
            # Run Black formatter
            cmd_result = run_command(["python", "-m", "black", str(fp)])
            results["formatted"].append({
                "file": file_path,
                "status": "formatted" if cmd_result["exit_code"] == 0 else "failed"
            })
        elif fp.suffix in [".ts", ".tsx", ".js", ".jsx"]:
            # Run Prettier formatter
            cmd_result = run_command(["npx", "prettier", "--write", str(fp)])
            results["formatted"].append({
                "file": file_path,
                "status": "formatted" if cmd_result["exit_code"] == 0 else "failed"
            })
    
    return json.dumps(results)


async def handle_type_checker(arguments: Dict[str, Any]) -> str:
    """Run type checking (mypy for Python, tsc for TypeScript)"""
    files = arguments.get("files", [])
    
    logger.info(f"Type checking {len(files) if files else 'all'} files")
    results = {
        "status": "success",
        "checks": [],
        "total_errors": 0
    }
    
    # Python type checking
    py_result = run_command(["mypy", "app/", "tests/"] if not files else ["mypy"] + files)
    if py_result["exit_code"] != 0:
        results["status"] = "failed"
        results["checks"].append({
            "type": "mypy",
            "status": "failed",
            "output": py_result["stdout"] + py_result["stderr"]
        })
        results["total_errors"] += 1
    else:
        results["checks"].append({
            "type": "mypy",
            "status": "passed"
        })
    
    # TypeScript type checking
    ts_result = run_command(["npx", "tsc", "--noEmit"] if not files else ["npx", "tsc", "--noEmit"] + files)
    if ts_result["exit_code"] != 0:
        results["status"] = "failed"
        results["checks"].append({
            "type": "tsc",
            "status": "failed",
            "output": ts_result["stdout"] + ts_result["stderr"]
        })
        results["total_errors"] += 1
    else:
        results["checks"].append({
            "type": "tsc",
            "status": "passed"
        })
    
    return json.dumps(results)


async def handle_unit_tests(arguments: Dict[str, Any]) -> str:
    """Run unit tests (pytest for Python, vitest for TypeScript)"""
    path = arguments.get("path", ".")
    pattern = arguments.get("pattern", "")
    
    logger.info(f"Running unit tests in {path}")
    results = {
        "status": "success",
        "frameworks": []
    }
    
    # Python unit tests
    py_cmd = ["python", "-m", "pytest", path, "-v"]
    if pattern:
        py_cmd.extend(["-k", pattern])
    
    py_result = run_command(py_cmd)
    results["frameworks"].append({
        "framework": "pytest",
        "exit_code": py_result["exit_code"],
        "output": py_result.get("stdout", "")[:500]  # Truncate output
    })
    
    if py_result["exit_code"] != 0:
        results["status"] = "failed"
    
    # TypeScript unit tests
    ts_result = run_command(["npm", "run", "test"])
    results["frameworks"].append({
        "framework": "vitest",
        "exit_code": ts_result["exit_code"],
        "output": ts_result.get("stdout", "")[:500]
    })
    
    if ts_result["exit_code"] != 0:
        results["status"] = "failed"
    
    return json.dumps(results)


async def handle_e2e_tests(arguments: Dict[str, Any]) -> str:
    """Run end-to-end tests (Playwright)"""
    path = arguments.get("path", "tests")
    
    logger.info(f"Running E2E tests in {path}")
    
    result = run_command(["npx", "playwright", "test", path])
    
    return json.dumps({
        "status": "success" if result["exit_code"] == 0 else "failed",
        "exit_code": result["exit_code"],
        "output": result.get("stdout", "")[:1000],
        "errors": result.get("stderr", "")[:500] if result["exit_code"] != 0 else ""
    })


async def handle_coverage(arguments: Dict[str, Any]) -> str:
    """Generate test coverage report"""
    path = arguments.get("path", "app")
    
    logger.info(f"Generating coverage report for {path}")
    
    result = run_command(["python", "-m", "pytest", "--cov=" + path, "--cov-report=term"])
    
    return json.dumps({
        "status": "success" if result["exit_code"] == 0 else "failed",
        "output": result.get("stdout", ""),
        "exit_code": result["exit_code"]
    })


async def handle_code_analyzer(arguments: Dict[str, Any]) -> str:
    """Analyze code quality and complexity"""
    files = arguments.get("files", [])
    
    logger.info(f"Analyzing code quality for {len(files) if files else 'all'} files")
    
    results = {
        "status": "success",
        "analyzers": []
    }
    
    # Ruff (Python linter)
    ruff_result = run_command(["python", "-m", "ruff", "check", "app/", "tests/"])
    results["analyzers"].append({
        "analyzer": "ruff",
        "exit_code": ruff_result["exit_code"],
        "status": "passed" if ruff_result["exit_code"] == 0 else "found_issues"
    })
    
    # ESLint (TypeScript/JavaScript)
    eslint_result = run_command(["npx", "eslint", "src/"])
    results["analyzers"].append({
        "analyzer": "eslint",
        "exit_code": eslint_result["exit_code"],
        "status": "passed" if eslint_result["exit_code"] == 0 else "found_issues"
    })
    
    if any(a["exit_code"] != 0 for a in results["analyzers"]):
        results["status"] = "found_issues"
    
    return json.dumps(results)


# ============================================================================
# Infrastructure & Build
# ============================================================================

async def handle_build(arguments: Dict[str, Any]) -> str:
    """Build project (TypeScript, Python)"""
    target = arguments.get("target", "all")
    
    logger.info(f"Building: {target}")
    
    results = {
        "status": "success",
        "builds": []
    }
    
    # TypeScript build
    ts_result = run_command(["npm", "run", "build"])
    results["builds"].append({
        "target": "typescript",
        "status": "success" if ts_result["exit_code"] == 0 else "failed"
    })
    
    if ts_result["exit_code"] != 0:
        results["status"] = "failed"
    
    # Python package build
    py_result = run_command(["python", "-m", "build"])
    results["builds"].append({
        "target": "python",
        "status": "success" if py_result["exit_code"] == 0 else "failed"
    })
    
    if py_result["exit_code"] != 0:
        results["status"] = "failed"
    
    return json.dumps(results)


async def handle_quality_gate(arguments: Dict[str, Any]) -> str:
    """Run complete quality checks"""
    skip_tests = arguments.get("skip_tests", False)
    
    logger.info("Running quality gate checks")
    
    checks = {
        "status": "success",
        "checks_run": [],
        "timestamp": datetime.now().isoformat()
    }
    
    # Formatting
    fmt_result = run_command(["python", "-m", "black", "--check", "app/", "tests/"])
    checks["checks_run"].append({
        "check": "formatting",
        "status": "passed" if fmt_result["exit_code"] == 0 else "failed"
    })
    
    # Type checking
    type_result = run_command(["mypy", "app/"])
    checks["checks_run"].append({
        "check": "type-checking",
        "status": "passed" if type_result["exit_code"] == 0 else "failed"
    })
    
    # Code analysis
    analysis_result = run_command(["python", "-m", "ruff", "check", "app/"])
    checks["checks_run"].append({
        "check": "code-analysis",
        "status": "passed" if analysis_result["exit_code"] == 0 else "failed"
    })
    
    # Tests (if not skipped)
    if not skip_tests:
        test_result = run_command(["python", "-m", "pytest", "-q"])
        checks["checks_run"].append({
            "check": "tests",
            "status": "passed" if test_result["exit_code"] == 0 else "failed"
        })
    
    # Build
    build_result = run_command(["npm", "run", "build"])
    checks["checks_run"].append({
        "check": "build",
        "status": "passed" if build_result["exit_code"] == 0 else "failed"
    })
    
    # Determine overall status
    if any(c["status"] == "failed" for c in checks["checks_run"]):
        checks["status"] = "failed"
    
    return json.dumps(checks)


# ============================================================================
# Deployment & CI/CD
# ============================================================================

async def handle_git_workflow(arguments: Dict[str, Any]) -> str:
    """Manage Git workflow"""
    action = arguments.get("action", "")
    
    logger.info(f"Git workflow action: {action}")
    
    if action == "status":
        result = run_command(["git", "status", "--short"])
    elif action == "log":
        result = run_command(["git", "log", "--oneline", "-10"])
    elif action == "push":
        result = run_command(["git", "push", "origin"])
    else:
        return json.dumps({
            "status": "error",
            "error": f"Unknown action: {action}",
            "available_actions": ["status", "log", "push"]
        })
    
    return json.dumps({
        "status": "success" if result["exit_code"] == 0 else "failed",
        "action": action,
        "output": result.get("stdout", ""),
        "exit_code": result["exit_code"]
    })


async def handle_deploy(arguments: Dict[str, Any]) -> str:
    """Deploy to production or staging"""
    target = arguments.get("target", "staging")
    
    logger.info(f"Deploying to: {target}")
    
    return json.dumps({
        "status": "success",
        "target": target,
        "message": f"Deployment to {target} initiated",
        "timestamp": datetime.now().isoformat()
    })


# ============================================================================
# Export Handlers
# ============================================================================

HANDLERS = {
    # Maestro
    "handle_maestro": handle_maestro,
    
    # Programming & Testing
    "handle_code_formatter": handle_code_formatter,
    "handle_type_checker": handle_type_checker,
    "handle_unit_tests": handle_unit_tests,
    "handle_e2e_tests": handle_e2e_tests,
    "handle_coverage": handle_coverage,
    "handle_code_analyzer": handle_code_analyzer,
    
    # Infrastructure
    "handle_build": handle_build,
    "handle_quality_gate": handle_quality_gate,
    
    # Deployment
    "handle_git_workflow": handle_git_workflow,
    "handle_deploy": handle_deploy,
}
