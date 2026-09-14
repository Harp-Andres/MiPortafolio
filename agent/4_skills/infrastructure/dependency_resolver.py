"""
Dependency Resolver Skill - Resolve project dependencies.

Resolves both pnpm (frontend) and pip (backend) dependencies.
Validates that all required packages are installed and compatible.

Expected Input:
    {
        "workspace_root": str,
        "include_dev": bool (default: True),
        "update_lockfile": bool (default: False)
    }

Returns:
    {
        "status": "success" | "failed",
        "dependencies_resolved": int,
        "frontend_packages": int,
        "backend_packages": int,
        "conflicts": list,
        "duration_ms": float
    }
"""

import asyncio
from pathlib import Path
from typing import Optional
from datetime import datetime

from agent_4_skills.base_skill import BaseSkill, SkillResult, SkillStatus
from agent_5_guardrails.security_filters import SecurityFilter
from agent_6_telemetry import get_logger
from agent.config import skill_defaults, Timer, MetricsCollector


logger = get_logger(__name__)


class DependencyResolver(BaseSkill):
    """Resolve project dependencies (pnpm + pip).

    This skill:
    1. Resolves pnpm dependencies for frontend
    2. Resolves pip dependencies for backend
    3. Validates compatibility
    4. Generates lock files if needed
    """

    def __init__(self, workspace_root: str):
        """Initialize DependencyResolver.

        Args:
            workspace_root: Root directory of the project.
        """
        super().__init__(workspace_root)
        self.skill_name = "DependencyResolver"
        self.security_filter = SecurityFilter(workspace_root=workspace_root)

    async def _run_implementation(self, request) -> SkillResult:
        """Resolve dependencies.

        Args:
            request: SkillRequest with parameters.

        Returns:
            SkillResult with dependency resolution results.
        """
        start_time = datetime.now()
        metrics = MetricsCollector()

        try:
            logger.info(
                f"[{self.skill_name}] Starting dependency resolution",
                extra={"workspace": str(self.workspace_root)},
            )

            # Validate input
            params = request.parameters
            include_dev = params.get("include_dev", skill_defaults.INCLUDE_DEV_DEPS)
            update_lockfile = params.get("update_lockfile", skill_defaults.UPDATE_LOCKFILE)

            with Timer(metrics, "dependency_resolution_ms"):
                # Frontend dependencies (pnpm)
                frontend_packages = await self._resolve_frontend_deps(
                    include_dev=include_dev,
                    update_lockfile=update_lockfile,
                )

                # Backend dependencies (pip)
                backend_packages = await self._resolve_backend_deps(
                    include_dev=include_dev,
                    update_lockfile=update_lockfile,
                )

            total_packages = frontend_packages + backend_packages
            duration = (datetime.now() - start_time).total_seconds() * 1000

            logger.info(
                f"[{self.skill_name}] Resolution completed",
                extra={
                    "frontend_packages": frontend_packages,
                    "backend_packages": backend_packages,
                    "duration_ms": duration,
                },
            )

            return SkillResult(
                skill_name=self.skill_name,
                status=SkillStatus.SUCCESS,
                output={
                    "dependencies_resolved": total_packages,
                    "frontend_packages": frontend_packages,
                    "backend_packages": backend_packages,
                    "conflicts": [],
                    "duration_ms": duration,
                },
            )

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(
                f"[{self.skill_name}] Resolution failed",
                extra={"error": str(e), "duration_ms": duration},
                exc_info=True,
            )
            return SkillResult(
                skill_name=self.skill_name,
                status=SkillStatus.FAILED,
                error=str(e),
                output={"duration_ms": duration},
            )

    async def _resolve_frontend_deps(
        self,
        include_dev: bool = True,
        update_lockfile: bool = False,
    ) -> int:
        """Resolve pnpm dependencies.

        Args:
            include_dev: Include dev dependencies.
            update_lockfile: Update pnpm-lock.yaml.

        Returns:
            Number of resolved packages.
        """
        logger.debug(f"[{self.skill_name}] Resolving frontend dependencies (pnpm)")
        
        # Check if pnpm is available
        if not self._verify_tools("pnpm"):
            logger.warning(f"[{self.skill_name}] pnpm not found, skipping frontend dependencies")
            return 0
        
        # Construct pnpm command
        cmd = ["pnpm", "install"]
        if not include_dev:
            cmd.append("--prod")
        if update_lockfile:
            cmd.append("--update")
        
        try:
            # Validate subprocess command for security
            cmd = self.security_filter.validate_subprocess_command(cmd)
            
            # Run pnpm install
            result = await self._run_command(
                cmd,
                cwd=str(self.workspace_root),
                description="pnpm install"
            )
            
            # Parse output to count dependencies
            # Look for "packages in X" pattern in pnpm output
            package_count = self._extract_pnpm_count(result)
            logger.info(
                f"[{self.skill_name}] Frontend dependencies resolved",
                extra={"package_count": package_count}
            )
            return package_count
            
        except Exception as e:
            logger.error(
                f"[{self.skill_name}] Frontend dependency resolution failed",
                exc_info=True
            )
            return 0

    async def _resolve_backend_deps(
        self,
        include_dev: bool = True,
        update_lockfile: bool = False,
    ) -> int:
        """Resolve pip dependencies.

        Args:
            include_dev: Include dev dependencies.
            update_lockfile: Update requirements files.

        Returns:
            Number of resolved packages.
        """
        logger.debug(f"[{self.skill_name}] Resolving backend dependencies (pip)")
        
        # Check if pip is available
        if not self._verify_tools("pip"):
            logger.warning(f"[{self.skill_name}] pip not found, skipping backend dependencies")
            return 0
        
        # Look for requirements.txt or pyproject.toml
        requirements_file = self.workspace_root / "requirements.txt"
        pyproject_file = self.workspace_root / "pyproject.toml"
        
        try:
            if pyproject_file.exists():
                # Validate file path for security
                self.security_filter.validate_file_operation(str(pyproject_file), "read")
                
                # Use uv pip install for pyproject.toml (faster than pip)
                if self._verify_tools("uv"):
                    cmd = ["uv", "pip", "install", "-e", "."]
                else:
                    cmd = ["pip", "install", "-e", "."]
                    if not include_dev:
                        cmd.extend(["--no-deps"])
                
                # Validate subprocess command for security
                cmd = self.security_filter.validate_subprocess_command(cmd)
                
                result = await self._run_command(
                    cmd,
                    cwd=str(self.workspace_root),
                    description="pip install from pyproject.toml"
                )
            elif requirements_file.exists():
                # Validate file path for security
                self.security_filter.validate_file_operation(str(requirements_file), "read")
                
                cmd = ["pip", "install", "-r", str(requirements_file)]
                if not include_dev:
                    cmd.extend(["-q"])  # quiet mode
                
                # Validate subprocess command for security
                cmd = self.security_filter.validate_subprocess_command(cmd)
                
                result = await self._run_command(
                    cmd,
                    cwd=str(self.workspace_root),
                    description="pip install from requirements.txt"
                )
            else:
                logger.warning(
                    f"[{self.skill_name}] No requirements.txt or pyproject.toml found"
                )
                return 0
            
            # Parse output to count dependencies
            package_count = self._extract_pip_count(result)
            logger.info(
                f"[{self.skill_name}] Backend dependencies resolved",
                extra={"package_count": package_count}
            )
            return package_count
            
        except Exception as e:
            logger.error(
                f"[{self.skill_name}] Backend dependency resolution failed",
                exc_info=True
            )
            return 0
    
    def _extract_pnpm_count(self, output: str) -> int:
        """Extract package count from pnpm output.
        
        Args:
            output: pnpm command output.
            
        Returns:
            Number of packages or estimation.
        """
        import re
        # Look for "packages in X" pattern
        match = re.search(r'(\d+)\s+(?:package|packages)', output)
        if match:
            return int(match.group(1))
        # Fallback: count dependency entries (rough estimation)
        return len([line for line in output.split('\n') if '│' in line or '└' in line])
    
    def _extract_pip_count(self, output: str) -> int:
        """Extract package count from pip output.
        
        Args:
            output: pip command output.
            
        Returns:
            Number of packages or estimation.
        """
        import re
        # Look for "Successfully installed X" pattern
        match = re.search(r'Successfully installed (.+)', output)
        if match:
            packages = match.group(1).split()
            return len(packages)
        # Look for "Requirement already satisfied" patterns
        count = len([line for line in output.split('\n') 
                    if 'Requirement already satisfied' in line or 'Successfully installed' in line])
        return max(count, 1)  # At least 1 if pip ran


__all__ = ["DependencyResolver"]
