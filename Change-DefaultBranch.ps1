# GitHub API Script to Change Default Branch
# Script: Change-DefaultBranch.ps1

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "GitHub Repository Configuration" -ForegroundColor Cyan
Write-Host "Cambiar rama default de 'master' a 'main'" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Opción 1: Leer token como variable segura (oculta)
Write-Host "Pega tu GitHub Personal Access Token (no será visible):" -ForegroundColor Yellow
$token = Read-Host -AsSecureString

# Convertir SecureString a texto plano para usar en API
$tokenBstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($token)
$tokenString = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($tokenBstr)

# Repository details
$owner = "Harp-Andres"
$repo = "MiPortafolio"
$newDefaultBranch = "main"

# GitHub API endpoint
$apiUrl = "https://api.github.com/repos/$owner/$repo"

# Prepare headers with Bearer token authentication
$headers = @{
    "Authorization" = "Bearer $tokenString"
    "Accept" = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
}

# Prepare request body
$body = @{
    "default_branch" = $newDefaultBranch
} | ConvertTo-Json

Write-Host "Attempting to change default branch to '$newDefaultBranch'..." -ForegroundColor Cyan
Write-Host "Repository: $owner/$repo" -ForegroundColor Gray

try {
    # Make PATCH request to GitHub API
    $response = Invoke-WebRequest -Uri $apiUrl `
        -Method PATCH `
        -Headers $headers `
        -Body $body `
        -ContentType "application/json"
    
    Write-Host "
✓ Success! Default branch changed to '$newDefaultBranch'" -ForegroundColor Green
    Write-Host "Response Status: $($response.StatusCode)" -ForegroundColor Green
    
    # Show response details
    $responseData = $response.Content | ConvertFrom-Json
    Write-Host "Repository: $($responseData.full_name)" -ForegroundColor Green
    Write-Host "Default Branch: $($responseData.default_branch)" -ForegroundColor Green
}
catch {
    Write-Host "
✗ Error changing default branch" -ForegroundColor Red
    Write-Host "Status Code: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    
    # Try to extract error message from response
    try {
        $errorResponse = $_.ErrorDetails.Message | ConvertFrom-Json
        Write-Host "Error Message: $($errorResponse.message)" -ForegroundColor Red
    }
    catch {
        Write-Host "Error Details: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Clear the token from memory
$tokenString = $null
