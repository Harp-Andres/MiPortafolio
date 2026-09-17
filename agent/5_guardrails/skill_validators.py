"""
Skill Request and Result Validators

Centralized Pydantic validators for all skill types.
Validates input parameters before skill execution and output after completion.

This eliminates the need for repeated validation logic in each skill
and provides consistent validation across all skill types.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, validator, root_validator
from enum import Enum
import re


class SkillType(str, Enum):
    """Types of skills in the agent"""
    INFRASTRUCTURE = "infrastructure"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    DOCUMENTS = "documents"
    PORTFOLIO = "portfolio"
    QUALITY = "quality"
    BACKEND = "backend"


# ============================================================================
# INFRASTRUCTURE SKILLS VALIDATORS
# ============================================================================

class DependencyResolverRequest(BaseModel):
    """Validator for DependencyResolver skill"""
    include_dev: bool = Field(default=False, description="Include dev dependencies")
    update_lockfile: bool = Field(default=False, description="Update lockfile")
    max_packages: int = Field(default=1000, description="Max packages allowed")
    
    @validator("max_packages")
    def validate_max_packages(cls, v):
        if v < 0:
            raise ValueError("max_packages must be >= 0")
        return v


class TypeCheckerRequest(BaseModel):
    """Validator for TypeChecker skill"""
    check_typescript: bool = Field(default=True, description="Check TypeScript")
    check_python: bool = Field(default=True, description="Check Python")
    strict_mode: bool = Field(default=False, description="Enable strict mode")
    max_errors: int = Field(default=100, description="Max errors before failing")
    
    @validator("max_errors")
    def validate_max_errors(cls, v):
        if v < 0:
            raise ValueError("max_errors must be >= 0")
        return v


class BuildOrchestratorRequest(BaseModel):
    """Validator for BuildOrchestrator skill"""
    build_frontend: bool = Field(default=True, description="Build frontend")
    build_backend: bool = Field(default=True, description="Build backend")
    environment: str = Field(default="production", description="Build environment")
    
    @validator("environment")
    def validate_environment(cls, v):
        valid = ["development", "staging", "production"]
        if v not in valid:
            raise ValueError(f"environment must be one of {valid}")
        return v


class QualityGateRequest(BaseModel):
    """Validator for QualityGate skill"""
    min_coverage: float = Field(default=80.0, description="Minimum coverage %")
    max_security_issues: int = Field(default=0, description="Max security issues")
    max_performance_regression: float = Field(default=10.0, description="Max performance regression %")
    
    @validator("min_coverage")
    def validate_coverage(cls, v):
        if not 0 <= v <= 100:
            raise ValueError("min_coverage must be between 0 and 100")
        return v
    
    @validator("max_security_issues")
    def validate_security_issues(cls, v):
        if v < 0:
            raise ValueError("max_security_issues must be >= 0")
        return v


# ============================================================================
# TESTING SKILLS VALIDATORS
# ============================================================================

class UnitTestRunnerRequest(BaseModel):
    """Validator for UnitTestRunner skill"""
    test_framework: str = Field(default="all", description="Test framework: vitest, pytest, all")
    verbose: bool = Field(default=False, description="Verbose output")
    watch_mode: bool = Field(default=False, description="Watch mode")
    update_snapshots: bool = Field(default=False, description="Update snapshots")
    
    @validator("test_framework")
    def validate_framework(cls, v):
        valid = ["vitest", "pytest", "all"]
        if v not in valid:
            raise ValueError(f"test_framework must be one of {valid}")
        return v


class E2ETestRunnerRequest(BaseModel):
    """Validator for E2ETestRunner skill"""
    browsers: List[str] = Field(default_factory=lambda: ["chromium"], description="Browsers to test (Chrome only)")
    headless: bool = Field(default=True, description="Run in headless mode")
    
    @validator("browsers")
    def validate_browsers(cls, v):
        valid = ["chromium", "firefox", "webkit"]
        for browser in v:
            if browser not in valid:
                raise ValueError(f"browser must be one of {valid}")
        if not v:
            raise ValueError("At least one browser must be specified")
        return v


class CoverageAnalyzerRequest(BaseModel):
    """Validator for CoverageAnalyzer skill"""
    min_coverage: float = Field(default=80.0, description="Minimum coverage %")
    include_e2e: bool = Field(default=False, description="Include E2E coverage")
    
    @validator("min_coverage")
    def validate_min_coverage(cls, v):
        if not 0 <= v <= 100:
            raise ValueError("min_coverage must be between 0 and 100")
        return v


class TestAggregatorRequest(BaseModel):
    """Validator for TestAggregator skill"""
    generate_html_report: bool = Field(default=True, description="Generate HTML report")
    report_format: str = Field(default="html", description="Report format: html, json, markdown")
    
    @validator("report_format")
    def validate_format(cls, v):
        valid = ["html", "json", "markdown"]
        if v not in valid:
            raise ValueError(f"report_format must be one of {valid}")
        return v


# ============================================================================
# DEPLOYMENT SKILLS VALIDATORS
# ============================================================================

class GitBranchCreatorRequest(BaseModel):
    """Validator for GitBranchCreator skill"""
    branch_name: str = Field(..., min_length=1, description="Branch name")
    base_branch: str = Field(default="main", description="Base branch")
    
    @validator("branch_name")
    def validate_branch_name(cls, v):
        # Git branch naming rules
        if v.startswith("-") or v.endswith("-") or v.endswith("."):
            raise ValueError("Invalid branch name format")
        if not re.match(r"^[a-zA-Z0-9._/-]+$", v):
            raise ValueError("Branch name contains invalid characters")
        return v


class GitWorkflowManagerRequest(BaseModel):
    """Validator for GitWorkflowManager skill"""
    workflow_file: str = Field(..., min_length=1, description="Workflow file path")
    enable: bool = Field(default=True, description="Enable workflow")


class GitHubPagesDeployerRequest(BaseModel):
    """Validator for GitHubPagesDeployer skill"""
    source_branch: str = Field(default="gh-pages", description="Source branch for Pages")
    custom_domain: Optional[str] = Field(default=None, description="Custom domain")
    
    @validator("custom_domain")
    def validate_domain(cls, v):
        if v and not re.match(r"^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$", v):
            raise ValueError("Invalid domain format")
        return v


class ReleaseOrchestratorRequest(BaseModel):
    """Validator for ReleaseOrchestrator skill"""
    version: str = Field(..., min_length=1, description="Version (semantic)")
    release_notes: Optional[str] = Field(default=None, description="Release notes")
    
    @validator("version")
    def validate_version(cls, v):
        # Semantic versioning: X.Y.Z
        if not re.match(r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?(\+[a-zA-Z0-9.]+)?$", v):
            raise ValueError("Version must follow semantic versioning (X.Y.Z)")
        return v


# ============================================================================
# DOCUMENT SKILLS VALIDATORS
# ============================================================================

class DocxGeneratorRequest(BaseModel):
    """Validator for DocxGenerator skill"""
    include_sections: List[str] = Field(default_factory=lambda: ["summary", "experience", "skills"], 
                                       description="Sections to include")
    template_style: str = Field(default="professional", description="Template style")
    
    @validator("template_style")
    def validate_style(cls, v):
        valid = ["professional", "modern", "creative"]
        if v not in valid:
            raise ValueError(f"template_style must be one of {valid}")
        return v


class PdfGeneratorRequest(BaseModel):
    """Validator for PdfGenerator skill"""
    page_size: str = Field(default="A4", description="Page size")
    margin_mm: int = Field(default=10, description="Margin in mm")
    
    @validator("margin_mm")
    def validate_margin(cls, v):
        if not 0 <= v <= 50:
            raise ValueError("margin_mm must be between 0 and 50")
        return v


class ExcelGeneratorRequest(BaseModel):
    """Validator for ExcelGenerator skill"""
    include_sheets: List[str] = Field(default_factory=lambda: ["projects", "skills", "experience"],
                                     description="Sheets to include")


class CVDataValidatorRequest(BaseModel):
    """Validator for CVDataValidator skill"""
    strict_mode: bool = Field(default=False, description="Strict validation mode")
    check_urls: bool = Field(default=True, description="Validate URLs")


class SyncVerifierRequest(BaseModel):
    """Validator for SyncVerifier skill"""
    check_frontend: bool = Field(default=True, description="Check frontend data")
    check_backend: bool = Field(default=True, description="Check backend data")


# ============================================================================
# PORTFOLIO SKILLS VALIDATORS
# ============================================================================

class PortfolioUpdaterRequest(BaseModel):
    """Validator for PortfolioUpdater skill"""
    project_name: str = Field(..., min_length=1, description="Project name")
    update_data: Dict[str, Any] = Field(default_factory=dict, description="Update data")
    validate_schema: bool = Field(default=True, description="Validate against schema")


class SkillsManagerRequest(BaseModel):
    """Validator for SkillsManager skill"""
    action: str = Field(..., description="Action: add, remove, update")
    skill_name: str = Field(..., min_length=1, description="Skill name")
    proficiency: Optional[str] = Field(default=None, description="Proficiency level")
    
    @validator("action")
    def validate_action(cls, v):
        valid = ["add", "remove", "update"]
        if v not in valid:
            raise ValueError(f"action must be one of {valid}")
        return v
    
    @validator("proficiency")
    def validate_proficiency(cls, v):
        if v:
            valid = ["beginner", "intermediate", "advanced", "expert"]
            if v not in valid:
                raise ValueError(f"proficiency must be one of {valid}")
        return v


class CertificateManagerRequest(BaseModel):
    """Validator for CertificateManager skill"""
    action: str = Field(..., description="Action: add, remove, verify")
    certificate_name: str = Field(..., min_length=1, description="Certificate name")
    issue_date: Optional[str] = Field(default=None, description="Issue date (YYYY-MM-DD)")
    authority: Optional[str] = Field(default=None, description="Issuing authority")
    
    @validator("action")
    def validate_action(cls, v):
        valid = ["add", "remove", "verify"]
        if v not in valid:
            raise ValueError(f"action must be one of {valid}")
        return v
    
    @validator("issue_date")
    def validate_date(cls, v):
        if v and not re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            raise ValueError("issue_date must be in YYYY-MM-DD format")
        return v


class ExperienceTrackerRequest(BaseModel):
    """Validator for ExperienceTracker skill"""
    company: str = Field(..., min_length=1, description="Company name")
    position: str = Field(..., min_length=1, description="Job position")
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(default=None, description="End date (YYYY-MM-DD)")
    
    @validator("start_date", "end_date")
    def validate_dates(cls, v):
        if v and not re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            raise ValueError("Dates must be in YYYY-MM-DD format")
        return v


# ============================================================================
# QUALITY SKILLS VALIDATORS
# ============================================================================

class CodeFormatterRequest(BaseModel):
    """Validator for CodeFormatter skill"""
    formatter: str = Field(default="prettier", description="Formatter tool")
    write: bool = Field(default=False, description="Write changes")
    
    @validator("formatter")
    def validate_formatter(cls, v):
        valid = ["prettier", "black", "autopep8"]
        if v not in valid:
            raise ValueError(f"formatter must be one of {valid}")
        return v


class LinterCheckerRequest(BaseModel):
    """Validator for LinterChecker skill"""
    linters: List[str] = Field(default_factory=lambda: ["eslint", "pylint"],
                              description="Linters to run")
    fix: bool = Field(default=False, description="Auto-fix issues")
    max_errors: int = Field(default=100, description="Max errors before failing")


class PerformanceMonitorRequest(BaseModel):
    """Validator for PerformanceMonitor skill"""
    monitor_type: str = Field(default="bundle-size", description="What to monitor")
    baseline_mb: float = Field(default=500.0, description="Baseline size in MB")
    
    @validator("monitor_type")
    def validate_type(cls, v):
        valid = ["bundle-size", "load-time", "memory"]
        if v not in valid:
            raise ValueError(f"monitor_type must be one of {valid}")
        return v


# ============================================================================
# BACKEND SKILLS VALIDATORS
# ============================================================================

class BackendServerRequest(BaseModel):
    """Validator for BackendServer skill"""
    port: int = Field(default=8000, description="Server port")
    host: str = Field(default="127.0.0.1", description="Server host")
    environment: str = Field(default="development", description="Environment")
    
    @validator("port")
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError("port must be between 1 and 65535")
        return v
    
    @validator("host")
    def validate_host(cls, v):
        if v not in ["127.0.0.1", "0.0.0.0", "localhost"]:
            raise ValueError("host must be 127.0.0.1, 0.0.0.0, or localhost")
        return v


class BackendTestRunnerRequest(BaseModel):
    """Validator for BackendTestRunner skill"""
    test_path: str = Field(default="tests", description="Test path")
    coverage: bool = Field(default=True, description="Generate coverage")
    min_coverage: float = Field(default=80.0, description="Minimum coverage %")


class APIValidatorRequest(BaseModel):
    """Validator for APIValidator skill"""
    api_url: str = Field(..., description="API URL")
    validate_schema: bool = Field(default=True, description="Validate schema")
    validate_security: bool = Field(default=True, description="Validate security")
    
    @validator("api_url")
    def validate_url(cls, v):
        url_pattern = r"^https?://"
        if not re.match(url_pattern, v):
            raise ValueError("API URL must start with http:// or https://")
        return v


# ============================================================================
# SKILL VALIDATOR FACTORY
# ============================================================================

SKILL_VALIDATORS = {
    "dependency_resolver": DependencyResolverRequest,
    "type_checker": TypeCheckerRequest,
    "build_orchestrator": BuildOrchestratorRequest,
    "quality_gate_runner": QualityGateRequest,
    "unit_test_runner": UnitTestRunnerRequest,
    "e2e_test_runner": E2ETestRunnerRequest,
    "coverage_analyzer": CoverageAnalyzerRequest,
    "test_aggregator": TestAggregatorRequest,
    "git_branch_creator": GitBranchCreatorRequest,
    "git_workflow_manager": GitWorkflowManagerRequest,
    "github_pages_deployer": GitHubPagesDeployerRequest,
    "release_orchestrator": ReleaseOrchestratorRequest,
    "docx_generator": DocxGeneratorRequest,
    "pdf_generator": PdfGeneratorRequest,
    "excel_generator": ExcelGeneratorRequest,
    "cv_data_validator": CVDataValidatorRequest,
    "sync_verifier": SyncVerifierRequest,
    "portfolio_updater": PortfolioUpdaterRequest,
    "skills_manager": SkillsManagerRequest,
    "certificate_manager": CertificateManagerRequest,
    "experience_tracker": ExperienceTrackerRequest,
    "code_formatter": CodeFormatterRequest,
    "linter_checker": LinterCheckerRequest,
    "performance_monitor": PerformanceMonitorRequest,
    "backend_server": BackendServerRequest,
    "backend_test_runner": BackendTestRunnerRequest,
    "api_validator": APIValidatorRequest,
}


def validate_skill_request(skill_name: str, parameters: Dict[str, Any]) -> bool:
    """
    Validate skill request parameters.
    
    Args:
        skill_name: Name of the skill
        parameters: Parameters dict
        
    Returns:
        bool: True if valid, raises ValidationError if not
        
    Raises:
        ValueError: If skill not found or validation fails
    """
    if skill_name not in SKILL_VALIDATORS:
        raise ValueError(f"Unknown skill: {skill_name}")
    
    validator_class = SKILL_VALIDATORS[skill_name]
    validator_class(**parameters)  # Will raise ValidationError if invalid
    return True


__all__ = [
    "validate_skill_request",
    "SKILL_VALIDATORS",
    "DependencyResolverRequest",
    "TypeCheckerRequest",
    "BuildOrchestratorRequest",
    "QualityGateRequest",
    "UnitTestRunnerRequest",
    "E2ETestRunnerRequest",
    "CoverageAnalyzerRequest",
    "TestAggregatorRequest",
    "SkillType",
]
