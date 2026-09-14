"""
Configuration Constants and Settings

Centralized configuration for the Master Orchestrator Agent.
All hardcoded values, paths, and domain-specific settings should be defined here.

This enables portability and agnósticismo de datos: agents can be used with
different projects by only changing configuration, without modifying code.
"""

import os
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass, field
from enum import Enum


class Environment(str, Enum):
    """Execution environments"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class BuildEnvironment(str, Enum):
    """Build environments"""
    DEV = "development"
    STAGING = "staging"
    PROD = "production"


class OutputFormat(str, Enum):
    """Document output formats"""
    DOCX = "docx"
    PDF = "pdf"
    EXCEL = "excel"
    MARKDOWN = "markdown"
    JSON = "json"


# ============================================================================
# PROJECT CONFIGURATION
# ============================================================================

@dataclass
class ProjectConfig:
    """Project-specific configuration"""
    
    # Project identification
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "portfolio-project")
    PROJECT_DESCRIPTION: str = os.getenv("PROJECT_DESCRIPTION", "Agentic portfolio system")
    
    # GitHub configuration
    GITHUB_REPO: str = os.getenv("GITHUB_REPO", "username/repo")
    GITHUB_USER: str = os.getenv("GITHUB_USER", "username")
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    
    # Repository paths
    WORKSPACE_ROOT: Path = Path(os.getenv("WORKSPACE_ROOT", "."))
    
    # Output directories
    OUTPUT_DIR: Path = Path(os.getenv("OUTPUT_DIR", "generated"))
    REPORTS_DIR: Path = Path(os.getenv("REPORTS_DIR", "generated/reports"))
    COVERAGE_DIR: Path = Path(os.getenv("COVERAGE_DIR", "coverage"))
    BUILD_DIR: Path = Path(os.getenv("BUILD_DIR", "dist"))
    
    # Document output paths
    RESUME_DOCX_PATH: Path = field(init=False)
    RESUME_PDF_PATH: Path = field(init=False)
    PROJECTS_EXCEL_PATH: Path = field(init=False)
    CV_JSON_PATH: Path = field(init=False)
    
    # API configuration
    API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_BASE_URL: str = field(init=False)
    
    # Environment
    ENVIRONMENT: Environment = Environment(os.getenv("ENVIRONMENT", "development"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "text")  # text, json, rich
    LOG_DIR: Path = Path(os.getenv("LOG_DIR", "logs"))
    
    def __post_init__(self):
        """Initialize derived paths"""
        self.RESUME_DOCX_PATH = self.OUTPUT_DIR / "resume.docx"
        self.RESUME_PDF_PATH = self.OUTPUT_DIR / "resume.pdf"
        self.PROJECTS_EXCEL_PATH = self.OUTPUT_DIR / "projects.xlsx"
        self.CV_JSON_PATH = self.OUTPUT_DIR / "cv.json"
        self.API_BASE_URL = f"http://{self.API_HOST}:{self.API_PORT}"
        
        # Create directories if they don't exist
        for dir_path in [self.OUTPUT_DIR, self.REPORTS_DIR, self.COVERAGE_DIR, 
                        self.LOG_DIR, self.BUILD_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)


# ============================================================================
# SKILL-SPECIFIC DEFAULTS
# ============================================================================

@dataclass
class SkillDefaults:
    """Default values for skill parameters"""
    
    # Testing defaults
    MIN_COVERAGE: float = 80.0
    MAX_COVERAGE: float = 100.0
    COVERAGE_THRESHOLD: float = 70.0
    INCLUDE_E2E_COVERAGE: bool = False
    GENERATE_HTML_REPORT: bool = True
    WATCH_MODE: bool = False
    UPDATE_SNAPSHOTS: bool = False
    
    # Security defaults
    MAX_SECURITY_ISSUES: int = 0  # Zero tolerance
    MAX_CRITICAL_ISSUES: int = 0
    MAX_HIGH_ISSUES: int = 5
    
    # Type checking defaults
    MAX_TYPE_ERRORS: int = 100
    TYPE_CHECKER_STRICT: bool = True
    TYPE_CHECKER_EXCLUDE: List[str] = field(default_factory=list)
    
    # Performance defaults
    MAX_BUNDLE_SIZE_MB: float = 500.0
    MAX_LOAD_TIME_MS: float = 3000.0
    MAX_PERF_REGRESSION: float = 10.0
    
    # Build defaults
    BUILD_TARGET: str = "production"
    SKIP_BUILD_TESTS: bool = False
    BUILD_OPTIMIZE: bool = True
    BUILD_TIMEOUT_SECONDS: int = 300
    TEST_TIMEOUT_SECONDS: int = 600
    DEPLOY_TIMEOUT_SECONDS: int = 900
    
    # Document defaults
    DOCX_TEMPLATE: str = "modern"
    PDF_TEMPLATE: str = "modern"
    INCLUDE_PROJECTS: bool = True
    INCLUDE_SKILLS: bool = True
    
    # Dependency defaults
    INCLUDE_DEV_DEPS: bool = True
    UPDATE_LOCKFILE: bool = False
    
    # E2E testing defaults
    E2E_BROWSERS: List[str] = field(default_factory=lambda: ["chromium", "firefox"])
    E2E_HEADLESS: bool = True
    
    # Retry defaults
    MAX_RETRIES: int = 3
    RETRY_DELAY_SECONDS: int = 5
    
    # Rate limiting
    REQUESTS_PER_MINUTE: int = 100
    TOKENS_PER_MINUTE: int = 90000


# ============================================================================
# TOOL PATHS AND COMMANDS
# ============================================================================

@dataclass
class ToolConfig:
    """Tool-specific configuration"""
    
    # Package managers
    NPM_CMD: str = "npm"
    PNPM_CMD: str = "pnpm"
    PIP_CMD: str = "pip"
    UV_CMD: str = "uv"
    
    # Test runners
    VITEST_CMD: str = "npm run test:unit"
    PYTEST_CMD: str = "pytest"
    PLAYWRIGHT_CMD: str = "npx playwright test"
    
    # Linters and formatters
    ESLINT_CMD: str = "npx eslint"
    PRETTIER_CMD: str = "npx prettier"
    PYLINT_CMD: str = "pylint"
    BLACK_CMD: str = "black"
    MYPY_CMD: str = "mypy"
    
    # Build tools
    TSC_CMD: str = "tsc"
    VITE_CMD: str = "npx vite"
    
    # Security tools
    BANDIT_CMD: str = "bandit"
    NPM_AUDIT_CMD: str = "npm audit"
    
    # Document generators
    PANDOC_CMD: str = "pandoc"
    WKHTMLTOPDF_CMD: str = "wkhtmltopdf"


# ============================================================================
# DOCUMENT TEMPLATES AND STYLES
# ============================================================================

@dataclass
class DocumentConfig:
    """Document generation configuration"""
    
    # DOCX/PDF styling
    PAGE_SIZE: str = "A4"
    MARGINS_MM: int = 10
    LINE_SPACING: float = 1.5
    FONT_FAMILY: str = "Calibri"
    FONT_SIZE_BODY: int = 11
    FONT_SIZE_HEADING: int = 14
    FONT_SIZE_TITLE: int = 18
    
    # DOCX templates
    DOCX_TEMPLATE_STYLE: str = "professional"  # professional, modern, creative
    DOCX_DEFAULT_SECTIONS: List[str] = field(
        default_factory=lambda: ["summary", "experience", "skills", "education", "projects"]
    )
    
    # PDF options
    PDF_COMPRESS: bool = True
    PDF_QUALITY: str = "high"  # low, medium, high
    PDF_MARGINS: Dict[str, int] = field(default_factory=lambda: {
        "top": 10, "bottom": 10, "left": 10, "right": 10
    })
    
    # Excel/CSV config
    EXCEL_DEFAULT_SHEETS: List[str] = field(
        default_factory=lambda: ["projects", "skills", "experience", "education"]
    )
    EXCEL_AUTO_WIDTH: bool = True


# ============================================================================
# PORTFOLIO-SPECIFIC CONFIGURATION
# ============================================================================

@dataclass
class PortfolioConfig:
    """Portfolio project-specific configuration"""
    
    # Portfolio data
    PORTFOLIO_NAME: str = os.getenv("PORTFOLIO_NAME", "Professional Portfolio")
    PORTFOLIO_AUTHOR: str = os.getenv("PORTFOLIO_AUTHOR", "Developer Name")
    PORTFOLIO_EMAIL: str = os.getenv("PORTFOLIO_EMAIL", "")
    PORTFOLIO_PHONE: str = os.getenv("PORTFOLIO_PHONE", "")
    PORTFOLIO_LOCATION: str = os.getenv("PORTFOLIO_LOCATION", "")
    
    # Portfolio URLs
    PORTFOLIO_URL: str = os.getenv("PORTFOLIO_URL", "https://portfolio.example.com")
    GITHUB_URL: str = os.getenv("GITHUB_URL", "https://github.com/username")
    LINKEDIN_URL: str = os.getenv("LINKEDIN_URL", "")
    TWITTER_URL: str = os.getenv("TWITTER_URL", "")
    
    # Deployment
    DEPLOY_TO_GITHUB_PAGES: bool = True
    GITHUB_PAGES_BRANCH: str = "gh-pages"
    CUSTOM_DOMAIN: str = os.getenv("CUSTOM_DOMAIN", "")
    
    # Data validation
    VALIDATE_URLS: bool = True
    VALIDATE_SCHEMA: bool = True
    ENFORCE_STRICT_VALIDATION: bool = False


# ============================================================================
# DEPLOYMENT CONFIGURATION
# ============================================================================

@dataclass
class DeploymentConfig:
    """Deployment settings"""
    
    # Git configuration
    GIT_USER_NAME: str = os.getenv("GIT_USER_NAME", "Bot User")
    GIT_USER_EMAIL: str = os.getenv("GIT_USER_EMAIL", "bot@example.com")
    GIT_COMMIT_MESSAGE_PREFIX: str = os.getenv("GIT_COMMIT_PREFIX", "build:")
    
    # Release configuration
    RELEASE_BRANCH_PREFIX: str = os.getenv("RELEASE_BRANCH_PREFIX", "feature/release")
    DEFAULT_VERSION: str = os.getenv("DEFAULT_VERSION", "1.0.0")
    SEMANTIC_VERSIONING: bool = True
    AUTO_RELEASE_ON_TAG: bool = True
    RELEASE_NOTES_FORMAT: str = "markdown"  # markdown, html
    
    # Deployment targets
    DEPLOY_TARGETS: List[str] = field(
        default_factory=lambda: ["github-pages", "production"]
    )
    
    # Environment-specific URLs
    STAGING_URL: str = os.getenv("STAGING_URL", "https://staging.example.com")
    PRODUCTION_URL: str = os.getenv("PRODUCTION_URL", "https://example.com")


# ============================================================================
# VALIDATION RULES
# ============================================================================

@dataclass
class ValidationConfig:
    """Validation and constraint configuration"""
    
    # Project name validation
    PROJECT_NAME_MIN_LENGTH: int = 1
    PROJECT_NAME_MAX_LENGTH: int = 256
    
    # Version validation
    STRICT_SEMVER: bool = True
    ALLOW_PRERELEASE: bool = True
    
    # File size limits
    MAX_FILE_SIZE_MB: int = 100
    MAX_PDF_SIZE_MB: int = 50
    MAX_IMAGE_SIZE_MB: int = 10
    
    # Path validation
    ALLOWED_EXTENSIONS: List[str] = field(
        default_factory=lambda: [".py", ".ts", ".tsx", ".js", ".json", ".yml", ".yaml"]
    )
    MAX_PATH_DEPTH: int = 10


# ============================================================================
# GLOBAL SINGLETON INSTANCES
# ============================================================================

# Initialize with environment variables
project_config = ProjectConfig()
skill_defaults = SkillDefaults()
tool_config = ToolConfig()
document_config = DocumentConfig()
portfolio_config = PortfolioConfig()
deployment_config = DeploymentConfig()
validation_config = ValidationConfig()


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_config(config_type: str) -> object:
    """Get configuration object by type"""
    configs = {
        "project": project_config,
        "skills": skill_defaults,
        "tools": tool_config,
        "documents": document_config,
        "portfolio": portfolio_config,
        "deployment": deployment_config,
        "validation": validation_config,
    }
    return configs.get(config_type)


def get_project_path(relative_path: str = "") -> Path:
    """Get full path relative to project root"""
    full_path = project_config.WORKSPACE_ROOT / relative_path if relative_path else project_config.WORKSPACE_ROOT
    return full_path


def get_output_path(filename: str, subdir: str = "") -> Path:
    """Get output file path"""
    base_dir = project_config.OUTPUT_DIR / subdir if subdir else project_config.OUTPUT_DIR
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / filename


def is_production() -> bool:
    """Check if running in production mode"""
    return project_config.ENVIRONMENT == Environment.PRODUCTION


def is_development() -> bool:
    """Check if running in development mode"""
    return project_config.ENVIRONMENT == Environment.DEVELOPMENT


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
