## 🎼 MAESTRO MCP AGENT - Quick Reference Guide

**Version**: Phase 1 Complete  
**Status**: Ready for MCP server execution  
**Last Updated**: 2026-09-14

---

## 🚀 Quick Start

### Using Maestro via IDE (MCP)
```
User in IDE: @maestro workflow: "ci"

Flow:
  1. IDE sends MCP request to MCP server
  2. MCP server routes to handle_maestro_async()
  3. handle_maestro() orchestrates workflow
  4. Results returned as JSON
```

### Using Maestro via CLI
```python
from agent.1_interface.handlers import handle_maestro

result = handle_maestro(workflow="ci")
print(result)
# {
#   "workflow": "ci",
#   "status": "success",
#   "stages": [...],
#   "duration_seconds": 45.2
# }
```

### Using Skills Directly
```python
from agent.4_skills.skill_registry import instantiate_skill

# Create skill instance
skill = instantiate_skill("type_checker")

# Skill is ready to execute
# (Implementation calls skill._run_implementation(request))
```

---

## 📋 Available Workflows

### 1. **ci** - Continuous Integration Pipeline
```
dependency_resolver → type_checker → linter_checker → 
build_orchestrator → unit_test_runner → coverage_analyzer
```
**Use Case**: Full code quality check
**Command**: `@maestro workflow: "ci"`

### 2. **deploy** - Deployment to GitHub Pages
```
quality_gate_runner → build_orchestrator → github_pages_deployer
```
**Use Case**: Deploy web app to production
**Command**: `@maestro workflow: "deploy"`

### 3. **test** - All Tests
```
unit_test_runner → e2e_test_runner → 
coverage_analyzer → test_aggregator
```
**Use Case**: Run all test suites
**Command**: `@maestro workflow: "test"`

### 4. **portfolio-update** - Update Portfolio Documents
```
cv_data_validator → pdf_generator → docx_generator → 
excel_generator → sync_verifier
```
**Use Case**: Generate all CV formats from data
**Command**: `@maestro workflow: "portfolio-update"`

### 5. **quality** - Quality Gates
```
linter_checker → type_checker → unit_test_runner → 
build_orchestrator → quality_gate_runner
```
**Use Case**: Enforce code quality standards
**Command**: `@maestro workflow: "quality"`

### 6. **full-pipeline** - Complete Workflow
```
All 28 skills in optimal sequence (ci + test + deploy + portfolio)
```
**Use Case**: Complete portfolio update with deployment
**Command**: `@maestro workflow: "full-pipeline"`

---

## 🔧 System Architecture

### Layer 1: MCP Protocol
```
File: agent/1_interface/mcp_server.py
Exposes 13 MCP tools for IDE integration
```

### Layer 2: Tool Dispatch
```
File: agent/1_interface/mcp_tools.py
Maps tool names → async handler functions
```

### Layer 3: Handlers
```
File: agent/1_interface/handlers.py
Implements async handlers for each tool
Main handler: handle_maestro_async()
```

### Layer 4: Orchestration
```
File: agent/1_interface/handlers.py
Function: handle_maestro()
Coordinates workflow execution
```

### Layer 5: Routing
```
File: agent/4_skills/skill_routing.py
SkillRouter class
Assigns skills to agents (6 roles)
```

### Layer 6: Registry
```
File: agent/4_skills/skill_registry.py
SkillRegistry class
Loads and instantiates all 28 skills
```

### Layer 7: Skills
```
Directory: agent/4_skills/*/
28 skill implementations
Each extends BaseSkill
```

---

## 📊 Skill Ownership Model

### Agent: Backend
**Primary Skills**:
- type_checker
- build_orchestrator
- dependency_resolver
- quality_gate_runner
- api_validator
- backend_server
- backend_test_runner

### Agent: Testing
**Primary Skills**:
- unit_test_runner
- e2e_test_runner
- coverage_analyzer
- test_aggregator

### Agent: Deployment
**Primary Skills**:
- github_pages_deployer
- git_workflow_manager
- release_orchestrator
- git_branch_creator

### Agent: Portfolio
**Primary Skills**:
- pdf_generator
- docx_generator
- excel_generator
- cv_data_validator
- sync_verifier
- certificate_manager
- experience_tracker
- portfolio_updater
- skills_manager

### Agent: Quality
**Primary Skills**:
- linter_checker
- code_formatter
- performance_monitor

### Shared Skills (Any Agent)
- type_checker
- dependency_resolver
- build_orchestrator
- backend_test_runner

---

## 🔌 Integration Points

### For CLI Implementation
```python
from agent.1_interface.handlers import (
    handle_maestro,
    handle_ci,
    handle_deploy,
    handle_test,
    handle_docs,
    handle_add_project
)

# Use these in CLI commands
```

### For MCP Server
```python
from agent.1_interface.mcp_server import MaestroMCPServer

server = MaestroMCPServer()
# MCP server automatically routes to async handlers
```

### For Direct Skill Usage
```python
from agent.4_skills.skill_registry import get_skill_registry

registry = get_skill_registry()
skill = registry.instantiate_skill("type_checker")
# Work with skill directly
```

### For Agent Routing
```python
from agent.4_skills.skill_routing import get_skill_router

router = get_skill_router()
agent = router.route_skill("type_checker")  # Returns AgentRole
deps = router.get_skill_dependencies("pdf_generator")  # Returns List[str]
```

---

## 🐛 Troubleshooting

### "Skill not found" Error
```python
from agent.4_skills.skill_registry import get_skill_registry
registry = get_skill_registry()
print(registry.get_all_skills().keys())  # List all loaded skills
```

### "Handler not implemented" Error
Check that handler function name in mcp_tools.py matches async function in handlers.py:
```python
# mcp_tools.py
handler_function="handle_maestro_async"

# handlers.py
async def handle_maestro_async(arguments: Dict[str, Any]) -> str:
    ...
```

### Workflow Not Recognized
```python
from agent.1_interface.handlers import _get_workflow_skills
skills = _get_workflow_skills("ci")  # Returns [] if not found
```

---

## 📝 Example Usage Patterns

### Pattern 1: Execute Workflow via Maestro
```python
from agent.1_interface.handlers import handle_maestro

result = handle_maestro(
    workflow="ci",
    options={"continue_on_error": False},
    verbose=True
)

if result["status"] == "success":
    print(f"✓ Completed in {result['duration_seconds']}s")
    for stage in result["stages"]:
        print(f"  - {stage['skill']}: {stage['status']}")
```

### Pattern 2: Get Skill Routing Info
```python
from agent.4_skills.skill_routing import get_skill_router

router = get_skill_router()

for skill_name in ["type_checker", "pdf_generator", "github_pages_deployer"]:
    info = router.get_routing_info(skill_name)
    print(f"{skill_name}:")
    print(f"  Owner: {info['primary_owner'].value}")
    print(f"  Dependencies: {info['dependencies']}")
    print(f"  Shared: {info['is_shared']}")
```

### Pattern 3: Custom Workflow
```python
from agent.1_interface.handlers import handle_maestro

# Create custom workflow by chaining workflows
result1 = handle_maestro(workflow="ci")
if result1["status"] == "success":
    result2 = handle_maestro(workflow="deploy")
    if result2["status"] == "success":
        print("✓ CI and Deploy both succeeded")
```

### Pattern 4: Get Skill Metadata
```python
from agent.4_skills.skill_registry import get_skill_registry

registry = get_skill_registry()
metadata = registry.get_skill("type_checker")

print(f"Name: {metadata.name}")
print(f"Category: {metadata.category}")
print(f"Class: {metadata.skill_class}")
print(f"Module: {metadata.module_name}")
```

---

## 📚 Key Components Reference

### SkillRegistry Methods
```python
get_instance() → SkillRegistry
get_skill(name) → Optional[SkillMetadata]
get_all_skills() → Dict[str, SkillMetadata]
get_skills_by_category(category) → Dict[str, SkillMetadata]
get_categories() → List[str]
instantiate_skill(name, workspace_root) → Optional[BaseSkill]
describe_skill(name) → Optional[Dict]
validate_skill_exists(name) → bool
list_skills_for_mcp() → List[Dict]
```

### SkillRouter Methods
```python
route_skill(skill_name, context) → AgentRole
get_skill_dependencies(skill_name) → List[str]
get_skill_owner(skill_name) → AgentRole
is_shared_skill(skill_name) → bool
update_agent_load(agent, delta) → None
can_execute_parallel(skills) → bool
validate_skill_exists(skill_name) → bool
list_skills_by_agent(agent) → List[str]
```

### Handler Functions
```python
# Sync handlers (CLI)
handle_maestro(workflow, options, verbose) → Dict[str, Any]
handle_ci(stages, verbose) → Dict[str, Any]
handle_deploy(environment, force, verbose) → Dict[str, Any]
handle_test(suite, coverage, verbose) → Dict[str, Any]
handle_docs(format, output_dir, sync_verify) → Dict[str, Any]
handle_add_project(name, description, tech, link, github) → Dict[str, Any]

# Async handlers (MCP)
handle_maestro_async(arguments) → str
handle_type_checker_async(arguments) → str
handle_build_orchestrator_async(arguments) → str
# ... (10 more async handlers)
```

---

## ✅ Ready to Use Features

- ✅ MCP server foundation
- ✅ 13 MCP tools exposed
- ✅ 28 skills registered
- ✅ 6 agents with ownership
- ✅ 6 predefined workflows
- ✅ Full error handling
- ✅ Structured logging
- ✅ Async/await support

---

## ⏳ Not Yet Implemented (Phase 2+)

- ⏳ Actual skill execution
- ⏳ LLM orchestration
- ⏳ ReAct engine
- ⏳ Memory management
- ⏳ RAG indexing
- ⏳ State persistence

---

## 📖 Additional Documentation

- Full architecture: [PHASE_1_COMPLETION.md](PHASE_1_COMPLETION.md)
- Master specification: [MAESTRO_SPECIFICATION.md](MAESTRO_SPECIFICATION.md)
- Agent definitions: [.github/agents/](.github/agents/)
