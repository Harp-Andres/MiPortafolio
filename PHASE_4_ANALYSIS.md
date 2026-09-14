---
title: "Phase 4: CI/CD Analysis & Master Agent Semantic Restructuring"
description: "Complete analysis of CI/CD pipeline with extracted transversal functionalities for Master Agent enhancement"
date: "2024"
version: "1.0"
---

# Phase 4: CI/CD Analysis & Agent Restructuring Plan

## 📋 Executive Summary

This document consolidates:
1. **CI/CD Pipeline Analysis** - 10-stage comprehensive workflow for Mi Portafolio
2. **Transversal Functionality Extraction** - 12 cross-cutting concerns + 12 business logic skills
3. **Agent Skill Mapping** - 28+ skills extracted from CI/CD for Master Agent
4. **Implementation Roadmap** - Sequential steps for Phase 4A → Phase 4B

**Impact:** Master Agent will have enterprise-grade CI/CD capabilities, enabling autonomous quality enforcement, deployment automation, and portfolio management.

---

## Part 1: Transversal Functionality Analysis

### 🔄 Cross-Cutting Concerns (12)

These patterns appear throughout the CI/CD pipeline and should become reusable agent capabilities:

| # | Concern | Application | Agent Skill |
|---|---------|-------------|------------|
| 1 | Quality Gate Enforcement | Unified validation rules (types, tests, build, sync) | `@quality-gate-runner` |
| 2 | Error Handling & Retry | Consistent failure patterns across all jobs | `@error-handler` |
| 3 | Git Workflow Management | Branch creation, commits, PR management | `@git-workflow-manager` |
| 4 | Dependency Resolution | pnpm workspace + Python venv management | `@dependency-resolver` |
| 5 | Type Checking Pipeline | TypeScript strict mode + Python type hints | `@type-checker` |
| 6 | Sync Verification | Web ↔ DOCX ↔ PDF ↔ Excel consistency | `@sync-verifier` |
| 7 | Build Artifact Management | Output generation, caching, optimization | `@artifact-manager` |
| 8 | Test Result Aggregation | Vitest + Playwright + PyTest combinations | `@test-aggregator` |
| 9 | Configuration Management | Environment variables, multi-env settings | `@config-manager` |
| 10 | Logging & Monitoring | Centralized status, progress, diagnostics | `@telemetry-recorder` |
| 11 | State Machine Orchestration | Workflow sequencing, dependency ordering | `@orchestrator-engine` |
| 12 | Performance Metrics | Build times, coverage, bundle size | `@metrics-analyzer` |

### 💼 Business Logic & Skills (12)

Reusable business functions extracted from codebase:

| # | Business Function | Implementation | Agent Skill |
|---|------------------|-----------------|------------|
| 1 | CV Data Validation | Pydantic models (skills, exp, education, certs) | `@cv-data-validator` |
| 2 | DOCX Generation | ATS-optimized Word document from CV data | `@docx-generator` |
| 3 | PDF Generation | Visually formatted PDF from CV data | `@pdf-generator` |
| 4 | Excel Generation | Multi-sheet workbook from CV data | `@excel-generator` |
| 5 | Sync Verification | Cross-platform validation algorithm | `@sync-verifier` |
| 6 | Responsive Design Tests | Playwright viewport coverage (360-1920px) | `@responsive-tester` |
| 7 | CV Download Handler | Trigger document generation on updates | `@cv-downloader` |
| 8 | Git Workflow Automation | Feature → PR → Merge → Deploy sequence | `@git-automator` |
| 9 | Type Coverage Analysis | AST analysis of TypeScript annotations | `@type-coverage-analyzer` |
| 10 | Test Suite Orchestration | Sequential unit → E2E → integration | `@test-orchestrator` |
| 11 | Code Coverage Analysis | Vitest aggregation, threshold enforcement | `@coverage-analyzer` |
| 12 | Build Optimization | Vite minification, tree-shake, code splitting | `@build-optimizer` |

---

## Part 2: Tools → Agent Skills Mapping (28 Skills)

### Complete Skills Catalog

```
INFRASTRUCTURE SKILLS
├── @dependency-resolver      pnpm install --frozen-lockfile
├── @type-checker             tsc --noEmit + mypy --strict
├── @build-orchestrator       pnpm run build (Web + Backend)
└── @quality-gate-runner      Enforce all gates before deploy

TESTING SKILLS
├── @unit-test-runner         Vitest + PyTest execution
├── @e2e-test-runner          Playwright multi-browser tests
├── @coverage-analyzer        Generate & analyze coverage reports
└── @test-aggregator          Combine results from multiple suites

DOCUMENT GENERATION SKILLS
├── @docx-generator           python-docx ATS-optimized documents
├── @pdf-generator            ReportLab PDF generation
├── @excel-generator          OpenPyXL multi-sheet workbooks
├── @sync-verifier            Validate Web=DOCX=PDF=Excel
└── @cv-data-validator        Pydantic model validation

DEPLOYMENT SKILLS
├── @git-branch-creator       git checkout -b feat/name
├── @git-workflow-manager     Commit, push, PR, merge automation
├── @github-pages-deployer    Deploy to gh-pages branch
└── @release-orchestrator     Full release pipeline automation

PORTFOLIO MANAGEMENT SKILLS
├── @portfolio-updater        Add/modify portfolio projects
├── @skills-manager           Manage skill categories
├── @certificate-manager      Manage certificates
└── @experience-tracker       Track work experience

CODE QUALITY SKILLS
├── @code-formatter           Prettier formatting
├── @linter-checker           ESLint + auto-fix
└── @performance-monitor      Build times, bundle size

BACKEND SKILLS
├── @backend-server           FastAPI dev server
├── @backend-test-runner      Python test execution
└── @api-validator            Validate API routes
```

### Detailed Tool Mapping

| Tool | Command | Agent Skill | Parameters | Purpose |
|------|---------|------------|-----------|---------|
| **npm/pnpm** | `pnpm install` | @dependency-resolver | workspace, strict | Install with lockfile |
| **TypeScript** | `tsc --noEmit` | @type-checker | files, exclude, strict | Type validation |
| **Python** | `mypy src/ --strict` | @type-checker | modules, config | Python type hints |
| **Vite** | `pnpm run build` | @build-orchestrator | minify, maps, base | Bundle production |
| **Vitest** | `pnpm run test` | @unit-test-runner | coverage, ui, reporter | Unit tests |
| **PyTest** | `pytest` | @unit-test-runner | markers, cov, asyncio | Python tests |
| **Playwright** | `playwright test` | @e2e-test-runner | project, headed, debug | Cross-browser E2E |
| **Prettier** | `prettier --write` | @code-formatter | glob, parser, config | Code formatting |
| **ESLint** | `eslint --fix` | @linter-checker | extensions, cache, max | Lint & fix |
| **python-docx** | `generate_cv_docx()` | @docx-generator | cv_data, path, style | DOCX creation |
| **ReportLab** | `generate_cv_pdf()` | @pdf-generator | cv_data, colors, fonts | PDF creation |
| **OpenPyXL** | `generate_cv_excel()` | @excel-generator | cv_data, sheets | Excel creation |
| **Sync Validator** | `verify_sync()` | @sync-verifier | web, docx, pdf, excel | Verify sync |
| **Pydantic** | `CVDataModel()` | @cv-data-validator | json, strict | Validate CV data |
| **Git** | `git checkout -b` | @git-branch-creator | pattern, base | Create branches |
| **Git** | `git commit -m` | @git-commit-formatter | type, scope, body | Format commits |
| **GitHub Pages** | `gh-pages -d dist` | @github-pages-deployer | branch, force | Deploy artifacts |
| **Uvicorn** | `uvicorn main:app` | @backend-server | reload, host, port | Dev server |

---

## Part 3: Complete CI/CD Pipeline Definition

### 10-Stage Pipeline Architecture

```
STAGE 1: INITIALIZE & VALIDATE
├── Detect Node/Python versions
├── Setup Node.js (20.x)
├── Setup Python (3.10)
└── Install pnpm + verify environment

        ↓

STAGE 2: DEPENDENCY RESOLUTION (parallel-capable)
├── npm: pnpm install --frozen-lockfile
├── Python: pip install -e ".[dev]"
├── Verify workspace structure
└── Cache dependencies for future stages

        ↓ (all dependencies must succeed)

STAGE 3: TYPE CHECKING (parallel-capable)
├── TypeScript: tsc --noEmit (strict mode)
├── Python: mypy src/ --strict
└── Fail if type errors found

        ↓ (type safety gate)

STAGE 4: CODE QUALITY (parallel-capable)
├── ESLint: eslint --ext .ts,.tsx src/
├── Prettier: prettier --check 'src/**/*'
├── Python Black: black --check src/
└── Python isort: isort --check-only src/

        ↓ (quality gate)

STAGE 5: BUILD (parallel-capable)
├── Web: pnpm run build:web (Vite)
├── Backend: pnpm run build:backend
├── Verify dist/ generation
├── Analyze bundle size
└── Upload build artifacts

        ↓ (successful build required)

STAGE 6A: TESTING - UNIT (parallel matrix: web, backend)
├── Web: pnpm run test:web --coverage
├── Backend: pytest tests/ --cov
├── Upload coverage to codecov
└── Enforce coverage thresholds

STAGE 6B: TESTING - E2E (parallel matrix: chromium, firefox, webkit)
├── Setup Playwright browsers
├── Run: pnpm run test:e2e --project={browser}
├── Upload Playwright reports
└── Validate cross-browser compatibility

        ↓ (all tests must pass)

STAGE 7: SYNCHRONIZATION VERIFICATION
├── Run: pnpm run sync:verify
├── Validate CV data models
├── Check Web ↔ DOCX ↔ PDF ↔ Excel consistency
└── Report sync status

        ↓ (sync gate)

STAGE 8: SECURITY & PERFORMANCE (parallel-capable)
├── npm audit --audit-level=moderate
├── Python security check
├── Generate security report
└── Continue on non-critical issues

        ↓

STAGE 9: QUALITY GATES SUMMARY
├── Type Check: PASS/FAIL ✓
├── Code Quality: PASS/FAIL ✓
├── Build: PASS/FAIL ✓
├── Unit Tests: PASS/FAIL ✓
├── E2E Tests: PASS/FAIL ✓
├── Sync Verify: PASS/FAIL ✓
└── FAIL if any gate failed

        ↓ (all gates must pass)

STAGE 10: DEPLOYMENT (main branch only, post-push)
├── Download build artifacts
├── Deploy to GitHub Pages
├── Create GitHub Deployment record
├── Verify deployment (HTTP 200)
└── Notify success

        ↓

STAGE 11: POST-DEPLOYMENT VALIDATION
├── Verify live site responds (HTTP 200)
├── Notify deployment success
└── Create issue if deployment failed
```

### Pipeline YAML Structure

**File:** `.github/workflows/cicd-complete.yml`

**Trigger Events:**
- `push` to: main, develop, feat/*, hotfix/*
- `pull_request` to: main, develop
- `schedule`: Weekly (cron '0 0 * * 0')
- `workflow_dispatch`: Manual trigger

**Environment:**
```yaml
NODE_VERSION: '20'
PYTHON_VERSION: '3.10'
PNPM_VERSION: '9.0.0'
```

**Jobs Dependency Graph:**
```
setup-and-validate
├── dependency-resolve (needs: setup)
│   ├── type-check (needs: deps)
│   │   └── quality-gates (needs: type)
│   ├── code-quality (needs: deps)
│   │   └── quality-gates (needs: quality)
│   ├── build (needs: deps+type+quality)
│   │   ├── test-unit (needs: build)
│   │   │   └── quality-gates (needs: test)
│   │   ├── test-e2e (needs: build)
│   │   │   └── quality-gates (needs: e2e)
│   │   └── sync-verify (needs: test-unit)
│   │       └── quality-gates (needs: sync)
│   └── security-scan (needs: deps)
│
└── deploy (needs: quality-gates + main branch)
    └── post-deploy (needs: deploy)
```

**Parallel Execution Strategies:**
- **Test Suite Matrix:** [web, backend] - simultaneous test execution
- **Browser Matrix:** [chromium, firefox, webkit] - parallel E2E runs
- **Independent Checks:** type-check, code-quality, security-scan can run in parallel

**Quality Gates (all must pass):**
1. ✅ Type checking (TypeScript strict + Python mypy)
2. ✅ Code formatting (Prettier + Black + isort)
3. ✅ Linting (ESLint + Flake8)
4. ✅ Build success
5. ✅ Unit tests (coverage ≥65%)
6. ✅ E2E tests (all 3 browsers)
7. ✅ Sync verification (Web=DOCX=PDF=Excel)
8. ✅ Security audit (moderate level)

**Deployment Conditions:**
- Only on `main` branch
- Only on `push` events (not PR)
- Only after all quality gates pass

---

## Part 4: Agent Skill Implementation Guide

### Skill Categories for Master Agent

#### 1. Infrastructure Skills (4)
```python
# @dependency-resolver
- Dependencies: pnpm, pip
- Input: --frozen-lockfile flag
- Output: installed packages, verified versions
- Validation: lockfile matches, all deps resolvable

# @type-checker
- Dependencies: tsc, mypy
- Input: files pattern, --strict flag
- Output: error count, line references
- Validation: zero errors before proceeding

# @build-orchestrator
- Dependencies: Vite, Python build
- Input: NODE_ENV, target
- Output: dist/ folder, bundle size
- Validation: dist/ exists, no build errors

# @quality-gate-runner
- Dependencies: all other skills
- Input: test results, coverage, sync status
- Output: PASS/FAIL verdict
- Validation: all gates must pass
```

#### 2. Testing Skills (4)
```python
# @unit-test-runner
- Framework: Vitest + PyTest
- Input: test suite (web/backend), coverage flag
- Output: test results, coverage reports
- Validation: coverage ≥65%, all tests pass

# @e2e-test-runner
- Framework: Playwright
- Input: browser matrix (chromium/firefox/webkit)
- Output: test results, video recordings
- Validation: all tests pass on all browsers

# @coverage-analyzer
- Input: coverage reports from Vitest/PyTest
- Output: coverage percentage, threshold check
- Validation: enforce minimum coverage

# @test-aggregator
- Input: multiple test suites
- Output: consolidated report
- Validation: combine all results
```

#### 3. Document Generation Skills (5)
```python
# @docx-generator
- Library: python-docx
- Input: CVDataModel, output_path, style
- Output: .docx file (ATS-optimized)
- Validation: file size, structure integrity

# @pdf-generator
- Library: ReportLab
- Input: CVDataModel, colors, fonts
- Output: .pdf file (visual formatting)
- Validation: file size, text extraction

# @excel-generator
- Library: OpenPyXL
- Input: CVDataModel, sheets config
- Output: .xlsx file (multi-sheet)
- Validation: formulas, data integrity

# @sync-verifier
- Input: web_data, docx_path, pdf_path, excel_path
- Output: match status, diff report
- Validation: Web=DOCX=PDF=Excel (byte-level where possible)

# @cv-data-validator
- Model: Pydantic CVDataModel
- Input: JSON CV data
- Output: validated object or errors
- Validation: all fields match schema
```

#### 4. Deployment Skills (4)
```python
# @git-branch-creator
- Input: branch_name, base_branch
- Output: git command, branch created
- Validation: branch exists remotely

# @git-workflow-manager
- Input: commit message, files
- Output: commit hash, push result
- Validation: push successful, remote updated

# @github-pages-deployer
- Input: build_path, branch
- Output: deployment status
- Validation: live site responds HTTP 200

# @release-orchestrator
- Input: version, changelog
- Output: release assets
- Validation: all deployment gates passed
```

#### 5. Portfolio Management Skills (4)
```python
# @portfolio-updater
- Input: project data (name, desc, tech, link)
- Output: updated portfolio
- Validation: project structure correct

# @skills-manager
- Input: category, skills list
- Output: updated skills in CV
- Validation: matches defined categories

# @certificate-manager
- Input: certificate data (title, issuer, date)
- Output: updated certs list
- Validation: data format correct

# @experience-tracker
- Input: job data (company, role, period)
- Output: updated experience
- Validation: chronological order, dates valid
```

#### 6. Code Quality Skills (3)
```python
# @code-formatter
- Tool: Prettier + Black
- Input: files glob, parser
- Output: formatted files
- Validation: no formatting changes needed

# @linter-checker
- Tool: ESLint + Flake8
- Input: extensions, max-warnings
- Output: linting report
- Validation: zero critical/error level

# @performance-monitor
- Input: build artifacts, test results
- Output: metrics (bundle size, build time)
- Validation: threshold comparison
```

#### 7. Backend Skills (3)
```python
# @backend-server
- Framework: FastAPI with Uvicorn
- Input: host, port, reload
- Output: server running
- Validation: health check 200

# @backend-test-runner
- Input: test patterns, markers
- Output: test results
- Validation: all tests pass

# @api-validator
- Input: API routes, sample requests
- Output: validation report
- Validation: responses match schemas
```

---

## Part 5: Portability & Execution Infrastructure (CRITICAL)

### 🌍 Portability Requirements

To guarantee the agent works on any developer's machine (Windows/Linux/Mac) and any IDE (VS Code/Cursor/IntelliJ), the following infrastructure requirements are **NON-NEGOTIABLE**:

### Requirement 1: Unified Environment Manager with `uv`

**Problem:** If Python version is not pinned, the agent fails when another dev has Python 3.9 while the code requires 3.12.

**Solution:** Use `uv` as the exclusive package manager for the agent layer.

**Implementation:**
```toml
# agent/pyproject.toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mportafolio-agent"
version = "0.1.0"
description = "Master orchestrator agent for Mi Portafolio"
requires-python = ">=3.11,<3.13"

[project.dependencies]
typer = "^0.12.0"
pydantic = "^2.0"
python-dotenv = "^1.0"
pytest = "^7.4"
playwright = "^1.40"
# ... other dependencies

[project.optional-dependencies]
dev = [
  "pytest-cov",
  "black",
  "ruff",
  "mypy"
]

[tool.uv]
python = "3.12"  # Exact version managed by uv
```

**Bootstrap Script in `agent/README.md`:**
```bash
# First time setup
cd agent
uv sync  # Downloads Python 3.12 if not installed, installs all deps

# Run agent
uv run python -m 1_interface.cli --help
```

### Requirement 2: Automatic MCP Configuration (.mcp.json)

**Problem:** When cloning the repo, IDEs don't know how to invoke the MCP server. Also, the developer may already have `.mcp.json` with other MCPs configured.

**Solution:** Integrate portfolio-agent into existing `.mcp.json` (non-destructive merge, not replacement).

**File:** `.mcp.json` (in repo root, alongside `.github/`)

**IMPORTANT - Integration Strategy:**
- ✅ If `.mcp.json` doesn't exist: Create new file with portfolio-agent
- ✅ If `.mcp.json` exists: **MERGE** portfolio-agent config WITHOUT removing existing MCPs
- ✅ Use `scripts/merge_mcp_config.py` to automate safe merging

**Portfolio Agent MCP Configuration Block:**
```json
{
  "mcpServers": {
    "portfolio-agent": {
      "command": "uv",
      "args": ["--directory", "agent", "run", "python", "-m", "1_interface.mcp_server"],
      "disabled": false,
      "autoStart": true,
      "env": {
        "PYTHONPATH": "${workspaceFolder}/agent"
      }
    }
  }
}
```

**Example: Integration into Existing .mcp.json**
```json
{
  "mcpServers": {
    "claude-tools": {
      "command": "npx",
      "args": ["@anthropic-ai/claude-tools"],
      "disabled": false
    },
    "github": {
      "command": "npx",
      "args": ["@github/mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "${env:GITHUB_TOKEN}"
      }
    },
    "portfolio-agent": {
      "command": "uv",
      "args": ["--directory", "agent", "run", "python", "-m", "1_interface.mcp_server"],
      "disabled": false,
      "autoStart": true,
      "env": {
        "PYTHONPATH": "${workspaceFolder}/agent"
      }
    }
  }
}
```

**Merge Script: `scripts/merge_mcp_config.py`**
```python
#!/usr/bin/env python3
"""
Safely merge portfolio-agent into existing .mcp.json
Non-destructive merge: preserves existing MCPs, adds/updates portfolio-agent
"""
import json
from pathlib import Path
from typing import Dict, Any

def merge_mcp_config():
    """Merge portfolio-agent config into .mcp.json"""
    
    mcp_path = Path.cwd() / ".mcp.json"
    
    # Portfolio agent configuration
    portfolio_mcp = {
        "command": "uv",
        "args": ["--directory", "agent", "run", "python", "-m", "1_interface.mcp_server"],
        "disabled": False,
        "autoStart": True,
        "env": {
            "PYTHONPATH": "${workspaceFolder}/agent"
        }
    }
    
    # Load existing config or create new
    if mcp_path.exists():
        with open(mcp_path) as f:
            config = json.load(f)
        action = "merged"
    else:
        config = {"mcpServers": {}}
        action = "created"
    
    # Ensure mcpServers exists
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    # Merge portfolio-agent (preserve existing MCPs)
    old_portfolio = config["mcpServers"].get("portfolio-agent")
    config["mcpServers"]["portfolio-agent"] = portfolio_mcp
    
    # Write back
    with open(mcp_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ .mcp.json {action} successfully")
    if old_portfolio:
        print("   📝 portfolio-agent config updated")
    else:
        print("   ✨ portfolio-agent config added")
    print(f"   📦 Existing MCPs preserved: {list(config['mcpServers'].keys())}")

if __name__ == "__main__":
    merge_mcp_config()
```

**Run on setup:**
```bash
cd agent/..  # repo root
python scripts/merge_mcp_config.py
```

**IDE Support:**
- **Cursor:** Automatically detects and reloads `.mcp.json`
- **Claude Code:** Native `.mcp.json` support with hot reload
- **VS Code:** Via MCP extension (MCP Inspector)
- **IntelliJ:** Via MCP plugin with config validation

### Requirement 3: OS-Agnostic Subprocess & Path Handling

**Problem:** Skills that call `npm run test` or `pytest` fail on Windows if programmed for Unix.

**Solution:** Use `subprocess.run()` + `pathlib.Path` + `shutil.which()` pattern.

**Pattern for All Skills:**
```python
# agent/4_skills/infrastructure/type_checker.py
from pathlib import Path
from typing import List
import subprocess
import shutil
from pydantic import BaseModel, Field

class TypeCheckRequest(BaseModel):
    """Validated input for type checking"""
    files: List[str] = Field(..., description="Files to check")
    strict_mode: bool = Field(default=True)
    exclude_dirs: List[str] = Field(default_factory=lambda: ["node_modules", ".venv", "dist"])

class TypeCheckResult(BaseModel):
    """Type check output"""
    success: bool
    error_count: int
    errors: List[str]
    duration_seconds: float

class TypeChecker:
    """Type checking skill - cross-platform compatible"""
    
    async def execute(self, request: TypeCheckRequest) -> TypeCheckResult:
        """
        Execute type checking with OS-agnostic subprocess handling
        """
        start_time = time()
        
        # WINDOWS + LINUX/MAC COMPATIBLE
        # 1. Find TypeScript compiler using shutil.which()
        tsc_path = shutil.which("tsc")
        if not tsc_path:
            raise RuntimeError("TypeScript compiler (tsc) not found in PATH")
        
        # 2. Build command with pathlib.Path
        workspace_root = Path(os.getcwd())
        files_to_check = [str(workspace_root / f) for f in request.files]
        
        # 3. Execute with subprocess.run() (no os.system, no shell=True)
        cmd = [
            tsc_path,
            "--noEmit",
            "--strict" if request.strict_mode else "",
            "--skipLibCheck",
            *files_to_check
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(workspace_root),
                timeout=30
            )
            
            errors = result.stderr.strip().split('\n') if result.stderr else []
            return TypeCheckResult(
                success=result.returncode == 0,
                error_count=len([e for e in errors if e.strip()]),
                errors=errors,
                duration_seconds=time() - start_time
            )
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("Type checking timed out after 30 seconds")
```

**OS-Agnostic Patterns for All Skills:**

| Pattern | Why | Usage |
|---------|-----|-------|
| `shutil.which("tsc")` | Finds executable in PATH on Windows/Unix | Finding CLI tools |
| `pathlib.Path(...)` | Handles Windows `\` and Unix `/` automatically | File operations |
| `subprocess.run(cmd, ...)` | Platform-neutral process execution | Running npm, pytest, etc |
| `os.linesep` instead of `\n` | Use OS-correct line separator | Log output |
| `tempfile.TemporaryDirectory()` | Platform-neutral temp files | Artifact handling |

**❌ FORBIDDEN Patterns:**
```python
# These will FAIL on Windows or Linux
os.system("npm run test")              # ❌ Shell-dependent
"C:\\path\\file.txt"                   # ❌ Hardcoded Windows path
subprocess.run("npm test", shell=True) # ❌ Shell injection risk
```

**✅ REQUIRED Patterns:**
```python
# These work on ALL platforms
subprocess.run(["npm", "run", "test"], capture_output=True)
Path("apps/web/src") / "index.ts"
shutil.which("npm")
```

### Requirement 4: Environment Template & Validation

**File:** `agent/.env.example`
```bash
# Environment variables required by the Master Agent

# LLM Configuration (choose one provider)
OPENAI_API_KEY=sk-proj-...
# ANTHROPIC_API_KEY=sk-ant-...
# OLLAMA_BASE_URL=http://localhost:11434

# GitHub Integration
GITHUB_TOKEN=ghp_...
GITHUB_REPO=Harp-Andres/MiPortafolio

# Local Development
LOG_LEVEL=INFO
DEBUG_MODE=false

# CI/CD Configuration
CI_ENVIRONMENT=development  # or: staging, production
DEPLOY_BRANCH=main
```

**Validation in Guardrails Layer:**
```python
# agent/5_guardrails/env_validator.py
from pathlib import Path
from typing import List
import os
from dotenv import load_dotenv

class EnvironmentValidator:
    """Validates .env file exists and contains required keys"""
    
    REQUIRED_KEYS = {
        "GITHUB_TOKEN": "GitHub API token for repository operations",
        "GITHUB_REPO": "Repository in format owner/repo",
    }
    
    OPTIONAL_KEYS = {
        "OPENAI_API_KEY": "OpenAI API key (required if using GPT)",
        "ANTHROPIC_API_KEY": "Anthropic API key (required if using Claude)",
        "OLLAMA_BASE_URL": "Local Ollama URL (for local LLM)",
        "LOG_LEVEL": "Logging level (INFO, DEBUG, ERROR)",
    }
    
    @staticmethod
    def validate() -> bool:
        """
        Validates environment configuration on agent startup
        
        Returns: True if valid
        Raises: EnvironmentConfigError if invalid
        """
        agent_dir = Path(__file__).parent.parent
        env_file = agent_dir / ".env"
        env_example = agent_dir / ".env.example"
        
        # Check if .env exists
        if not env_file.exists():
            example_path = env_example.relative_to(Path.cwd())
            raise EnvironmentConfigError(
                f"❌ Missing .env file\n"
                f"   Copy template: cp {example_path} {env_file.relative_to(Path.cwd())}\n"
                f"   Edit: {env_file} and add your API keys"
            )
        
        # Load environment
        load_dotenv(env_file)
        
        # Check required keys
        missing_required = []
        for key, description in EnvironmentValidator.REQUIRED_KEYS.items():
            if not os.getenv(key):
                missing_required.append(f"  • {key}: {description}")
        
        if missing_required:
            raise EnvironmentConfigError(
                f"❌ Missing required environment variables:\n" + 
                "\n".join(missing_required) +
                f"\n   Edit {env_file} and add missing keys"
            )
        
        # Check at least one LLM provider is configured
        llm_providers = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "OLLAMA_BASE_URL"]
        if not any(os.getenv(p) for p in llm_providers):
            raise EnvironmentConfigError(
                f"❌ No LLM provider configured\n"
                f"   Add ONE of: {', '.join(llm_providers)}\n"
                f"   Edit {env_file} and add your LLM credentials"
            )
        
        return True

class EnvironmentConfigError(Exception):
    """Raised when environment configuration is invalid"""
    pass
```

**MCP Server Startup Validation:**
```python
# agent/1_interface/mcp_server.py
from pathlib import Path
from 5_guardrails.env_validator import EnvironmentValidator, EnvironmentConfigError
import sys

async def main():
    """MCP server startup"""
    try:
        # Validate environment on startup
        EnvironmentValidator.validate()
        print("✅ Environment validated", file=sys.stderr)
        
        # ... start server
        
    except EnvironmentConfigError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
```

**CLI Startup Validation:**
```python
# agent/1_interface/cli.py
import typer
from 5_guardrails.env_validator import EnvironmentValidator, EnvironmentConfigError

app = typer.Typer()

@app.callback()
def startup():
    """Validate environment before any command"""
    try:
        EnvironmentValidator.validate()
    except EnvironmentConfigError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)

@app.command()
def ci():
    """Run CI pipeline"""
    # ... implementation
    pass
```

---

## Part 5.5: Portability Checklist for Phase 4B Implementation

Before implementing each skill in `4_skills/`, verify:

- [ ] **Imports:** `from pathlib import Path`, `import subprocess`, `import shutil`
- [ ] **Path handling:** All paths use `Path(...)`, no hardcoded separators
- [ ] **Subprocess:** All exec uses `subprocess.run([cmd, args], ...)`, never `os.system()`
- [ ] **CLI tools:** Find executables with `shutil.which("tool_name")`
- [ ] **Error output:** Capture `stderr` via `subprocess.run(..., capture_output=True)`
- [ ] **Line separators:** Use `os.linesep` in output, not `\n`
- [ ] **Temp files:** Use `tempfile.TemporaryDirectory()` for cross-platform temp handling
- [ ] **Logging:** Use structured logging (not print statements)

---

## Part 6: Implementation Roadmap

**Status:** DONE
- [x] Analyzed deployment strategy
- [x] Extracted 12 transversal functionalities
- [x] Extracted 12 business logic skills
- [x] Mapped 28+ tools to agent skills
- [x] Designed complete 10-stage pipeline
- [x] Documented quality gates and deployment automation

### Phase 4B: Agent Skill Implementation (📋 PENDING)

**PREREQUISITE: Portability Infrastructure Setup** (1-2 hours)

Before implementing skills, set up the execution infrastructure:

1. **Create `agent/pyproject.toml`** with `uv` configuration
   - Pin Python version: `3.12`
   - Define all dependencies (typer, pydantic, pytest, playwright, etc)
   - Configure build system for `uv` exclusively

2. **Create `.mcp.json`** in repo root for IDE auto-detection
   - Enable Cursor/Claude Code/VS Code to auto-discover MCP server
   - Point to `uv run python -m 1_interface.mcp_server`

3. **Create `agent/.env.example`** template
   - Define all required keys (GITHUB_TOKEN, LLM provider keys)
   - Document each variable with description

4. **Create `agent/5_guardrails/env_validator.py`**
   - Validate `.env` exists on startup
   - Check required keys present
   - Provide friendly error messages

5. **Create bootstrap script** in `agent/README.md`
   ```bash
   cd agent
   uv sync  # One-command setup
   ```

**Task 1: Create Skills Layer** (2-3 hours)
```
Create directory: agent/4_skills/
├── infrastructure/
│   ├── dependency_resolver.py
│   ├── type_checker.py
│   ├── build_orchestrator.py
│   └── quality_gate_runner.py
├── testing/
│   ├── unit_test_runner.py
│   ├── e2e_test_runner.py
│   ├── coverage_analyzer.py
│   └── test_aggregator.py
├── documents/
│   ├── docx_generator.py
│   ├── pdf_generator.py
│   ├── excel_generator.py
│   ├── sync_verifier.py
│   └── cv_data_validator.py
├── deployment/
│   ├── git_branch_creator.py
│   ├── git_workflow_manager.py
│   ├── github_pages_deployer.py
│   └── release_orchestrator.py
├── portfolio/
│   ├── portfolio_updater.py
│   ├── skills_manager.py
│   ├── certificate_manager.py
│   └── experience_tracker.py
├── quality/
│   ├── code_formatter.py
│   ├── linter_checker.py
│   └── performance_monitor.py
└── backend/
    ├── backend_server.py
    ├── backend_test_runner.py
    └── api_validator.py
```

**Task 2: Implement Skills Layer** (3-4 hours)
- Implement each skill class with execute() method
- Add parameter validation (Pydantic models)
- Implement error handling and retry logic
- Add logging and telemetry hooks
- Create integration tests for each skill

**Task 3: Create Orchestrator** (2-3 hours)
- Implement ReAct engine for skill sequencing
- Create workflow templates (CI/CD, deployment, portfolio update)
- Implement dependency resolution between skills
- Add state machine for workflow progress tracking

**Task 4: Create Memory System** (1-2 hours)
- Implement conversation history storage
- Create repo RAG indexer for codebase understanding
- Add checkpoint management for state persistence

**Task 5: Create Guardrails** (1-2 hours)
- Implement Pydantic validation for all skill inputs
- Add security filters (command injection prevention)
- Implement rate limiting and quota management

**Task 6: Create Interfaces** (2-3 hours)
- Implement CLI via Typer with subcommands:
  ```bash
  agent ci           # Run CI pipeline
  agent deploy       # Deploy to production
  agent portfolio    # Manage portfolio
  agent test         # Run test suite
  ```
- Implement MCP server for IDE integration
- Create webhook handlers for GitHub events

### Phase 4C: Agent Restructuring (📋 PENDING)

**Target Directory Structure:**
```
agent/
├── pyproject.toml                 # Poetry/uv dependencies
├── 1_interface/                   # CLI + MCP server
│   ├── cli.py                    # Typer CLI
│   ├── mcp_server.py            # MCP protocol
│   └── handlers.py              # Request handlers
├── 2_orchestrator/               # ReAct engine
│   ├── react_engine.py          # Core orchestration
│   ├── lm_factory.py            # LLM factory
│   ├── prompts.py               # Agent prompts
│   └── workflows/               # Workflow templates
│       ├── cicd_workflow.py
│       ├── deployment_workflow.py
│       └── portfolio_workflow.py
├── 3_memory/                     # Conversation + RAG
│   ├── conversation.py          # History storage
│   ├── rag_indexer.py           # Codebase indexing
│   └── checkpoint.py            # State persistence
├── 4_skills/                     # All 28 skills
│   ├── infrastructure/
│   ├── testing/
│   ├── documents/
│   ├── deployment/
│   ├── portfolio/
│   ├── quality/
│   └── backend/
├── 5_guardrails/                 # Validation + Security
│   ├── validators.py            # Pydantic validators
│   ├── security_filters.py      # Injection prevention
│   └── rate_limiter.py          # Quota management
├── 6_telemetry/                  # Logging
│   ├── logger.py               # Structured logging
│   ├── metrics.py              # Performance metrics
│   └── tracer.py               # Distributed tracing
└── 7_state/                      # Checkpoint management
    ├── state_manager.py         # State persistence
    ├── models.py                # State models
    └── repository.py            # State storage
```

---

## Part 6: Execution Sequence

### Week 1: Phase 4B Implementation
- **Day 1-2:** Create skills layer (28 skills with stubs)
- **Day 2-3:** Implement core skills (dependency resolver, type checker, test runners)
- **Day 3:** Implement document generation skills
- **Day 4:** Implement deployment skills
- **Day 5:** Create orchestrator + interfaces

### Week 2: Phase 4C Restructuring
- **Day 1:** Restructure agent to 7-layer architecture
- **Day 2:** Implement ReAct engine
- **Day 3:** Create CLI and MCP server
- **Day 4:** Add memory and checkpoint systems
- **Day 5:** Testing and validation

### Deliverables

**Phase 4A (Complete):**
- ✅ CI/CD pipeline definition
- ✅ 28+ skills mapped from CI/CD
- ✅ Quality gates specification
- ✅ Deployment automation plan

**Phase 4B (Pending):**
- 📋 Skills implementation (28 files)
- 📋 Orchestrator engine
- 📋 Memory and checkpoint systems
- 📋 Guardrails and validation

**Phase 4C (Pending):**
- 📋 7-layer directory structure
- 📋 CLI interface (Typer)
- 📋 MCP server for IDE integration
- 📋 Complete portable agent core

---

## Part 7: Success Criteria

### Quality Metrics
- ✅ 28+ skills implemented and tested
- ✅ 65%+ code coverage on skills layer
- ✅ All CI/CD gates passing automatically
- ✅ Sync verification 100% consistency
- ✅ E2E tests passing on all 3 browsers
- ✅ Zero TypeScript/Python type errors
- ✅ Deployment automated and verified

### Capability Metrics
- ✅ Agent can autonomously run full CI/CD pipeline
- ✅ Agent can generate and sync all document formats
- ✅ Agent can manage portfolio updates
- ✅ Agent can orchestrate releases
- ✅ Agent can manage git workflows
- ✅ Agent available via CLI and MCP

### Business Metrics
- ✅ Deployment time reduced to <5 minutes
- ✅ Manual QA effort reduced to <10%
- ✅ Document synchronization 100% accurate
- ✅ Portfolio update cycle <30 minutes

---

## Part 8: Notes for Phase Implementation

### Critical Dependencies
1. **Phase 4B must complete before Phase 4C** - Skills are needed for orchestrator
2. **All 28 skills must have consistent interface** - For orchestrator to chain them
3. **Memory system critical for agent learning** - Must track workflow results
4. **Guardrails must prevent dangerous operations** - Security is non-negotiable

### Integration Points
- Skills use `@dependency-resolver` before any command
- Orchestrator uses `@quality-gate-runner` as final validation
- Memory system must track all skill executions
- Telemetry must log performance metrics

### Testing Strategy
- Unit tests: Each skill independently (28 test files)
- Integration tests: Skill combinations (workflows)
- E2E tests: Full CI/CD pipeline via agent
- Security tests: Guardrails prevent injection

### Deployment Strategy
- Deploy skills layer → orchestrator → interfaces
- CLI testing before MCP server deployment
- Gradual rollout: local → CI/CD → production

---

## 📊 Summary Statistics

| Category | Count | Hours |
|----------|-------|-------|
| Transversal Functionalities | 12 | - |
| Business Logic Skills | 12 | - |
| Total Skills to Implement | 28 | 15-20 |
| CI/CD Pipeline Stages | 10 | - |
| Quality Gates | 8 | - |
| Agent Architecture Layers | 7 | - |
| Implementation Weeks | 2 | 40-50 |

---

**Next Step:** Begin Phase 4B - Skills Layer Implementation

When ready, user will request: `"IMPLEMENTA LAS NUEVAS FUNCIONALIDADES AL AGENTE"`
