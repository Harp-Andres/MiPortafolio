# Build and validation utilities for MiPortafolio
# Usage: .\scripts\build.ps1 -Command <command> [-Package <package>]

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('lint', 'build', 'type-check', 'validate', 'clean')]
    [string]$Command,
    
    [Parameter(Mandatory=$false)]
    [string]$Package = 'apps/web'
)

$ErrorActionPreference = 'Stop'

function Write-Section {
    param([string]$Title)
    Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "  $Title" -ForegroundColor Cyan
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan
}

switch ($Command) {
    'lint' {
        Write-Section "Linting: $Package"
        pnpm -C $Package lint
    }
    
    'build' {
        Write-Section "Building: $Package"
        pnpm -C $Package build
    }
    
    'type-check' {
        Write-Section "Type Checking: $Package"
        pnpm -C $Package type-check
    }
    
    'validate' {
        Write-Section "Full Validation Pipeline"
        Write-Host "1️⃣  Linting..." -ForegroundColor Yellow
        pnpm -C $Package lint
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Lint failed!" -ForegroundColor Red
            exit 1
        }
        
        Write-Host "2️⃣  Type checking..." -ForegroundColor Yellow
        pnpm -C $Package type-check
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Type check failed!" -ForegroundColor Red
            exit 1
        }
        
        Write-Host "3️⃣  Running tests..." -ForegroundColor Yellow
        pnpm -C $Package test
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Tests failed!" -ForegroundColor Red
            exit 1
        }
        
        Write-Host "4️⃣  Building..." -ForegroundColor Yellow
        pnpm -C $Package build
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Build failed!" -ForegroundColor Red
            exit 1
        }
        
        Write-Section "✅ All validations passed!"
    }
    
    'clean' {
        Write-Section "Cleaning: $Package"
        if (Test-Path "$Package/dist") {
            Remove-Item -Path "$Package/dist" -Recurse -Force
            Write-Host "Removed dist/" -ForegroundColor Green
        }
        if (Test-Path "$Package/.turbo") {
            Remove-Item -Path "$Package/.turbo" -Recurse -Force
            Write-Host "Removed .turbo/" -ForegroundColor Green
        }
        if (Test-Path "$Package/coverage") {
            Remove-Item -Path "$Package/coverage" -Recurse -Force
            Write-Host "Removed coverage/" -ForegroundColor Green
        }
        Write-Host "✅ Clean completed!" -ForegroundColor Green
    }
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Command succeeded!" -ForegroundColor Green
} else {
    Write-Host "`n❌ Command failed!" -ForegroundColor Red
    exit 1
}
