"""
Execution State Manager

Tracks workflow execution state for recovery, retry logic,
and structured feedback re-injection to Copilot.

Usage:
    state = StateManager()
    state.start_workflow("ci")
    state.mark_step_done("type_checker", result)
    state.mark_step_failed("unit_test_runner", result)
    state.get_recovery_plan()   # what to retry
"""

import json
import logging
from enum import Enum
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

STATE_DIR = Path(__file__).parent.parent / ".state"


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowStep:
    def __init__(self, skill_name: str):
        self.skill_name = skill_name
        self.status = StepStatus.PENDING
        self.result_output: Optional[str] = None
        self.errors: List[str] = []
        self.started_at: Optional[str] = None
        self.finished_at: Optional[str] = None

    def start(self):
        self.status = StepStatus.RUNNING
        self.started_at = datetime.now().isoformat()

    def complete(self, output: Optional[str] = None):
        self.status = StepStatus.SUCCESS
        self.result_output = output
        self.finished_at = datetime.now().isoformat()

    def fail(self, errors: List[str], output: Optional[str] = None):
        self.status = StepStatus.FAILED
        self.errors = errors
        self.result_output = output
        self.finished_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_name": self.skill_name,
            "status": self.status.value,
            "result_output": self.result_output,
            "errors": self.errors,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
        }


class WorkflowState:
    """Full state of a running workflow"""

    def __init__(self, workflow_name: str, steps: List[str]):
        self.workflow_name = workflow_name
        self.steps: Dict[str, WorkflowStep] = {s: WorkflowStep(s) for s in steps}
        self.step_order = steps
        self.started_at = datetime.now().isoformat()
        self.finished_at: Optional[str] = None

    @property
    def is_complete(self) -> bool:
        return all(
            s.status in (StepStatus.SUCCESS, StepStatus.FAILED, StepStatus.SKIPPED)
            for s in self.steps.values()
        )

    @property
    def has_failures(self) -> bool:
        return any(s.status == StepStatus.FAILED for s in self.steps.values())

    @property
    def failed_steps(self) -> List[WorkflowStep]:
        return [s for s in self.steps.values() if s.status == StepStatus.FAILED]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_name": self.workflow_name,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "steps": {name: step.to_dict() for name, step in self.steps.items()},
        }


class StateManager:
    """
    Tracks workflow execution state for recovery and feedback.

    The recovery loop:
    1. Workflow starts → state persisted
    2. Step fails → step marked FAILED with errors
    3. get_recovery_plan() → returns what to retry and why
    4. Context injected to Copilot for auto-fix suggestion
    5. Retry runs → state updated
    """

    _instance: Optional["StateManager"] = None

    def __init__(self):
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        self._current_workflow: Optional[WorkflowState] = None

    @classmethod
    def get_instance(cls) -> "StateManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def start_workflow(self, workflow_name: str, steps: List[str]) -> WorkflowState:
        """Initialize state for a new workflow run"""
        self._current_workflow = WorkflowState(workflow_name, steps)
        self._persist()
        logger.info(f"Workflow '{workflow_name}' started with {len(steps)} steps")
        return self._current_workflow

    def mark_step_running(self, skill_name: str):
        """Mark a step as currently executing"""
        if self._current_workflow and skill_name in self._current_workflow.steps:
            self._current_workflow.steps[skill_name].start()
            self._persist()

    def mark_step_done(self, skill_name: str, result: Any):
        """Mark a step complete with its SkillResult"""
        if not self._current_workflow or skill_name not in self._current_workflow.steps:
            return
        step = self._current_workflow.steps[skill_name]
        if result.success:
            step.complete(output=result.output)
        else:
            step.fail(errors=result.errors, output=result.output)
        self._persist()

    def finish_workflow(self):
        """Mark workflow as fully complete"""
        if self._current_workflow:
            self._current_workflow.finished_at = datetime.now().isoformat()
            self._persist()
            status = "FAILED" if self._current_workflow.has_failures else "SUCCESS"
            logger.info(f"Workflow '{self._current_workflow.workflow_name}' finished: {status}")

    def get_recovery_plan(self) -> str:
        """
        Return a structured recovery plan for failed steps.
        This text is injected into Copilot for auto-fix suggestions.
        """
        if not self._current_workflow or not self._current_workflow.has_failures:
            return ""

        lines = [f"## 🔁 Recovery Plan — Workflow: `{self._current_workflow.workflow_name}`\n"]
        for step in self._current_workflow.failed_steps:
            lines.append(f"### ❌ Failed Step: `{step.skill_name}`")
            if step.errors:
                lines.append("**Errors to fix:**")
                for err in step.errors:
                    lines.append(f"  - {err}")
            if step.result_output:
                output_lines = step.result_output.strip().splitlines()
                trimmed = "\n".join(output_lines[-30:])
                lines.append(f"**Output:**\n```\n{trimmed}\n```")
            lines.append(f"**Action**: Re-run `{step.skill_name}` after fixing above errors.\n")

        return "\n".join(lines)

    def get_current_state(self) -> Optional[Dict[str, Any]]:
        """Return current workflow state as dict"""
        if self._current_workflow:
            return self._current_workflow.to_dict()
        return None

    def _persist(self):
        """Write current state to disk"""
        if not self._current_workflow:
            return
        try:
            filename = STATE_DIR / f"workflow_{self._current_workflow.workflow_name}.json"
            filename.write_text(json.dumps(self._current_workflow.to_dict(), indent=2))
        except Exception as e:
            logger.warning(f"Could not persist state: {e}")

    def load_last_state(self, workflow_name: str) -> Optional[Dict[str, Any]]:
        """Load last persisted state for a workflow"""
        filename = STATE_DIR / f"workflow_{workflow_name}.json"
        if filename.exists():
            try:
                return json.loads(filename.read_text())
            except Exception:
                return None
        return None
