$MaxAttempts = 10  # 10 attempts * 2 min = 20 min max
$Attempt = 0

while ($Attempt -lt $MaxAttempts) {
    $Attempt++
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] Checking workflow status (Attempt $Attempt/$MaxAttempts)..."
    
    $result = gh api repos/Harp-Andres/MiPortafolio/actions/runs/35003461131/jobs | `
        ConvertFrom-Json | `
        Select-Object -ExpandProperty jobs | `
        Where-Object { $_.name -eq "test" } | `
        Select-Object status, conclusion, @{n='elapsed';e={
            if ($_.completed_at) {
                [timespan]::Parse($_.completed_at) - [timespan]::Parse($_.started_at)
            } else {
                [timespan]$([datetime]::UtcNow - [datetime]$_.started_at)
            }
        }}
    
    Write-Host "  Status: $($result.status) | Conclusion: $($result.conclusion) | Elapsed: $($result.elapsed.TotalMinutes.ToString('F1')) min"
    
    if ($result.conclusion -ne $null) {
        Write-Host "✅ Test job COMPLETED with conclusion: $($result.conclusion)"
        break
    }
    
    if ($Attempt -lt $MaxAttempts) {
        Write-Host "  Waiting 2 minutes before next check..."
        Start-Sleep -Seconds 120
    }
}

if ($Attempt -eq $MaxAttempts) {
    Write-Host "❌ Workflow still running after 20 minutes - this may indicate a hang"
}
