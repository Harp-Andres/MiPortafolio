---
applyTo: ".github/workflows/**,scripts/*.ps1,scripts/*.sh,scripts/*.py"
---

# Deployment / CI-CD skill

Role: `portfolio-deployment-manager` / `github-cicd-manager` / `devops-cicd-manager` (see `.github/agents/`).

- `deploy.yml` structure: `install` → `lint` + (`test-unit` ‖ `test-e2e` in parallel) → `build` → `deploy` (main only) → `notify`. Keep `test-unit`/`test-e2e` independent (`needs: install` only) so they stay parallel.
- `deploy` job only runs on `push` to `main` (`github.ref == 'refs/heads/main'`) — there is no automatic PR creation to `main` anywhere in this repo.
- Triggers currently cover `main`, `develop`, `refactor/*`, `fix/*`. Add new branch patterns here when a new long-lived branch prefix is introduced.
- Every test job must upload its own report artifacts independently (`vitest-coverage`, `vitest-html-report`, `playwright-report`) with `if: always()`.
- Reusable setup/verification scripts belong in `scripts/` (see `scripts/README.md`), never loose at the repo root.
- Before pushing a workflow change, validate it end-to-end locally first (`pnpm -F @mportafolio/web test:e2e`, `test:coverage`, `lint`) — don't rely on CI alone to catch mistakes.
