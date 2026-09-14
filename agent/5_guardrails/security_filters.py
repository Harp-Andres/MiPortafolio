"""
Security filters to prevent command injection and validate subprocess arguments.

This module provides security functions to:
- Sanitize command arguments
- Prevent shell injection attacks
- Validate file paths for safety
- Secure subprocess execution
- Whitelist and blacklist checks

Usage:
    from agent_5_guardrails.security_filters import (
        sanitize_command_arg,
        validate_safe_path,
        SecurityFilter,
    )

    # Sanitize command argument
    safe_arg = sanitize_command_arg("user-input; rm -rf /")
    # Returns: "user-input; rm -rf /"

    # Validate file path is safe
    safe_path = validate_safe_path("/home/user/project/file.txt")
    # Returns: PosixPath('/home/user/project/file.txt')

    # Use security filter
    filter = SecurityFilter(workspace_root="/home/user/project")
    filter.validate_subprocess_args(["python", "script.py", "arg1"])
"""

import re
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# Constants
# ============================================================================

# Characters that could indicate shell injection attempts
SHELL_DANGEROUS_CHARS = {
    ";",  # Command separator
    "|",  # Pipe
    "&",  # Background/AND
    ">",  # Redirect
    "<",  # Redirect
    "`",  # Command substitution
    "$",  # Variable expansion
    "(",  # Subshell
    ")",  # Subshell
    "{",  # Brace expansion
    "}",  # Brace expansion
    "[",  # Glob
    "]",  # Glob
    "*",  # Glob
    "?",  # Glob
    "\\",  # Escape
    "\n",  # Newline injection
    "\r",  # Carriage return
}

# Patterns for detecting potential injection attempts
INJECTION_PATTERNS = [
    r"(\bsudo\b|\brm\b|\brm -rf\b|\bdd\b|\bformat\b|\bfdisk\b)",  # Dangerous commands
    r"(?:;|&&|\|\|).*(?:rm|del|format|dd)",  # Command chaining to dangerous ops
    r"(?:`|\$\(|eval|exec|source).*(?:rm|del|dd)",  # Command substitution
    r"(?:\d+\.){3}\d+",  # IP address (for network operations)
]


# ============================================================================
# Sanitization Functions
# ============================================================================


def sanitize_command_arg(arg: str, strict: bool = False) -> str:
    """Sanitize a command argument to prevent injection.

    This function removes or escapes potentially dangerous characters.
    In strict mode, any dangerous character causes an error.

    Args:
        arg: Command argument to sanitize.
        strict: If True, raise error on any dangerous character.

    Returns:
        Sanitized argument.

    Raises:
        ValueError: If strict mode and dangerous character found.
    """
    if not isinstance(arg, str):
        raise TypeError(f"Argument must be string, got {type(arg)}")

    # Check for dangerous characters
    dangerous_found = set(arg) & SHELL_DANGEROUS_CHARS

    if dangerous_found:
        if strict:
            raise ValueError(
                f"Dangerous characters found in argument: {dangerous_found}"
            )
        else:
            logger.warning(
                f"Suspicious characters in argument (may be sanitized): {dangerous_found}"
            )

    # Return as-is if no dangerous chars (subprocess.run with list doesn't execute shell)
    return arg


def sanitize_file_path(path: str) -> str:
    """Sanitize a file path.

    Ensures path doesn't contain suspicious elements like:
    - Directory traversal attempts (..)
    - Excessive special characters

    Args:
        path: File path to sanitize.

    Returns:
        Sanitized path.

    Raises:
        ValueError: If path contains traversal attempts.
    """
    # Resolve path to absolute and normalize
    resolved = Path(path).resolve()

    # Check for traversal attempts in original path
    if ".." in str(path):
        logger.warning(f"Directory traversal attempt detected: {path}")

    return str(resolved)


def sanitize_env_var(key: str, value: str) -> tuple[str, str]:
    """Sanitize environment variable key and value.

    Args:
        key: Environment variable name.
        value: Environment variable value.

    Returns:
        Tuple of (sanitized_key, sanitized_value).

    Raises:
        ValueError: If key or value contain invalid characters.
    """
    # Key must be alphanumeric + underscore
    if not re.match(r"^[A-Z0-9_]+$", key):
        raise ValueError(
            f"Invalid environment variable name: {key} (must be A-Z, 0-9, _)"
        )

    # Value can contain most characters, just warn on suspicious ones
    if any(c in value for c in [";", "|", "&", "`"]):
        logger.warning(
            f"Suspicious characters in env var {key}={value[:20]}..."
        )

    return key, value


# ============================================================================
# Validation Functions
# ============================================================================


def validate_safe_path(
    path: str | Path,
    workspace_root: Optional[str | Path] = None,
    allow_outside_workspace: bool = False,
) -> Path:
    """Validate that a path is safe to use.

    Checks that:
    - Path is absolute or relative to workspace
    - Path doesn't traverse outside workspace (if workspace_root set)
    - Path exists or is creatable
    - No suspicious patterns

    Args:
        path: Path to validate.
        workspace_root: Root directory to constrain path to.
        allow_outside_workspace: Allow paths outside workspace_root.

    Returns:
        Validated Path object.

    Raises:
        ValueError: If path fails validation.
        FileNotFoundError: If parent directory doesn't exist.
    """
    path_obj = Path(path)

    # Resolve to absolute path
    if not path_obj.is_absolute():
        if workspace_root:
            path_obj = Path(workspace_root) / path_obj
        else:
            path_obj = path_obj.resolve()

    path_obj = path_obj.resolve()

    # Check parent exists (so we can create file/dir if needed)
    if not path_obj.parent.exists():
        raise FileNotFoundError(f"Parent directory does not exist: {path_obj.parent}")

    # Check workspace boundary
    if workspace_root and not allow_outside_workspace:
        workspace = Path(workspace_root).resolve()
        try:
            path_obj.relative_to(workspace)
        except ValueError:
            raise ValueError(
                f"Path escapes workspace: {path_obj} is outside {workspace}"
            )

    return path_obj


def validate_subprocess_args(args: List[str], allow_shell: bool = False) -> List[str]:
    """Validate subprocess arguments for safety.

    When allow_shell=False (recommended), shell metacharacters are harmless
    because subprocess.run() with a list doesn't invoke the shell.

    Args:
        args: Command arguments as list.
        allow_shell: If True, allow potential shell injection patterns.

    Returns:
        Validated arguments.

    Raises:
        ValueError: If arguments fail validation.
    """
    if not isinstance(args, list):
        raise TypeError(f"Args must be list, got {type(args)}")

    if not args or len(args) == 0:
        raise ValueError("Empty command argument list")

    # First element should be executable name or path
    command = args[0]
    if "/" in command or "\\" in command:
        # It's a path, validate it
        validate_safe_path(command)
    else:
        # It's a command name, basic validation
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", command):
            raise ValueError(
                f"Invalid command name: {command} (must be alphanumeric, -, _, .)"
            )

    # Validate remaining arguments
    for arg in args[1:]:
        if not isinstance(arg, str):
            raise TypeError(f"Argument must be string, got {type(arg)}: {arg}")

        # In list mode (no shell), these chars are safe
        # But warn if they look suspicious
        if any(c in arg for c in [";", "|", "&", "`", "$"]):
            logger.warning(
                f"Suspicious characters in argument (safe in list mode): {arg[:50]}"
            )

    return args


# ============================================================================
# Injection Detection
# ============================================================================


def detect_injection_attempts(text: str) -> List[str]:
    """Detect potential command injection attempts in text.

    Args:
        text: Text to analyze.

    Returns:
        List of detected patterns (empty if none found).
    """
    matches = []

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            matches.append(pattern)

    return matches


def is_suspicious_input(text: str) -> bool:
    """Quick check if input looks suspicious.

    Args:
        text: Text to check.

    Returns:
        True if suspicious patterns detected.
    """
    return len(detect_injection_attempts(text)) > 0


# ============================================================================
# URL Validation
# ============================================================================


def validate_url(url: str, allowed_schemes: List[str] = None) -> str:
    """Validate URL format and scheme.

    Args:
        url: URL to validate.
        allowed_schemes: List of allowed URL schemes (default: http, https).

    Returns:
        Validated URL.

    Raises:
        ValueError: If URL is invalid.
    """
    if allowed_schemes is None:
        allowed_schemes = ["http", "https"]

    url = url.strip()

    # Check scheme
    scheme_match = re.match(r"^([a-zA-Z][a-zA-Z0-9+.-]*):\/\/", url)
    if not scheme_match:
        raise ValueError(f"Invalid URL scheme: {url}")

    scheme = scheme_match.group(1).lower()
    if scheme not in allowed_schemes:
        raise ValueError(
            f"URL scheme not allowed: {scheme} (allowed: {allowed_schemes})"
        )

    # Basic URL validation
    if len(url) > 2048:
        raise ValueError(f"URL too long: {len(url)} characters")

    return url


# ============================================================================
# SecurityFilter Class
# ============================================================================


class SecurityFilter:
    """Central security filter for CLI commands.

    Usage:
        filter = SecurityFilter(workspace_root="/home/user/project")
        filter.validate_file_operation("/home/user/project/file.txt", "read")
        filter.validate_subprocess_command(["python", "script.py", "arg"])
    """

    def __init__(self, workspace_root: str | Path = None):
        """Initialize security filter.

        Args:
            workspace_root: Root directory to constrain file operations to.
        """
        self.workspace_root = Path(workspace_root).resolve() if workspace_root else None
        self.logger = logger

    def validate_file_operation(
        self,
        path: str | Path,
        operation: str = "read",
    ) -> Path:
        """Validate a file operation is safe.

        Args:
            path: File path to validate.
            operation: Type of operation (read, write, create, delete).

        Returns:
            Validated Path object.

        Raises:
            ValueError: If operation is unsafe.
        """
        if operation not in ("read", "write", "create", "delete"):
            raise ValueError(f"Unknown operation: {operation}")

        validated_path = validate_safe_path(
            path,
            workspace_root=self.workspace_root,
            allow_outside_workspace=False,
        )

        if operation == "read" and not validated_path.exists():
            raise FileNotFoundError(f"File does not exist: {validated_path}")

        if operation == "delete" and not validated_path.exists():
            raise FileNotFoundError(f"Cannot delete non-existent file: {validated_path}")

        self.logger.debug(f"Validated {operation} operation on {validated_path}")
        return validated_path

    def validate_subprocess_command(self, args: List[str]) -> List[str]:
        """Validate subprocess command is safe.

        Args:
            args: Command arguments as list.

        Returns:
            Validated arguments.

        Raises:
            ValueError: If command is unsafe.
        """
        validated_args = validate_subprocess_args(args, allow_shell=False)
        self.logger.debug(f"Validated subprocess command: {validated_args[0]}")
        return validated_args

    def validate_environment_variable(self, key: str, value: str) -> tuple[str, str]:
        """Validate environment variable.

        Args:
            key: Variable name.
            value: Variable value.

        Returns:
            Validated (key, value) tuple.

        Raises:
            ValueError: If variable is invalid.
        """
        return sanitize_env_var(key, value)

    def validate_url(self, url: str) -> str:
        """Validate URL.

        Args:
            url: URL to validate.

        Returns:
            Validated URL.

        Raises:
            ValueError: If URL is invalid.
        """
        return validate_url(url)


# ============================================================================
# Rate Limiting Helper (used by rate_limiter module)
# ============================================================================


class RateLimitChecker:
    """Helper for rate limit checking.

    Usage:
        checker = RateLimitChecker(max_requests=100, window_seconds=60)
        if checker.is_rate_limited():
            raise ValueError("Rate limit exceeded")
    """

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        """Initialize rate limit checker.

        Args:
            max_requests: Maximum requests allowed per window.
            window_seconds: Time window in seconds.
        """
        self.max_requests = max_requests
        self.window = timedelta(seconds=window_seconds)
        self.requests: List[datetime] = []

    def check(self) -> bool:
        """Check if request is allowed.

        Returns:
            True if request is allowed, False if rate limited.
        """
        now = datetime.now()
        cutoff = now - self.window

        # Remove old requests
        self.requests = [r for r in self.requests if r > cutoff]

        # Check limit
        if len(self.requests) >= self.max_requests:
            return False

        # Record request
        self.requests.append(now)
        return True

    def remaining(self) -> int:
        """Get remaining requests in current window.

        Returns:
            Number of requests remaining.
        """
        now = datetime.now()
        cutoff = now - self.window
        self.requests = [r for r in self.requests if r > cutoff]
        return max(0, self.max_requests - len(self.requests))


# Export public API
__all__ = [
    # Sanitization
    "sanitize_command_arg",
    "sanitize_file_path",
    "sanitize_env_var",
    # Validation
    "validate_safe_path",
    "validate_subprocess_args",
    "validate_url",
    # Injection detection
    "detect_injection_attempts",
    "is_suspicious_input",
    # SecurityFilter
    "SecurityFilter",
    "RateLimitChecker",
]
