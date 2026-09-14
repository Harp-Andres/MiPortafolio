# 🤖 Mi Portafolio Master Agent

Autonomous AI agent for CV/Portfolio management, CI/CD orchestration, and document generation.

**Architecture:** 7-layer portable core with CLI + MCP server interfaces.

**Status:** Phase 4B - Skills Implementation (In Progress)

---

## ⚡ Quick Start (One-Command Setup)

### Prerequisites
- **Python:** 3.11+ (but `uv` handles this automatically)
- **Git:** For version control operations
- **Node.js:** 20.x (for web builds and frontend tools)
- **pnpm:** For monorepo package management

### Setup

```bash
# 1. Navigate to agent directory
cd agent

# 2. One-command setup (uv handles Python version + dependencies)
uv sync

# 3. Copy environment template
cp .env.example .env

# 4. Edit .env with your API keys
# Add at minimum:
#   - GITHUB_TOKEN (for git operations)
#   - OPENAI_API_KEY or ANTHROPIC_API_KEY (for LLM)
nano .env  # or your preferred editor

# 5. Merge MCP configuration (integrates with your IDE)
uv run python ../scripts/merge_mcp_config.py

# 6. Verify setup
uv run python -m 1_interface.cli --help
```

**That's it!** The agent is now ready to use.

---

## 🏗️ Architecture Overview

### 7-Layer Portable Core

```
1_interface/       CLI (Typer) + MCP server for IDE integration
2_orchestrator/    ReAct engine, LLM factory, workflow templates
3_memory/          Conversation history, repo RAG indexer, checkpoints
4_skills/          28+ autonomous skills (CI/CD, document gen, portfolio management)
5_guardrails/      Input validation, security filters, rate limiting
6_telemetry/       Structured logging, metrics, distributed tracing
7_state/           Checkpoint management, state persistence
```

### Execution Flow

```
IDE / Terminal
    ↓
1_interface (CLI or MCP)
    ↓
5_guardrails (Validate input, check .env)
    ↓
3_memory (Load conversation history, repo context)
    ↓
2_orchestrator (ReAct: Reason → Act → Observe → Plan)
    ↓
4_skills (Execute autonomous operations)
    ↓
6_telemetry (Log execution, capture metrics)
    ↓
7_state (Save progress, create checkpoints)
```

---

## 🚀 Usage

### Via CLI

```bash
# Activate environment
cd agent

# Run CI pipeline
uv run mportafolio-agent ci

# Deploy to production
uv run mportafolio-agent deploy

# Manage portfolio
uv run mportafolio-agent portfolio add-project --name "MyProject" --tech "React,TypeScript"

# Generate documents
uv run mportafolio-agent documents generate --format all

# Run tests
uv run mportafolio-agent test --suite all

# View help
uv run mportafolio-agent --help
```

### Via MCP (IDE Integration)

After running merge_mcp_config.py:

**In Cursor/Claude Code/VS Code MCP:**
```
@portfolio-agent ci
@portfolio-agent deploy
@portfolio-agent portfolio add-project --name "MyProject" --tech "React"
```

---

## 📋 Configuration

### Required Files

| File | Purpose | Example |
|------|---------|---------|
| `.env` | API keys and settings | Copy from `.env.example`, add your keys |
| `pyproject.toml` | Dependencies and Python version | Managed by uv (3.12 pinned) |
| `.mcp.json` (repo root) | IDE MCP integration | Created by merge_mcp_config.py |

### Environment Variables

**CRITICAL (agent won't start without these):**
- `GITHUB_TOKEN` - GitHub PAT for git/deployment operations
- `GITHUB_REPO` - Repository in format: owner/repo

**REQUIRED (for LLM reasoning):**
- `OPENAI_API_KEY` OR `ANTHROPIC_API_KEY` OR `OLLAMA_BASE_URL`

**OPTIONAL:**
- `LOG_LEVEL` - DEBUG, INFO, WARNING, ERROR
- `DEBUG_MODE` - Enable detailed output
- `AGENT_MODEL` - LLM model name
- `TELEMETRY_ENABLED` - Send usage stats (opt-in)

See `.env.example` for full documentation.

---

## 🛠️ Development

### Running Tests

```bash
# All tests with coverage
uv run pytest --cov

# Specific test suite
uv run pytest tests/4_skills/infrastructure/ -v

# Watch mode (requires pytest-watch)
uv run pytest-watch
```

### Code Quality

```bash
# Type checking
uv run mypy 1_interface 2_orchestrator 4_skills

# Linting
uv run ruff check .

# Formatting
uv run black .
```

### Debugging

```bash
# Enable debug mode in .env
DEBUG_MODE=true

# Run with verbose logging
LOG_LEVEL=DEBUG uv run mportafolio-agent ci --verbose

# Debug specific skill
uv run python -c "from 4_skills.infrastructure.type_checker import TypeChecker; ..."
```

---

## 28 Skills Reference

### Infrastructure (4)
- `@dependency-resolver` - Install and resolve dependencies
- `@type-checker` - TypeScript + Python type validation
- `@build-orchestrator` - Build web + backend
- `@quality-gate-runner` - Enforce all quality gates

### Testing (4)
- `@unit-test-runner` - Vitest + PyTest execution
- `@e2e-test-runner` - Playwright multi-browser tests
- `@coverage-analyzer` - Coverage report generation
- `@test-aggregator` - Combine test results

### Document Generation (5)
- `@docx-generator` - Generate ATS-optimized Word docs
- `@pdf-generator` - Generate visual PDFs
- `@excel-generator` - Generate multi-sheet workbooks
- `@sync-verifier` - Verify Web=DOCX=PDF=Excel sync
- `@cv-data-validator` - Validate CV data structure

### Deployment (4)
- `@git-branch-creator` - Create feature branches
- `@git-workflow-manager` - Commit, push, PR automation
- `@github-pages-deployer` - Deploy to GitHub Pages
- `@release-orchestrator` - Full release pipeline

### Portfolio Management (4)
- `@portfolio-updater` - Add/modify projects
- `@skills-manager` - Manage skill categories
- `@certificate-manager` - Manage certificates
- `@experience-tracker` - Track work experience

### Code Quality (3)
- `@code-formatter` - Prettier + Black formatting
- `@linter-checker` - ESLint + Flake8 checking
- `@performance-monitor` - Build time/bundle size tracking

### Backend (3)
- `@backend-server` - Run FastAPI dev server
- `@backend-test-runner` - Python test execution
- `@api-validator` - Validate API routes

---

## 🔒 Security & Portability

### Cross-Platform Support

All skills use:
- ✅ `pathlib.Path` for file operations (works on Windows/Linux/Mac)
- ✅ `subprocess.run()` for CLI commands (no shell injection)
- ✅ `shutil.which()` to find executables
- ✅ Environment variable validation
- ✅ Secure subprocess timeout handling

### Environment Validation

On startup, the agent validates:
- [x] `.env` file exists
- [x] Critical keys present (GITHUB_TOKEN, LLM provider)
- [x] GitHub repo format valid
- [x] Friendly error messages if missing

---

## 📊 CI/CD Integration

The agent orchestrates a **10-stage CI/CD pipeline**:

```
INITIALIZE → DEPENDENCIES → TYPE-CHECK → CODE-QUALITY →
BUILD → UNIT-TEST ↔ E2E-TEST → SYNC-VERIFY →
SECURITY → QUALITY-GATES → DEPLOY → POST-DEPLOY
```

**Quality Gates (all must pass):**
- ✅ Type checking (strict mode)
- ✅ Code formatting/linting
- ✅ Build success
- ✅ Unit tests (65%+ coverage)
- ✅ E2E tests (all browsers)
- ✅ Sync verification (Web=DOCX=PDF=Excel)
- ✅ Security audit

---

## 🚨 Troubleshooting

### "uv: command not found"
```bash
# Install uv (once per system)
pip install uv

# Or use Python module syntax
python -m uv sync
```

### ".env file not found"
```bash
# Copy template
cd agent
cp .env.example .env

# Edit with your API keys
nano .env
```

### "No LLM provider configured"
Add ONE of these to `.env`:
```bash
OPENAI_API_KEY=sk-proj-...
# OR
ANTHROPIC_API_KEY=sk-ant-...
# OR
OLLAMA_BASE_URL=http://localhost:11434
```

### "MCP server not appearing in IDE"
```bash
# Re-run merge script
cd ..
python scripts/merge_mcp_config.py

# Reload IDE/editor
# In Cursor: Cmd+Shift+P → Developer: Reload Window
```

### Skills failing with "tool not found"
Ensure tools are in PATH:
```bash
# Check if npm is available
which npm

# Check if python is available
which python

# If not in PATH, add to .env
NODE_EXECUTABLE=/usr/local/bin/node
PYTHON_EXECUTABLE=/usr/local/bin/python3
```

---

## 📚 Documentation

- **[Architecture Guide](../ARCHITECTURE_COMPLETE.md)** - High-level design
- **[Phase 4 Analysis](../PHASE_4_ANALYSIS.md)** - Complete specification
- **[CI/CD Pipeline](../PHASE_4_ANALYSIS.md#10-stage-pipeline)** - Pipeline details
- **[Skills Reference](../PHASE_4_ANALYSIS.md#28-skills-reference)** - All skills documented

---

## 🤝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines.

---

## 📝 License

MIT License - See [LICENSE](../LICENSE) for details

---

## 🎯 Roadmap

- [x] Phase 1: Architecture Design
- [x] Phase 2: Packages & Components
- [x] Phase 3: Backend Refactorization + Frontend Integration
- [x] Phase 4A: CI/CD Analysis
- [ ] Phase 4B: Skills Implementation (Current)
- [ ] Phase 4C: Agent Restructuring
- [ ] Phase 5: Testing & Validation
- [ ] Phase 6: Documentation & Polish
- [ ] Phase 7: Production Release

---

**Last Updated:** 2024
**Maintained by:** Copilot Agent
**Status:** 🟡 In Development (Phase 4B)
