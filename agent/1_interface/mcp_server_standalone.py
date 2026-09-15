#!/usr/bin/env python3
"""
Maestro MCP Server - Simple Implementation without external MCP library

Implements Model Context Protocol via JSON-RPC over stdio.
This version works without the mcp package, communicating directly over stdout/stderr.

Usage:
    python -m agent.1_interface.mcp_server_standalone
    uv run python -m agent.1_interface.mcp_server_standalone

Or as entry point in VS Code settings:
    "python -m agent.1_interface.mcp_server_standalone 2>&1"
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

# Add agent root to path for imports
_AGENT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_AGENT_ROOT))

from config.constants import get_logger

logger = get_logger("mcp_standalone")


# ============================================================================
# JSON-RPC MCP Protocol Implementation
# ============================================================================

@dataclass
class JSONRPCRequest:
    """JSON-RPC 2.0 request"""
    jsonrpc: str = "2.0"
    method: str = ""
    params: Dict[str, Any] = None
    id: Any = None


@dataclass
class JSONRPCResponse:
    """JSON-RPC 2.0 response"""
    jsonrpc: str = "2.0"
    result: Any = None
    error: Any = None
    id: Any = None


class MCPToolRegistry:
    """Simple tool registry for MCP"""
    
    def __init__(self):
        self.tools = {
            # Maestro
            "maestro": {
                "name": "maestro",
                "description": "Master orchestrator - Coordinate multiple workflows (CI, deploy, test, etc.)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "workflow": {"type": "string", "description": "ci, test, deploy, full-pipeline"},
                        "options": {"type": "object", "default": {}}
                    }
                }
            },
            # Programming & Testing
            "skill-code-formatter": {
                "name": "skill-code-formatter",
                "description": "Format and lint Python/TypeScript code",
                "inputSchema": {"type": "object", "properties": {"files": {"type": "array", "items": {"type": "string"}}}}
            },
            "skill-type-checker": {
                "name": "skill-type-checker",
                "description": "Run type checking (mypy for Python, tsc for TypeScript)",
                "inputSchema": {"type": "object", "properties": {"files": {"type": "array", "items": {"type": "string"}}}}
            },
            "skill-unit-test-runner": {
                "name": "skill-unit-test-runner",
                "description": "Run unit tests (pytest for Python, vitest for TypeScript)",
                "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}, "pattern": {"type": "string"}}}
            },
            "skill-e2e-test-runner": {
                "name": "skill-e2e-test-runner",
                "description": "Run end-to-end tests (Playwright)",
                "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}}
            },
            "skill-test-coverage": {
                "name": "skill-test-coverage",
                "description": "Generate test coverage report",
                "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}}
            },
            "skill-code-analyzer": {
                "name": "skill-code-analyzer",
                "description": "Analyze code quality and complexity",
                "inputSchema": {"type": "object", "properties": {"files": {"type": "array", "items": {"type": "string"}}}}
            },
            # Infrastructure
            "skill-build": {
                "name": "skill-build",
                "description": "Build project (TypeScript compilation, Python packaging)",
                "inputSchema": {"type": "object", "properties": {"target": {"type": "string"}}}
            },
            "skill-quality-gate": {
                "name": "skill-quality-gate",
                "description": "Run complete quality checks (format + type + lint + test)",
                "inputSchema": {"type": "object", "properties": {"skip_tests": {"type": "boolean"}}}
            },
            # Deployment
            "skill-git-workflow": {
                "name": "skill-git-workflow",
                "description": "Manage Git workflow (commit, push, PR)",
                "inputSchema": {"type": "object", "properties": {"action": {"type": "string"}}}
            },
            "skill-deploy": {
                "name": "skill-deploy",
                "description": "Deploy to production or staging",
                "inputSchema": {"type": "object", "properties": {"target": {"type": "string"}}}
            },
        }


class MaestroMCPServer:
    """Maestro MCP Server - Implements Model Context Protocol"""

    def __init__(self):
        self.registry = MCPToolRegistry()
        self.handlers_cache = None
        logger.info(f"Maestro MCP Server initialized with {len(self.registry.tools)} tools")

    async def handle_request(self, request: JSONRPCRequest) -> JSONRPCResponse:
        """Handle a JSON-RPC request"""
        logger.debug(f"Handling request: {request.method}")

        if request.method == "initialize":
            return await self._handle_initialize(request)
        elif request.method == "tools/list":
            return await self._handle_tools_list(request)
        elif request.method == "tools/call":
            return await self._handle_tools_call(request)
        else:
            return JSONRPCResponse(
                error={"code": -32601, "message": f"Method not found: {request.method}"},
                id=request.id
            )

    async def _handle_initialize(self, request: JSONRPCRequest) -> JSONRPCResponse:
        """Initialize MCP connection"""
        logger.info("Initializing MCP connection")
        return JSONRPCResponse(
            result={
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "maestro",
                    "version": "0.1.0"
                }
            },
            id=request.id
        )

    async def _handle_tools_list(self, request: JSONRPCRequest) -> JSONRPCResponse:
        """List all available tools"""
        tools = list(self.registry.tools.values())
        logger.info(f"Listing {len(tools)} tools")
        return JSONRPCResponse(result={"tools": tools}, id=request.id)

    async def _handle_tools_call(self, request: JSONRPCRequest) -> JSONRPCResponse:
        """Call a tool"""
        params = request.params or {}
        tool_name = params.get("name", "")
        tool_args = params.get("arguments", {})

        logger.info(f"Calling tool: {tool_name}")

        if tool_name not in self.registry.tools:
            return JSONRPCResponse(
                error={"code": -32602, "message": f"Tool not found: {tool_name}"},
                id=request.id
            )

        try:
            # Import and call handler
            result = await self._call_handler(tool_name, tool_args)
            return JSONRPCResponse(result=result, id=request.id)
        except Exception as e:
            logger.error(f"Tool execution failed: {e}", exc_info=True)
            return JSONRPCResponse(
                error={"code": -32603, "message": f"Internal error: {str(e)}"},
                id=request.id
            )

    async def _call_handler(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a handler function by tool name"""
        try:
            # Lazy load handlers module
            if self.handlers_cache is None:
                import importlib.util as _ilu
                handlers_path = _AGENT_ROOT / "1_interface" / "skill_handlers.py"
                spec = _ilu.spec_from_file_location("skill_handlers", handlers_path)
                handlers_mod = _ilu.module_from_spec(spec)
                spec.loader.exec_module(handlers_mod)
                self.handlers_cache = handlers_mod.HANDLERS

            # Map tool names to handler names
            tool_to_handler = {
                "maestro": "handle_maestro",
                "skill-code-formatter": "handle_code_formatter",
                "skill-type-checker": "handle_type_checker",
                "skill-unit-test-runner": "handle_unit_tests",
                "skill-e2e-test-runner": "handle_e2e_tests",
                "skill-test-coverage": "handle_coverage",
                "skill-code-analyzer": "handle_code_analyzer",
                "skill-build": "handle_build",
                "skill-quality-gate": "handle_quality_gate",
                "skill-git-workflow": "handle_git_workflow",
                "skill-deploy": "handle_deploy",
            }

            handler_name = tool_to_handler.get(tool_name)
            if not handler_name:
                return {
                    "status": "error",
                    "error": f"No handler for tool: {tool_name}"
                }

            handler = self.handlers_cache.get(handler_name)
            if not handler:
                return {
                    "status": "error",
                    "error": f"Handler not found: {handler_name}"
                }

            # Execute handler (async)
            if asyncio.iscoroutinefunction(handler):
                result_str = await handler(arguments)
            else:
                result_str = handler(arguments)

            # Parse result if it's a JSON string
            if isinstance(result_str, str):
                try:
                    return json.loads(result_str)
                except json.JSONDecodeError:
                    return {"status": "success", "output": result_str}
            else:
                return result_str

        except Exception as e:
            logger.error(f"Handler call error: {e}", exc_info=True)
            raise


async def read_json_rpc_request() -> Optional[JSONRPCRequest]:
    """Read a JSON-RPC request from stdin"""
    try:
        # Read line from stdin
        loop = asyncio.get_event_loop()
        line = await loop.run_in_executor(None, sys.stdin.readline)
        
        if not line:
            return None

        line = line.strip()
        if not line:
            return None

        data = json.loads(line)
        return JSONRPCRequest(**data)
    except json.JSONDecodeError:
        logger.error("Invalid JSON received")
        return None
    except Exception as e:
        logger.error(f"Error reading request: {e}")
        return None


def write_json_rpc_response(response: JSONRPCResponse):
    """Write a JSON-RPC response to stdout"""
    response_dict = asdict(response)
    # Remove None values
    response_dict = {k: v for k, v in response_dict.items() if v is not None}
    print(json.dumps(response_dict))
    sys.stdout.flush()


async def main():
    """Main server loop"""
    logger.info("🎼 Maestro MCP Server (Standalone)")
    logger.info(f"Python: {sys.version}")
    logger.info(f"Root: {_AGENT_ROOT}")
    logger.info("Waiting for connections on stdin...")

    server = MaestroMCPServer()

    # Main loop: read requests from stdin, send responses to stdout
    try:
        while True:
            request = await read_json_rpc_request()
            if request is None:
                # EOF or error
                break

            response = await server.handle_request(request)
            write_json_rpc_response(response)

    except KeyboardInterrupt:
        logger.info("⛔ Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
