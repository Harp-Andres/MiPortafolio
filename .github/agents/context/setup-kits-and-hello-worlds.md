# Setup Kits and Advanced Hello Worlds

This file defines the minimum technical toolkit each specialized agent needs, plus an advanced hello world target.

## @devops (devops-cicd-manager)

Technology kit:
- GitHub Actions
- pnpm + Node build cache
- uv + Python jobs
- artifact upload and retention

Setup baseline:
- Validate workflow yaml syntax
- Add matrix strategy for os/runtime
- Add dependency cache keys
- Add quality gate summary in job outputs

Advanced hello world:
- Monorepo CI pipeline that runs lint, unit tests, e2e smoke and build
- Parallel jobs with needs chain
- Artifact upload and release-ready package output

## @architect (software-architecture-manager)

Technology kit:
- ADR templates
- module dependency map
- boundary validation checks

Setup baseline:
- Define bounded contexts and layers
- Define allowed imports by layer
- Define migration plan for legacy modules

Advanced hello world:
- Hexagonal app slice with one use case, one domain model, two adapters
- Contract tests proving adapter interchangeability

## @sdet (sdet-quality-manager)

Technology kit:
- Playwright multi-browser config
- pytest markers and fixtures
- API contract assertions
- mobile test strategy (Appium-ready)

Setup baseline:
- Test pyramid map (unit/integration/e2e)
- Flaky test quarantine protocol
- Evidence collection (traces/screenshots/reports)

Advanced hello world:
- Login flow tested in UI + API + mobile smoke
- Retry-safe fixtures and deterministic test data
- Failure triage output with probable root cause

## @platform (platform-architecture-manager)

Technology kit:
- Docker multi-stage builds
- Kubernetes deployment/service/ingress
- readiness/liveness probes
- resource and security contexts

Setup baseline:
- Standard base image and user model
- Namespace and workload naming conventions
- Rollout/rollback runbook

Advanced hello world:
- API container with health endpoint
- K8s deployment with rolling updates and probes
- HPA-ready resource profile and logs integration

## @sysops (os-platform-manager)

Technology kit:
- Windows PowerShell scripts
- Linux bash scripts
- process and service diagnostics
- env parity checks

Setup baseline:
- Unified prerequisite checks
- Path, permissions and shell profile setup
- Script execution policy guidance

Advanced hello world:
- Cross-platform service launcher script
- Health check endpoint polling
- Graceful stop and structured log capture

## Operational sequence for new machines

1. Run setup portability checks first.
2. Run niche setup kit for the target domain.
3. Run advanced hello world to validate baseline.
4. Integrate into CI only after local baseline passes.
