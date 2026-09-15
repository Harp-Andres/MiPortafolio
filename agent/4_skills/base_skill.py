"""
Base Skill Template - All 28 skills inherit from this class

Implements:
- Cross-platform subprocess execution (Windows/Linux/Mac)
- Pydantic input/output validation
- Error handling and retry logic
- Structured logging
- Timeout management
- Platform detection

Every skill must inherit from BaseSkill and implement:
  async def _run_implementation(self, request: SkillRequest) -> str
"""

import os
import sys
import logging
import subprocess
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any, Callable, Coroutine
from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod
from functools import wraps

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


def skill_wrapper(skill_name: str) -> Callable:
    """
    Decorator that wraps skill execution with:
    - Timing and duration tracking
    - Structured logging
    - Error handling and exceptions
    - Status management
    
    Eliminates ~50 lines of duplicate code from all 27 skills.
    
    Usage:
        @skill_wrapper("MySkill")
        async def _run_implementation(self, request: SkillRequest) -> SkillResult:
            # implementation
            return SkillResult(success=True, ...)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(self, request: SkillRequest) -> 'SkillResult':
            start_time = datetime.now()
            try:
                logger.debug(f"[{skill_name}] Starting execution")
                result = await func(self, request)
                duration = (datetime.now() - start_time).total_seconds() * 1000
                logger.info(
                    f"[{skill_name}] Execution successful",
                    extra={"duration_ms": duration, "skill": skill_name}
                )
                return result
            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds() * 1000
                logger.error(
                    f"[{skill_name}] Execution failed: {str(e)}",
                    exc_info=True,
                    extra={"duration_ms": duration, "skill": skill_name}
                )
                return SkillResult(
                    success=False,
                    status=SkillStatus.FAILED,
                    message=f"{skill_name} failed",
                    errors=[str(e)],
                    duration_seconds=duration / 1000,
                )
        return wrapper
    return decorator


class SkillStatus(str, Enum):
    """Skill execution status"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class SkillRequest(BaseModel):
    """Base request model - all skills override and extend this"""
    timeout_seconds: int = Field(default=30, description="Execution timeout")
    retry_count: int = Field(default=0, description="Number of retries")
    verbose: bool = Field(default=False, description="Verbose output")


class SkillResult(BaseModel):
    """Base result model - all skills return this or subclass"""
    success: bool
    status: SkillStatus
    message: str
    output: Optional[str] = None
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    duration_seconds: float
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseSkill(ABC):
    """
    Base class for all 28 skills in the agent.

    Provides:
    - Cross-platform subprocess execution
    - Pydantic validation
    - Error handling and logging
    - Timeout management
    - Platform detection
    """

    # Override in subclasses
    SKILL_NAME: str = "UnnamedSkill"
    SKILL_DESCRIPTION: str = "Skill description"
    REQUIRED_TOOLS: List[str] = []  # Tools to verify on init
    REQUIRED_ENV_VARS: List[str] = []  # Environment variables needed

    def __init__(self, workspace_root: Optional[Path] = None):
        """
        Initialize skill.

        Args:
            workspace_root: Root directory for workspace (defaults to cwd)
        """
        self.workspace_root = workspace_root or Path.cwd()
        self.platform = os.name  # 'nt' for Windows, 'posix' for Unix
        self.is_windows = sys.platform.startswith("win")
        self.verified_tools: Dict[str, Path] = {}
        
        logger.info(f"Initializing {self.SKILL_NAME} on platform: {self.platform}")
        self._verify_tools()
        self._verify_env_vars()

    def _verify_tools(self) -> None:
        """Verify all required tools are available in PATH"""
        for tool in self.REQUIRED_TOOLS:
            tool_path = shutil.which(tool)
            if tool_path:
                self.verified_tools[tool] = Path(tool_path)
                logger.debug(f"✓ Tool found: {tool} at {tool_path}")
            else:
                logger.warning(f"✗ Tool not found: {tool} (will attempt to use anyway)")

    def has_tool(self, tool: str) -> bool:
        """Check if a tool is available in PATH.
        
        Args:
            tool: Tool name to check (e.g., 'pnpm', 'tsc', 'mypy')
            
        Returns:
            True if tool is found in PATH, False otherwise
        """
        tool_path = shutil.which(tool)
        return tool_path is not None

    def _verify_env_vars(self) -> None:
        """Verify required environment variables are set"""
        missing = []
        for var in self.REQUIRED_ENV_VARS:
            if not os.getenv(var):
                missing.append(var)
        
        if missing:
            logger.warning(
                f"Missing environment variables: {', '.join(missing)}"
            )

    async def execute(self, request: SkillRequest) -> SkillResult:
        """
        Execute skill with error handling and timing.

        Args:
            request: Validated skill request

        Returns:
            SkillResult with success status and output

        This is the main entry point - subclasses should NOT override this,
        but instead implement _run_implementation().
        """
        start_time = datetime.now()
        result_status = SkillStatus.RUNNING

        try:
            logger.info(f"[{self.SKILL_NAME}] Executing with request: {request}")

            # Run skill implementation
            output = await self._run_implementation(request)

            result_status = SkillStatus.SUCCESS

            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"[{self.SKILL_NAME}] Completed successfully in {duration:.2f}s")

            return SkillResult(
                success=True,
                status=result_status,
                message=f"{self.SKILL_NAME} executed successfully",
                output=output,
                duration_seconds=duration,
            )

        except subprocess.TimeoutExpired as e:
            result_status = SkillStatus.TIMEOUT
            error_msg = f"{self.SKILL_NAME} timed out after {request.timeout_seconds}s"
            logger.error(error_msg)
            return SkillResult(
                success=False,
                status=result_status,
                message=error_msg,
                errors=[str(e)],
                duration_seconds=(datetime.now() - start_time).total_seconds(),
            )

        except Exception as e:
            result_status = SkillStatus.FAILED
            error_msg = f"{self.SKILL_NAME} failed: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return SkillResult(
                success=False,
                status=result_status,
                message=error_msg,
                errors=[str(e)],
                duration_seconds=(datetime.now() - start_time).total_seconds(),
            )

    @abstractmethod
    async def _run_implementation(self, request: SkillRequest) -> str:
        """
        Implement skill-specific logic.

        Must be implemented by subclasses.

        Args:
            request: Validated request

        Returns:
            String output/result

        Raises:
            Exception: Any error encountered during execution
        """
        raise NotImplementedError(
            f"{self.SKILL_NAME} must implement _run_implementation()"
        )

    def _run_command(
        self,
        cmd: List[str],
        timeout: int = 30,
        cwd: Optional[Path] = None,
        env: Optional[Dict[str, str]] = None,
    ) -> subprocess.CompletedProcess:
        """
        Execute command cross-platform (Windows/Linux/Mac).

        Args:
            cmd: Command as list (e.g., ["npm", "run", "test"])
            timeout: Timeout in seconds
            cwd: Working directory
            env: Environment variables (inherits parent if not set)

        Returns:
            CompletedProcess with stdout, stderr, returncode

        Raises:
            subprocess.TimeoutExpired: If command exceeds timeout
            FileNotFoundError: If command not found
        """
        logger.debug(f"Running command: {' '.join(cmd)}")

        # Validate command
        if not cmd or not isinstance(cmd, list):
            raise ValueError(f"Invalid command format: {cmd}")

        # Use provided env or inherit parent
        full_env = {**os.environ, **(env or {})}

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(cwd or self.workspace_root),
                env=full_env,
            )

            if result.returncode != 0:
                logger.warning(
                    f"Command exited with code {result.returncode}: {' '.join(cmd)}"
                )

            return result

        except subprocess.TimeoutExpired as e:
            logger.error(f"Command timed out after {timeout}s: {' '.join(cmd)}")
            raise

        except FileNotFoundError as e:
            logger.error(f"Command not found: {cmd[0]}")
            raise

    def _resolve_tool(self, tool_name: str) -> str:
        """
        Resolve tool path - use verified path if available, else tool name.

        Args:
            tool_name: Name of tool (npm, python, pytest, etc)

        Returns:
            Full path to tool or tool name
        """
        if tool_name in self.verified_tools:
            return str(self.verified_tools[tool_name])
        return tool_name

    def _resolve_path(self, path: str) -> Path:
        """
        Resolve relative path to absolute path.

        Args:
            path: Relative or absolute path

        Returns:
            Absolute pathlib.Path
        """
        p = Path(path)
        if p.is_absolute():
            return p
        return self.workspace_root / p

    def _get_line_separator(self) -> str:
        """Get OS-correct line separator"""
        return os.linesep

    def _format_output(self, lines: List[str]) -> str:
        """Format output with OS-correct line separators"""
        return self._get_line_separator().join(lines)


# Example usage in a subclass:
#
# class MySkill(BaseSkill):
#     SKILL_NAME = "my-skill"
#     SKILL_DESCRIPTION = "Description of my skill"
#     REQUIRED_TOOLS = ["npm", "python"]
#
#     async def _run_implementation(self, request: SkillRequest) -> str:
#         # Run implementation using self._run_command(), self._resolve_tool(), etc
#         result = self._run_command(["npm", "run", "test"])
#         return result.stdout
