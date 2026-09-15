"""
Master Orchestrator Agent - CLI Interface

Main entry point for terminal usage via Typer.

Usage:
  mportafolio-agent ci              # Run CI pipeline
  mportafolio-agent deploy          # Deploy to production
  mportafolio-agent portfolio       # Manage portfolio
  mportafolio-agent test            # Run tests
  mportafolio-agent docs            # Generate documents
  mportafolio-agent --help          # Show help
"""

import sys
import logging
from typing import Optional
from pathlib import Path

import typer
from rich.console import Console
from rich.logging import RichHandler

# Import environment validator
try:
    from agent_5_guardrails.env_validator import EnvironmentValidator, EnvironmentConfigError
except ImportError:
    # Fallback for development
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from agent_5_guardrails.env_validator import EnvironmentValidator, EnvironmentConfigError

# Create Typer app
app = typer.Typer(
    name="mportafolio-agent",
    help="Master Orchestrator Agent for Mi Portafolio",
    no_args_is_help=True,
)

# Rich console for pretty output
console = Console()

# Logger setup
def setup_logging(debug: bool = False) -> logging.Logger:
    """Setup structured logging with Rich handler"""
    level = logging.DEBUG if debug else logging.INFO
    
    # Remove default handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add Rich handler
    handler = RichHandler(
        console=console,
        show_time=True,
        show_level=True,
        show_path=False,
    )
    handler.setLevel(level)
    
    # Configure root logger
    root_logger.setLevel(level)
    root_logger.addHandler(handler)
    
    return logging.getLogger(__name__)


# Startup validation callback
def validate_environment(debug: bool = False) -> None:
    """Validate environment on startup"""
    logger = setup_logging(debug)
    
    try:
        EnvironmentValidator.validate(raise_on_error=True)
        logger.debug("✅ Environment validation passed")
    except EnvironmentConfigError as e:
        console.print(f"\n{e.message}\n", style="bold red")
        sys.exit(1)


# Main callback for all commands
@app.callback()
def main(
    ctx: typer.Context,
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable debug mode with verbose logging"
    ),
) -> None:
    """
    Master Orchestrator Agent for Mi Portafolio
    
    Automates CI/CD, document generation, and portfolio management.
    """
    # Validate environment on startup
    validate_environment(debug=debug)
    
    # Store debug flag in context for subcommands
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug


# ============================================================================
# CI/CD COMMAND
# ============================================================================

@app.command(name="ci")
def ci(
    ctx: typer.Context,
    stages: Optional[str] = typer.Option(
        None,
        "--stages",
        help="Run specific stages (comma-separated): dependencies,types,quality,build,test,sync,security,gates,deploy"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """
    Run complete CI/CD pipeline
    
    Executes full quality gates:
    - Dependency resolution
    - Type checking (TypeScript + Python)
    - Code quality (lint, format)
    - Build compilation
    - Unit tests (Vitest + PyTest)
    - E2E tests (Playwright)
    - Sync verification (Web=DOCX=PDF=Excel)
    - Security scanning
    - Quality gates summary
    
    Example:
      mportafolio-agent ci                              # Full pipeline
      mportafolio-agent ci --stages types,quality,test  # Specific stages
      mportafolio-agent ci --verbose                    # Detailed output
    """
    from agent_1_interface.handlers import handle_ci
    
    logger = logging.getLogger(__name__)
    logger.info("🚀 Starting CI pipeline...")
    
    try:
        handle_ci(
            stages=stages,
            verbose=verbose or ctx.obj.get("debug", False),
        )
        console.print("\n✅ CI pipeline completed successfully\n", style="bold green")
    except Exception as e:
        console.print(f"\n❌ CI pipeline failed: {e}\n", style="bold red")
        logger.exception("CI pipeline error")
        sys.exit(1)


# ============================================================================
# DEPLOYMENT COMMAND
# ============================================================================

@app.command(name="deploy")
def deploy(
    ctx: typer.Context,
    environment: str = typer.Option(
        "production",
        "--env",
        help="Deployment environment: development, staging, production"
    ),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmations"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """
    Deploy to production
    
    Runs full deployment pipeline:
    - Quality gate verification
    - Build artifact deployment
    - GitHub Pages update
    - Post-deployment validation
    
    Example:
      mportafolio-agent deploy                      # Deploy to production
      mportafolio-agent deploy --env staging        # Deploy to staging
      mportafolio-agent deploy --force              # Skip confirmations
    """
    from agent_1_interface.handlers import handle_deploy
    
    logger = logging.getLogger(__name__)
    logger.info(f"🚀 Starting deployment to {environment}...")
    
    try:
        handle_deploy(
            environment=environment,
            force=force,
            verbose=verbose or ctx.obj.get("debug", False),
        )
        console.print(f"\n✅ Deployment to {environment} completed successfully\n", style="bold green")
    except Exception as e:
        console.print(f"\n❌ Deployment failed: {e}\n", style="bold red")
        logger.exception("Deployment error")
        sys.exit(1)


# ============================================================================
# TESTING COMMAND
# ============================================================================

@app.command(name="test")
def test(
    ctx: typer.Context,
    suite: str = typer.Option(
        "all",
        "--suite",
        help="Test suite: all, unit, e2e, backend, frontend"
    ),
    coverage: bool = typer.Option(True, "--coverage/--no-coverage", help="Generate coverage report"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """
    Run test suite
    
    Executes tests:
    - Unit tests (Vitest + PyTest)
    - E2E tests (Playwright)
    - Coverage analysis
    - Test result aggregation
    
    Example:
      mportafolio-agent test                    # All tests
      mportafolio-agent test --suite unit       # Unit tests only
      mportafolio-agent test --suite e2e        # E2E tests
      mportafolio-agent test --no-coverage      # Skip coverage
    """
    from agent_1_interface.handlers import handle_test
    
    logger = logging.getLogger(__name__)
    logger.info(f"🧪 Running {suite} test suite...")
    
    try:
        handle_test(
            suite=suite,
            coverage=coverage,
            verbose=verbose or ctx.obj.get("debug", False),
        )
        console.print(f"\n✅ Test suite completed successfully\n", style="bold green")
    except Exception as e:
        console.print(f"\n❌ Test suite failed: {e}\n", style="bold red")
        logger.exception("Test error")
        sys.exit(1)


# ============================================================================
# DOCUMENT GENERATION COMMAND
# ============================================================================

@app.command(name="docs")
def docs(
    ctx: typer.Context,
    format: str = typer.Option(
        "all",
        "--format",
        help="Document format: all, docx, pdf, excel"
    ),
    output_dir: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory for generated documents"
    ),
    sync_verify: bool = typer.Option(
        True,
        "--verify/--no-verify",
        help="Verify sync between all formats"
    ),
) -> None:
    """
    Generate CV/Portfolio documents
    
    Generates documents in multiple formats:
    - DOCX (ATS-optimized for job applications)
    - PDF (visually formatted)
    - Excel (structured data)
    
    Optionally verifies sync (all formats match).
    
    Example:
      mportafolio-agent docs                    # Generate all formats
      mportafolio-agent docs --format docx      # DOCX only
      mportafolio-agent docs --format pdf       # PDF only
      mportafolio-agent docs -o ./output        # Custom output dir
    """
    from agent_1_interface.handlers import handle_docs
    
    logger = logging.getLogger(__name__)
    logger.info(f"📄 Generating {format} documents...")
    
    try:
        handle_docs(
            format=format,
            output_dir=output_dir,
            sync_verify=sync_verify,
        )
        console.print(f"\n✅ Documents generated successfully\n", style="bold green")
    except Exception as e:
        console.print(f"\n❌ Document generation failed: {e}\n", style="bold red")
        logger.exception("Document generation error")
        sys.exit(1)


# ============================================================================
# PORTFOLIO COMMAND
# ============================================================================

@app.command(name="portfolio")
def portfolio(
    ctx: typer.Context,
) -> None:
    """
    Manage portfolio projects, skills, and certificates
    
    Subcommands:
      portfolio add-project      Add new project
      portfolio add-skill        Add skill category
      portfolio add-cert         Add certificate
      portfolio list             List all items
    
    Example:
      mportafolio-agent portfolio add-project --name "MyProject" --tech "React,TypeScript"
      mportafolio-agent portfolio list
    """
    # This will be handled by subcommands
    pass


@app.command(name="add-project")
def add_project(
    name: str = typer.Argument(..., help="Project name"),
    description: Optional[str] = typer.Option(None, "--desc", "-d", help="Project description"),
    tech: Optional[str] = typer.Option(None, "--tech", "-t", help="Technologies (comma-separated)"),
    link: Optional[str] = typer.Option(None, "--link", "-l", help="Project URL"),
    github: Optional[str] = typer.Option(None, "--github", help="GitHub repository URL"),
) -> None:
    """
    Add new portfolio project
    
    Example:
      mportafolio-agent add-project "MyProject" --tech "React,TypeScript" --link "https://example.com"
    """
    from agent_1_interface.handlers import handle_add_project
    
    logger = logging.getLogger(__name__)
    logger.info(f"➕ Adding project: {name}")
    
    try:
        handle_add_project(
            name=name,
            description=description,
            tech=tech,
            link=link,
            github=github,
        )
        console.print(f"\n✅ Project '{name}' added successfully\n", style="bold green")
    except Exception as e:
        console.print(f"\n❌ Failed to add project: {e}\n", style="bold red")
        logger.exception("Add project error")
        sys.exit(1)


# ============================================================================
# VERSION & HELP COMMANDS
# ============================================================================

@app.command(name="version")
def version() -> None:
    """Show agent version"""
    from agent_1_interface import __version__
    console.print(f"mportafolio-agent version {__version__}")


@app.command(name="env-check")
def env_check(
    ctx: typer.Context,
) -> None:
    """
    Check environment configuration
    
    Validates:
    - .env file exists
    - Required keys present
    - LLM provider configured
    - GitHub credentials valid
    """
    logger = logging.getLogger(__name__)
    
    try:
        EnvironmentValidator.validate(raise_on_error=True)
        EnvironmentValidator.print_summary()
        console.print("✅ Environment is properly configured", style="bold green")
    except EnvironmentConfigError as e:
        console.print(f"\n{e.message}\n", style="bold red")
        sys.exit(1)


# ============================================================================
# SETUP & INFRASTRUCTURE COMMANDS (Setup Agent)
# ============================================================================

@app.command(name="setup-init")
def setup_init() -> None:
    """
    Initialize portable agentic ecosystem
    
    Generates:
    - .env.example with all required variables
    - .mcp.json for IDE/Copilot integration
    - Agent layer directories and __init__.py
    - Validation checklist
    
    Example:
      mportafolio-agent setup-init
    """
    from agent_setup_agent import setup_init as setup_agent_init
    
    console.print("\n[bold cyan]🚀 Initializing Portable Agentic Ecosystem[/bold cyan]\n")
    
    try:
        setup_agent_init()
        console.print("[bold green]✅ Setup Complete![/bold green]\n")
    except Exception as e:
        console.print(f"\n❌ Setup failed: {e}\n", style="bold red")
        sys.exit(1)


@app.command(name="setup-status")
def setup_status() -> None:
    """
    Display setup status and architecture
    
    Shows:
    - 7-layer architecture diagram
    - Validation checklist (pass/fail)
    - Configuration summary
    
    Example:
      mportafolio-agent setup-status
    """
    from agent_setup_agent import status
    
    try:
        status()
    except Exception as e:
        console.print(f"\n❌ Status check failed: {e}\n", style="bold red")
        sys.exit(1)


@app.command(name="setup-validate")
def setup_validate() -> None:
    """
    Validate all infrastructure components
    
    Checks:
    - 7-layer directory structure
    - Configuration files
    - Environment variables
    - MCP server configuration
    
    Example:
      mportafolio-agent setup-validate
    """
    from agent_setup_agent import validate
    
    try:
        validate()
    except Exception as e:
        console.print(f"\n❌ Validation failed: {e}\n", style="bold red")
        sys.exit(1)


@app.command(name="setup-mcp-check")
def setup_mcp_check() -> None:
    """
    Verify MCP server registration
    
    Validates:
    - .mcp.json exists and is valid JSON
    - Server command is executable
    - Supported IDEs listed
    
    Example:
      mportafolio-agent setup-mcp-check
    """
    from agent_setup_agent import check_mcp
    
    try:
        check_mcp()
    except Exception as e:
        console.print(f"\n❌ MCP check failed: {e}\n", style="bold red")
        sys.exit(1)


@app.command(name="setup-list-skills")
def setup_list_skills() -> None:
    """
    List all registered skills by domain
    
    Domains:
    - testing: Unit & E2E test runners
    - building: Build & compilation skills
    - quality: Linting, formatting, type checking
    - deployment: GitHub Pages, release management
    - documents: PDF, DOCX, Excel generation
    - infrastructure: GitHub, workflows, CI/CD
    
    Example:
      mportafolio-agent setup-list-skills
    """
    from agent_setup_agent import list_skills
    
    try:
        list_skills()
    except Exception as e:
        console.print(f"\n❌ List skills failed: {e}\n", style="bold red")
        sys.exit(1)


@app.command(name="setup-show-architecture")
def setup_show_architecture() -> None:
    """
    Display 7-layer architecture in detail
    
    Shows:
    - Layer 1: Interface (CLI + MCP Server)
    - Layer 2: Orchestrator (ReAct + LLM Factory)
    - Layer 3: Memory (Conversation + RAG + Checkpoints)
    - Layer 4: Skills (28+ autonomous skills)
    - Layer 5: Guardrails (Security + Validation)
    - Layer 6: Telemetry (Logging + Metrics)
    - Layer 7: State (Persistence + Recovery)
    
    Example:
      mportafolio-agent setup-show-architecture
    """
    from agent_setup_agent import show_architecture
    
    try:
        show_architecture()
    except Exception as e:
        console.print(f"\n❌ Show architecture failed: {e}\n", style="bold red")
        sys.exit(1)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main_cli() -> None:
    """Main entry point for CLI"""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n⚠️  Operation cancelled by user\n", style="bold yellow")
        sys.exit(130)
    except Exception as e:
        console.print(f"\n❌ Unexpected error: {e}\n", style="bold red")
        logging.getLogger(__name__).exception("Unexpected error")
        sys.exit(1)


if __name__ == "__main__":
    main_cli()
