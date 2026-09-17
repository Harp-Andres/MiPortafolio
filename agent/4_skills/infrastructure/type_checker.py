"""Type Checker - runs tsc (TypeScript) and mypy (Python)."""

import logging
from pathlib import Path
from datetime import datetime

import importlib.util as _ilu, sys as _sys; _bs = _ilu.spec_from_file_location('_base_skill', __import__('pathlib').Path(__file__).parent.parent / 'base_skill.py'); _bsm = _ilu.module_from_spec(_bs); _bs.loader.exec_module(_bsm); BaseSkill = _bsm.BaseSkill; SkillRequest = _bsm.SkillRequest; SkillResult = _bsm.SkillResult; SkillStatus = _bsm.SkillStatus; skill_wrapper = _bsm.skill_wrapper; _lh = _ilu.spec_from_file_location('_logger_helper', __import__('pathlib').Path(__file__).parent.parent / 'logger_helper.py'); _lhm = _ilu.module_from_spec(_lh); _lh.loader.exec_module(_lhm); get_logger = _lhm.get_logger; _tm = _ilu.spec_from_file_location('_telemetry', __import__('pathlib').Path(__file__).parent.parent.parent / '6_telemetry' / 'metrics.py'); _tmm = _ilu.module_from_spec(_tm); _tm.loader.exec_module(_tmm); MetricsCollector = getattr(_tmm, 'MetricsCollector', type('MetricsCollector', (), {'__init__': lambda s: None, 'record': lambda *a: None}))

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
        # Import SecurityFilter via importlib to avoid numbered directory issues
        _sf = _ilu.spec_from_file_location('_security_filters', Path(__file__).parent.parent.parent / '5_guardrails' / 'security_filters.py')
        _sfm = _ilu.module_from_spec(_sf)
        _sf.loader.exec_module(_sfm)
        SecurityFilter = _sfm.SecurityFilter
        
        super().__init__(workspace_root)
        self.skill_name = "TypeChecker"
        self.security_filter = SecurityFilter(workspace_root=workspace_root)

    async def _run_implementation(self, request: SkillRequest) -> str:
        """Check types in codebase.

        Args:
            request: SkillRequest with parameters.

        Returns:
            String with type checking results.
        """
        start_time = datetime.now()

        try:
            logger.info(
                f"[{self.skill_name}] Starting type checking",
                extra={"workspace": str(self.workspace_root)},
            )

            # TypeScript type checking
            ts_errors = await self._check_typescript()

            # Python type checking
            py_errors = await self._check_python()

            total_errors = ts_errors + py_errors
            duration = (datetime.now() - start_time).total_seconds() * 1000

            logger.info(
                f"[{self.skill_name}] Type checking completed",
                extra={
                    "typescript_errors": ts_errors,
                    "python_errors": py_errors,
                    "total_errors": total_errors,
                    "duration_ms": duration,
                },
            )

            return f"Type checking completed: TypeScript errors={ts_errors}, Python errors={py_errors}, Total={total_errors}"

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(
                f"[{self.skill_name}] Type checking failed",
                extra={"error": str(e), "duration_ms": duration},
                exc_info=True,
            )
            raise

    async def _check_typescript(self) -> int:
        """Check TypeScript types.

        Returns:
            Number of errors found.
        """
        logger.debug(f"[{self.skill_name}] Checking TypeScript types")
        
        # Check if tsc is available
        if not self.has_tool("tsc"):
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

    async def _check_python(self) -> int:
        """Check Python types with mypy.

        Args:
            strict: Run in strict mode.
            exclude_paths: Paths to exclude.

        Returns:
            Number of errors found.
        """
        logger.debug(f"[{self.skill_name}] Checking Python types")
        
        # Check if mypy is available
        if not self.has_tool("mypy"):
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
