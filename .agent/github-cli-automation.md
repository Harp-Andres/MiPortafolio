---
name: github-cli-automation
description: PowerShell CLI scripts for testing, building, and managing CI/CD workflows in MiPortafolio
---

# GitHub CLI Automation Skill

This skill enables the agent to interact with the MiPortafolio monorepo using CLI scripts for testing, building, and GitHub Actions management.

## Available Scripts

### 1. Testing: `scripts/test.ps1`

Run tests in the monorepo with various modes.

**When to use:**
- Verifying code passes tests
- Debugging test failures
- Running tests with coverage
- Watch mode for iterative development

**Invocations:**
```powershell
# Unit tests
.\scripts\test.ps1 -Command unit -Package apps/web

# All tests with coverage
.\scripts\test.ps1 -Command coverage

# E2E tests
.\scripts\test.ps1 -Command e2e

# Watch mode
.\scripts\test.ps1 -Command watch
```

**Exit codes:** 0 (success), 1 (failure)

---

### 2. Building: `scripts/build.ps1`

Build, lint, and validate code.

**When to use:**
- Before creating PRs (always run `validate`)
- Building the application
- Type checking
- Cleaning artifacts

**Invocations:**
```powershell
# Full validation pipeline
.\scripts\build.ps1 -Command validate

# Just build
.\scripts\build.ps1 -Command build -Package apps/web

# Lint
.\scripts\build.ps1 -Command lint

# Type check
.\scripts\build.ps1 -Command type-check

# Clean
.\scripts\build.ps1 -Command clean
```

**Always use `validate` before PRs:**
```powershell
.\scripts\build.ps1 -Command validate
```

---

### 3. Workflow: `scripts/workflow.ps1`

Manage GitHub Actions workflows.

**When to use:**
- Triggering workflows manually
- Checking workflow status
- Verifying branch protection
- Viewing workflow logs
- Waiting for completion

**Invocations:**
```powershell
# Trigger workflow
.\scripts\workflow.ps1 -Command run -Branch refactor/complete-monorepo-restructuring

# Check status
.\scripts\workflow.ps1 -Command status

# List recent runs
.\scripts\workflow.ps1 -Command list

# View logs
.\scripts\workflow.ps1 -Command logs -RunId 34917884678

# Wait for completion
.\scripts\workflow.ps1 -Command wait

# Verify branch protection
.\scripts\workflow.ps1 -Command verify-protection
```

---

### 4. Pull Requests: `scripts/pr.ps1`

Manage pull requests.

**When to use:**
- Creating PRs
- Checking PR status
- Merging PRs
- Reviewing PR details

**Invocations:**
```powershell
# Create PR
.\scripts\pr.ps1 -Command create `
  -Base main `
  -Title "fix: description" `
  -Body "Detailed description"

# List PRs
.\scripts\pr.ps1 -Command list

# Check status
.\scripts\pr.ps1 -Command status -PRNumber 123

# View details
.\scripts\pr.ps1 -Command review -PRNumber 123

# Merge (auto-validates checks)
.\scripts\pr.ps1 -Command merge -PRNumber 123
```

---

## Standard Workflows

### Fix Tests → Create PR → Merge

```powershell
# 1. Run tests to see failures
.\scripts\test.ps1 -Command unit

# 2. Fix issues... (edit code)

# 3. Verify fix
.\scripts\test.ps1 -Command unit

# 4. Full validation
.\scripts\build.ps1 -Command validate

# 5. Create PR
.\scripts\pr.ps1 -Command create -Base main -Title "fix: test failures"

# 6. Monitor
.\scripts\pr.ps1 -Command status -PRNumber <number>

# 7. Merge
.\scripts\pr.ps1 -Command merge -PRNumber <number>
```

### Deploy Feature Branch

```powershell
# 1. Validate locally
.\scripts\build.ps1 -Command validate

# 2. Trigger workflow
.\scripts\workflow.ps1 -Command run -Branch feature/my-feature

# 3. Wait
.\scripts\workflow.ps1 -Command wait

# 4. Check status
.\scripts\workflow.ps1 -Command status

# 5. Create PR if successful
.\scripts\pr.ps1 -Command create -Base main -Title "feat: new feature"
```

---

## Requirements

- PowerShell 5.1+ (Windows) or PowerShell Core 7+
- GitHub CLI: `winget install --id GitHub.cli`
- Git configured
- pnpm v8+
- Node.js v24+

## Setup

```powershell
# Install GitHub CLI
winget install --id GitHub.cli

# Authenticate
gh auth login

# Allow scripts to run
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Key Information

**Repository:** https://github.com/Harp-Andres/MiPortafolio

**Branch Protection (main):**
- 1 PR review required
- Status checks: lint, test, build, notify
- Requires up-to-date before merge
- Enforced for admins
- Blocks force push and deletion

**CI/CD Pipeline:**
1. install → 2. lint + test → 3. build → 4. deploy → 5. notify

