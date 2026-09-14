"""
Master Orchestrator Agent - Layer 4: Skills

28+ autonomous skills organized by domain:

Subpackages:
  - infrastructure/: Build, test, type checking, quality gates
  - testing/: Unit tests, E2E tests, coverage analysis
  - documents/: DOCX, PDF, Excel generation and sync
  - deployment/: Git operations, GitHub Pages, releases
  - portfolio/: Portfolio and CV management
  - quality/: Code formatting, linting, performance
  - backend/: FastAPI server, Python tests, API validation
"""

__version__ = "0.1.0"

# Skills will be dynamically loaded by orchestrator
__all__ = [
    "infrastructure",
    "testing",
    "documents",
    "deployment",
    "portfolio",
    "quality",
    "backend",
]
