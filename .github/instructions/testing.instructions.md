---
applyTo: "apps/web/tests/e2e/**,apps/web/src/**/__tests__/**,apps/web/vitest.config.ts,apps/web/playwright.config.ts,apps/api/tests/**"
---

# Testing skill (unit + E2E)

Role: `portfolio-test-manager` / `sdet-quality-manager` (see `.github/agents/`).

- Prefer semantic selectors (`getByRole`, accessible names) over `data-testid` in Playwright specs.
- `playwright.config.ts` already runs 2 workers in CI (`PLAYWRIGHT_WORKERS` overridable) and generates html/json/junit reports — don't lower parallelism or drop a reporter without a reason.
- Verify things that actually cross the network/filesystem for real (e.g. use Playwright's `page.waitForEvent('download')` + `download.failure()`, not just checking a static file exists on disk) — filesystem-only checks can mask real bugs (e.g. wrong base path).
- `HashRouter` section hash-links (`/#skills`) can be flaky in E2E; assert on heading visibility/scroll instead of the hash itself.
- Run web tests with `pnpm -F @mportafolio/web test` (unit) / `pnpm -F @mportafolio/web test:e2e` (E2E) / `pnpm -F @mportafolio/web test:coverage` (coverage).
- Run API tests with `cd apps/api && uv run pytest`.
- Before declaring a fix done, re-run the affected suite and confirm the previously-failing test now passes — don't rely solely on lint/type-check.
