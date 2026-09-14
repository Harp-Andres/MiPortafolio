"""
Agent Configuration Package

Centralized configuration management for the Master Orchestrator Agent.
All settings, constants, and defaults are defined in this package.
"""

from agent.config.constants import (
    ProjectConfig,
    SkillDefaults,
    ToolConfig,
    DocumentConfig,
    PortfolioConfig,
    DeploymentConfig,
    ValidationConfig,
    Environment,
    BuildEnvironment,
    OutputFormat,
    project_config,
    skill_defaults,
    tool_config,
    document_config,
    portfolio_config,
    deployment_config,
    validation_config,
    get_config,
    get_project_path,
    get_output_path,
    is_production,
    is_development,
)

__version__ = "0.1.0"

__all__ = [
    "ProjectConfig",
    "SkillDefaults",
    "ToolConfig",
    "DocumentConfig",
    "PortfolioConfig",
    "DeploymentConfig",
    "ValidationConfig",
    "Environment",
    "BuildEnvironment",
    "OutputFormat",
    "project_config",
    "skill_defaults",
    "tool_config",
    "document_config",
    "portfolio_config",
    "deployment_config",
    "validation_config",
    "get_config",
    "get_project_path",
    "get_output_path",
    "is_production",
    "is_development",
]
