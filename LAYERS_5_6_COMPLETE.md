---
title: "Layer 5 & 6: Guardrails + Telemetry - Complete"
description: "Validation, security, rate limiting, logging, metrics, and tracing"
date: "2024"
---

# ✅ Layers 5 & 6 Complete

## 📋 Implementation Summary

**Layer 5 (Guardrails) - COMPLETE:** Input validation, security, rate limiting
**Layer 6 (Telemetry) - COMPLETE:** Logging, metrics, distributed tracing

### Files Created

#### Layer 5: Guardrails (3 files, 1,100+ lines)

| File | Lines | Purpose |
|------|-------|---------|
| `agent/5_guardrails/validators.py` | 500+ | Pydantic input validation for all CLI commands |
| `agent/5_guardrails/security_filters.py` | 450+ | Command injection prevention, security checks |
| `agent/5_guardrails/rate_limiter.py` | 450+ | API rate limiting and quota management |

#### Layer 6: Telemetry (3 files, 1,200+ lines)

| File | Lines | Purpose |
|------|-------|---------|
| `agent/6_telemetry/logger.py` | 450+ | Structured logging with Rich/JSON output |
| `agent/6_telemetry/metrics.py` | 400+ | Performance metrics collection |
| `agent/6_telemetry/tracer.py` | 350+ | Distributed tracing and span management |

**Total:** 2,300+ lines of infrastructure code

---

## 🛡️ Layer 5: Guardrails

### Validators (`validators.py`)

**6 Pydantic Validator Classes:**

```python
# 1. CI/CD Pipeline Validation
ci_request = CICommandValidator(
    stages="types,quality,build",
    verbose=True
)

# 2. Deployment Validation
deploy_request = DeployCommandValidator(
    environment=Environment.PRODUCTION,
    force=False,
    verbose=True
)

# 3. Testing Validation
test_request = TestCommandValidator(
    suite=TestSuite.UNIT,
    coverage=True,
    verbose=False
)

# 4. Documentation Validation
docs_request = DocsCommandValidator(
    format=DocumentFormat.ALL,
    output_dir="/output",
    sync_verify=True
)

# 5. Portfolio Project Validation
project_request = AddProjectCommandValidator(
    name="My AI Project",
    description="An AI-powered assistant",
    technologies="Python,FastAPI,LangChain",
    link="https://example.com",
    github="https://github.com/user/project"
)

# 6. Environment Check Validation
env_request = EnvironmentCheckValidator(verbose=True)
```

**Features:**
- ✅ Automatic type validation
- ✅ Enum-based constraints
- ✅ Path validation (resolve, check existence)
- ✅ URL validation (http/https)
- ✅ Technology list parsing
- ✅ Friendly error messages

**ValidatorFactory for Dynamic Creation:**
```python
validator = ValidatorFactory.create("ci", stages="types,quality")
# or
validator = ValidatorFactory.create("deploy", environment="staging")
```

---

### Security Filters (`security_filters.py`)

**Sanitization Functions:**
```python
# Sanitize command arguments
safe_arg = sanitize_command_arg("user-input; rm -rf /")

# Sanitize file paths
safe_path = sanitize_file_path("/path/to/file.txt")

# Sanitize environment variables
key, value = sanitize_env_var("API_KEY", "secret123")
```

**Validation Functions:**
```python
# Validate file path (resolve, check workspace boundary)
validated_path = validate_safe_path(
    "/file.txt",
    workspace_root="/home/user/project",
    allow_outside_workspace=False
)

# Validate subprocess arguments (list-based, no shell)
validate_subprocess_args(["python", "script.py", "arg1"])

# Validate URL
validate_url("https://github.com/user/repo")
```

**Injection Detection:**
```python
# Detect injection attempts
injections = detect_injection_attempts("user; rm -rf /")
# Returns: ['dangerous_commands_pattern', ...]

# Quick check
if is_suspicious_input(user_input):
    raise SecurityError("Suspicious input detected")
```

**SecurityFilter Class:**
```python
filter = SecurityFilter(workspace_root="/project")

# Validate file operations
safe_path = filter.validate_file_operation("/file.txt", "read")

# Validate subprocess commands
filter.validate_subprocess_command(["python", "script.py"])

# Validate environment variables
key, value = filter.validate_environment_variable("API_KEY", "secret")

# Validate URLs
filter.validate_url("https://example.com")
```

---

### Rate Limiting (`rate_limiter.py`)

**Generic Rate Limiter:**
```python
limiter = RateLimiter(max_requests=3, window_seconds=60)

if limiter.can_make_request():
    # Make API call
    pass
else:
    limiter.wait_for_reset()

remaining = limiter.remaining()  # Requests left in window
```

**Token Budget (for LLM calls):**
```python
budget = TokenBudget(
    max_tokens_per_minute=90000,
    max_tokens_per_day=1000000
)

if budget.can_use_tokens(1500):
    budget.record_tokens(1500)

tokens_left_minute = (
    budget.max_tokens_per_minute 
    - budget.tokens_used_this_minute()
)
```

**LLM Rate Limiter:**
```python
limiter = LLMRateLimiter(provider="openai", model="gpt-4")

# Check before request
if limiter.can_make_request(estimated_tokens=500):
    # Make request
    limiter.record_request(
        prompt_tokens=450,
        completion_tokens=150,
        success=True,
        latency_seconds=0.5
    )

# Track costs
status = limiter.get_budget_status()
print(f"Daily spent: ${status.daily_spent:.2f}")
print(f"Quota remaining: ${status.daily_remaining:.2f}")

# Get statistics
stats = limiter.get_stats()
```

**Provider Rate Limits:**
- OpenAI: 3 req/min, 90k tokens/min
- Anthropic: 5 req/min, 100k tokens/min
- Ollama: 100 req/min (local)

**Budget Limits:**
- Daily: $10
- Monthly: $100

---

## 📊 Layer 6: Telemetry

### Logger (`logger.py`)

**Setup Logging:**
```python
from agent_6_telemetry import setup_logging, get_logger

# Setup at startup
setup_logging(
    level="INFO",
    json_output=True,  # JSON for files
    use_rich=True,     # Rich colors for console
    debug=False
)

# Get logger for module
logger = get_logger(__name__)
```

**Output Formats:**
- **Console:** Rich-formatted with colors
- **File:** Structured format (plain or JSON)
- **JSON:** For parsing by log aggregators

**Logging Examples:**
```python
logger = get_logger("my_module")

# Basic logging
logger.info("Operation started")
logger.error("Error occurred", exc_info=True)

# Structured logging with context
logger.info(
    "Task completed",
    extra={
        "task_id": "123",
        "duration_ms": 1500,
        "status": "success"
    }
)

# Log skill execution
logger.info("Skill execution", extra={
    "skill": "type_checker",
    "duration_ms": 2500,
    "files_checked": 45,
    "errors": 3
})
```

**Log Context (automatic context injection):**
```python
from agent_6_telemetry import LogContext

with LogContext(task_id="123", stage="build"):
    logger.info("Building...")  # Auto includes task_id and stage
    logger.info("Linking...")   # Auto includes task_id and stage
```

**Structured Log Records:**
```python
from agent_6_telemetry import LogRecord

# Skill records
logger.info("Event", extra=LogRecord.skill_started(
    "type_checker",
    params={"strict": True}
))

logger.info("Event", extra=LogRecord.skill_completed(
    "type_checker",
    duration_ms=2500,
    result={"errors": 3}
))

# API records
logger.info("Event", extra=LogRecord.api_call(
    provider="openai",
    model="gpt-4",
    tokens_used=1500,
    cost_usd=0.045
))
```

---

### Metrics (`metrics.py`)

**Counters (monotonically increasing):**
```python
from agent_6_telemetry import MetricsCollector

metrics = MetricsCollector()

metrics.increment("tests_passed", 5)
metrics.increment("tests_failed", 2)

# Get value
failed_count = metrics.get_counter("tests_failed")
```

**Gauges (current values):**
```python
metrics.set_gauge("memory_mb", 512)
metrics.set_gauge("cpu_percent", 45.5)

# Get value
memory = metrics.get_gauge("memory_mb")
```

**Histograms (distributions):**
```python
# Record timing
metrics.observe_histogram("request_time_ms", 125.5)
metrics.observe_histogram("request_time_ms", 150.2)
metrics.observe_histogram("request_time_ms", 98.7)

# Get histogram
hist = metrics.get_histogram("request_time_ms")
print(f"Mean: {hist.mean():.2f}ms")
print(f"Median: {hist.median():.2f}ms")
print(f"Min: {hist.min():.2f}ms, Max: {hist.max():.2f}ms")
print(f"Std Dev: {hist.stdev():.2f}ms")
```

**Timer Context Manager:**
```python
from agent_6_telemetry import Timer

with Timer(metrics, "build_time_ms"):
    run_build()  # Automatically recorded

with Timer(metrics, "build_stage_compile_ms", labels={"target": "web"}):
    compile_web()
```

**Metrics Report:**
```python
# Get full report
report = metrics.get_report()
# {
#   "timestamp": "2024-...",
#   "uptime_seconds": 123.45,
#   "counters": {"tests_passed": 5, "tests_failed": 2},
#   "gauges": {"memory_mb": 512},
#   "histograms": {
#     "request_time_ms": {
#       "count": 3,
#       "mean": 124.8,
#       "median": 125.5,
#       ...
#     }
#   }
# }

# Get summary
print(metrics.get_summary())
```

**Specialized Metrics:**
```python
from agent_6_telemetry import BuildMetrics, TestMetrics

# Build metrics
build_metrics = BuildMetrics(metrics)
build_metrics.record_build_stage_complete("compile", 500.5)
build_metrics.record_build_artifact("app.tar.gz", 1024000)

# Test metrics
test_metrics = TestMetrics(metrics)
test_metrics.record_test_result(
    suite="unit",
    passed=150,
    failed=2,
    skipped=5,
    duration_ms=3500
)
test_metrics.record_coverage("unit", 92.5)
```

---

### Tracer (`tracer.py`)

**Create Traces:**
```python
from agent_6_telemetry import get_tracer

tracer = get_tracer("my-service")

# Start root span
with tracer.start_span("ci_pipeline") as root_span:
    root_span.add_attribute("env", "production")
    root_span.add_event("started")

    # Create child spans
    with tracer.start_span("dependencies", parent=root_span) as span:
        span.add_event("resolving")
        span.add_attribute("packages", 50)
        # Work...

    with tracer.start_span("build", parent=root_span) as span:
        span.add_event("compiling")
        span.add_attribute("target", "web")
        # Work...
        # On exception, status is automatically set to ERROR

    with tracer.start_span("tests", parent=root_span) as span:
        span.add_attribute("suite", "unit")
        span.add_event("tests_started")
        # On success, status is automatically set to OK
```

**Span Information:**
- **Attributes:** Key-value metadata
- **Events:** Named events with timestamps
- **Duration:** Auto-calculated
- **Status:** UNSET, OK, or ERROR (on exception)
- **Parent/Child:** Trace hierarchy

**Export Traces:**
```python
# Get all spans as list
traces = tracer.export_traces()

# Get as JSON
json_str = tracer.export_json()

# Get tree structure
tree = tracer.get_trace_tree()
# {
#   "name": "ci_pipeline",
#   "trace_id": "...",
#   "duration_ms": 1500,
#   "status": "OK",
#   "children": [
#     {"name": "dependencies", "duration_ms": 500, ...},
#     {"name": "build", "duration_ms": 600, ...},
#     {"name": "tests", "duration_ms": 300, ...}
#   ]
# }

# Get summary
print(tracer.get_summary())
# Trace: ci_pipeline
#   Total duration: 1500.00ms
#   Spans: 4
#   Errors: 0
```

**Trace Context Propagation:**
```python
from agent_6_telemetry import TraceContext

ctx = TraceContext()  # Or from existing trace

# Convert to HTTP headers for remote calls
headers = ctx.to_headers()
# {
#   "traceparent": "00-...-...-01",
#   "x-trace-id": "...",
#   "x-span-id": "..."
# }

# Receive and parse headers
ctx_received = TraceContext.from_headers(headers)
```

---

## 🔗 Integration Flow

```
CLI Command
    ↓
Validators (Layer 5)
    ├─ Validate input types
    ├─ Check file paths exist
    ├─ Validate enum values
    └─ Raise ValueError if invalid
    ↓
Security Filters (Layer 5)
    ├─ Sanitize arguments
    ├─ Check for injection attempts
    ├─ Validate subprocess safety
    └─ Secure file operations
    ↓
Rate Limiter (Layer 5)
    ├─ Check request quota
    ├─ Check token budget
    ├─ Wait if needed
    └─ Record usage
    ↓
Logger (Layer 6)
    ├─ Log operation start
    ├─ Structured context
    └─ Log operation result
    ↓
Metrics (Layer 6)
    ├─ Record timing
    ├─ Track counts
    ├─ Set gauges
    └─ Observe histograms
    ↓
Tracer (Layer 6)
    ├─ Create root span
    ├─ Track steps
    ├─ Record events
    └─ Export trace
    ↓
Skills (Layer 4)
    └─ Execute with safety checks and observability
```

---

## ✨ Key Features

### Validation (Layer 5)
✅ All CLI command inputs validated
✅ Type safety via Pydantic
✅ Path validation (exists, workspace-constrained)
✅ URL validation (http/https only)
✅ Enum constraints
✅ Factory pattern for easy extension

### Security (Layer 5)
✅ Injection attack prevention
✅ Workspace boundary enforcement
✅ Subprocess argument validation
✅ Environment variable sanitization
✅ URL scheme validation

### Rate Limiting (Layer 5)
✅ Request rate limiting (per minute)
✅ Token budget tracking (per minute/day)
✅ Cost calculation (estimated USD)
✅ Exponential backoff support
✅ Provider-specific limits (OpenAI, Anthropic, Ollama)

### Logging (Layer 6)
✅ Multiple output formats (console, file, JSON)
✅ Structured logging with context
✅ Rich console formatting (colors)
✅ Automatic exception logging
✅ Contextual log injection

### Metrics (Layer 6)
✅ Counters (event counts)
✅ Gauges (current values)
✅ Histograms (distributions, percentiles)
✅ Automatic timing (Timer context manager)
✅ Summary and export capabilities

### Tracing (Layer 6)
✅ Distributed tracing spans
✅ Parent-child span relationships
✅ Event and attribute recording
✅ Automatic status (OK/ERROR)
✅ Trace tree export
✅ Header propagation (W3C traceparent)

---

## 📊 Code Statistics

| Category | Count |
|----------|-------|
| Validator Classes | 6 |
| Validation Enums | 5 |
| Security Functions | 10+ |
| Rate Limiter Classes | 3 |
| Logger Formatters | 3 |
| Metric Types | 4 |
| Specialized Metrics | 2 |
| Tracer Classes | 4 |
| Total Exports | 60+ |
| Total Lines | 2,300+ |

---

## 🚀 Usage in CLI

### Before Skill Execution

```python
# In handlers.py
from agent_5_guardrails import ValidatorFactory, SecurityFilter
from agent_5_guardrails import LLMRateLimiter
from agent_6_telemetry import get_logger, MetricsCollector, get_tracer

def handle_ci(stages: str, verbose: bool):
    # 1. Validate input
    request = ValidatorFactory.create("ci", stages=stages, verbose=verbose)
    
    # 2. Check security
    filter = SecurityFilter(workspace_root=os.getcwd())
    
    # 3. Check rate limits
    limiter = LLMRateLimiter("openai", "gpt-4")
    if not limiter.can_make_request():
        limiter.wait_for_reset()
    
    # 4. Setup observability
    logger = get_logger("handle_ci")
    metrics = MetricsCollector()
    tracer = get_tracer("agent")
    
    # 5. Execute with tracing
    with tracer.start_span("ci_pipeline") as root_span:
        logger.info("CI pipeline started")
        
        with Timer(metrics, "ci_total_ms"):
            # Execute skills...
            pass
        
        logger.info("CI pipeline completed", extra=metrics.get_report())
```

---

## ✅ Architecture Complete

```
┌─────────────────────────────────────────┐
│  Layer 1: CLI Interface ✅              │
│  ├─ cli.py (Typer commands)             │
│  └─ handlers.py (Command routing)       │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  Layer 5: Guardrails ✅                 │
│  ├─ validators.py (Input validation)    │
│  ├─ security_filters.py (Injection)     │
│  └─ rate_limiter.py (Quota mgmt)        │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  Layer 6: Telemetry ✅                  │
│  ├─ logger.py (Structured logging)      │
│  ├─ metrics.py (Performance tracking)   │
│  └─ tracer.py (Distributed tracing)     │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  Layer 4: Skills (NEXT - 28 skills)     │
│  ├─ Infrastructure (4 skills)           │
│  ├─ Testing (4 skills)                  │
│  ├─ Documents (5 skills)                │
│  ├─ Deployment (4 skills)               │
│  ├─ Portfolio (4 skills)                │
│  ├─ Quality (3 skills)                  │
│  └─ Backend (3 skills)                  │
└─────────────────────────────────────────┘
```

---

## 📋 Next Phase: Layer 4 - Skills

Ready to implement 28 autonomous skills:

1. **Infrastructure Skills** (4)
   - `DependencyResolver` - Resolve pnpm + pip
   - `TypeChecker` - TypeScript strict + mypy
   - `BuildOrchestrator` - Vite + Python builds
   - `QualityGateRunner` - Final validation

2. **Testing Skills** (4)
   - `UnitTestRunner` - Vitest + PyTest
   - `E2ETestRunner` - Playwright
   - `CoverageAnalyzer` - Coverage reports
   - `TestAggregator` - Combine results

3. **Document Skills** (5)
   - `DocxGenerator` - ATS-optimized CV
   - `PdfGenerator` - Visual CV
   - `ExcelGenerator` - Project tracking
   - `SyncVerifier` - Data consistency
   - `CVDataValidator` - Field validation

4. **Deployment Skills** (4)
   - `GitBranchCreator` - Feature branches
   - `GitWorkflowManager` - CI/CD workflows
   - `GitHubPagesDeployer` - Deploy site
   - `ReleaseOrchestrator` - Versioning

5. **Portfolio Skills** (4)
   - `PortfolioUpdater` - Update JSON
   - `SkillsManager` - Manage skills
   - `CertificateManager` - Certificates
   - `ExperienceTracker` - Work history

6. **Quality Skills** (3)
   - `CodeFormatter` - Prettier + Black
   - `LinterChecker` - ESLint + Pylint
   - `PerformanceMonitor` - Benchmarks

7. **Backend Skills** (3)
   - `BackendServer` - Run FastAPI
   - `BackendTestRunner` - Backend tests
   - `ApiValidator` - Schema validation

---

**Status:** ✅ Layers 1, 5, 6 Complete | 📋 Ready for Layer 4 Skills

**Time Invested:** ~8 hours on infrastructure
**Expected Time for Skills:** 20-25 hours
**Total Project Timeline:** 30-35 hours

¿Comenzamos con Layer 4: Skills? 🚀
