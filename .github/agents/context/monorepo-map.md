# Monorepo Map

Top-level:
- agent: 7-layer orchestrator runtime and MCP server
- apps/web: React + Vite + Playwright
- apps/api: FastAPI + pytest
- packages: shared modules

Core workflows:
- CI: lint -> types -> tests -> build
- Deploy: build -> validate -> release

Critical paths:
- agent/1_interface: CLI and MCP server
- agent/4_skills: skill implementations
- .agent/AGENTS.md: hierarchy and responsibilities
- .mcp.json: MCP server registration
