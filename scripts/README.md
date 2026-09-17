# 🚀 MiPortafolio Scripts

Utilities for managing CI/CD, testing, and builds in the MiPortafolio monorepo.

## Scripts Overview

### 1. `scripts/test.ps1` - Testing Utilities

Run tests for the monorepo packages.

**Usage:**
```powershell
.\scripts\test.ps1 -Command <command> [-Package <package>]
```

**Commands:**
- `unit` - Run unit tests only
- `e2e` - Run end-to-end tests
- `all` - Run all tests
- `coverage` - Run tests with coverage report
- `watch` - Run tests in watch mode

**Examples:**
```powershell
# Run unit tests for web app
.\scripts\test.ps1 -Command unit

# Run all tests with coverage
.\scripts\test.ps1 -Command coverage -Package apps/web

# Watch mode
.\scripts\test.ps1 -Command watch
```

---

### 2. `scripts/build.ps1` - Build & Validation

Build and validate the application code.

**Usage:**
```powershell
.\scripts\build.ps1 -Command <command> [-Package <package>]
```

**Commands:**
- `lint` - Run linter only
- `build` - Build the application
- `type-check` - Run TypeScript type checking
- `validate` - Run full validation pipeline (lint → type-check → test → build)
- `clean` - Clean build artifacts

**Examples:**
```powershell
# Full validation (lint → type-check → test → build)
.\scripts\build.ps1 -Command validate

# Build only
.\scripts\build.ps1 -Command build -Package apps/web

# Clean artifacts
.\scripts\build.ps1 -Command clean
```

---

### 3. `scripts/workflow.ps1` - GitHub Actions Management

Manage and monitor GitHub Actions workflows.

**Usage:**
```powershell
.\scripts\workflow.ps1 -Command <command> [-Branch <branch>] [-RunId <id>]
```

**Commands:**
- `run` - Trigger workflow on a branch
- `status` - Check workflow status
- `logs` - View workflow logs (requires RunId)
- `list` - List recent workflow runs
- `verify-protection` - Verify branch protection rules
- `wait` - Wait for workflow to complete

**Examples:**
```powershell
# Trigger workflow on current branch
.\scripts\workflow.ps1 -Command run -Branch refactor/complete-monorepo-restructuring

# Check workflow status
.\scripts\workflow.ps1 -Command status

# View logs for specific run
.\scripts\workflow.ps1 -Command logs -RunId 34917884678

# Wait for latest run to complete
.\scripts\workflow.ps1 -Command wait

# Verify branch protection on main
.\scripts\workflow.ps1 -Command verify-protection
```

---

### 4. `scripts/pr.ps1` - Pull Request Management

Create and manage pull requests with GitHub CLI.

**Usage:**
```powershell
.\scripts\pr.ps1 -Command <command> [-PRNumber <number>] [-Title <title>]
```

**Commands:**
- `create` - Create a new PR
- `list` - List open PRs
- `checks` - View status checks for a PR
- `merge` - Merge a PR (only if all checks pass)
- `review` - View PR details
- `status` - Check PR status with checks and reviews

**Examples:**
```powershell
# Create PR from current branch to main
.\scripts\pr.ps1 -Command create `
  -Title "fix: resolve test import issues" `
  -Body "Adds missing vitest path aliases for workspace packages"

# List open PRs
.\scripts\pr.ps1 -Command list

# Check status of PR #123
.\scripts\pr.ps1 -Command status -PRNumber 123

# Merge PR #123 (checks all tests pass first)
.\scripts\pr.ps1 -Command merge -PRNumber 123
```

---

## Common Workflows

### 🔄 Full CI Pipeline Locally

```powershell
# 1. Validate everything locally first
.\scripts\build.ps1 -Command validate

# 2. Trigger workflow on GitHub
.\scripts\workflow.ps1 -Command run -Branch refactor/complete-monorepo-restructuring

# 3. Wait for completion
.\scripts\workflow.ps1 -Command wait

# 4. View results if needed
.\scripts\workflow.ps1 -Command logs -RunId <run_id>
```

### 📤 Create and Merge PR

```powershell
# 1. Ensure code passes locally
.\scripts\build.ps1 -Command validate

# 2. Create PR to main
.\scripts\pr.ps1 -Command create `
  -Base main `
  -Title "your-pr-title" `
  -Body "description"

# 3. Wait for checks and approval
.\scripts\pr.ps1 -Command status -PRNumber <number>

# 4. Merge when ready (auto-checks that all tests pass)
.\scripts\pr.ps1 -Command merge -PRNumber <number>
```

### 🐛 Debug Test Failures

```powershell
# 1. Run tests locally
.\scripts\test.ps1 -Command unit

# 2. Run with watch mode for iteration
.\scripts\test.ps1 -Command watch

# 3. Get coverage for detailed analysis
.\scripts\test.ps1 -Command coverage
```

---

## Requirements

- **PowerShell** 5.1+ (Windows) or **PowerShell Core** 7+ (cross-platform)
- **GitHub CLI** (`gh`) - Install: `winget install --id GitHub.cli`
- **Git** configured with credentials
- **pnpm** v8+ - Package manager
- **Node.js** v24+ - Runtime

## Quick Setup

```powershell
# 1. Install GitHub CLI if needed
winget install --id GitHub.cli

# 2. Authenticate with GitHub
gh auth login

# 3. Set script execution policy (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 4. Use scripts from root directory
.\scripts\test.ps1 -Command unit
```

## Script Execution Policy

If scripts won't run, set execution policy:

```powershell
# For current user only
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# For local machine (admin required)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine

# Verify
Get-ExecutionPolicy
```

---

## Notes

- All scripts use `$ErrorActionPreference = 'Stop'` to exit on first error
- Output is color-coded: Cyan (info), Yellow (warning), Red (error), Green (success)
- Run scripts from the repository root directory
- GitHub CLI must be authenticated (`gh auth login`)
- Scripts are PowerShell only (for Windows/PowerShell Core compatibility)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `gh: command not found` | Install GitHub CLI: `winget install --id GitHub.cli` |
| `Script not found` | Run from repo root: `cd e:\UnidadPrincipal\Documentos\Repos\MiPortafolio` |
| `Permission denied` | Set execution policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `Not authenticated` | Run: `gh auth login` and follow prompts |
| `Cannot find pnpm` | Install pnpm: `npm install -g pnpm` |

