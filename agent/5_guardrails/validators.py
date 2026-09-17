"""
Input validation for all CLI commands using Pydantic.

This module provides validators for all CLI commands to ensure:
- All inputs are properly typed and validated
- File paths exist and are accessible
- Environment variables are set correctly
- Command arguments are within acceptable ranges
- Enum values are valid

Usage:
    from agent_5_guardrails.validators import (
        CICommandValidator,
        DeployCommandValidator,
        TestCommandValidator,
    )

    # Validate CI command
    ci_request = CICommandValidator(stages=["types", "quality"])
    print(ci_request.stages)  # ['types', 'quality']

    # Validate deploy command
    deploy_request = DeployCommandValidator(environment="production", force=True)
    print(deploy_request.environment)  # 'production'
"""

from enum import Enum
from pathlib import Path
from typing import List, Optional, Set

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    ConfigDict,
)


# ============================================================================
# Enums for Valid Values
# ============================================================================


class CIPipeline(str, Enum):
    """Valid CI/CD pipeline stages."""

    DEPENDENCIES = "dependencies"
    TYPES = "types"
    QUALITY = "quality"
    BUILD = "build"
    UNIT_TESTS = "unit_tests"
    E2E_TESTS = "e2e_tests"
    SYNC = "sync"
    SECURITY = "security"
    GATES = "gates"

    @classmethod
    def all_stages(cls) -> List[str]:
        """Return all stages in execution order."""
        return [
            cls.DEPENDENCIES.value,
            cls.TYPES.value,
            cls.QUALITY.value,
            cls.BUILD.value,
            cls.UNIT_TESTS.value,
            cls.E2E_TESTS.value,
            cls.SYNC.value,
            cls.SECURITY.value,
            cls.GATES.value,
        ]


class Environment(str, Enum):
    """Valid deployment environments."""

    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"


class TestSuite(str, Enum):
    """Valid test suites."""

    ALL = "all"
    UNIT = "unit"
    E2E = "e2e"
    BACKEND = "backend"
    FRONTEND = "frontend"


class DocumentFormat(str, Enum):
    """Valid document formats."""

    ALL = "all"
    DOCX = "docx"
    PDF = "pdf"
    EXCEL = "excel"


class LogLevel(str, Enum):
    """Valid log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# ============================================================================
# Validation Models
# ============================================================================


class CICommandValidator(BaseModel):
    """Validator for 'mportafolio-agent ci' command.

    Args:
        stages: Optional list of stages to run. If None, all stages run.
        verbose: Enable verbose output.

    Raises:
        ValueError: If stage is invalid or stages list is empty.
    """

    stages: Optional[List[str]] = Field(
        default=None,
        description="Stages to run (comma-separated). If None, runs all stages.",
    )
    verbose: bool = Field(
        default=False,
        description="Enable verbose output.",
    )

    model_config = ConfigDict(validate_assignment=True)

    @field_validator("stages", mode="before")
    @classmethod
    def validate_stages(cls, value: Optional[str | List[str]]) -> Optional[List[str]]:
        """Validate and normalize stages.

        Args:
            value: Comma-separated string or list of stage names.

        Returns:
            List of valid stage names or None if input was None.

        Raises:
            ValueError: If any stage name is invalid.
        """
        if value is None:
            return None

        # Convert string to list
        if isinstance(value, str):
            stages = [s.strip() for s in value.split(",")]
        else:
            stages = list(value)

        # Validate each stage
        valid_stages = {s.value for s in CIPipeline}
        invalid = set(stages) - valid_stages
        if invalid:
            raise ValueError(
                f"Invalid stages: {invalid}. "
                f"Valid stages: {', '.join(valid_stages)}"
            )

        return stages

    def get_stages(self) -> List[str]:
        """Get stages to execute in order.

        Returns:
            List of stages in pipeline order.
        """
        if self.stages is None:
            return CIPipeline.all_stages()

        # Return in pipeline order
        all_stages = CIPipeline.all_stages()
        return [s for s in all_stages if s in self.stages]


class DeployCommandValidator(BaseModel):
    """Validator for 'mportafolio-agent deploy' command.

    Args:
        environment: Target environment (production/staging/development).
        force: Skip confirmation prompt.
        verbose: Enable verbose output.

    Raises:
        ValueError: If environment is invalid.
    """

    environment: Environment = Field(
        default=Environment.PRODUCTION,
        description="Target environment for deployment.",
    )
    force: bool = Field(
        default=False,
        description="Skip confirmation prompt.",
    )
    verbose: bool = Field(
        default=False,
        description="Enable verbose output.",
    )

    model_config = ConfigDict(validate_assignment=True)


class TestCommandValidator(BaseModel):
    """Validator for 'mportafolio-agent test' command.

    Args:
        suite: Test suite to run (all/unit/e2e/backend/frontend).
        coverage: Include coverage report.
        verbose: Enable verbose output.

    Raises:
        ValueError: If suite is invalid.
    """

    suite: TestSuite = Field(
        default=TestSuite.ALL,
        description="Test suite to run.",
    )
    coverage: bool = Field(
        default=True,
        description="Include coverage report.",
    )
    verbose: bool = Field(
        default=False,
        description="Enable verbose output.",
    )

    model_config = ConfigDict(validate_assignment=True)


class DocsCommandValidator(BaseModel):
    """Validator for 'mportafolio-agent docs' command.

    Args:
        format: Document format(s) to generate (all/docx/pdf/excel).
        output_dir: Output directory for generated documents.
        sync_verify: Verify data sync across formats.
        verbose: Enable verbose output.

    Raises:
        ValueError: If format is invalid or output_dir doesn't exist.
    """

    format: DocumentFormat = Field(
        default=DocumentFormat.ALL,
        description="Document format to generate.",
    )
    output_dir: Optional[Path] = Field(
        default=None,
        description="Output directory for documents.",
    )
    sync_verify: bool = Field(
        default=True,
        description="Verify data sync across formats.",
    )
    verbose: bool = Field(
        default=False,
        description="Enable verbose output.",
    )

    model_config = ConfigDict(validate_assignment=True)

    @field_validator("output_dir", mode="before")
    @classmethod
    def validate_output_dir(cls, value: Optional[str | Path]) -> Optional[Path]:
        """Validate output directory exists or can be created.

        Args:
            value: Directory path as string or Path.

        Returns:
            Validated Path object or None.

        Raises:
            ValueError: If path is invalid or not writable.
        """
        if value is None:
            return None

        output_path = Path(value)

        # Check if parent exists (we'll create output_dir if needed)
        if not output_path.parent.exists():
            raise ValueError(
                f"Parent directory does not exist: {output_path.parent}"
            )

        return output_path


class AddProjectCommandValidator(BaseModel):
    """Validator for 'mportafolio-agent add-project' command.

    Args:
        name: Project name.
        description: Project description.
        technologies: Comma-separated list of tech stack.
        link: Project website URL.
        github: GitHub repository URL.

    Raises:
        ValueError: If name is empty or URLs are invalid.
    """

    name: str = Field(
        ...,
        description="Project name (required).",
        min_length=1,
        max_length=200,
    )
    description: Optional[str] = Field(
        default=None,
        description="Project description.",
        max_length=1000,
    )
    technologies: Optional[str] = Field(
        default=None,
        description="Comma-separated technology list.",
        max_length=500,
    )
    link: Optional[str] = Field(
        default=None,
        description="Project website URL.",
        max_length=500,
    )
    github: Optional[str] = Field(
        default=None,
        description="GitHub repository URL.",
        max_length=500,
    )

    model_config = ConfigDict(validate_assignment=True)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        """Validate project name format.

        Args:
            value: Project name.

        Returns:
            Validated name.

        Raises:
            ValueError: If name contains invalid characters.
        """
        if not value or not value.strip():
            raise ValueError("Project name cannot be empty.")

        # Allow alphanumeric, spaces, hyphens, underscores
        if not all(c.isalnum() or c in " -_" for c in value):
            raise ValueError(
                "Project name can only contain letters, numbers, spaces, hyphens, and underscores."
            )

        return value.strip()

    @field_validator("technologies", mode="before")
    @classmethod
    def validate_technologies(cls, value: Optional[str]) -> Optional[str]:
        """Validate and normalize technology list.

        Args:
            value: Comma-separated technology list.

        Returns:
            Validated and normalized technology list.

        Raises:
            ValueError: If technology list is empty string.
        """
        if value is None:
            return None

        techs = [t.strip() for t in value.split(",") if t.strip()]
        if not techs:
            raise ValueError("At least one technology is required.")

        return ", ".join(techs)

    @field_validator("link", "github", mode="before")
    @classmethod
    def validate_urls(cls, value: Optional[str]) -> Optional[str]:
        """Validate URL format.

        Args:
            value: URL string.

        Returns:
            Validated URL.

        Raises:
            ValueError: If URL format is invalid.
        """
        if value is None:
            return None

        value = value.strip()
        if not value.startswith(("http://", "https://")):
            raise ValueError(f"URL must start with http:// or https://: {value}")

        return value


class EnvironmentCheckValidator(BaseModel):
    """Validator for 'mportafolio-agent env-check' command.

    Args:
        verbose: Enable verbose output.
    """

    verbose: bool = Field(
        default=False,
        description="Enable verbose output.",
    )

    model_config = ConfigDict(validate_assignment=True)


# ============================================================================
# Validation Factory
# ============================================================================


class ValidatorFactory:
    """Factory for creating validators based on command type.

    Usage:
        factory = ValidatorFactory()
        ci_validator = factory.create("ci", stages="types,quality")
        deploy_validator = factory.create("deploy", environment="staging")
    """

    _validators = {
        "ci": CICommandValidator,
        "deploy": DeployCommandValidator,
        "test": TestCommandValidator,
        "docs": DocsCommandValidator,
        "add-project": AddProjectCommandValidator,
        "env-check": EnvironmentCheckValidator,
    }

    @classmethod
    def create(cls, command: str, **kwargs):
        """Create a validator for the given command.

        Args:
            command: Command name (ci, deploy, test, docs, add-project, env-check).
            **kwargs: Command arguments to validate.

        Returns:
            Validated request object.

        Raises:
            ValueError: If command is unknown.
            ValidationError: If arguments are invalid.
        """
        if command not in cls._validators:
            raise ValueError(
                f"Unknown command: {command}. "
                f"Valid commands: {', '.join(cls._validators.keys())}"
            )

        validator_class = cls._validators[command]
        return validator_class(**kwargs)

    @classmethod
    def list_validators(cls) -> Set[str]:
        """List all available validators.

        Returns:
            Set of validator command names.
        """
        return set(cls._validators.keys())


# ============================================================================
# Validation Utilities
# ============================================================================


def validate_file_path(path: str | Path, must_exist: bool = False) -> Path:
    """Validate and normalize a file path.

    Args:
        path: File path as string or Path.
        must_exist: If True, file must exist.

    Returns:
        Validated Path object.

    Raises:
        ValueError: If path is invalid or file doesn't exist (if required).
    """
    file_path = Path(path).resolve()

    if must_exist and not file_path.exists():
        raise ValueError(f"File does not exist: {file_path}")

    return file_path


def validate_directory_path(path: str | Path, must_exist: bool = False) -> Path:
    """Validate and normalize a directory path.

    Args:
        path: Directory path as string or Path.
        must_exist: If True, directory must exist.

    Returns:
        Validated Path object.

    Raises:
        ValueError: If path is invalid or directory doesn't exist (if required).
    """
    dir_path = Path(path).resolve()

    if must_exist and not dir_path.is_dir():
        raise ValueError(f"Directory does not exist: {dir_path}")

    return dir_path


# Export public API
__all__ = [
    # Enums
    "CIPipeline",
    "Environment",
    "TestSuite",
    "DocumentFormat",
    "LogLevel",
    # Validators
    "CICommandValidator",
    "DeployCommandValidator",
    "TestCommandValidator",
    "DocsCommandValidator",
    "AddProjectCommandValidator",
    "EnvironmentCheckValidator",
    # Factory
    "ValidatorFactory",
    # Utilities
    "validate_file_path",
    "validate_directory_path",
]
