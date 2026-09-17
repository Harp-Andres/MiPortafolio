#!/usr/bin/env python3
"""
MCP Server - Maestro Agent

Exposes maestro orchestrator and portfolio skills as MCP tools.
Implements Model Context Protocol 2.2.0

Usage:
    python 1_interface/mcp_server.py
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

# MCP imports
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, CallToolRequestParams, ListToolsResult, CallToolResult

# Setup path
_AGENT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_AGENT_ROOT))


def get_logger(name: str):
    """Simple logger without circular dependency issues"""
    import logging
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


logger = get_logger("mcp_server")

# Create MCP server
server = Server("maestro")


def get_tools() -> list[Tool]:
    """Get all available MCP tools"""
    return [
        Tool(
            name="maestro",
            description="[MAESTRO] Master orchestrator - Execute workflows: ci, test, deploy, portfolio-update, full-pipeline",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow": {
                        "type": "string",
                        "description": "Workflow to execute",
                        "enum": ["ci", "test", "deploy", "portfolio-update", "quality", "full-pipeline"]
                    },
                    "options": {
                        "type": "object",
                        "description": "Workflow options (verbose, dry_run, etc.)",
                        "default": {}
                    }
                },
                "required": ["workflow"]
            }
        ),
        Tool(
            name="maestro-plan",
            description="[PLAN] Preview maestro orchestration plan (specialized agents and skill sequence) without executing skills",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow": {
                        "type": "string",
                        "description": "Workflow to preview",
                        "enum": ["ci", "test", "deploy", "portfolio-update", "quality", "full-pipeline"]
                    }
                },
                "required": ["workflow"]
            }
        ),
        Tool(
            name="skill-type-checker",
            description="[CHECK] Run type checking (mypy for Python, tsc for TypeScript)",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="skill-unit-test-runner",
            description="[TEST] Run unit tests (pytest for Python, vitest for TypeScript)",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="skill-e2e-test-runner",
            description="[PLAY] Run E2E tests (Playwright)",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="skill-build-orchestrator",
            description="[BUILD] Build all projects",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="skill-quality-gate-runner",
            description="[GATE] Run quality gates",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="skill-coverage-analyzer",
            description="[COVERAGE] Analyze and report test coverage",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="skill-pdf-generator",
            description="[PDF] Generate PDF documents",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="skill-docx-generator",
            description="[DOCX] Generate DOCX documents",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="skill-excel-generator",
            description="[EXCEL] Generate Excel documents",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="skill-github-pages-deployer",
            description="[DEPLOY] Deploy artifacts to GitHub Pages",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="skill-release-orchestrator",
            description="[RELEASE] Orchestrate release pipeline",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="skill-git-workflow-manager",
            description="[GIT] Execute git workflow operations",
            inputSchema={"type": "object", "properties": {}}
        ),
    ]


async def handle_list_tools() -> ListToolsResult:
    """Handle list tools request - MCP protocol method: tools/list"""
    logger.info("[TOOLS] Listing tools")
    tools = get_tools()
    logger.info(f"   Found {len(tools)} tools")
    return ListToolsResult(tools=tools)


async def handle_call_tool(params: CallToolRequestParams) -> CallToolResult:
    """Handle tool call request - MCP protocol method: tools/call"""
    tool_name = params.name
    arguments = params.arguments or {}
    
    logger.info(f"[CALL] Tool invoked: {tool_name}")
    logger.debug(f"   Arguments: {arguments}")
    
    try:
        # Dynamically load handlers to avoid numbered-directory issues
        import importlib.util as _ilu
        handlers_path = _AGENT_ROOT / "1_interface" / "handlers.py"
        spec = _ilu.spec_from_file_location("handlers", handlers_path)
        handlers_mod = _ilu.module_from_spec(spec)
        spec.loader.exec_module(handlers_mod)
        
        # Map tool names to handler functions
        handler_map = {
            "maestro": "handle_maestro_async",
            "maestro-plan": "handle_maestro_plan_async",
            "skill-type-checker": "handle_type_checker_async",
            "skill-unit-test-runner": "handle_unit_test_runner_async",
            "skill-e2e-test-runner": "handle_e2e_test_runner_async",
            "skill-build-orchestrator": "handle_build_orchestrator_async",
            "skill-quality-gate-runner": "handle_quality_gate_runner_async",
            "skill-coverage-analyzer": "handle_coverage_analyzer_async",
            "skill-pdf-generator": "handle_pdf_generator_async",
            "skill-docx-generator": "handle_docx_generator_async",
            "skill-excel-generator": "handle_excel_generator_async",
            "skill-github-pages-deployer": "handle_github_pages_deployer_async",
            "skill-release-orchestrator": "handle_release_orchestrator_async",
            "skill-git-workflow-manager": "handle_git_workflow_manager_async",
        }
        
        handler_name = handler_map.get(tool_name)
        if not handler_name:
            error_msg = f"Tool '{tool_name}' not found"
            logger.warning(f"❌ {error_msg}")
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps({"status": "error", "error": error_msg})
                )]
            )
        
        handler = getattr(handlers_mod, handler_name, None)
        if not handler:
            error_msg = f"Handler '{handler_name}' not implemented"
            logger.warning(f"❌ {error_msg}")
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps({"status": "error", "error": error_msg})
                )]
            )
        
        # Execute handler
        if asyncio.iscoroutinefunction(handler):
            result = await handler(arguments)
        else:
            result = handler(arguments)
        
        logger.info(f"✅ Tool completed: {tool_name}")
        
        # Ensure result is a string
        if isinstance(result, str):
            text_result = result
        else:
            text_result = json.dumps(result)
        
        return CallToolResult(
            content=[TextContent(type="text", text=text_result)]
        )
        
    except Exception as e:
        logger.error(f"❌ Tool error: {tool_name} - {str(e)}", exc_info=True)
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=json.dumps({"status": "error", "error": str(e)})
            )]
        )


async def main():
    """Main entry point - run MCP server over stdio"""
    logger.info("Starting Maestro MCP Server...")
    logger.info("Listening on stdio for MCP protocol messages")
    
    # Register request handlers with correct MCP 2.2.0 API
    # Signature: add_request_handler(method: str, params_type: type, handler: callable)
    server.add_request_handler("tools/list", type(None), handle_list_tools)
    server.add_request_handler("tools/call", CallToolRequestParams, handle_call_tool)
    
    logger.info("Handlers registered")
    
    # Use stdio_server as the transport layer
    # stdio_server yields a tuple (read_stream, write_stream)
    async with stdio_server() as (read_stream, write_stream):
        logger.info("MCP Server is running and ready for protocol messages")
        # Run server with the stdio streams
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
