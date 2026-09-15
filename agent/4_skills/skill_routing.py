"""
Skill Routing - Determines which agent should execute which skill

Implements routing logic based on:
1. Primary skill ownership (which agent owns this skill)
2. Skill dependencies (prerequisites)
3. Agent availability/load
4. Fallback routing (if primary agent unavailable)

Usage:
    router = SkillRouter()
    agent_id = router.route_skill("type_checker", context)
"""

import logging
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class AgentRole(str, Enum):
    """Agent roles in the system"""
    MAESTRO = "maestro"  # Master orchestrator
    BACKEND = "backend"  # Backend/Infrastructure agent
    TESTING = "testing"  # Testing agent
    DEPLOYMENT = "deployment"  # Deployment agent
    PORTFOLIO = "portfolio"  # Portfolio/Documents agent
    QUALITY = "quality"  # Code quality agent


@dataclass
class RoutingContext:
    """Context for skill routing decisions"""
    skill_name: str
    requested_by: Optional[AgentRole] = None
    execution_order: int = 0
    allow_parallel: bool = True
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class SkillRouter:
    """
    Routes skills to appropriate agents based on ownership and dependencies.
    
    Skill Ownership Model:
    - Each skill has a PRIMARY agent (usually executes it)
    - Some skills are SHARED (any agent can execute)
    - Some skills have DEPENDENCIES on other skills
    """

    # Primary skill ownership - maps skill_name to primary AgentRole
    SKILL_OWNERSHIP: Dict[str, AgentRole] = {
        # Infrastructure Skills - Backend agent (or any)
        "type_checker": AgentRole.BACKEND,
        "build_orchestrator": AgentRole.BACKEND,
        "dependency_resolver": AgentRole.BACKEND,
        "quality_gate_runner": AgentRole.BACKEND,
        
        # Testing Skills - Testing agent (primary)
        "unit_test_runner": AgentRole.TESTING,
        "e2e_test_runner": AgentRole.TESTING,
        "coverage_analyzer": AgentRole.TESTING,
        "test_aggregator": AgentRole.TESTING,
        
        # Document Skills - Portfolio agent (primary)
        "pdf_generator": AgentRole.PORTFOLIO,
        "docx_generator": AgentRole.PORTFOLIO,
        "excel_generator": AgentRole.PORTFOLIO,
        "cv_data_validator": AgentRole.PORTFOLIO,
        "sync_verifier": AgentRole.PORTFOLIO,
        
        # Deployment Skills - Deployment agent (primary)
        "github_pages_deployer": AgentRole.DEPLOYMENT,
        "git_workflow_manager": AgentRole.DEPLOYMENT,
        "release_orchestrator": AgentRole.DEPLOYMENT,
        "git_branch_creator": AgentRole.DEPLOYMENT,
        
        # Portfolio Skills - Portfolio agent
        "certificate_manager": AgentRole.PORTFOLIO,
        "experience_tracker": AgentRole.PORTFOLIO,
        "portfolio_updater": AgentRole.PORTFOLIO,
        "skills_manager": AgentRole.PORTFOLIO,
        
        # Quality Skills - Quality agent
        "linter_checker": AgentRole.QUALITY,
        "code_formatter": AgentRole.QUALITY,
        "performance_monitor": AgentRole.QUALITY,
        
        # Backend Skills - Backend agent
        "api_validator": AgentRole.BACKEND,
        "backend_server": AgentRole.BACKEND,
        "backend_test_runner": AgentRole.BACKEND,
    }

    # Skill dependencies - which skills must run before this one
    SKILL_DEPENDENCIES: Dict[str, List[str]] = {
        "test_aggregator": ["unit_test_runner", "e2e_test_runner"],
        "quality_gate_runner": ["type_checker", "unit_test_runner"],
        "coverage_analyzer": ["unit_test_runner", "e2e_test_runner"],
        "github_pages_deployer": ["quality_gate_runner", "build_orchestrator"],
        "release_orchestrator": ["github_pages_deployer", "git_workflow_manager"],
        "pdf_generator": ["cv_data_validator"],
        "docx_generator": ["cv_data_validator"],
        "excel_generator": ["cv_data_validator"],
        "sync_verifier": ["pdf_generator", "docx_generator", "excel_generator"],
        "portfolio_updater": ["cv_data_validator"],
    }

    # Shared skills - can be executed by any agent
    SHARED_SKILLS: Set[str] = {
        "type_checker",
        "dependency_resolver",
        "build_orchestrator",
        "backend_test_runner",
    }

    def __init__(self):
        """Initialize skill router"""
        self.agent_loads: Dict[AgentRole, int] = {
            AgentRole.BACKEND: 0,
            AgentRole.TESTING: 0,
            AgentRole.DEPLOYMENT: 0,
            AgentRole.PORTFOLIO: 0,
            AgentRole.QUALITY: 0,
        }

    def route_skill(
        self,
        skill_name: str,
        context: Optional[RoutingContext] = None,
    ) -> AgentRole:
        """
        Route a skill to the appropriate agent.

        Routing logic (in priority order):
        1. If skill is shared and requested_by is set, use requested_by
        2. Use primary ownership
        3. If primary unavailable, use fallback agent
        4. Use least-loaded agent if multiple can handle

        Args:
            skill_name: Name of skill to route
            context: Routing context with additional info

        Returns:
            AgentRole that should execute the skill
        """
        if context is None:
            context = RoutingContext(skill_name=skill_name)

        logger.debug(
            f"Routing skill: {skill_name} "
            f"(requested_by={context.requested_by}, order={context.execution_order})"
        )

        # Rule 1: Check if this is a shared skill and requester specified
        if skill_name in self.SHARED_SKILLS and context.requested_by:
            logger.debug(f"  → Shared skill, using requested agent: {context.requested_by}")
            return context.requested_by

        # Rule 2: Use primary ownership
        primary_agent = self.SKILL_OWNERSHIP.get(skill_name, AgentRole.MAESTRO)
        if primary_agent and primary_agent != AgentRole.MAESTRO:
            logger.debug(f"  → Using primary owner: {primary_agent}")
            return primary_agent

        # Rule 3: Fallback to least-loaded suitable agent
        logger.debug(f"  → No specific owner, using least-loaded agent")
        return self._get_least_loaded_agent()

    def get_skill_dependencies(self, skill_name: str) -> List[str]:
        """
        Get list of skills that must run before this skill.

        Args:
            skill_name: Name of skill

        Returns:
            List of dependency skill names
        """
        return self.SKILL_DEPENDENCIES.get(skill_name, [])

    def get_skill_owner(self, skill_name: str) -> AgentRole:
        """
        Get primary owner of a skill.

        Args:
            skill_name: Name of skill

        Returns:
            AgentRole that primarily owns this skill
        """
        return self.SKILL_OWNERSHIP.get(skill_name, AgentRole.BACKEND)

    def is_shared_skill(self, skill_name: str) -> bool:
        """
        Check if a skill can be executed by any agent.

        Args:
            skill_name: Name of skill

        Returns:
            True if skill is shared
        """
        return skill_name in self.SHARED_SKILLS

    def update_agent_load(self, agent: AgentRole, delta: int = 1) -> None:
        """
        Update agent load tracking (for scheduling).

        Args:
            agent: Agent role
            delta: Change in load (usually +1 for starting task, -1 for completing)
        """
        if agent in self.agent_loads:
            self.agent_loads[agent] += delta
            logger.debug(f"Agent load updated: {agent}={self.agent_loads[agent]}")

    def reset_loads(self) -> None:
        """Reset all agent load counters"""
        for agent in self.agent_loads:
            self.agent_loads[agent] = 0
        logger.debug("Agent loads reset")

    def get_agent_load(self, agent: AgentRole) -> int:
        """Get current load for agent"""
        return self.agent_loads.get(agent, 0)

    def _get_least_loaded_agent(self) -> AgentRole:
        """Get the least-loaded agent"""
        return min(self.agent_loads, key=self.agent_loads.get)

    def can_execute_parallel(
        self,
        skills: List[str],
    ) -> bool:
        """
        Check if multiple skills can be executed in parallel.

        Args:
            skills: List of skill names

        Returns:
            True if skills can run in parallel (no dependencies between them)
        """
        # Build dependency graph
        for skill in skills:
            deps = self.get_skill_dependencies(skill)
            for dep in deps:
                if dep in skills:
                    # Found circular dependency or conflicting requirement
                    logger.warning(
                        f"Skill '{skill}' depends on '{dep}' but both scheduled in parallel"
                    )
                    return False
        return True

    def validate_skill_exists(self, skill_name: str) -> bool:
        """Check if skill is registered"""
        return skill_name in self.SKILL_OWNERSHIP

    def list_skills_by_agent(self, agent: AgentRole) -> List[str]:
        """Get all skills owned by an agent"""
        return [
            skill for skill, owner in self.SKILL_OWNERSHIP.items()
            if owner == agent
        ]

    def get_routing_info(self, skill_name: str) -> Dict[str, any]:
        """
        Get routing information for a skill.

        Args:
            skill_name: Name of skill

        Returns:
            Dict with routing info
        """
        return {
            "skill_name": skill_name,
            "primary_owner": self.get_skill_owner(skill_name),
            "dependencies": self.get_skill_dependencies(skill_name),
            "is_shared": self.is_shared_skill(skill_name),
        }


# Singleton instance
_router_instance: Optional[SkillRouter] = None


def get_skill_router() -> SkillRouter:
    """Get global skill router instance"""
    global _router_instance
    if _router_instance is None:
        _router_instance = SkillRouter()
    return _router_instance
