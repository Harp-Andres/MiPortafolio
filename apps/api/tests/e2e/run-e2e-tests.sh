#!/usr/bin/env bash
# Run API E2E tests with Hurl
# 
# Usage:
#   ./run-e2e-tests.sh                           # Run all tests
#   ./run-e2e-tests.sh -f 01-cv-sync.hurl        # Run specific test
#   ./run-e2e-tests.sh --report                  # Generate HTML report
#   ./run-e2e-tests.sh --verbose                 # Show verbose output

set -e

# Colors for output
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
TEST_FILE="*.hurl"
BASE_URL="http://localhost:8000"
REPORT_FILE="report.html"
GENERATE_REPORT=false
VERBOSE=false
VERY_VERBOSE=false
PARALLEL=false
WORKERS=4

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--file)
            TEST_FILE="$2"
            shift 2
            ;;
        -b|--base-url)
            BASE_URL="$2"
            shift 2
            ;;
        -r|--report)
            GENERATE_REPORT=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        --very-verbose)
            VERY_VERBOSE=true
            shift
            ;;
        -p|--parallel)
            PARALLEL=true
            WORKERS="${2:-4}"
            shift 2
            ;;
        -o|--output)
            REPORT_FILE="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -f, --file FILE          Test file to run (default: *.hurl)"
            echo "  -b, --base-url URL       API base URL (default: http://localhost:8000)"
            echo "  -r, --report             Generate HTML report"
            echo "  -o, --output FILE        Report file name (default: report.html)"
            echo "  -v, --verbose            Show verbose output"
            echo "  --very-verbose           Show very verbose output"
            echo "  -p, --parallel [N]       Run in parallel with N workers (default: 4)"
            echo "  -h, --help               Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                              # Run all tests"
            echo "  $0 -f 01-cv-sync.hurl          # Run specific test"
            echo "  $0 --report                     # Generate HTML report"
            echo "  $0 -v --parallel 8              # Verbose, parallel, 8 workers"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Helper functions
print_header() {
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if Hurl is installed
print_header "Checking Hurl installation"
if ! command -v hurl &> /dev/null; then
    print_error "Hurl is not installed"
    print_info "Install Hurl using: brew install hurl (macOS)"
    print_info "Or: cargo install hurl"
    print_info "Or download from: https://hurl.dev"
    exit 1
fi

print_success "Hurl found: $(which hurl)"
print_info "Version: $(hurl --version)"

# Check if API is running
print_header "Checking API server"
if curl -s "$BASE_URL/health" > /dev/null 2>&1; then
    print_success "API is running at $BASE_URL"
else
    print_warning "API is not running at $BASE_URL"
    print_info "To start the API, run:"
    print_info "  cd apps/api"
    print_info "  python run.py"
    print_info ""
    read -p "Press Enter to continue anyway..."
fi

# Check test file exists
TEST_PATH="apps/api/tests/e2e/$TEST_FILE"
if ! ls $TEST_PATH > /dev/null 2>&1; then
    print_error "Test file not found: $TEST_PATH"
    exit 1
fi

# Build Hurl command
print_header "Running E2E Tests"
print_info "Test path: $TEST_PATH"
print_info "Base URL: $BASE_URL"

HURL_ARGS=(
    "--test"
    "--variable" "base_url=$BASE_URL"
)

if [ "$GENERATE_REPORT" = true ]; then
    HURL_ARGS+=("--html" "$REPORT_FILE")
    print_info "Report file: $REPORT_FILE"
fi

if [ "$VERBOSE" = true ]; then
    HURL_ARGS+=("--verbose")
    print_info "Running in verbose mode"
fi

if [ "$VERY_VERBOSE" = true ]; then
    HURL_ARGS+=("--very-verbose")
    print_info "Running in very verbose mode"
fi

if [ "$PARALLEL" = true ]; then
    HURL_ARGS+=("--parallel" "$WORKERS")
    print_info "Running in parallel mode ($WORKERS workers)"
fi

HURL_ARGS+=("$TEST_PATH")

echo ""
print_info "Running: hurl ${HURL_ARGS[@]}"
echo ""

# Run tests
hurl "${HURL_ARGS[@]}"
EXIT_CODE=$?

# Show results
echo ""
if [ $EXIT_CODE -eq 0 ]; then
    print_success "All tests passed! ✨"
else
    print_error "Some tests failed (exit code: $EXIT_CODE)"
fi

# Show report info
if [ "$GENERATE_REPORT" = true ] && [ -f "$REPORT_FILE" ]; then
    print_success "Report generated: $REPORT_FILE"
    print_info "Open report: open $REPORT_FILE"
fi

exit $EXIT_CODE
