"""
Master Orchestrator Agent - Layer 1: Interface

Provides CLI and MCP server interfaces for the agent.

Modules:
  - cli.py: Typer CLI for terminal usage
  - mcp_server.py: MCP protocol server for IDE integration
  - handlers.py: Request handlers for different commands
"""

__version__ = "0.1.0"
__all__ = ["cli", "mcp_server", "handlers"]


# Make version accessible
def get_version() -> str:
    """Get agent version"""
    return __version__
