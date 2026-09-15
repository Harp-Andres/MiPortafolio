"""
MCP Tools Definition

Define all MCP tools exposed to Copilot/Claude/IDEs:
  - maestro (Master orchestrator)
  - Individual skills as tools
  - Shared context managers
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field


class ToolDefinition(BaseModel):
    """MCP tool definition"""
    name: str
    description: str
    input_schema: Dict[str, Any]
    handler_function: str  # Reference to handler in mcp_server.py


# ============================================================================
# MAESTRO TOOL - Master Orchestrator
# ============================================================================

MAESTRO_TOOL = ToolDefinition(
    name="maestro",
    description="Master orchestrator for coordinating portfolio agents and skills. Execute complete workflows with automatic agent coordination.",
    input_schema={
        "type": "object",
        "properties": {
            "workflow": {
                "type": "string",
                "description": "Workflow to execute: ci, deploy, test, portfolio-update, full-pipeline, etc.",
            },
            "options": {
                "type": "object",
                "description": "Workflow options (verbose, dry_run, skip_tests, etc.)",
                "default": {},
            },
        },
        "required": ["workflow"],
    },
    handler_function="handle_maestro_async",
)


# ============================================================================
# SKILL TOOLS
# ============================================================================

# Infrastructure Skills
TYPE_CHECKER_TOOL = ToolDefinition(
    name="skill-type-checker",
    description="Run TypeScript and Python type checking on specified files.",
    input_schema={
        "type": "object",
        "properties": {
            "files": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Files to type check",
            },
            "strict": {
                "type": "boolean",
                "description": "Enable strict mode",
                "default": True,
            },
        },
        "required": ["files"],
    },
    handler_function="handle_type_checker_async",
)

BUILD_ORCHESTRATOR_TOOL = ToolDefinition(
    name="skill-build-orchestrator",
    description="Orchestrate build process for web and backend components.",
    input_schema={
        "type": "object",
        "properties": {
            "package": {
                "type": "string",
                "description": "Package to build (apps/web, apps/api, all)",
                "default": "all",
            },
            "production": {
                "type": "boolean",
                "description": "Build for production",
                "default": True,
            },
        },
    },
    handler_function="handle_build_orchestrator_async",
)

QUALITY_GATE_RUNNER_TOOL = ToolDefinition(
    name="skill-quality-gate-runner",
    description="Run quality gates: linting, type-checking, testing, build verification.",
    input_schema={
        "type": "object",
        "properties": {
            "gates": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Gates to run (lint, type-check, test, build)",
                "default": ["lint", "type-check", "test", "build"],
            },
        },
    },
    handler_function="handle_quality_gate_runner_async",
)

# Testing Skills
UNIT_TEST_RUNNER_TOOL = ToolDefinition(
    name="skill-unit-test-runner",
    description="Run unit tests for web and backend.",
    input_schema={
        "type": "object",
        "properties": {
            "package": {
                "type": "string",
                "description": "Package to test (apps/web, apps/api, all)",
                "default": "all",
            },
            "coverage": {
                "type": "boolean",
                "description": "Generate coverage report",
                "default": False,
            },
        },
    },
    handler_function="handle_unit_test_runner_async",
)

E2E_TEST_RUNNER_TOOL = ToolDefinition(
    name="skill-e2e-test-runner",
    description="Run end-to-end tests with Playwright.",
    input_schema={
        "type": "object",
        "properties": {
            "ui_mode": {
                "type": "boolean",
                "description": "Run in interactive UI mode",
                "default": False,
            },
            "browsers": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Browsers to test (chromium, firefox, webkit)",
                "default": ["chromium", "firefox", "webkit"],
            },
        },
    },
    handler_function="handle_e2e_test_runner_async",
)

COVERAGE_ANALYZER_TOOL = ToolDefinition(
    name="skill-coverage-analyzer",
    description="Analyze and report test coverage.",
    input_schema={
        "type": "object",
        "properties": {
            "threshold": {
                "type": "number",
                "description": "Minimum coverage threshold (%)",
                "default": 80,
            },
        },
    },
    handler_function="handle_coverage_analyzer_async",
)

# Document Skills
PDF_GENERATOR_TOOL = ToolDefinition(
    name="skill-pdf-generator",
    description="Generate PDF documents from CV data.",
    input_schema={
        "type": "object",
        "properties": {
            "format": {
                "type": "string",
                "description": "Format: ats or visual",
                "default": "visual",
            },
        },
    },
    handler_function="handle_pdf_generator_async",
)

DOCX_GENERATOR_TOOL = ToolDefinition(
    name="skill-docx-generator",
    description="Generate DOCX (Word) documents from CV data.",
    input_schema={
        "type": "object",
        "properties": {
            "include_cover_letter": {
                "type": "boolean",
                "description": "Include cover letter in DOCX",
                "default": False,
            },
        },
    },
    handler_function="handle_docx_generator_async",
)

EXCEL_GENERATOR_TOOL = ToolDefinition(
    name="skill-excel-generator",
    description="Generate Excel spreadsheets with projects and skills.",
    input_schema={
        "type": "object",
        "properties": {
            "include_metrics": {
                "type": "boolean",
                "description": "Include performance metrics",
                "default": True,
            },
        },
    },
    handler_function="handle_excel_generator_async",
)

# Deployment Skills
GITHUB_PAGES_DEPLOYER_TOOL = ToolDefinition(
    name="skill-github-pages-deployer",
    description="Deploy web application to GitHub Pages.",
    input_schema={
        "type": "object",
        "properties": {
            "environment": {
                "type": "string",
                "description": "Deployment environment",
                "default": "production",
            },
            "verify": {
                "type": "boolean",
                "description": "Verify deployment success",
                "default": True,
            },
        },
    },
    handler_function="handle_github_pages_deployer_async",
)

RELEASE_ORCHESTRATOR_TOOL = ToolDefinition(
    name="skill-release-orchestrator",
    description="Orchestrate complete release process.",
    input_schema={
        "type": "object",
        "properties": {
            "version": {
                "type": "string",
                "description": "Version for release (e.g., 1.2.3)",
            },
            "dry_run": {
                "type": "boolean",
                "description": "Dry run mode",
                "default": False,
            },
        },
        "required": ["version"],
    },
    handler_function="handle_release_orchestrator_async",
)

GIT_WORKFLOW_MANAGER_TOOL = ToolDefinition(
    name="skill-git-workflow-manager",
    description="Manage Git workflow: create branches, commits, push.",
    input_schema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "Action: create-branch, commit, push, create-pr",
            },
            "options": {
                "type": "object",
                "description": "Action-specific options",
            },
        },
        "required": ["action"],
    },
    handler_function="handle_git_workflow_manager_async",
)

# ============================================================================
# ALL TOOLS REGISTRY
# ============================================================================

ALL_MCP_TOOLS: List[ToolDefinition] = [
    # Master Orchestrator
    MAESTRO_TOOL,
    # Infrastructure
    TYPE_CHECKER_TOOL,
    BUILD_ORCHESTRATOR_TOOL,
    QUALITY_GATE_RUNNER_TOOL,
    # Testing
    UNIT_TEST_RUNNER_TOOL,
    E2E_TEST_RUNNER_TOOL,
    COVERAGE_ANALYZER_TOOL,
    # Documents
    PDF_GENERATOR_TOOL,
    DOCX_GENERATOR_TOOL,
    EXCEL_GENERATOR_TOOL,
    # Deployment
    GITHUB_PAGES_DEPLOYER_TOOL,
    RELEASE_ORCHESTRATOR_TOOL,
    GIT_WORKFLOW_MANAGER_TOOL,
]

TOOL_HANDLERS_MAP = {tool.name: tool.handler_function for tool in ALL_MCP_TOOLS}
