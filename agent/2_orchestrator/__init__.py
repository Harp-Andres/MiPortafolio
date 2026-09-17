"""
Master Orchestrator Agent - Layer 2: Orchestrator

Implements the ReAct (Reasoning + Acting) engine that orchestrates skill execution.

Modules:
  - react_engine.py: Core ReAct loop implementation
  - lm_factory.py: LLM provider factory (OpenAI, Anthropic, Ollama)
  - prompts.py: Agent prompts and templates
  - workflows/: Predefined workflow templates
"""

__version__ = "0.1.0"
__all__ = ["react_engine", "lm_factory", "prompts"]
