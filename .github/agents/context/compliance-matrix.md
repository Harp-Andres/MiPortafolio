# Agent Platform Compliance Matrix

## Componentes Clave VS Code

1. Prompt Files and Custom Instructions
- Status: PASS
- Evidence: .github/copilot-instructions.md, .github/prompts/*.prompt.md

2. Custom Agents and Participant Handlers
- Status: PASS
- Evidence: .github/agents/*.agent.md (master + specialized agents with descriptions)

3. MCP Servers
- Status: PASS
- Evidence: .mcp.json configured for maestro via stdio

4. Workspace Knowledge and Indexing
- Status: PASS
- Evidence: .github/agents/context/* knowledge index files

5. Evaluators and Self-Healing Loops
- Status: PASS
- Evidence: .github/prompts/self-heal-loop.prompt.md + handlers/checkpoint/state feedback loop

## Operational Note

To apply the model consistently, invoke workflows with validation-first behavior and keep CI green before merge.
