#!/usr/bin/env python3
"""
Safely merge portfolio-agent into existing .mcp.json

This script implements NON-DESTRUCTIVE merging:
- Preserves existing MCPs configured in .mcp.json
- Adds or updates portfolio-agent config
- Works on Windows, Linux, Mac
- Provides clear feedback on changes

Usage:
  python scripts/merge_mcp_config.py
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional


def get_portfolio_agent_config() -> Dict[str, Any]:
    """Get the portfolio-agent MCP configuration"""
    return {
        "command": "uv",
        "args": ["--directory", "agent", "run", "python", "-m", "1_interface.mcp_server"],
        "disabled": False,
        "autoStart": True,
        "env": {
            "PYTHONPATH": "${workspaceFolder}/agent"
        }
    }


def load_mcp_config(mcp_path: Path) -> Dict[str, Any]:
    """Load existing .mcp.json or create new structure"""
    if mcp_path.exists():
        try:
            with open(mcp_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"⚠️  Warning: Failed to parse existing .mcp.json: {e}", file=sys.stderr)
            print(f"   Backing up to .mcp.json.bak and creating new config", file=sys.stderr)
            # Backup corrupted file
            backup_path = mcp_path.with_suffix(".json.bak")
            mcp_path.rename(backup_path)
            return {"mcpServers": {}}
    else:
        return {"mcpServers": {}}


def save_mcp_config(mcp_path: Path, config: Dict[str, Any]) -> None:
    """Save .mcp.json with proper formatting"""
    with open(mcp_path, "w") as f:
        json.dump(config, f, indent=2)
    # Add newline at end of file (standard practice)
    mcp_path.write_text(mcp_path.read_text().rstrip() + "\n")


def merge_mcp_config(
    repo_root: Optional[Path] = None,
    verbose: bool = True
) -> bool:
    """
    Merge portfolio-agent into .mcp.json

    Args:
        repo_root: Repository root path (defaults to current directory)
        verbose: Print status messages

    Returns:
        True if merge successful, False otherwise
    """
    if repo_root is None:
        repo_root = Path.cwd()

    mcp_path = repo_root / ".mcp.json"
    portfolio_config = get_portfolio_agent_config()

    try:
        # Load existing config
        config = load_mcp_config(mcp_path)

        # Ensure mcpServers key exists
        if "mcpServers" not in config:
            config["mcpServers"] = {}

        # Check if portfolio-agent already exists
        old_portfolio = config["mcpServers"].get("portfolio-agent")

        # Merge portfolio-agent
        config["mcpServers"]["portfolio-agent"] = portfolio_config

        # Save back
        save_mcp_config(mcp_path, config)

        # Print feedback
        if verbose:
            if not mcp_path.exists():
                print("✨ .mcp.json created successfully")
            elif old_portfolio:
                print("📝 portfolio-agent config updated in .mcp.json")
            else:
                print("✅ portfolio-agent config added to .mcp.json")

            other_mcps = [k for k in config["mcpServers"].keys() if k != "portfolio-agent"]
            if other_mcps:
                print(f"   Preserved existing MCPs: {', '.join(other_mcps)}")
            else:
                print("   (No other MCPs in configuration)")

        return True

    except Exception as e:
        print(f"❌ Error during .mcp.json merge: {e}", file=sys.stderr)
        return False


def main():
    """CLI entry point"""
    print("Merging portfolio-agent into .mcp.json...\n")

    success = merge_mcp_config(verbose=True)

    if success:
        print("\n✅ MCP configuration merge completed successfully")
        print("   IDEs will auto-detect portfolio-agent on next reload")
        sys.exit(0)
    else:
        print("\n❌ MCP configuration merge failed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
