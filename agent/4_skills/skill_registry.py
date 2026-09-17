"""
Skill Registry - Central registry for all 28 skills

Dynamically loads all skill classes from subdirectories and provides:
- Skill lookup by name
- Skill metadata (name, description, inputs, outputs)
- Instantiation with proper context
- MCP tool schema generation

Skills are organized by category:
- Infrastructure: type_checker, build_orchestrator, dependency_resolver, quality_gate_runner
- Testing: unit_test_runner, e2e_test_runner, coverage_analyzer, test_aggregator
- Documents: pdf_generator, docx_generator, excel_generator, cv_data_validator, sync_verifier
- Deployment: github_pages_deployer, git_workflow_manager, release_orchestrator, git_branch_creator
- Portfolio: certificate_manager, experience_tracker, portfolio_updater, skills_manager
- Quality: linter_checker, code_formatter, performance_monitor
- Backend: api_validator, backend_server, backend_test_runner
"""

import logging
import importlib
import importlib.util
from pathlib import Path
from typing import Dict, Type, Optional, List, Any
from dataclasses import dataclass
import sys

# Load base_skill using importlib to avoid relative import issues
_SKILLS_ROOT = Path(__file__).parent
_base_skill_path = _SKILLS_ROOT / "base_skill.py"
_spec = importlib.util.spec_from_file_location("base_skill", _base_skill_path)
_base_skill_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_base_skill_mod)
BaseSkill = _base_skill_mod.BaseSkill

# Also load logger_helper
_logger_helper_path = _SKILLS_ROOT / "logger_helper.py"
_spec_lh = importlib.util.spec_from_file_location("logger_helper", _logger_helper_path)
_logger_helper_mod = importlib.util.module_from_spec(_spec_lh)
_spec_lh.loader.exec_module(_logger_helper_mod)
get_logger = _logger_helper_mod.get_logger

logger = get_logger(__name__)


@dataclass
class SkillMetadata:
    """Metadata for a skill"""
    name: str
    description: str
    category: str
    skill_class: Type[BaseSkill]
    module_name: str


class SkillRegistry:
    """Central registry for all 28 portfolio skills"""

    # Singleton instance
    _instance: Optional['SkillRegistry'] = None
    
    # Define all skills with their categories
    SKILL_DEFINITIONS = {
        # Infrastructure Skills (4)
        "type_checker": ("infrastructure", "TypeChecker"),
        "build_orchestrator": ("infrastructure", "BuildOrchestrator"),
        "dependency_resolver": ("infrastructure", "DependencyResolver"),
        "quality_gate_runner": ("infrastructure", "QualityGateRunner"),
        
        # Testing Skills (4)
        "unit_test_runner": ("testing", "UnitTestRunner"),
        "e2e_test_runner": ("testing", "E2ETestRunner"),
        "coverage_analyzer": ("testing", "CoverageAnalyzer"),
        "test_aggregator": ("testing", "TestAggregator"),
        
        # Document Skills (5)
        "pdf_generator": ("documents", "PdfGenerator"),
        "docx_generator": ("documents", "DocxGenerator"),
        "excel_generator": ("documents", "ExcelGenerator"),
        "cv_data_validator": ("documents", "CVDataValidator"),
        "sync_verifier": ("documents", "SyncVerifier"),
        
        # Deployment Skills (4)
        "github_pages_deployer": ("deployment", "GitHubPagesDeployer"),
        "git_workflow_manager": ("deployment", "GitWorkflowManager"),
        "release_orchestrator": ("deployment", "ReleaseOrchestrator"),
        "git_branch_creator": ("deployment", "GitBranchCreator"),
        
        # Portfolio Skills (4)
        "certificate_manager": ("portfolio", "CertificateManager"),
        "experience_tracker": ("portfolio", "ExperienceTracker"),
        "portfolio_updater": ("portfolio", "PortfolioUpdater"),
        "skills_manager": ("portfolio", "SkillsManager"),
        
        # Quality Skills (3)
        "linter_checker": ("quality", "LinterChecker"),
        "code_formatter": ("quality", "CodeFormatter"),
        "performance_monitor": ("quality", "PerformanceMonitor"),
        
        # Backend Skills (3)
        "api_validator": ("backend", "ApiValidator"),
        "backend_server": ("backend", "BackendServer"),
        "backend_test_runner": ("backend", "BackendTestRunner"),
    }

    def __init__(self):
        """Initialize skill registry and load all skills"""
        self.skills: Dict[str, SkillMetadata] = {}
        self._load_all_skills()

    @classmethod
    def get_instance(cls) -> 'SkillRegistry':
        """Get or create singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_all_skills(self) -> None:
        """Load all skill classes from subdirectories using file paths (avoids numbered-dir import restriction)"""
        skills_root = Path(__file__).parent

        for skill_name, (category, class_name) in self.SKILL_DEFINITIONS.items():
            try:
                module_file = skills_root / category / f"{_snake_to_module(skill_name)}.py"
                if not module_file.exists():
                    logger.warning(f"Skill file not found: {module_file}")
                    continue

                # Load by file path to bypass Python's numbered-directory restriction
                spec = importlib.util.spec_from_file_location(
                    f"_skill_{category}_{skill_name}", module_file
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                skill_class = getattr(module, class_name, None)
                if skill_class is None:
                    logger.warning(f"Skill class '{class_name}' not found in {module_file}")
                    continue

                metadata = SkillMetadata(
                    name=skill_name,
                    description=getattr(skill_class, "SKILL_DESCRIPTION", ""),
                    category=category,
                    skill_class=skill_class,
                    module_name=str(module_file),
                )

                self.skills[skill_name] = metadata
                logger.debug(f"✓ Loaded skill: {skill_name} ({category})")

            except Exception as e:
                logger.warning(f"Could not load skill '{skill_name}': {e}")

        logger.info(f"Loaded {len(self.skills)}/{len(self.SKILL_DEFINITIONS)} skills")

    def get_skill(self, skill_name: str) -> Optional[SkillMetadata]:
        """Get skill metadata by name"""
        return self.skills.get(skill_name.lower())

    def get_all_skills(self) -> Dict[str, SkillMetadata]:
        """Get all registered skills"""
        return self.skills.copy()

    def get_skills_by_category(self, category: str) -> Dict[str, SkillMetadata]:
        """Get all skills in a category"""
        return {
            name: metadata
            for name, metadata in self.skills.items()
            if metadata.category == category
        }

    def get_categories(self) -> List[str]:
        """Get list of all skill categories"""
        return sorted(set(metadata.category for metadata in self.skills.values()))

    def instantiate_skill(
        self, skill_name: str, workspace_root: Optional[Path] = None
    ) -> Optional[BaseSkill]:
        """
        Instantiate a skill instance

        Args:
            skill_name: Name of skill to instantiate
            workspace_root: Root directory for workspace (defaults to cwd)

        Returns:
            Instantiated skill or None if not found
        """
        metadata = self.get_skill(skill_name)
        if not metadata:
            logger.error(f"Skill not found: {skill_name}")
            return None

        try:
            skill_instance = metadata.skill_class(workspace_root=workspace_root)
            logger.debug(f"Instantiated skill: {skill_name}")
            return skill_instance
        except Exception as e:
            logger.error(f"Failed to instantiate skill '{skill_name}': {e}", exc_info=True)
            return None

    def describe_skill(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """
        Generate MCP tool schema for a skill

        Returns:
            Tool definition dict or None if skill not found
        """
        metadata = self.get_skill(skill_name)
        if not metadata:
            return None

        skill_class = metadata.skill_class
        return {
            "name": f"skill-{skill_name}",
            "description": metadata.description,
            "category": metadata.category,
            "required_tools": getattr(skill_class, "REQUIRED_TOOLS", []),
            "required_env_vars": getattr(skill_class, "REQUIRED_ENV_VARS", []),
        }

    def validate_skill_exists(self, skill_name: str) -> bool:
        """Check if a skill is registered"""
        return skill_name.lower() in self.skills

    def list_skills_for_mcp(self) -> List[Dict[str, Any]]:
        """
        Generate list of skill tools for MCP exposure

        Returns:
            List of skill tool definitions
        """
        tools = []
        for skill_name, metadata in self.skills.items():
            tools.append({
                "name": f"skill-{skill_name}",
                "description": metadata.description,
                "category": metadata.category,
            })
        return tools


def _snake_to_module(name: str) -> str:
    """Convert skill_name to module_name (snake_case to snake_case)"""
    return name.lower()


# Singleton functions for convenience
def get_skill_registry() -> SkillRegistry:
    """Get global skill registry instance"""
    return SkillRegistry.get_instance()


def get_skill_metadata(skill_name: str) -> Optional[SkillMetadata]:
    """Get metadata for a skill"""
    return get_skill_registry().get_skill(skill_name)


def instantiate_skill(
    skill_name: str, workspace_root: Optional[Path] = None
) -> Optional[BaseSkill]:
    """Instantiate a skill"""
    return get_skill_registry().instantiate_skill(skill_name, workspace_root)


def list_all_skills() -> Dict[str, SkillMetadata]:
    """List all available skills"""
    return get_skill_registry().get_all_skills()


def list_skills_by_category(category: str) -> Dict[str, SkillMetadata]:
    """List all skills in a category"""
    return get_skill_registry().get_skills_by_category(category)
