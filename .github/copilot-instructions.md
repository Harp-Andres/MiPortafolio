# GitHub Copilot - Portfolio Agent Instructions

## 🗣️ Idioma de comunicación

Responde siempre en **español** en el chat, salvo que el usuario escriba explícitamente en otro idioma.

Todo lo relacionado con **programación** (código fuente en cualquier lenguaje, nombres de variables/funciones/clases, comentarios dentro del código, mensajes de commit y nombres de branches) se mantiene siempre en **inglés**, como estándar de la industria.

## 🎼 Maestro Agent System

This repository uses the **Maestro Agent** — a 7-layer Python agent system exposed via MCP.
Invoke skills directly using the MCP tools registered in `.mcp.json`.

## 🧠 Master delegation & skill auto-creation (always active, any mode)

Regardless of which chat mode is selected, behave as the master orchestrator described in `.github/agents/agent-master-portfolio.agent.md`:

1. **Delegate by domain.** Before acting, check if the task matches one of the specialized agents in `.github/agents/*.agent.md` (CV/docs, testing, deployment, CI/CD, architecture, SDET, platform, OS, setup). If it does, follow that agent's description/responsibilities as if you were it.
2. **Reuse before creating.** Before writing new logic, check `.github/instructions/*.instructions.md` for an existing generic "skill" covering this domain and apply it.
3. **Skills belong to their owning specialist.** A skill under `.github/skills/*/SKILL.md` is owned by whichever specialized agent declares it (see that agent's `.agent.md`). When acting as the master/orchestrator, delegate to that specialist instead of invoking the skill directly yourself. Only use a skill directly if no specialist owns that domain.
4. **Auto-create reusable skills.** If you complete a multi-step task that is costly (≥3 tool calls or likely to repeat) and is not yet covered by an existing instructions/prompt file, propose creating one:
   - Domain-scoped conventions that should apply automatically whenever matching files are edited → new file in `.github/instructions/<topic>.instructions.md` with an `applyTo` glob (see existing ones for the pattern).
   - On-demand multi-step workflows invoked by name → new file in `.github/prompts/<name>.prompt.md`.
   - Never duplicate this logic into `agent/` (the Python Maestro MCP server) unless explicitly asked — that layer is a separate system, currently not wired into Copilot Chat.
5. **Keep it portable.** Prefer `AGENTS.md`-style plain instructions over VS Code-only mechanisms when possible, since other tools (e.g. Claude Code) may read this repo later.

---

## 🏗️ Architecture

```
agent/
├── 1_interface/   CLI (Typer) + MCP Server (exposes 28 skills to IDEs)
├── 2_orchestrator/ ReAct engine + LLM factory + workflow templates
├── 3_memory/      Conversation history + RAG indexer + checkpoints
├── 4_skills/      28 autonomous skills across 6 domains
├── 5_guardrails/  Pydantic validation + security filters + rate limiter
├── 6_telemetry/   Structured logging + metrics + tracing
└── 7_state/       Execution state + persistence + recovery

apps/
├── web/           React + TypeScript + Tailwind + Vite + Playwright
└── api/           FastAPI (Python) + Pytest

packages/          Shared code (core, ui, api-client, config)
```

---

## 🧹 Project structure hygiene (enforced)

- Never commit runtime artifacts: logs (`*.log`, `*.err`), `output.txt`, `summary.txt`, coverage/, dist/, playwright-report/, test-results/, `.venv/`, `.state/`, `.checkpoints/`. These must stay gitignored.
- Reusable setup/verification/maintenance scripts belong in `scripts/` (see `scripts/README.md`), never loose at the repo root. Repo-root `.ps1`/`.sh` files are only acceptable if they are one-off, throwaway, and never committed.
- The `agent/` root only holds package metadata (`pyproject.toml`, `uv.lock`, `README.md`, `__init__.py`, `.env.example`) and the bootstrap/setup CLI entry points (`setup_agent.py`, `setup_bootstrap_cli.py`, `phase2_setup_agent.py`). All runtime logic lives inside the numbered layer folders (`1_interface/` … `7_state/`).
- **Never create markdown documentation directly at the repo root.** Follow `docs/DOCUMENTATION_GUIDE.md`:
  - End-user/external docs → `docs/` (e.g. `docs/QUICK_START.md`, `docs/SETUP.md`, `docs/MAESTRO_REFERENCE.md`).
  - Internal analysis, session summaries, phase reports → `.dev-docs/` (e.g. `.dev-docs/architecture/`, `.dev-docs/sessions/`).
  - Agent/skill configuration → `.agent/` (only files with agent/skill frontmatter, not prose reports).
  - The only markdown allowed at repo root is `README.md` and a short `QUICK_START.md` stub that links to `docs/QUICK_START.md`.
- Before finishing a task that adds new top-level files, verify they match this structure. If a new file doesn't fit an existing layer/folder, ask where it should go instead of defaulting to the repo root.
- When moving/renaming a doc, grep the repo for old references (other docs, scripts, `.github/agents/*.agent.md`) and update them so links don't break.

---

## 🚀 Workflows (via MCP or CLI)

| Workflow | What it does | Command |
|----------|-------------|---------|
| `ci` | Lint → Type-check → Build → Unit Tests | `agent ci` |
| `test` | Unit + E2E + Coverage report | `agent test` |
| `deploy` | Build → Quality gate → GitHub Pages | `agent deploy` |
| `portfolio-update` | PDF + DOCX + Excel from CV data | `agent docs` |
| `quality` | Ruff + ESLint + mypy + type coverage | `agent ci --quality-only` |
| `full-pipeline` | All 28 skills end-to-end | `@maestro workflow: full-pipeline` |

---

## 🔧 CLI Commands

```bash
# Install and run agent
cd agent
uv run python -m 1_interface.cli --help

# Run workflows
uv run python -m 1_interface.cli ci
uv run python -m 1_interface.cli test
uv run python -m 1_interface.cli deploy
uv run python -m 1_interface.cli docs

# Web frontend (apps/web/)
pnpm --filter web dev
pnpm --filter web test
pnpm --filter web build

# API backend (apps/api/)
cd apps/api && uv run pytest
cd apps/api && uv run python run.py
```

---

## 📋 Code Conventions

### Python (agent/, apps/api/, packages/backend/)
- **Version**: Python 3.11–3.12
- **Package manager**: `uv` (NOT pip, NOT poetry)
- **Framework**: Typer (CLI), FastAPI (API), Pydantic v2 (validation)
- **Testing**: pytest + pytest-asyncio
- **Linting**: ruff (linter + formatter)
- **Typing**: Full type hints required. Use `Optional[T]` not `T | None`
- **Path handling**: Always use `pathlib.Path`, never string concatenation
- **Logging**: Use `from agent.config.constants import get_logger`, NOT `logging.getLogger`
- **Skills**: All new skills MUST inherit from `agent.4_skills.base_skill.BaseSkill`
- **Guardrails**: Any subprocess execution MUST go through `BaseSkill.run_command()`

### TypeScript (apps/web/, packages/)
- **Version**: TypeScript 5.x strict mode
- **Package manager**: `pnpm` (NOT npm, NOT yarn)
- **Framework**: React 19 + Vite + Tailwind CSS
- **Testing**: Vitest (unit) + Playwright (E2E)
- **Linting**: ESLint + Prettier (config in `packages/config/`)
- **Components**: Functional components only, no class components
- **State**: useState/useReducer for local, context for shared
- **Imports**: Use absolute paths with `@/` prefix (configured in tsconfig)

---

## 🛡️ Security Rules (NEVER violate these)

1. **NEVER** run shell commands directly — always use `BaseSkill.run_command()` (Pydantic-validated)
2. **NEVER** commit secrets — use env vars from `.env` (local) or GitHub Secrets (CI/CD)
3. **NEVER** modify `.github/workflows/` without running tests first
4. **NEVER** push to `main` directly — always use PRs with passing CI
5. **NEVER** skip `skill_validators.py` for user-provided input

---

## 🎯 Agent Hierarchy

```
@maestro (agent-master-portfolio)
├── portfolio-cv-manager       → documents/ skills
├── portfolio-test-manager     → testing/ skills
├── portfolio-deployment-manager → deployment/ skills
├── github-cicd-manager        → infrastructure/ + quality/ skills
├── setup-portability-manager  → setup/bootstrapping + MCP validation
├── devops-cicd-manager        → CI/CD engineering and release governance
├── software-architecture-manager → architecture and ADR governance
├── sdet-quality-manager       → web/api/mobile test strategy
├── platform-architecture-manager → Docker/K8s runtime architecture
└── os-platform-manager        → Linux/Windows environment parity
```

---

## 🧩 Custom Prompts & Local Knowledge

Prompt files for specialist behaviors are stored in `.github/prompts/`:
- `devops.prompt.md`
- `architect.prompt.md`
- `sdet.prompt.md`
- `platform.prompt.md`
- `sysops.prompt.md`
- `self-heal-loop.prompt.md`

Workspace grounding context for local indexing/RAG is stored in `.github/agents/context/`:
- `monorepo-map.md`
- `api-contracts.md`
- `testing-matrix.md`
- `platform-topology.md`
- `os-compatibility.md`
- `compliance-matrix.md`

Before major changes, consult these context files first to reduce hallucinations and enforce architecture consistency.

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `.mcp.json` | MCP server config for all IDEs (VS Code, Cursor, Claude, IntelliJ) |
| `.github/agents/*.agent.md` | Custom Agents: master + 10 specialized agent definitions (workspace-scoped, auto-appear in the agent picker) |
| `.github/instructions/*.instructions.md` | Generic per-role skills, auto-applied by `applyTo` glob |
| `.github/prompts/*.prompt.md` | On-demand multi-step workflows, invoked via `/name` |
| `agent/4_skills/base_skill.py` | Abstract base for all 28 skills |
| `agent/4_skills/skill_registry.py` | Skill discovery and registry |
| `agent/4_skills/skill_routing.py` | Routes tasks to correct agent/skill |
| `agent/1_interface/mcp_server.py` | MCP server (IDE connector) |
| `agent/1_interface/handlers.py` | All workflow handlers |

---

## 🔁 Feedback Loop (Self-Correction)

When a skill fails:
1. `SkillResult.success=False` is returned with `errors[]` list
2. `3_memory/checkpoint.py` captures the error state
3. `7_state/state_manager.py` persists for retry
4. The error is re-injected to Copilot as structured context
5. Copilot proposes a fix using the structured error output

**Always return structured `SkillResult` — never raw strings or exceptions.**

---

## 🧪 Testing Protocol

Before any PR:
```bash
# Backend tests
cd agent && uv run pytest tests/ -v

# Frontend unit tests
cd apps/web && pnpm test

# E2E tests
cd apps/web && pnpm playwright test

# Full quality gate
cd agent && uv run python -m 1_interface.cli ci
```

---

## 💡 Common 1-line Prompts

```
"Agente: ejecuta el pipeline completo y repara si falla"
"@maestro workflow: ci"
"@maestro workflow: deploy"
"Skill: run E2E tests on chromium only"
"@maestro workflow: portfolio-update"
```
