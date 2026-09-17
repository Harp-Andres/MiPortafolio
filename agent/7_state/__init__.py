"""
Master Orchestrator Agent - Layer 7: State

Checkpoint management and state persistence.

Modules:
  - state_manager.py: State lifecycle management
  - models.py: State data models
  - repository.py: State storage backend (SQLite, file-based)
"""

__version__ = "0.1.0"
__all__ = ["state_manager", "models", "repository"]
