#!/usr/bin/env python3
"""
MCP Server Implementation - Simplified and Portable Version

Exposes maestro and all skills as MCP tools for IDE integration.
Implements Model Context Protocol (https://modelcontextprotocol.io)

Usage:
    python -m agent.1_interface.mcp_server_v2
    uv run python -m agent.1_interface.mcp_server_v2

Environment:
    - GITHUB_TOKEN: GitHub authentication token (optional)
    - GITHUB_REPO: Repository (org/repo) (optional)
    - API_KEY: For LLM integration (optional)
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
except ImportError:
    print("❌ python-mcp not installed. Run: pip install python-mcp")
    print("   or: uv pip install python-mcp")
    sys.exit(1)

# Add agent root to path for imports
_AGENT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_AGENT_ROOT))

from config.constants import get_logger

logger = get_logger("mcp_server")


# ============================================================================
# Tool Definitions
# ============================================================================

class ToolDef:
    """Simple tool definition"""
    def __init__(self, name: str, description: str, handler: str, params: Dict = None):
        self.name = name
        self.description = description
        self.handler = handler
        self.input_schema = {
            "type": "object",
            "properties": params or {},
            "required": []
        }


# Skills for Programming & Testing (Priority Focus)
PROGRAMMING_TOOLS = [
    ToolDef("skill-code-formatter", 
            "Format and lint Python/TypeScript code",
            "handle_code_formatter",
            {"files": {"type": "array", "items": {"type": "string"}}}),
    
    ToolDef("skill-type-checker",
            "Run type checking (mypy for Python, tsc for TypeScript)",
            "handle_type_checker",
            {"files": {"type": "array", "items": {"type": "string"}}}),
    
    ToolDef("skill-unit-test-runner",
            "Run unit tests (pytest for Python, vitest for TypeScript)",
            "handle_unit_tests",
            {"path": {"type": "string"}, "pattern": {"type": "string", "default": ""}}),
    
    ToolDef("skill-e2e-test-runner",
            "Run end-to-end tests (Playwright)",
            "handle_e2e_tests",
            {"path": {"type": "string"}}),
    
    ToolDef("skill-test-coverage",
            "Generate test coverage report",
            "handle_coverage",
            {"path": {"type": "string"}}),
    
    ToolDef("skill-code-analyzer",
            "Analyze code quality and complexity",
            "handle_code_analyzer",
            {"files": {"type": "array", "items": {"type": "string"}}}),
]

# Infrastructure & Build Tools
INFRASTRUCTURE_TOOLS = [
    ToolDef("skill-build",
            "Build project (TypeScript compilation, Python packaging)",
            "handle_build",
            {"target": {"type": "string", "default": "all"}}),
    
    ToolDef("skill-quality-gate",
            "Run complete quality checks (format + type + lint + test)",
            "handle_quality_gate",
            {"skip_tests": {"type": "boolean", "default": False}}),
]

# Deployment & CI/CD Tools
DEPLOYMENT_TOOLS = [
    ToolDef("skill-git-workflow",
            "Manage Git workflow (commit, push, PR)",
            "handle_git_workflow",
            {"action": {"type": "string"}}),
    
    ToolDef("skill-deploy",
            "Deploy to production or staging",
            "handle_deploy",
            {"target": {"type": "string"}}),
]

# Master Orchestrator Tool
MAESTRO_TOOL = ToolDef("maestro",
            "Master orchestrator - Coordinate multiple workflows (CI, deploy, test, etc.)",
            "handle_maestro",
            {
                "workflow": {"type": "string", "description": "ci, test, deploy, full-pipeline"},
                "options": {"type": "object", "default": {}}
            })

ALL_TOOLS = [MAESTRO_TOOL] + PROGRAMMING_TOOLS + INFRASTRUCTURE_TOOLS + DEPLOYMENT_TOOLS


# ============================================================================
# MCP Server Implementation
# ============================================================================

class MaestroMCPServer:
    """Maestro MCP Server - Coordinator for portfolio skills"""

    def __init__(self):
        self.server = Server("maestro")
        self.tools_map = {tool.name: tool for tool in ALL_TOOLS}
        self._register_handlers()
        logger.info(f"Maestro MCP Server initialized with {len(ALL_TOOLS)} tools")

    def _register_handlers(self):
        """Register MCP protocol handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """Return all available tools"""
            return [
                Tool(
                    name=tool.name,
                    description=tool.description,
                    inputSchema=tool.input_schema,
                )
                for tool in ALL_TOOLS
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]):
            """Execute a tool by name"""
            logger.info(f"🔧 Tool called: {name}")
            
            tool = self.tools_map.get(name)
            if not tool:
                error_msg = f"Unknown tool: {name}"
                logger.error(error_msg)
                return TextContent(type="text", text=json.dumps({
                    "status": "error",
                    "error": error_msg,
                    "available": list(self.tools_map.keys())
                }))

            try:
                # Route to handler
                result = await self._execute_handler(tool.handler, arguments)
                return TextContent(type="text", text=result)
            except Exception as e:
                logger.error(f"Tool execution failed: {e}", exc_info=True)
                return TextContent(type="text", text=json.dumps({
                    "status": "error",
                    "error": str(e)
                }))

    async def _execute_handler(self, handler_name: str, arguments: Dict[str, Any]) -> str:
        """Execute a handler function and return JSON response"""
        try:
            # Import from skill_handlers (new simplified handlers)
            from agent_1_interface import skill_handlers
            
            handler_func = skill_handlers.HANDLERS.get(handler_name)
            if not handler_func:
                # Fallback: try importing from original handlers module
                import importlib.util as _ilu
                handlers_path = _AGENT_ROOT / "1_interface" / "handlers.py"
                spec = _ilu.spec_from_file_location("handlers", handlers_path)
                handlers = _ilu.module_from_spec(spec)
                spec.loader.exec_module(handlers)
                handler_func = getattr(handlers, handler_name, None)
            
            if not handler_func:
                return json.dumps({
                    "status": "error",
                    "error": f"Handler '{handler_name}' not found",
                    "available_handlers": list(skill_handlers.HANDLERS.keys())
                })
            
            # Call handler (async)
            if asyncio.iscoroutinefunction(handler_func):
                result = await handler_func(arguments)
            else:
                result = handler_func(arguments)
            
            # Ensure response is JSON string
            if isinstance(result, str):
                return result
            else:
                return json.dumps({"status": "success", "result": result})
        except Exception as e:
            logger.error(f"Handler execution error: {e}", exc_info=True)
            return json.dumps({
                "status": "error",
                "error": str(e),
                "handler": handler_name
            })

    async def run(self):
        """Run the MCP server"""
        logger.info("🚀 Starting Maestro MCP Server...")
        try:
            async with self.server:
                logger.info("✅ Maestro MCP Server is running and ready for connections")
                # Keep server alive
                while True:
                    await asyncio.sleep(86400)  # 24 hours
        except KeyboardInterrupt:
            logger.info("⛔ Maestro MCP Server stopped by user")
        except Exception as e:
            logger.error(f"❌ Server error: {e}", exc_info=True)
            raise


# ============================================================================
# Entry Point
# ============================================================================

async def main():
    """Start the MCP server"""
    logger.info("🎼 Maestro Agent System - MCP Server v2")
    logger.info(f"Python: {sys.version}")
    logger.info(f"Root: {_AGENT_ROOT}")
    
    server = MaestroMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
