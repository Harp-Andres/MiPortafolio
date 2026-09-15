# Pull Request and Branch management
# Usage: .\scripts\pr.ps1 -Command <command> [options]

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('create', 'list', 'checks', 'merge', 'review', 'status')]
    [string]$Command,
    
    [Parameter(Mandatory=$false)]
    [string]$Base = 'main',
    
    [Parameter(Mandatory=$false)]
    [string]$Head = '',
    
    [Parameter(Mandatory=$false)]
    [string]$Title = '',
    
    [Parameter(Mandatory=$false)]
    [string]$Body = '',
    
    [Parameter(Mandatory=$false)]
    [string]$PRNumber
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
    'create' {
        if (-not $Head) {
            $Head = (git rev-parse --abbrev-ref HEAD)
        }
        
        if (-not $Title) {
            Write-Host "❌ Title required for creating PR" -ForegroundColor Red
            Write-Host "Usage: .\scripts\pr.ps1 -Command create -Title 'Your PR title' [-Body 'Description']"
            exit 1
        }
        
        Write-Host "📝 Creating PR from $Head to $Base" -ForegroundColor Cyan
        $bodyArg = if ($Body) { "--body `"$Body`"" } else { '' }
        
        gh pr create --title $Title --base $Base --head $Head $bodyArg
        Write-Host "✅ PR created!" -ForegroundColor Green
    }
    
    'list' {
        Write-Host "📋 Open Pull Requests:" -ForegroundColor Cyan
        gh pr list --base $Base --state open --repo $RepoOwner/$RepoName
    }
    
    'checks' {
        if (-not $PRNumber) {
            Write-Host "❌ PR number required" -ForegroundColor Red
            Write-Host "Usage: .\scripts\pr.ps1 -Command checks -PRNumber <number>"
            exit 1
        }
        
        Write-Host "🔍 Status checks for PR #$PRNumber" -ForegroundColor Cyan
        gh pr checks $PRNumber --repo $RepoOwner/$RepoName
    }
    
    'merge' {
        if (-not $PRNumber) {
            Write-Host "❌ PR number required" -ForegroundColor Red
            Write-Host "Usage: .\scripts\pr.ps1 -Command merge -PRNumber <number>"
            exit 1
        }
        
        Write-Host "⚠️  Merging PR #$PRNumber..." -ForegroundColor Yellow
        
        # Check if all checks passed
        $checks = gh pr checks $PRNumber --repo $RepoOwner/$RepoName --json state,status
        $jsonChecks = $checks | ConvertFrom-Json
        
        $allPassed = $true
        foreach ($check in $jsonChecks) {
            if ($check.state -ne 'SUCCESS') {
                $allPassed = $false
                Write-Host "⚠️  Check failed: $($check.status)" -ForegroundColor Red
            }
        }
        
        if (-not $allPassed) {
            Write-Host "❌ Cannot merge: not all checks passed" -ForegroundColor Red
            exit 1
        }
        
        gh pr merge $PRNumber --repo $RepoOwner/$RepoName --squash
        Write-Host "✅ PR merged successfully!" -ForegroundColor Green
    }
    
    'review' {
        if (-not $PRNumber) {
            Write-Host "❌ PR number required" -ForegroundColor Red
            Write-Host "Usage: .\scripts\pr.ps1 -Command review -PRNumber <number>"
            exit 1
        }
        
        Write-Host "👀 PR #$PRNumber details:" -ForegroundColor Cyan
        gh pr view $PRNumber --repo $RepoOwner/$RepoName
    }
    
    'status' {
        if (-not $PRNumber) {
            Write-Host "❌ PR number required" -ForegroundColor Red
            Write-Host "Usage: .\scripts\pr.ps1 -Command status -PRNumber <number>"
            exit 1
        }
        
        Write-Host "🔍 PR #$PRNumber Status:" -ForegroundColor Cyan
        $pr = gh pr view $PRNumber --repo $RepoOwner/$RepoName --json state,statusCheckRollup,reviews
        $jsonPr = $pr | ConvertFrom-Json
        
        Write-Host "State: $($jsonPr.state)" -ForegroundColor Yellow
        Write-Host "Status Checks:"
        $jsonPr.statusCheckRollup | ForEach-Object {
            $status = if ($_.state -eq 'SUCCESS') { '✅' } else { '❌' }
            Write-Host "  $status $($_.name)"
        }
        
        if ($jsonPr.reviews.Count -gt 0) {
            Write-Host "Reviews:"
            $jsonPr.reviews | ForEach-Object {
                Write-Host "  • $($_.author.login): $($_.state)"
            }
        }
    }
}
