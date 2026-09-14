"""
Master Orchestrator Agent - Layer 3: Memory

Manages conversation history, repository understanding, and state persistence.

Modules:
  - conversation.py: Conversation history storage and retrieval
  - rag_indexer.py: Repository RAG indexer for codebase understanding
  - checkpoint.py: Checkpoint management for state persistence
"""

__version__ = "0.1.0"
__all__ = ["conversation", "rag_indexer", "checkpoint"]
