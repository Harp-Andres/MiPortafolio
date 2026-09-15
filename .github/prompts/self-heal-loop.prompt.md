# Self-Healing Loop Prompt

Goal: enforce automatic verify-and-fix loop after changes.

Loop:
1. Run relevant checks (lint, typecheck, unit/e2e).
2. Parse stdout/stderr and classify failures.
3. Apply minimal safe fix.
4. Re-run failed checks.
5. Stop only when green or when blocked with explicit report.

Policies:
- Do not hide failing checks.
- Do not widen test timeouts blindly.
- Prefer root-cause fixes over retries.

Output contract:
- Files changed.
- Checks executed.
- Before/after status.
- Remaining risks.
