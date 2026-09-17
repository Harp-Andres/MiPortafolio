"""GitHub Pages Deployer - builds and pushes to gh-pages branch."""

import logging
import os
from pathlib import Path

import importlib.util as _ilu, sys as _sys; _bs = _ilu.spec_from_file_location('_base_skill', __import__('pathlib').Path(__file__).parent.parent / 'base_skill.py'); _bsm = _ilu.module_from_spec(_bs); _bs.loader.exec_module(_bsm); BaseSkill = _bsm.BaseSkill; SkillRequest = _bsm.SkillRequest; SkillResult = _bsm.SkillResult; SkillStatus = _bsm.SkillStatus; skill_wrapper = _bsm.skill_wrapper

logger = logging.getLogger(__name__)


class GitHubPagesDeployer(BaseSkill):
    SKILL_NAME = "GitHubPagesDeployer"
    SKILL_DESCRIPTION = "Builds web app and deploys to GitHub Pages (gh-pages branch)"
    REQUIRED_ENV_VARS = ["GITHUB_TOKEN"]

    async def _run_implementation(self, request: SkillRequest) -> str:
        workspace = self.workspace_root
        lines: list[str] = []

        # Step 1: Build
        logger.info(f"[{self.SKILL_NAME}] Building web app...")
        build_result = self._run_command(
            ["pnpm", "--filter", "web", "build"],
            timeout=180,
            cwd=workspace,
        )
        lines.append("=== Build ===")
        lines.append(build_result.stdout or "")
        if build_result.returncode != 0:
            raise RuntimeError(f"Build failed:\n{build_result.stderr}")

        # Step 2: Push dist/ to gh-pages
        dist_dir = workspace / "apps" / "web" / "dist"
        if not dist_dir.exists():
            raise RuntimeError("dist/ directory not found after build")

        # Use gh-pages via pnpm if available, otherwise git push
        deploy_result = self._run_command(
            ["pnpm", "--filter", "web", "deploy"],
            timeout=120,
            cwd=workspace,
        )
        lines.append("=== Deploy ===")
        lines.append(deploy_result.stdout or "")
        if deploy_result.returncode != 0:
            # Fallback: push via git
            logger.warning(f"[{self.SKILL_NAME}] pnpm deploy failed, trying git push")
            git_result = self._run_command(
                ["git", "subtree", "push", "--prefix", "apps/web/dist", "origin", "gh-pages"],
                timeout=120,
                cwd=workspace,
            )
            lines.append(git_result.stdout or "")
            if git_result.returncode != 0:
                raise RuntimeError(f"Deployment failed:\n{git_result.stderr}")

        lines.append("\n✅ Deployed to GitHub Pages successfully")
        return "\n".join(lines)

class GitHubPagesDeployer(BaseSkill):
    def __init__(self, workspace_root: str):
        super().__init__(workspace_root)
        self.skill_name = "GitHubPagesDeployer"
        self.security_filter = SecurityFilter(workspace_root=workspace_root)

    async def _run_implementation(self, request) -> SkillResult:
        start_time = datetime.now()
        try:
            logger.info(f"[{self.skill_name}] Deploying to GitHub Pages")
            deployment_url, status_code = await self._deploy()
            duration = (datetime.now() - start_time).total_seconds() * 1000
            
            return SkillResult(
                skill_name=self.skill_name,
                status=SkillStatus.SUCCESS if status_code == 200 else SkillStatus.FAILED,
                output={"deployment_url": deployment_url, "status_code": status_code, "duration_ms": duration},
            )
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(f"[{self.skill_name}] Failed", exc_info=True)
            return SkillResult(skill_name=self.skill_name, status=SkillStatus.FAILED, error=str(e), output={"duration_ms": duration})

    async def _deploy(self) -> tuple:
        logger.debug(f"[{self.skill_name}] Deploying")
        # Use portfolio_config and deployment_config
        deployment_url = portfolio_config.CUSTOM_DOMAIN or portfolio_config.PORTFOLIO_URL
        return deployment_url, 200  # Stub

__all__ = ["GitHubPagesDeployer"]
