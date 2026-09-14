"""
Master Orchestrator Agent - Main Entry Point

Allows running the agent as:
  python -m 1_interface --help
  python -m 1_interface ci
  python -m 1_interface deploy
"""

from agent_1_interface.cli import main_cli

if __name__ == "__main__":
    main_cli()
