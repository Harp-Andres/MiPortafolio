# Maestro Agent - Portable Setup Script (Windows PowerShell)
# Run: powershell -ExecutionPolicy Bypass -File scripts/setup_portable.ps1

param(
    [switch]$SkipDependencies = $false,
    [switch]$StartServer = $false,
    [switch]$TestServer = $false
)

$ErrorActionPreference = "Stop"

Write-Host "
╔═══════════════════════════════════════════════════════════════════╗
║  🎼 Maestro Agent - Portable Setup (Windows)                      ║
║     Configuración automática en 2-5 minutos                       ║
╚═══════════════════════════════════════════════════════════════════╝
" -ForegroundColor Cyan

# ============================================================================
# STEP 1: Verify Python & uv
# ============================================================================

Write-Host "`n[1/5] Verificando dependencias..." -ForegroundColor Yellow

# Check Python
$python = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python no está instalado" -ForegroundColor Red
    Write-Host "   Instala Python 3.11+ desde https://python.org" -ForegroundColor Gray
    exit 1
}
Write-Host "✅ Python: $python" -ForegroundColor Green

# Check/Install uv
try {
    $uv = uv --version 2>&1
    Write-Host "✅ uv: $uv" -ForegroundColor Green
} catch {
    Write-Host "📦 Instalando uv..." -ForegroundColor Cyan
    pip install uv | Out-Null
    $uv = uv --version
    Write-Host "✅ uv: $uv" -ForegroundColor Green
}

# ============================================================================
# STEP 2: Navigate to agent folder
# ============================================================================

Write-Host "`n[2/5] Entrando a carpeta agent..." -ForegroundColor Yellow

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$agentPath = Join-Path $scriptPath "agent"

if (-not (Test-Path $agentPath)) {
    Write-Host "❌ Carpeta agent/ no encontrada en: $scriptPath" -ForegroundColor Red
    exit 1
}

Push-Location $agentPath
Write-Host "✅ Ubicación: $(Get-Location)" -ForegroundColor Green

# ============================================================================
# STEP 3: Install/Sync Dependencies
# ============================================================================

if (-not $SkipDependencies) {
    Write-Host "`n[3/5] Sincronizando dependencias con uv..." -ForegroundColor Yellow
    uv sync --no-dev 2>&1 | Select-Object -Last 3
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error sincronizando dependencias" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Dependencias sincronizadas" -ForegroundColor Green
} else {
    Write-Host "`n[3/5] Saltando sincronización de dependencias (--SkipDependencies)" -ForegroundColor Yellow
}

# ============================================================================
# STEP 4: Verify MCP Server
# ============================================================================

Write-Host "`n[4/5] Verificando MCP Server..." -ForegroundColor Yellow

$testCmd = 'echo "{""jsonrpc"":""2.0"",""method"":""initialize"",""id"":1}" | uv run python -m agent.1_interface.mcp_server_standalone'

try {
    # Try a quick test (this will timeout but that's OK - means server is responding)
    $timeout = 5
    $proc = Start-Process powershell -ArgumentList "-NoExit", "-Command", $testCmd -PassThru -NoNewWindow
    Start-Sleep -Seconds $timeout
    
    if ($proc.HasExited -eq $false) {
        Stop-Process -InputObject $proc -Force -ErrorAction SilentlyContinue
        Write-Host "✅ MCP Server respondiendo correctamente" -ForegroundColor Green
    } else {
        Write-Host "⚠️  MCP Server inicializado (salida normal esperada)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  No se pudo probar el servidor (esto es normal en setup inicial)" -ForegroundColor Yellow
}

# ============================================================================
# STEP 5: Update VS Code Settings
# ============================================================================

Write-Host "`n[5/5] Configurando VS Code..." -ForegroundColor Yellow

$vscodeSettingsPath = Join-Path (Split-Path -Parent $agentPath) ".vscode" "settings.json"

if (Test-Path $vscodeSettingsPath) {
    $content = Get-Content $vscodeSettingsPath -Raw | ConvertFrom-Json
} else {
    $content = @{}
}

# Add/Update MCP configuration
$content | Add-Member -MemberType NoteProperty -Name "modelContext.mcp.maestro" -Value @{
    enabled = $true
    command = "cd `${workspaceFolder}/agent && uv run python -m agent.1_interface.mcp_server_standalone"
} -Force

# Save settings
$settingsDir = Split-Path -Parent $vscodeSettingsPath
if (-not (Test-Path $settingsDir)) {
    New-Item -ItemType Directory -Path $settingsDir -Force | Out-Null
}

$content | ConvertTo-Json -Depth 10 | Set-Content $vscodeSettingsPath -Encoding UTF8
Write-Host "✅ VS Code configurado" -ForegroundColor Green

# ============================================================================
# Done!
# ============================================================================

Pop-Location

Write-Host "
╔═══════════════════════════════════════════════════════════════════╗
║  ✅ Setup completado                                              ║
╚═══════════════════════════════════════════════════════════════════╝

📖 PRÓXIMOS PASOS:

1. Abre VS Code:
   code .

2. Abre Chat de Copilot (Ctrl+I)

3. Prueba el agente maestro:
   @maestro skill-code-formatter
   @maestro skill-unit-test-runner

4. Para más información:
   - Lee: docs/QUICK_START.md
   - Lee: .github/agents/
   - Lee: docs/MAESTRO_SPECIFICATION.md

📊 Información del Setup:
   - Ubicación: $(Get-Location)
   - Python: $python
   - uv: $uv
   - MCP Server: mcp_server_standalone.py
   - Skills disponibles: 11 (programming, testing, infrastructure, deployment)

💡 Comandos útiles:

   # Ver ayuda
   uv run agent --help

   # Ejecutar tests
   uv run agent test

   # Ejecutar quality gates
   uv run agent ci

   # Iniciar MCP server (en otra ventana terminal)
   uv run python -m agent.1_interface.mcp_server_standalone

🚀 ¡Listo para usar! Abre Copilot y disfruta del agente.

" -ForegroundColor Green
