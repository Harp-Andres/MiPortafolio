#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Run API E2E tests with Hurl
    
.DESCRIPTION
    This script helps run the API E2E tests using Hurl.
    It handles starting the API server and running the tests.
    
.EXAMPLE
    .\run-e2e-tests.ps1                    # Run all tests
    .\run-e2e-tests.ps1 -TestFile "01-cv-sync.hurl"  # Run specific file
    .\run-e2e-tests.ps1 -GenerateReport    # Generate HTML report
    .\run-e2e-tests.ps1 -Verbose           # Show verbose output
#>

param(
    [string]$TestFile = "*.hurl",
    [switch]$GenerateReport,
    [switch]$Verbose,
    [switch]$VeryVerbose,
    [switch]$Parallel,
    [int]$Workers = 4,
    [string]$BaseUrl = "http://localhost:8000",
    [string]$ReportFile = "report.html"
)

function Write-Header {
    param([string]$Message)
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "  $Message" -ForegroundColor Cyan
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Error2 {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Cyan
}

function Write-Warning2 {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

# Check if Hurl is installed
Write-Header "Checking Hurl installation"
$hurlCommand = Get-Command hurl -ErrorAction SilentlyContinue

if (-not $hurlCommand) {
    Write-Error2 "Hurl is not installed"
    Write-Info "Install Hurl using: cargo install hurl"
    Write-Info "Or download from: https://hurl.dev"
    exit 1
}

Write-Success "Hurl found: $($hurlCommand.Source)"
$hurlVersion = & hurl --version
Write-Info "Version: $hurlVersion"

# Check if API is running
Write-Header "Checking API server"
try {
    $response = Invoke-WebRequest -Uri "$BaseUrl/health" -Method Get -ErrorAction Stop -TimeoutSec 2
    Write-Success "API is running at $BaseUrl"
} catch {
    Write-Warning2 "API is not running at $BaseUrl"
    Write-Info "To start the API, run:"
    Write-Info "  cd apps/api"
    Write-Info "  python run.py"
    Write-Info ""
    Write-Info "Or press Enter to continue anyway..."
    Read-Host "Press Enter to continue"
}

# Get test file path
$testPath = "apps/api/tests/e2e/$TestFile"
$absolutePath = Convert-Path -Path $testPath -ErrorAction SilentlyContinue

if (-not $absolutePath) {
    Write-Error2 "Test file not found: $testPath"
    exit 1
}

# Build Hurl command
Write-Header "Running E2E Tests"
Write-Info "Test path: $testPath"
Write-Info "Base URL: $BaseUrl"

$hurlArgs = @(
    "--test",
    "--variable", "base_url=$BaseUrl"
)

if ($GenerateReport) {
    $hurlArgs += @("--html", $ReportFile)
    Write-Info "Report file: $ReportFile"
}

if ($Verbose) {
    $hurlArgs += "--verbose"
    Write-Info "Running in verbose mode"
}

if ($VeryVerbose) {
    $hurlArgs += "--very-verbose"
    Write-Info "Running in very verbose mode"
}

if ($Parallel) {
    $hurlArgs += @("--parallel", $Workers)
    Write-Info "Running in parallel mode ($Workers workers)"
}

$hurlArgs += $absolutePath

Write-Host ""
Write-Info "Running: hurl $($hurlArgs -join ' ')"
Write-Host ""

# Run tests
& hurl @hurlArgs
$exitCode = $LASTEXITCODE

# Show results
Write-Host ""
if ($exitCode -eq 0) {
    Write-Success "All tests passed! ✨"
} else {
    Write-Error2 "Some tests failed (exit code: $exitCode)"
}

# Show report info
if ($GenerateReport -and (Test-Path $ReportFile)) {
    Write-Success "Report generated: $ReportFile"
    Write-Info "Open report: start $ReportFile"
}

exit $exitCode
