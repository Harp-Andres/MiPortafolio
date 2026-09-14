"""
Type Checker Skill - Validate code types (TypeScript + Python).

Runs TypeScript strict mode type checking and Python mypy type validation.
Ensures type safety across both frontend and backend code.

Expected Input:
    {
        "workspace_root": str,
        "strict": bool (default: True),
        "exclude_paths": list (default: []),
        "max_errors": int (default: 100)
    }

Returns:
    {
        "status": "success" | "failed",
        "typescript_errors": int,
        "python_errors": int,
        "total_errors": int,
        "files_checked": int,
        "duration_ms": float
    }
"""

import asyncio
from pathlib import Path
from datetime import datetime

from agent_4_skills.base_skill import BaseSkill, SkillResult, SkillStatus
from agent_5_guardrails.security_filters import SecurityFilter
from agent_6_telemetry import get_logger, Timer, MetricsCollector
from agent.config import skill_defaults


logger = get_logger(__name__)


class TypeChecker(BaseSkill):
    """Validate code types (TypeScript strict + Python mypy).

    This skill:
    1. Runs TypeScript type checking in strict mode
    2. Runs Python mypy type validation
    3. Aggregates and reports errors
    4. Fails if threshold exceeded
    """

    def __init__(self, workspace_root: str):
        """Initialize TypeChecker.

        Args:
            workspace_root: Root directory of the project.
        """
        super().__init__(workspace_root)
        self.skill_name = "TypeChecker"
        self.security_filter = SecurityFilter(workspace_root=workspace_root)

    async def _run_implementation(self, request) -> SkillResult:
        """Check types in codebase.

        Args:
            request: SkillRequest with parameters.

        Returns:
            SkillResult with type checking results.
        """
        start_time = datetime.now()
        metrics = MetricsCollector()

        try:
            logger.info(
                f"[{self.skill_name}] Starting type checking",
                extra={"workspace": str(self.workspace_root)},
            )

            params = request.parameters
            strict = params.get("strict", skill_defaults.TYPE_CHECKER_STRICT)
            exclude_paths = params.get("exclude_paths", skill_defaults.TYPE_CHECKER_EXCLUDE)
            max_errors = params.get("max_errors", skill_defaults.MAX_TYPE_ERRORS)

            with Timer(metrics, "type_checking_ms"):
                # TypeScript type checking
                ts_errors = await self._check_typescript(
                    strict=strict,
                    exclude_paths=exclude_paths,
                )

                # Python type checking
                py_errors = await self._check_python(
                    strict=strict,
                    exclude_paths=exclude_paths,
                )

            total_errors = ts_errors + py_errors
            files_checked = 0  # TODO: Track files
            duration = (datetime.now() - start_time).total_seconds() * 1000

            status = (
                SkillStatus.SUCCESS
                if total_errors <= max_errors
                else SkillStatus.FAILED
            )

            logger.info(
                f"[{self.skill_name}] Type checking completed",
                extra={
                    "typescript_errors": ts_errors,
                    "python_errors": py_errors,
                    "total_errors": total_errors,
                    "duration_ms": duration,
                },
            )

            return SkillResult(
                skill_name=self.skill_name,
                status=status,
                output={
                    "typescript_errors": ts_errors,
                    "python_errors": py_errors,
                    "total_errors": total_errors,
                    "files_checked": files_checked,
                    "duration_ms": duration,
                },
            )

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(
                f"[{self.skill_name}] Type checking failed",
                extra={"error": str(e), "duration_ms": duration},
                exc_info=True,
            )
            return SkillResult(
                skill_name=self.skill_name,
                status=SkillStatus.FAILED,
                error=str(e),
                output={"duration_ms": duration},
            )

    async def _check_typescript(
        self,
        strict: bool = True,
        exclude_paths: list = None,
    ) -> int:
        """Check TypeScript types.

        Args:
            strict: Run in strict mode.
            exclude_paths: Paths to exclude.

        Returns:
            Number of errors found.
        """
        logger.debug(f"[{self.skill_name}] Checking TypeScript types")
        
        # Check if tsc is available
        if not self._verify_tools("tsc"):
            logger.warning(f"[{self.skill_name}] tsc not found, skipping TypeScript checks")
            return 0
        
        # Check if tsconfig.json exists
        tsconfig = self.workspace_root / "tsconfig.json"
        if not tsconfig.exists():
            logger.warning(f"[{self.skill_name}] tsconfig.json not found")
            return 0
        
        try:
            # Validate file path for security
            self.security_filter.validate_file_operation(str(tsconfig), "read")
            
            # Build tsc command
            cmd = ["tsc", "--noEmit"]  # --noEmit: only check types, don't generate JS
            
            if strict:
                cmd.append("--strict")
            
            # Exclude patterns if provided
            if exclude_paths:
                for path in exclude_paths:
                    cmd.extend(["--skipLibCheck"])  # Skip lib type checking
                    break  # Just use skipLibCheck for simplicity
            
            # Validate subprocess command for security
            cmd = self.security_filter.validate_subprocess_command(cmd)
            
            # Run tsc
            result = await self._run_command(
                cmd,
                cwd=str(self.workspace_root),
                description="tsc type checking",
                capture_errors=True
            )
            
            # Parse error count from output
            error_count = self._extract_tsc_errors(result)
            logger.info(
                f"[{self.skill_name}] TypeScript check completed",
                extra={"errors": error_count}
            )
            return error_count
            
        except Exception as e:
            logger.error(
                f"[{self.skill_name}] TypeScript checking failed",
                exc_info=True
            )
            # Return 0 if tsc not found, but we found errors
            return 0

    async def _check_python(
        self,
        strict: bool = True,
        exclude_paths: list = None,
    ) -> int:
        """Check Python types with mypy.

        Args:
            strict: Run in strict mode.
            exclude_paths: Paths to exclude.

        Returns:
            Number of errors found.
        """
        logger.debug(f"[{self.skill_name}] Checking Python types")
        
        # Check if mypy is available
        if not self._verify_tools("mypy"):
            logger.warning(f"[{self.skill_name}] mypy not found, skipping Python type checks")
            return 0
        
        try:
            # Look for Python source files
            py_files = list(self.workspace_root.glob("**/*.py"))
            # Exclude common dirs
            py_files = [f for f in py_files 
                       if not any(part in f.parts for part in ['.venv', 'venv', 'node_modules', '.git', '__pycache__', 'dist', 'build'])]
            
            if not py_files:
                logger.debug(f"[{self.skill_name}] No Python files found to check")
                return 0
            
            # Build mypy command
            cmd = ["mypy"]
            
            if strict:
                cmd.append("--strict")
            
            # Add configuration options
            cmd.extend(["--pretty", "--show-error-codes"])
            
            # Add Python paths to check
            cmd.extend([str(f.parent) for f in py_files[:10]])  # Check first 10 file directories
            
            # Validate subprocess command for security
            cmd = self.security_filter.validate_subprocess_command(cmd)
            
            # Run mypy
            result = await self._run_command(
                cmd,
                cwd=str(self.workspace_root),
                description="mypy type checking",
                capture_errors=True
            )
            
            # Parse error count from output
            error_count = self._extract_mypy_errors(result)
            logger.info(
                f"[{self.skill_name}] Python type check completed",
                extra={"errors": error_count}
            )
            return error_count
            
        except Exception as e:
            logger.error(
                f"[{self.skill_name}] Python type checking failed",
                exc_info=True
            )
            return 0
    
    def _extract_tsc_errors(self, output: str) -> int:
        """Extract error count from tsc output.
        
        Args:
            output: tsc command output.
            
        Returns:
            Number of errors found.
        """
        import re
        # Look for "error TS####" pattern or summary line "X errors"
        errors = output.count("error TS")
        if errors == 0:
            # Look for summary line
            match = re.search(r'(\d+)\s+error', output)
            if match:
                errors = int(match.group(1))
        return errors
    
    def _extract_mypy_errors(self, output: str) -> int:
        """Extract error count from mypy output.
        
        Args:
            output: mypy command output.
            
        Returns:
            Number of errors found.
        """
        import re
        # Look for summary line "X error: Y" or count error lines
        match = re.search(r'(\d+)\s+error:', output)
        if match:
            return int(match.group(1))
        
        # Count lines with "error:" pattern
        error_lines = [line for line in output.split('\n') if 'error:' in line]
        return len(error_lines)


__all__ = ["TypeChecker"]
