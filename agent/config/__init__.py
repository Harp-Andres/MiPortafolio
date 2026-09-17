"""
Agent Configuration Package

Centralized configuration management for the Master Orchestrator Agent.
All settings, constants, and defaults are defined in this package.
"""

# File-path based imports (workaround for numbered directories)
import importlib.util as _ilu
from pathlib import Path

_cfg_root = Path(__file__).parent
_constants_spec = _ilu.spec_from_file_location("constants", _cfg_root / "constants.py")
_constants_mod = _ilu.module_from_spec(_constants_spec)
_constants_spec.loader.exec_module(_constants_mod)

# Re-export all public items
ProjectConfig = _constants_mod.ProjectConfig
SkillDefaults = _constants_mod.SkillDefaults
ToolConfig = _constants_mod.ToolConfig
DocumentConfig = _constants_mod.DocumentConfig
PortfolioConfig = _constants_mod.PortfolioConfig
DeploymentConfig = _constants_mod.DeploymentConfig
ValidationConfig = _constants_mod.ValidationConfig
Environment = _constants_mod.Environment
BuildEnvironment = _constants_mod.BuildEnvironment
OutputFormat = _constants_mod.OutputFormat
project_config = _constants_mod.project_config
skill_defaults = _constants_mod.skill_defaults
tool_config = _constants_mod.tool_config
document_config = _constants_mod.document_config
portfolio_config = _constants_mod.portfolio_config
deployment_config = _constants_mod.deployment_config
validation_config = _constants_mod.validation_config
get_config = _constants_mod.get_config
get_project_path = _constants_mod.get_project_path
get_output_path = _constants_mod.get_output_path
is_production = _constants_mod.is_production
is_development = _constants_mod.is_development

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
