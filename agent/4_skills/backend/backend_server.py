"""Backend Server Skill - Run FastAPI backend server."""
import asyncio
from datetime import datetime
from agent_4_skills.base_skill import BaseSkill, SkillResult, SkillStatus
from agent_5_guardrails.security_filters import SecurityFilter
from agent_6_telemetry import get_logger
from agent.config import project_config

logger = get_logger(__name__)

class BackendServer(BaseSkill):
    def __init__(self, workspace_root: str):
        super().__init__(workspace_root)
        self.skill_name = "BackendServer"
        self.security_filter = SecurityFilter(workspace_root=workspace_root)

    async def _run_implementation(self, request) -> SkillResult:
        start_time = datetime.now()
        try:
            logger.info(f"[{self.skill_name}] Starting backend server")
            params = request.parameters
            port = params.get("port", None)
            server_port = port or project_config.API_PORT
            
            server_info = await self._start_server(server_port)
            duration = (datetime.now() - start_time).total_seconds() * 1000
            
            return SkillResult(
                skill_name=self.skill_name,
                status=SkillStatus.SUCCESS,
                output={**server_info, "duration_ms": duration},
            )
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(f"[{self.skill_name}] Failed", exc_info=True)
            return SkillResult(skill_name=self.skill_name, status=SkillStatus.FAILED, error=str(e), output={"duration_ms": duration})

    async def _start_server(self, port: int) -> dict:
        logger.debug(f"[{self.skill_name}] Starting")
        server_host = project_config.API_HOST
        server_port = port or project_config.API_PORT
        return {"server_url": f"http://{server_host}:{server_port}", "status": "running"}  # Stub

__all__ = ["BackendServer"]
