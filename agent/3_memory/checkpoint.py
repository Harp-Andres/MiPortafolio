"""
Execution Checkpoint Manager

Captures SkillResult (stdout/stderr/errors) at each execution step
and persists them for feedback loop re-injection to Copilot.

Usage:
    checkpoint = CheckpointManager()
    checkpoint.save(skill_name, result)
    last = checkpoint.get_last_failure("type_checker")
    context = checkpoint.get_feedback_context()   # inject back to Copilot
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

# Store checkpoints in agent/.checkpoints/ (gitignored)
CHECKPOINT_DIR = Path(__file__).parent.parent / ".checkpoints"


class ExecutionRecord:
    """Single skill execution snapshot"""

    def __init__(
        self,
        skill_name: str,
        success: bool,
        output: Optional[str],
        errors: List[str],
        duration_seconds: float,
        metadata: Dict[str, Any],
    ):
        self.skill_name = skill_name
        self.success = success
        self.output = output
        self.errors = errors
        self.duration_seconds = duration_seconds
        self.metadata = metadata
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_name": self.skill_name,
            "success": self.success,
            "output": self.output,
            "errors": self.errors,
            "duration_seconds": self.duration_seconds,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_skill_result(cls, skill_name: str, result: Any) -> "ExecutionRecord":
        """Create from a SkillResult Pydantic object"""
        return cls(
            skill_name=skill_name,
            success=result.success,
            output=result.output,
            errors=result.errors,
            duration_seconds=result.duration_seconds,
            metadata=result.metadata if hasattr(result, "metadata") else {},
        )


class CheckpointManager:
    """
    Persists and retrieves execution state for the feedback loop.

    The feedback loop works:
    1. Skill fails → save checkpoint with errors
    2. get_feedback_context() returns structured error context
    3. Context is re-injected to Copilot prompt
    4. Copilot proposes fix based on structured errors
    5. Agent retries → save new checkpoint
    """

    _instance: Optional["CheckpointManager"] = None

    def __init__(self):
        CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
        self._session_records: List[ExecutionRecord] = []

    @classmethod
    def get_instance(cls) -> "CheckpointManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def save(self, skill_name: str, result: Any) -> ExecutionRecord:
        """Save execution result and persist to disk"""
        record = ExecutionRecord.from_skill_result(skill_name, result)
        self._session_records.append(record)

        # Persist failures to disk for recovery across sessions
        if not result.success:
            self._persist_failure(record)

        return record

    def get_last_failure(self, skill_name: Optional[str] = None) -> Optional[ExecutionRecord]:
        """Get most recent failure, optionally filtered by skill"""
        failures = [r for r in self._session_records if not r.success]
        if skill_name:
            failures = [r for r in failures if r.skill_name == skill_name]
        return failures[-1] if failures else None

    def get_session_summary(self) -> Dict[str, Any]:
        """Return session summary: successes, failures, duration"""
        total = len(self._session_records)
        successes = sum(1 for r in self._session_records if r.success)
        failures = total - successes
        return {
            "total_executions": total,
            "successes": successes,
            "failures": failures,
            "success_rate": round(successes / total * 100, 1) if total > 0 else 0,
            "failed_skills": [r.skill_name for r in self._session_records if not r.success],
        }

    def get_feedback_context(self) -> str:
        """
        Return structured error context for Copilot re-injection.
        This is what gets appended to the next Copilot prompt.
        """
        failures = [r for r in self._session_records if not r.success]
        if not failures:
            return ""

        lines = ["## ⚠️ Previous Execution Failures (feedback context)\n"]
        for record in failures[-5:]:  # Last 5 failures only
            lines.append(f"### Skill: `{record.skill_name}` — FAILED at {record.timestamp}")
            if record.errors:
                lines.append("**Errors:**")
                for err in record.errors:
                    lines.append(f"  - {err}")
            if record.output:
                # Trim output to last 50 lines to avoid context overflow
                output_lines = record.output.strip().splitlines()
                trimmed = "\n".join(output_lines[-50:])
                lines.append(f"**Output (last 50 lines):**\n```\n{trimmed}\n```")
            lines.append("")

        return "\n".join(lines)

    def clear_session(self):
        """Clear in-memory session records"""
        self._session_records.clear()

    def _persist_failure(self, record: ExecutionRecord):
        """Write failure to disk for cross-session recovery"""
        try:
            filename = CHECKPOINT_DIR / f"failure_{record.skill_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filename.write_text(json.dumps(record.to_dict(), indent=2))
        except Exception as e:
            logger.warning(f"Could not persist checkpoint: {e}")

    def load_last_disk_failure(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """Load most recent persisted failure for a skill"""
        pattern = f"failure_{skill_name}_*.json"
        files = sorted(CHECKPOINT_DIR.glob(pattern))
        if not files:
            return None
        try:
            return json.loads(files[-1].read_text())
        except Exception:
            return None
