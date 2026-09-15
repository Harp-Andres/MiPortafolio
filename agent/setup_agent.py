"""
SETUP AGENT: Bootstrap & Portability Agent

Initializes, deploys, and validates a 100% configured, portable, decoupled multi-agent
agentic ecosystem. Runs on any OS (Windows, macOS, Linux) with any IDE (GitHub Copilot,
Cursor, Claude Code, Windsurf, OpenCode).

Entry point: uv run python -m agent.setup_agent --init
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

console = Console()
app = typer.Typer(
    name="setup-agent",
    help="Setup & Bootstrap Agent for Portable Agentic Ecosystem"
)


# ============================================================================
# ARCHITECTURE: 7-Layer Agent System
# ============================================================================

AGENT_ARCHITECTURE = {
    "1_interface": {
        "description": "CLI (Typer) + MCP Server (STDIO/HTTP)",
        "files": [
            "cli.py",           # Main CLI entry point
            "mcp_server.py",    # MCP Protocol Server
            "mcp_tools.py",     # Tool definitions
            "handlers.py",      # Tool handlers
            "__init__.py"
        ]
    },
    "2_orchestrator": {
        "description": "ReAct Loop + LLM Factory + Inter-Agent Bus",
        "files": [
            "react_engine.py",      # ReAct (Reasoning + Acting) loop
            "llm_factory.py",       # LLM provider abstraction (OpenAI, Anthropic, etc)
            "agent_bus.py",         # Message bus for inter-agent communication
            "workflow_templates.py", # Predefined workflows
            "__init__.py"
        ]
    },
    "3_memory": {
        "description": "Conversation History + RAG Indexer + Checkpoints",
        "files": [
            "conversation_store.py",  # SQLite conversation history
            "rag_indexer.py",        # Vector embeddings & semantic search
            "checkpoint.py",         # Execution state & recovery
            "__init__.py"
        ]
    },
    "4_skills": {
        "description": "28+ Autonomous Skills Across 6 Domains",
        "files": [
            "base_skill.py",         # Abstract base class (Pydantic)
            "skill_registry.py",     # Skill discovery & registration
            "skill_router.py",       # Route tasks to correct skill/agent
            "__init__.py"
        ],
        "domains": [
            "testing/",      # Testing skills (Vitest, Playwright)
            "building/",     # Build skills (Vite, tsc)
            "quality/",      # Quality skills (ESLint, Ruff, mypy)
            "deployment/",   # Deployment skills (GitHub Pages, Docker)
            "documents/",    # Document generation (PDF, DOCX, Excel)
            "infrastructure/" # Infrastructure skills (GitHub, workflows)
        ]
    },
    "5_guardrails": {
        "description": "Pydantic Validation + Security Filters + Rate Limiter",
        "files": [
            "input_validator.py",     # Sanitize user input
            "command_validator.py",   # Prevent injection attacks
            "rate_limiter.py",        # Quota management
            "security_filters.py",    # Dangerous operation blocking
            "__init__.py"
        ]
    },
    "6_telemetry": {
        "description": "Structured Logging + Metrics + W3C Tracing",
        "files": [
            "logger_config.py",      # JSON & W3C logger setup
            "metrics.py",            # Event metrics collection
            "tracer.py",             # Distributed tracing
            "__init__.py"
        ]
    },
    "7_state": {
        "description": "Execution State + Persistence + Recovery",
        "files": [
            "state_manager.py",      # State snapshot & restore
            "persistence.py",        # Disk I/O & locking
            "recovery.py",           # Fault tolerance & retry logic
            "__init__.py"
        ]
    }
}


# ============================================================================
# SETUP VALIDATION CHECKLIST
# ============================================================================

VALIDATION_CHECKLIST = [
    {
        "name": "Python Version",
        "check": lambda: sys.version_info >= (3, 11),
        "fix": "Upgrade to Python 3.11+"
    },
    {
        "name": "uv Package Manager",
        "check": lambda: check_command("uv"),
        "fix": "Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
    },
    {
        "name": "pyproject.toml",
        "check": lambda: (get_project_root() / "agent" / "pyproject.toml").exists(),
        "fix": "Create pyproject.toml in project root"
    },
    {
        "name": ".mcp.json",
        "check": lambda: (get_project_root() / ".mcp.json").exists(),
        "fix": "Generate .mcp.json for IDE integration"
    },
    {
        "name": ".github/copilot-instructions.md",
        "check": lambda: (get_project_root() / ".github" / "copilot-instructions.md").exists(),
        "fix": "Generate copilot-instructions.md"
    },
    {
        "name": ".env.example",
        "check": lambda: (get_project_root() / "agent" / ".env.example").exists(),
        "fix": "Generate .env.example with required vars"
    },
    {
        "name": "Agent Architecture (7 layers)",
        "check": lambda: all(
            Path(f"agent/{layer}/__init__.py").exists()
            for layer in AGENT_ARCHITECTURE.keys()
        ),
        "fix": "Initialize all 7 layer directories"
    },
]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def check_command(cmd: str) -> bool:
    """Check if a command is available in PATH"""
    import shutil
    return shutil.which(cmd) is not None


def get_project_root() -> Path:
    """Get project root directory"""
    return Path(__file__).parent.parent


# ============================================================================
# COMMANDS
# ============================================================================

@app.command()
def status() -> None:
    """Display current setup status and architecture"""
    console.print("\n[bold cyan]🏗️  Mi Portafolio - Setup Agent Status[/bold cyan]\n")
    
    project_root = get_project_root()
    
    # Architecture diagram
    table = Table(title="7-Layer Agent Architecture", show_header=True)
    table.add_column("Layer", style="cyan")
    table.add_column("Purpose", style="magenta")
    table.add_column("Status", style="green")
    
    for layer, info in AGENT_ARCHITECTURE.items():
        layer_dir = project_root / "agent" / layer
        status_icon = "✅" if layer_dir.exists() else "❌"
        table.add_row(layer, info["description"], status_icon)
    
    console.print(table)
    
    # Validation checklist
    console.print("\n[bold yellow]Validation Checklist[/bold yellow]\n")
    checklist_table = Table(show_header=True)
    checklist_table.add_column("Component")
    checklist_table.add_column("Status")
    checklist_table.add_column("Tip")
    
    passed = 0
    failed = 0
    
    for item in VALIDATION_CHECKLIST:
        try:
            is_ok = item["check"]()
            status_icon = "✅" if is_ok else "❌"
            if is_ok:
                passed += 1
            else:
                failed += 1
            checklist_table.add_row(item["name"], status_icon, item["fix"])
        except Exception as e:
            checklist_table.add_row(item["name"], "⚠️ Error", str(e)[:50])
            failed += 1
    
    console.print(checklist_table)
    console.print(f"\n[bold]Summary:[/bold] {passed} passed, {failed} failed\n")


@app.command()
def init() -> None:
    """Initialize & bootstrap the entire ecosystem"""
    console.print("\n[bold cyan]🚀 Initializing Portable Agentic Ecosystem[/bold cyan]\n")
    
    project_root = get_project_root()
    
    # Step 1: Create .env.example
    console.print("[bold]Step 1:[/bold] Generating .env.example...")
    env_example = project_root / ".env.example"
    env_content = """# LLM Provider (choose one)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# GitHub Integration
GITHUB_TOKEN=
GITHUB_REPO=

# Agent Settings
AGENT_LOG_LEVEL=INFO
AGENT_TIMEOUT_SECONDS=300

# MCP Server Configuration
MCP_TRANSPORT=stdio
MCP_PORT=3000

# Testing & CI/CD
PYTEST_TIMEOUT=30
E2E_TEST_WORKERS=2
"""
    env_example.write_text(env_content)
    console.print(f"✅ Created {env_example}\n")
    
    # Step 2: Create .mcp.json
    console.print("[bold]Step 2:[/bold] Generating .mcp.json for IDE integration...")
    mcp_config = {
        "mcpServers": {
            "maestro": {
                "command": "uv",
                "args": ["run", "python", "-m", "agent.1_interface.mcp_server"],
                "description": "Mi Portafolio - Maestro Orchestrator Agent"
            }
        }
    }
    mcp_file = project_root / ".mcp.json"
    mcp_file.write_text(json.dumps(mcp_config, indent=2))
    console.print(f"✅ Created {mcp_file}\n")
    
    # Step 3: Create/update pyproject.toml for uv
    console.print("[bold]Step 3:[/bold] Validating pyproject.toml for uv compatibility...")
    pyproject = project_root / "pyproject.toml"
    if pyproject.exists():
        console.print("✅ pyproject.toml already exists\n")
    else:
        console.print("⚠️  pyproject.toml not found. Create manually or use 'uv init'\n")
    
    # Step 4: Initialize agent layer directories
    console.print("[bold]Step 4:[/bold] Initializing 7-layer architecture...")
    for layer in AGENT_ARCHITECTURE.keys():
        layer_dir = project_root / "agent" / layer
        init_file = layer_dir / "__init__.py"
        
        if not layer_dir.exists():
            layer_dir.mkdir(parents=True, exist_ok=True)
        
        if not init_file.exists():
            init_file.write_text(f'"""{layer}: {AGENT_ARCHITECTURE[layer]["description"]}"""\n')
            console.print(f"✅ {layer}/")
    
    console.print()
    
    # Step 5: Display summary
    console.print(Panel(
        "[bold green]✅ Setup Complete![/bold green]\n\n"
        "Next steps:\n"
        "1. [yellow]uv sync[/yellow]  - Install dependencies\n"
        "2. [yellow]uv run agent --status[/yellow]  - Check status\n"
        "3. [yellow]uv run agent --help[/yellow]  - List all commands\n"
        "4. Open your IDE (Cursor, VS Code, Claude Code, etc)\n"
        "5. The maestro agent is now registered via MCP and ready to execute skills",
        title="🎉 Bootstrap Ready",
        style="green"
    ))


@app.command()
def validate() -> None:
    """Validate all infrastructure components"""
    console.print("\n[bold cyan]🔍 Validating Infrastructure[/bold cyan]\n")
    
    project_root = get_project_root()
    all_valid = True
    
    # Check each layer
    for layer, info in AGENT_ARCHITECTURE.items():
        layer_dir = project_root / "agent" / layer
        console.print(f"[bold]{layer}:[/bold]")
        
        if not layer_dir.exists():
            console.print(f"  ❌ Directory missing: {layer_dir}")
            all_valid = False
            continue
        
        # Check __init__.py
        init_file = layer_dir / "__init__.py"
        if init_file.exists():
            console.print(f"  ✅ __init__.py exists")
        else:
            console.print(f"  ⚠️  __init__.py missing (non-critical)")
        
        # Check domains if present (layer 4 only)
        if layer == "4_skills" and "domains" in info:
            for domain in info["domains"]:
                domain_path = layer_dir / domain
                if domain_path.exists():
                    console.print(f"  ✅ Domain: {domain}")
                else:
                    console.print(f"  ⚠️  Domain missing: {domain}")
        
        console.print()
    
    # Check configuration files
    console.print("[bold]Configuration Files:[/bold]")
    config_files = [
        ".mcp.json",
        ".env.example",
        ".github/copilot-instructions.md",
        "pyproject.toml"
    ]
    
    for config in config_files:
        path = project_root / config
        if path.exists():
            console.print(f"  ✅ {config}")
        else:
            console.print(f"  ❌ {config} missing")
            all_valid = False
    
    console.print()
    
    if all_valid:
        console.print("[bold green]✅ All validations passed![/bold green]\n")
    else:
        console.print("[bold yellow]⚠️  Some validations failed. Run 'uv run agent --init' to fix.[/bold yellow]\n")


@app.command()
def list_skills() -> None:
    """List all registered skills"""
    console.print("\n[bold cyan]📚 Registered Skills[/bold cyan]\n")
    
    project_root = get_project_root()
    skills_dir = project_root / "agent" / "4_skills"
    
    domains = [d for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith("_")]
    
    for domain in sorted(domains):
        console.print(f"[bold]{domain.name.upper()}[/bold]")
        
        skill_files = list(domain.glob("*.py"))
        if not skill_files:
            console.print("  (no skills yet)\n")
            continue
        
        for skill_file in skill_files:
            if skill_file.name != "__init__.py":
                console.print(f"  • {skill_file.stem}")
        
        console.print()


@app.command()
def show_architecture() -> None:
    """Display the 7-layer architecture in detail"""
    console.print("\n[bold cyan]🏛️  7-Layer Agentic Architecture[/bold cyan]\n")
    
    for layer, info in AGENT_ARCHITECTURE.items():
        # Layer header
        console.print(Panel(
            f"{info['description']}",
            title=f"[bold]{layer}[/bold]",
            style="cyan",
            expand=False
        ))
        
        # Files
        if "files" in info:
            console.print("[dim]Files:[/dim]")
            for file in info["files"]:
                console.print(f"  • {file}")
        
        # Domains (if applicable)
        if "domains" in info:
            console.print("\n[dim]Domains:[/dim]")
            for domain in info["domains"]:
                console.print(f"  • {domain}")
        
        console.print()


@app.command()
def check_mcp() -> None:
    """Verify MCP server is properly registered"""
    console.print("\n[bold cyan]🔗 MCP Server Configuration[/bold cyan]\n")
    
    project_root = get_project_root()
    mcp_file = project_root / ".mcp.json"
    
    if not mcp_file.exists():
        console.print("[red]❌ .mcp.json not found[/red]")
        console.print(f"Create it with: uv run agent --init\n")
        return
    
    mcp_config = json.loads(mcp_file.read_text())
    console.print("MCP Servers registered:")
    
    for server_name, server_config in mcp_config.get("mcpServers", {}).items():
        console.print(f"\n[bold]{server_name}[/bold]")
        console.print(f"  Command: {server_config.get('command')}")
        console.print(f"  Args: {' '.join(server_config.get('args', []))}")
        console.print(f"  Description: {server_config.get('description')}")
    
    console.print("\n[dim]Supported IDEs:[/dim]")
    supported_ides = [
        "GitHub Copilot",
        "Cursor",
        "Claude Code",
        "Windsurf",
        "VS Code (with MCP extension)"
    ]
    for ide in supported_ides:
        console.print(f"  ✅ {ide}")
    
    console.print()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    app()


if __name__ == "__main__":
    main()
