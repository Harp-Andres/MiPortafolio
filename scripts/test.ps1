# Testing utilities for MiPortafolio monorepo
# Usage: .\scripts\test.ps1 -Command <command> [-Package <package>]

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('unit', 'e2e', 'all', 'coverage', 'watch')]
    [string]$Command,
    
    [Parameter(Mandatory=$false)]
    [string]$Package = 'apps/web'
)

$ErrorActionPreference = 'Stop'

Write-Host "🧪 Running tests: $Command for $Package" -ForegroundColor Cyan

switch ($Command) {
    'unit' {
        Write-Host "Running unit tests..." -ForegroundColor Yellow
        pnpm -C $Package test
    }
    'e2e' {
        Write-Host "Running E2E tests..." -ForegroundColor Yellow
        pnpm -C $Package test:e2e
    }
    'all' {
        Write-Host "Running all tests..." -ForegroundColor Yellow
        pnpm -C $Package test:all
    }
    'coverage' {
        Write-Host "Running tests with coverage..." -ForegroundColor Yellow
        pnpm -C $Package test:coverage
    }
    'watch' {
        Write-Host "Running tests in watch mode..." -ForegroundColor Yellow
        pnpm -C $Package test:watch
    }
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Tests passed!" -ForegroundColor Green
} else {
    Write-Host "❌ Tests failed!" -ForegroundColor Red
    exit 1
}
