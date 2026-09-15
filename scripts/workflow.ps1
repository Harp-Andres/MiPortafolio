# GitHub Actions workflow management
# Usage: .\scripts\workflow.ps1 -Command <command> [options]

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('run', 'status', 'logs', 'list', 'verify-protection', 'wait')]
    [string]$Command,
    
    [Parameter(Mandatory=$false)]
    [string]$Branch = 'refactor/complete-monorepo-restructuring',
    
    [Parameter(Mandatory=$false)]
    [int]$RunId,
    
    [Parameter(Mandatory=$false)]
    [switch]$Wait
)

$ErrorActionPreference = 'Stop'
$RepoOwner = 'Harp-Andres'
$RepoName = 'MiPortafolio'

function Check-GHAuth {
    try {
        gh auth status --show-token | Out-Null
    } catch {
        Write-Host "❌ GitHub CLI not authenticated. Run: gh auth login" -ForegroundColor Red
        exit 1
    }
}

Check-GHAuth

switch ($Command) {
    'run' {
        Write-Host "🚀 Triggering workflow on branch: $Branch" -ForegroundColor Cyan
        gh workflow run deploy.yml -r $Branch
        Write-Host "✅ Workflow triggered!" -ForegroundColor Green
        Write-Host "View status: gh workflow view deploy.yml -r $Branch"
    }
    
    'status' {
        Write-Host "📊 Workflow status for branch: $Branch" -ForegroundColor Cyan
        gh workflow view deploy.yml -r $Branch
    }
    
    'logs' {
        if (-not $RunId) {
            Write-Host "❌ RunId required for logs command" -ForegroundColor Red
            Write-Host "Usage: .\scripts\workflow.ps1 -Command logs -RunId <run_id>"
            exit 1
        }
        Write-Host "📋 Fetching logs for run: $RunId" -ForegroundColor Cyan
        gh run view $RunId --log -r $RepoOwner/$RepoName
    }
    
    'list' {
        Write-Host "📋 Recent workflow runs:" -ForegroundColor Cyan
        gh run list --repo $RepoOwner/$RepoName --branch $Branch --limit 10
    }
    
    'verify-protection' {
        Write-Host "🔒 Verifying branch protection for main branch" -ForegroundColor Cyan
        $protection = gh api repos/$RepoOwner/$RepoName/branches/main/protection | ConvertFrom-Json
        
        Write-Host "Branch Protection Settings:" -ForegroundColor Yellow
        Write-Host "  - Require PR Reviews: $($protection.required_pull_request_reviews.required_approving_review_count) review(s)"
        Write-Host "  - Status Checks: $($protection.required_status_checks.strict ? 'Strict' : 'Non-strict')"
        Write-Host "  - Enforce Admins: $($protection.enforce_admins)"
        Write-Host "  - Allow Force Push: $($protection.allow_force_pushes)"
        Write-Host "  - Allow Deletions: $($protection.allow_deletions)"
        
        if ($protection.required_status_checks.checks) {
            Write-Host "  - Required Checks:"
            $protection.required_status_checks.checks | ForEach-Object {
                Write-Host "      • $($_.context)"
            }
        }
        Write-Host "✅ Branch protection verified!" -ForegroundColor Green
    }
    
    'wait' {
        if (-not $RunId) {
            Write-Host "Getting latest run ID..." -ForegroundColor Yellow
            $latest = gh run list --repo $RepoOwner/$RepoName --branch $Branch --limit 1 --json databaseId --jq '.[0].databaseId'
            $RunId = [int]$latest
        }
        
        Write-Host "⏳ Waiting for workflow run $RunId to complete..." -ForegroundColor Cyan
        gh run watch $RunId --repo $RepoOwner/$RepoName
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Workflow completed successfully!" -ForegroundColor Green
        } else {
            Write-Host "❌ Workflow failed!" -ForegroundColor Red
        }
    }
}
