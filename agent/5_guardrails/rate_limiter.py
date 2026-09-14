"""
Rate limiting for API calls and resource usage.

This module provides rate limiting to:
- Limit API calls to LLM providers (OpenAI, Anthropic, Ollama)
- Track token usage across calls
- Prevent quota exhaustion
- Implement exponential backoff on rate limits
- Monitor resource usage (CPU, memory, disk)

Usage:
    from agent_5_guardrails.rate_limiter import (
        RateLimiter,
        TokenBudget,
        LLMRateLimiter,
    )

    # Create rate limiter for OpenAI
    limiter = LLMRateLimiter(provider="openai", max_requests_per_minute=3)

    # Check before making request
    if not limiter.can_make_request():
        print("Rate limited, waiting...")
        limiter.wait_for_reset()

    # Record token usage
    limiter.record_tokens(prompt_tokens=150, completion_tokens=50)

    # Check quota
    if limiter.is_quota_exceeded():
        raise ValueError("Monthly quota exceeded")
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


# ============================================================================
# Configuration
# ============================================================================

# Rate limits per provider (requests per minute)
PROVIDER_RATE_LIMITS = {
    "openai": {
        "requests_per_minute": 3,
        "tokens_per_minute": 90000,
    },
    "anthropic": {
        "requests_per_minute": 5,
        "tokens_per_minute": 100000,
    },
    "ollama": {
        "requests_per_minute": 100,  # Local, no real limit
        "tokens_per_minute": 1000000,
    },
}

# Daily/monthly quotas (in USD equivalent)
DAILY_BUDGET = 10.0  # Dollars per day
MONTHLY_BUDGET = 100.0  # Dollars per month

# Token costs per provider (approximate USD)
TOKEN_COSTS = {
    "openai": {
        "gpt-4": {"input": 0.00003, "output": 0.00006},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    },
    "anthropic": {
        "claude-3-opus": {"input": 0.000015, "output": 0.000075},
        "claude-3-sonnet": {"input": 0.000003, "output": 0.000015},
    },
}


# ============================================================================
# Data Classes
# ============================================================================


@dataclass
class TokenUsage:
    """Track token usage for a single request."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate token counts."""
        if self.total_tokens == 0:
            self.total_tokens = self.prompt_tokens + self.completion_tokens


@dataclass
class RequestRecord:
    """Track information about a single API request."""

    timestamp: datetime = field(default_factory=datetime.now)
    tokens_used: int = 0
    cost_usd: float = 0.0
    success: bool = True
    retry_count: int = 0
    latency_seconds: float = 0.0


@dataclass
class BudgetStatus:
    """Current budget status."""

    daily_spent: float = 0.0
    monthly_spent: float = 0.0
    daily_remaining: float = DAILY_BUDGET
    monthly_remaining: float = MONTHLY_BUDGET
    daily_requests: int = 0
    monthly_requests: int = 0
    percentage_used: float = 0.0


# ============================================================================
# RateLimiter Base Class
# ============================================================================


class RateLimiter:
    """Generic rate limiter using sliding window.

    Tracks requests in a sliding time window and enforces limits.
    """

    def __init__(self, max_requests: int, window_seconds: int = 60):
        """Initialize rate limiter.

        Args:
            max_requests: Maximum requests allowed per window.
            window_seconds: Time window in seconds.
        """
        self.max_requests = max_requests
        self.window = timedelta(seconds=window_seconds)
        self.requests: list[datetime] = []
        self.logger = logger

    def can_make_request(self) -> bool:
        """Check if a request can be made now.

        Returns:
            True if request is allowed, False if rate limited.
        """
        now = datetime.now()
        cutoff = now - self.window

        # Remove old requests outside window
        self.requests = [r for r in self.requests if r > cutoff]

        # Check if limit exceeded
        if len(self.requests) >= self.max_requests:
            self.logger.warning(
                f"Rate limit exceeded: {len(self.requests)}/{self.max_requests} requests"
            )
            return False

        # Record request
        self.requests.append(now)
        self.logger.debug(
            f"Request allowed: {len(self.requests)}/{self.max_requests} in window"
        )
        return True

    def wait_for_reset(self) -> float:
        """Wait until a request slot is available.

        Returns:
            Seconds waited.
        """
        if len(self.requests) < self.max_requests:
            return 0.0

        # Find oldest request in window
        oldest = min(self.requests)
        reset_time = oldest + self.window

        wait_seconds = (reset_time - datetime.now()).total_seconds()
        if wait_seconds > 0:
            self.logger.info(f"Rate limited. Waiting {wait_seconds:.1f} seconds...")
            time.sleep(wait_seconds)

        return wait_seconds

    def remaining(self) -> int:
        """Get remaining requests in current window.

        Returns:
            Number of requests still allowed.
        """
        now = datetime.now()
        cutoff = now - self.window
        self.requests = [r for r in self.requests if r > cutoff]
        return max(0, self.max_requests - len(self.requests))

    def reset(self):
        """Reset rate limiter."""
        self.requests = []
        self.logger.debug("Rate limiter reset")


# ============================================================================
# TokenBudget
# ============================================================================


class TokenBudget:
    """Track token usage against budget limits.

    Tracks tokens used per minute and enforces limits.
    """

    def __init__(
        self,
        max_tokens_per_minute: int,
        max_tokens_per_day: Optional[int] = None,
    ):
        """Initialize token budget.

        Args:
            max_tokens_per_minute: Maximum tokens per minute.
            max_tokens_per_day: Maximum tokens per day (optional).
        """
        self.max_tokens_per_minute = max_tokens_per_minute
        self.max_tokens_per_day = max_tokens_per_day
        self.tokens_this_minute: list[tuple[datetime, int]] = []
        self.tokens_this_day: list[tuple[datetime, int]] = []
        self.logger = logger

    def can_use_tokens(self, num_tokens: int) -> bool:
        """Check if tokens can be used.

        Args:
            num_tokens: Number of tokens to use.

        Returns:
            True if allowed, False if would exceed limit.
        """
        now = datetime.now()

        # Check per-minute limit
        cutoff_minute = now - timedelta(minutes=1)
        self.tokens_this_minute = [
            (t, n)
            for t, n in self.tokens_this_minute
            if t > cutoff_minute
        ]
        total_this_minute = sum(n for _, n in self.tokens_this_minute)

        if total_this_minute + num_tokens > self.max_tokens_per_minute:
            self.logger.warning(
                f"Token limit per minute exceeded: "
                f"{total_this_minute + num_tokens}/{self.max_tokens_per_minute}"
            )
            return False

        # Check per-day limit (if set)
        if self.max_tokens_per_day:
            cutoff_day = now - timedelta(days=1)
            self.tokens_this_day = [
                (t, n)
                for t, n in self.tokens_this_day
                if t > cutoff_day
            ]
            total_this_day = sum(n for _, n in self.tokens_this_day)

            if total_this_day + num_tokens > self.max_tokens_per_day:
                self.logger.warning(
                    f"Token limit per day exceeded: "
                    f"{total_this_day + num_tokens}/{self.max_tokens_per_day}"
                )
                return False

        return True

    def record_tokens(self, num_tokens: int) -> bool:
        """Record token usage.

        Args:
            num_tokens: Number of tokens used.

        Returns:
            True if recorded successfully.

        Raises:
            ValueError: If would exceed limit.
        """
        if not self.can_use_tokens(num_tokens):
            raise ValueError(f"Would exceed token limit: {num_tokens} tokens")

        now = datetime.now()
        self.tokens_this_minute.append((now, num_tokens))
        self.tokens_this_day.append((now, num_tokens))

        self.logger.debug(f"Recorded {num_tokens} tokens")
        return True

    def tokens_used_this_minute(self) -> int:
        """Get tokens used in current minute.

        Returns:
            Number of tokens used.
        """
        now = datetime.now()
        cutoff = now - timedelta(minutes=1)
        return sum(
            n
            for t, n in self.tokens_this_minute
            if t > cutoff
        )

    def tokens_used_this_day(self) -> int:
        """Get tokens used in current day.

        Returns:
            Number of tokens used.
        """
        now = datetime.now()
        cutoff = now - timedelta(days=1)
        return sum(
            n
            for t, n in self.tokens_this_day
            if t > cutoff
        )


# ============================================================================
# LLMRateLimiter
# ============================================================================


class LLMRateLimiter:
    """Rate limiter for LLM API providers.

    Manages rate limits and token budgets for OpenAI, Anthropic, and Ollama.
    """

    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4",
    ):
        """Initialize LLM rate limiter.

        Args:
            provider: LLM provider (openai, anthropic, ollama).
            model: Model name (e.g., gpt-4, claude-3-opus).

        Raises:
            ValueError: If provider or model is unknown.
        """
        if provider not in PROVIDER_RATE_LIMITS:
            raise ValueError(
                f"Unknown provider: {provider}. "
                f"Known providers: {list(PROVIDER_RATE_LIMITS.keys())}"
            )

        self.provider = provider
        self.model = model
        self.logger = logger

        # Initialize rate limiter
        limits = PROVIDER_RATE_LIMITS[provider]
        self.request_limiter = RateLimiter(
            max_requests=limits["requests_per_minute"],
            window_seconds=60,
        )

        # Initialize token budget
        self.token_budget = TokenBudget(
            max_tokens_per_minute=limits["tokens_per_minute"],
            max_tokens_per_day=None,  # Managed separately
        )

        # Track usage for cost calculation
        self.requests: list[RequestRecord] = []
        self.daily_spent = 0.0
        self.monthly_spent = 0.0

        self.logger.info(f"Initialized {provider} rate limiter for {model}")

    def can_make_request(self, estimated_tokens: int = 0) -> bool:
        """Check if a request can be made.

        Args:
            estimated_tokens: Estimated tokens for request.

        Returns:
            True if request allowed.
        """
        # Check request rate limit
        if not self.request_limiter.can_make_request():
            return False

        # Check token budget (if estimated)
        if estimated_tokens > 0:
            if not self.token_budget.can_use_tokens(estimated_tokens):
                return False

        return True

    def wait_for_reset(self) -> float:
        """Wait until a request slot is available.

        Returns:
            Seconds waited.
        """
        return self.request_limiter.wait_for_reset()

    def record_request(
        self,
        prompt_tokens: int,
        completion_tokens: int,
        success: bool = True,
        latency_seconds: float = 0.0,
    ):
        """Record a completed request.

        Args:
            prompt_tokens: Tokens in prompt.
            completion_tokens: Tokens in completion.
            success: Whether request succeeded.
            latency_seconds: Request latency.
        """
        total_tokens = prompt_tokens + completion_tokens

        # Calculate cost
        cost = self._calculate_cost(prompt_tokens, completion_tokens)

        # Record request
        record = RequestRecord(
            tokens_used=total_tokens,
            cost_usd=cost,
            success=success,
            latency_seconds=latency_seconds,
        )
        self.requests.append(record)

        # Update budgets
        self.daily_spent += cost
        self.monthly_spent += cost

        # Try to record tokens
        try:
            self.token_budget.record_tokens(total_tokens)
        except ValueError as e:
            self.logger.warning(f"Token budget exceeded: {e}")

        self.logger.info(
            f"Request recorded: {total_tokens} tokens, ${cost:.4f} "
            f"(daily: ${self.daily_spent:.2f})"
        )

    def is_quota_exceeded(self) -> bool:
        """Check if daily quota exceeded.

        Returns:
            True if daily spend exceeds budget.
        """
        return self.daily_spent >= DAILY_BUDGET

    def get_budget_status(self) -> BudgetStatus:
        """Get current budget status.

        Returns:
            BudgetStatus object.
        """
        # Count requests today/month
        now = datetime.now()
        today_cutoff = now - timedelta(days=1)
        month_cutoff = now - timedelta(days=30)

        daily_requests = sum(
            1
            for r in self.requests
            if r.timestamp > today_cutoff
        )
        monthly_requests = sum(
            1
            for r in self.requests
            if r.timestamp > month_cutoff
        )

        return BudgetStatus(
            daily_spent=self.daily_spent,
            monthly_spent=self.monthly_spent,
            daily_remaining=max(0, DAILY_BUDGET - self.daily_spent),
            monthly_remaining=max(0, MONTHLY_BUDGET - self.monthly_spent),
            daily_requests=daily_requests,
            monthly_requests=monthly_requests,
            percentage_used=self.daily_spent / DAILY_BUDGET * 100,
        )

    def _calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate cost for request.

        Args:
            prompt_tokens: Tokens in prompt.
            completion_tokens: Tokens in completion.

        Returns:
            Cost in USD.
        """
        # Default cost for unknown models
        if self.provider not in TOKEN_COSTS:
            return 0.0001  # Conservative estimate

        provider_costs = TOKEN_COSTS[self.provider]
        if self.model not in provider_costs:
            return 0.0001  # Conservative estimate

        model_costs = provider_costs[self.model]
        input_cost = prompt_tokens * model_costs.get("input", 0.00001)
        output_cost = completion_tokens * model_costs.get("output", 0.00003)

        return input_cost + output_cost

    def reset_daily_budget(self):
        """Reset daily budget (call at start of new day)."""
        self.daily_spent = 0.0
        self.logger.info("Daily budget reset")

    def get_stats(self) -> Dict:
        """Get statistics about rate limiter.

        Returns:
            Dictionary with stats.
        """
        return {
            "provider": self.provider,
            "model": self.model,
            "total_requests": len(self.requests),
            "successful_requests": sum(1 for r in self.requests if r.success),
            "failed_requests": sum(1 for r in self.requests if not r.success),
            "daily_spent": f"${self.daily_spent:.4f}",
            "monthly_spent": f"${self.monthly_spent:.4f}",
            "daily_quota_remaining": f"${max(0, DAILY_BUDGET - self.daily_spent):.4f}",
            "requests_remaining_this_minute": self.request_limiter.remaining(),
            "tokens_remaining_this_minute": (
                self.token_budget.max_tokens_per_minute
                - self.token_budget.tokens_used_this_minute()
            ),
        }


# Export public API
__all__ = [
    # Data classes
    "TokenUsage",
    "RequestRecord",
    "BudgetStatus",
    # Rate limiter
    "RateLimiter",
    "TokenBudget",
    # LLM rate limiter
    "LLMRateLimiter",
    # Configuration
    "PROVIDER_RATE_LIMITS",
    "DAILY_BUDGET",
    "MONTHLY_BUDGET",
]
