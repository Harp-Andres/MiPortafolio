"""
Master Orchestrator Agent - Layer 5: Guardrails

Security, validation, and rate limiting.

Modules:
  - env_validator.py: Environment configuration validation
  - validators.py: Input validation for all skill parameters
  - security_filters.py: Command injection prevention, security checks
  - rate_limiter.py: API rate limiting and quota management
  - skill_validators.py: Pydantic validators for each skill type
"""

from agent_5_guardrails.validators import (
    CIPipeline,
    Environment,
    TestSuite,
    DocumentFormat,
    LogLevel,
    CICommandValidator,
    DeployCommandValidator,
    TestCommandValidator,
    DocsCommandValidator,
    AddProjectCommandValidator,
    EnvironmentCheckValidator,
    ValidatorFactory,
    validate_file_path,
    validate_directory_path,
)

from agent_5_guardrails.skill_validators import (
    validate_skill_request,
    SKILL_VALIDATORS,
    SkillType,
)

from agent_5_guardrails.security_filters import (
    sanitize_command_arg,
    sanitize_file_path,
    sanitize_env_var,
    validate_safe_path,
    validate_subprocess_args,
    validate_url,
    detect_injection_attempts,
    is_suspicious_input,
    SecurityFilter,
    RateLimitChecker,
)

from agent_5_guardrails.rate_limiter import (
    TokenUsage,
    RequestRecord,
    BudgetStatus,
    RateLimiter,
    TokenBudget,
    LLMRateLimiter,
    PROVIDER_RATE_LIMITS,
    DAILY_BUDGET,
    MONTHLY_BUDGET,
)

__version__ = "0.1.0"

__all__ = [
    # Validators
    "ValidatorFactory",
    "CICommandValidator",
    "DeployCommandValidator",
    "TestCommandValidator",
    "DocsCommandValidator",
    "AddProjectCommandValidator",
    "EnvironmentCheckValidator",
    # Skill validators
    "validate_skill_request",
    "SKILL_VALIDATORS",
    "SkillType",
    # Enums
    "CIPipeline",
    "Environment",
    "TestSuite",
    "DocumentFormat",
    "LogLevel",
    # Security
    "SecurityFilter",
    "sanitize_command_arg",
    "sanitize_file_path",
    "sanitize_env_var",
    "validate_safe_path",
    "validate_subprocess_args",
    "validate_url",
    "detect_injection_attempts",
    "is_suspicious_input",
    "RateLimitChecker",
    # Rate limiting
    "RateLimiter",
    "TokenBudget",
    "LLMRateLimiter",
    "TokenUsage",
    "RequestRecord",
    "BudgetStatus",
    # Config
    "PROVIDER_RATE_LIMITS",
    "DAILY_BUDGET",
    "MONTHLY_BUDGET",
]
