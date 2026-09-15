"""
Environment Configuration Validator

Validates .env file exists and contains required keys on agent startup.
Provides friendly error messages guiding users to fix missing configuration.

Non-destructive: Only warns, doesn't modify files.
Cross-platform: Works on Windows/Linux/Mac.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set
from enum import Enum

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class EnvironmentValidationLevel(str, Enum):
    """Validation strictness levels"""
    CRITICAL = "critical"  # Agent cannot start
    REQUIRED = "required"  # Feature will not work
    RECOMMENDED = "recommended"  # Feature degraded
    OPTIONAL = "optional"  # Nice-to-have


class EnvironmentConfigError(Exception):
    """Raised when environment configuration is invalid or incomplete"""

    def __init__(self, message: str, level: EnvironmentValidationLevel = EnvironmentValidationLevel.CRITICAL):
        self.message = message
        self.level = level
        super().__init__(message)


class EnvironmentValidator:
    """
    Validates environment configuration for the Master Agent.

    Checks:
    - .env file exists
    - Required keys present with non-empty values
    - At least one LLM provider configured
    - GitHub credentials valid format
    """

    # Variables that MUST be present (agent cannot start without them)
    CRITICAL_KEYS: Dict[str, str] = {
        "GITHUB_TOKEN": "GitHub Personal Access Token (required for git operations)",
        "GITHUB_REPO": "GitHub repository in format owner/repo (required for deployments)",
    }

    # Variables that SHOULD be present (features degrade without them)
    REQUIRED_KEYS: Dict[str, str] = {
        "LOG_LEVEL": "Logging level (DEBUG, INFO, WARNING, ERROR)",
    }

    # LLM providers (at least ONE must be configured)
    LLM_PROVIDERS: Dict[str, str] = {
        "OPENAI_API_KEY": "OpenAI API key (for GPT models)",
        "ANTHROPIC_API_KEY": "Anthropic API key (for Claude models)",
        "OLLAMA_BASE_URL": "Local Ollama URL (for local LLM fallback)",
    }

    # Optional but recommended
    RECOMMENDED_KEYS: Dict[str, str] = {
        "AGENT_MODEL": "LLM model name for agent reasoning",
        "AGENT_MAX_TOKENS": "Maximum tokens per LLM response",
        "DEBUG_MODE": "Enable detailed logging and debugging",
        "TELEMETRY_ENABLED": "Send usage statistics (opt-in)",
    }

    @classmethod
    def validate(cls, raise_on_error: bool = True) -> bool:
        """
        Validate environment configuration.

        Args:
            raise_on_error: If True, raise EnvironmentConfigError on validation failure.
                          If False, return False and log warnings.

        Returns:
            True if validation passes, False if raise_on_error=False and validation fails.

        Raises:
            EnvironmentConfigError: If raise_on_error=True and validation fails.
        """
        try:
            env_file = cls._get_env_file()

            # Check .env file existence
            if not env_file.exists():
                error = cls._create_missing_file_error(env_file)
                if raise_on_error:
                    raise EnvironmentConfigError(error, EnvironmentValidationLevel.CRITICAL)
                logger.error(error)
                return False

            # Load environment
            load_dotenv(env_file)

            # Validate critical keys
            missing_critical = cls._check_keys(cls.CRITICAL_KEYS)
            if missing_critical:
                error = cls._create_missing_keys_error(missing_critical, "CRITICAL")
                if raise_on_error:
                    raise EnvironmentConfigError(error, EnvironmentValidationLevel.CRITICAL)
                logger.error(error)
                return False

            # Validate required keys
            missing_required = cls._check_keys(cls.REQUIRED_KEYS)
            if missing_required:
                logger.warning(
                    f"[WARN] Missing recommended keys: {', '.join(missing_required.keys())}"
                )

            # Validate LLM provider
            if not cls._check_llm_provider():
                error = cls._create_llm_provider_error()
                if raise_on_error:
                    raise EnvironmentConfigError(error, EnvironmentValidationLevel.REQUIRED)
                logger.error(error)
                return False

            # Validate GitHub format
            github_repo = os.getenv("GITHUB_REPO", "")
            if github_repo and "/" not in github_repo:
                error = (
                    f"[ERROR] Invalid GITHUB_REPO format: '{github_repo}'\n"
                    f"   Expected: 'owner/repo' (e.g., 'Harp-Andres/MiPortafolio')\n"
                    f"   Edit: {env_file}"
                )
                if raise_on_error:
                    raise EnvironmentConfigError(error, EnvironmentValidationLevel.CRITICAL)
                logger.error(error)
                return False

            # Warn about recommended keys
            missing_recommended = cls._check_keys(cls.RECOMMENDED_KEYS)
            if missing_recommended:
                logger.info(
                    f"[INFO] Optional keys not configured: {', '.join(missing_recommended.keys())}"
                )

            logger.info("[OK] Environment validation passed")
            return True

        except EnvironmentConfigError:
            raise
        except Exception as e:
            error = f"[ERROR] Unexpected error during environment validation: {str(e)}"
            logger.error(error)
            if raise_on_error:
                raise EnvironmentConfigError(error, EnvironmentValidationLevel.CRITICAL)
            return False

    @staticmethod
    def _get_env_file() -> Path:
        """Get path to .env file (agent directory)"""
        return Path(__file__).parent.parent / ".env"

    @staticmethod
    def _get_env_example() -> Path:
        """Get path to .env.example template"""
        return Path(__file__).parent.parent / ".env.example"

    @classmethod
    def _check_keys(cls, keys: Dict[str, str]) -> Dict[str, str]:
        """
        Check if keys exist and have non-empty values.

        Args:
            keys: Dict of key -> description

        Returns:
            Dict of missing keys -> description
        """
        missing = {}
        for key, desc in keys.items():
            value = os.getenv(key, "").strip()
            if not value:
                missing[key] = desc
        return missing

    @classmethod
    def _check_llm_provider(cls) -> bool:
        """Check if at least one LLM provider is configured"""
        for provider_key in cls.LLM_PROVIDERS.keys():
            if os.getenv(provider_key, "").strip():
                logger.info(f"[OK] LLM Provider detected: {provider_key}")
                return True
        return False

    @staticmethod
    def _create_missing_file_error(env_file: Path) -> str:
        """Create error message for missing .env file"""
        env_example = env_file.parent / ".env.example"
        
        if env_example.exists():
            return (
                f"[ERROR] Missing .env file\n\n"
                f"Setup:\n"
                f"  1. Copy template:\n"
                f"     cp {env_example.name} {env_file.name}\n"
                f"  2. Edit {env_file.name} and add your API keys\n"
                f"  3. Restart the agent\n\n"
                f"Location: {env_file}\n"
                f"Template: {env_example}"
            )
        else:
            return (
                f"[ERROR] Missing .env file\n"
                f"   Create: {env_file}\n"
                f"   Add required keys (see CRITICAL_KEYS in env_validator.py)"
            )

    @staticmethod
    def _create_missing_keys_error(missing_keys: Dict[str, str], level: str) -> str:
        """Create error message for missing keys"""
        keys_str = "\n".join(
            [f"  • {key}: {desc}" for key, desc in missing_keys.items()]
        )
        env_file = Path(__file__).parent.parent / ".env"
        
        return (
            f"[ERROR] Missing {level} environment variables:\n\n{keys_str}\n\n"
            f"Fix:\n"
            f"  1. Edit: {env_file}\n"
            f"  2. Add values for missing keys\n"
            f"  3. Save and restart agent"
        )

    @staticmethod
    def _create_llm_provider_error() -> str:
        """Create error message for missing LLM provider"""
        return (
            f"[ERROR] No LLM provider configured\n\n"
            f"Add ONE of these to your .env:\n"
            f"  • OPENAI_API_KEY=sk-proj-... (for OpenAI/GPT)\n"
            f"  • ANTHROPIC_API_KEY=sk-ant-... (for Anthropic/Claude)\n"
            f"  • OLLAMA_BASE_URL=http://localhost:11434 (for local LLM)\n\n"
            f"Get API keys at:\n"
            f"  • OpenAI: https://platform.openai.com/api-keys\n"
            f"  • Anthropic: https://console.anthropic.com/\n"
            f"  • Ollama: https://ollama.ai/ (free, local)"
        )

    @staticmethod
    def print_summary():
        """Print environment configuration summary"""
        print("\n" + "=" * 60)
        print("ENVIRONMENT CONFIGURATION SUMMARY")
        print("=" * 60)
        
        print("\n[OK] CRITICAL KEYS:")
        for key in EnvironmentValidator.CRITICAL_KEYS.keys():
            status = "[YES]" if os.getenv(key) else "[NO]"
            print(f"  {status} {key}")
        
        print("\n📦 LLM PROVIDER:")
        found = False
        for key in EnvironmentValidator.LLM_PROVIDERS.keys():
            if os.getenv(key):
                print(f"  [✓] {key}")
                found = True
        if not found:
            print(f"  [✗] No LLM provider configured")
        
        print("\n⚙️  OTHER CONFIGURATION:")
        for key in EnvironmentValidator.REQUIRED_KEYS.keys():
            value = os.getenv(key, "(not set)")
            status = "✓" if os.getenv(key) else "✗"
            print(f"  [{status}] {key}={value}")
        
        print("\n" + "=" * 60 + "\n")


def validate_on_startup():
    """
    Convenience function for startup validation.
    Call this at the beginning of your CLI or MCP server main().
    """
    try:
        EnvironmentValidator.validate(raise_on_error=True)
    except EnvironmentConfigError as e:
        print(f"\n{e.message}\n", file=sys.stderr)
        sys.exit(1)
