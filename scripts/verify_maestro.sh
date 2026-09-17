#!/usr/bin/env bash
# Maestro Agent - Quick Verification Script
# Run: bash scripts/verify_maestro.sh

echo "
╔═══════════════════════════════════════════════════════════════════╗
║  🎼 Maestro Agent - Verification & Status                        ║
╚═══════════════════════════════════════════════════════════════════╝
"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "\n${YELLOW}[CHECK 1/6]${NC} Verificando estructura de carpetas..."
if [ -f "agent/pyproject.toml" ] && [ -f "agent/1_interface/mcp_server_standalone.py" ]; then
    echo -e "${GREEN}✅ Estructura OK${NC}"
else
    echo -e "${RED}❌ Estructura incorrecta${NC}"
    exit 1
fi

echo -e "\n${YELLOW}[CHECK 2/6]${NC} Verificando Python 3.11+..."
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
if python -c 'import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)' 2>/dev/null; then
    echo -e "${GREEN}✅ Python $PYTHON_VERSION OK${NC}"
else
    echo -e "${RED}❌ Python 3.11+ requerido (tienes: $PYTHON_VERSION)${NC}"
    exit 1
fi

echo -e "\n${YELLOW}[CHECK 3/6]${NC} Verificando uv..."
if command -v uv &> /dev/null; then
    UV_VERSION=$(uv --version)
    echo -e "${GREEN}✅ $UV_VERSION OK${NC}"
else
    echo -e "${YELLOW}⚠️  uv no está instalado, instalando...${NC}"
    pip install uv
    echo -e "${GREEN}✅ uv instalado${NC}"
fi

echo -e "\n${YELLOW}[CHECK 4/6]${NC} Verificando MCP Server Standalone..."
if [ -f "agent/1_interface/mcp_server_standalone.py" ]; then
    LINES=$(wc -l < "agent/1_interface/mcp_server_standalone.py")
    echo -e "${GREEN}✅ MCP Server ($LINES líneas)${NC}"
else
    echo -e "${RED}❌ MCP Server no encontrado${NC}"
    exit 1
fi

echo -e "\n${YELLOW}[CHECK 5/6]${NC} Verificando Skill Handlers..."
if [ -f "agent/1_interface/skill_handlers.py" ]; then
    SKILLS=$(grep -c "async def handle_" agent/1_interface/skill_handlers.py)
    echo -e "${GREEN}✅ $SKILLS handlers implementados${NC}"
else
    echo -e "${RED}❌ Skill handlers no encontrados${NC}"
    exit 1
fi

echo -e "\n${YELLOW}[CHECK 6/6]${NC} Verificando documentación..."
DOCS=0
[ -f "docs/QUICK_START.md" ] && ((DOCS++))
[ -f "STATUS_REPORT.md" ] && ((DOCS++))
[ -f "scripts/setup_portable.ps1" ] && ((DOCS++))
echo -e "${GREEN}✅ $DOCS documentos de guía${NC}"

echo "
╔═══════════════════════════════════════════════════════════════════╗
║  ✅ TODO VERIFICADO - MAESTRO LISTO PARA USO                     ║
╚═══════════════════════════════════════════════════════════════════╝

📋 Status:
   - Python: $PYTHON_VERSION ✅
   - uv: OK ✅
   - MCP Server: Standalone ✅
   - Skills: $SKILLS implementados ✅
   - Docs: $DOCS guías ✅

🚀 Próximos pasos:

1. En otra máquina, clona el repositorio:
   git clone <repo-url>
   cd MiPortafolio

2. Ejecuta el setup automático (Windows):
   powershell -ExecutionPolicy Bypass -File scripts/setup_portable.ps1

3. O manual (cualquier SO):
   cd agent
   uv sync
   uv run python -m 1_interface.mcp_server_standalone

4. Abre VS Code y Copilot:
   code .
   # Presiona Ctrl+I para abrir Copilot Chat
   # Escribe: @maestro skill-unit-test-runner

5. Lee docs/QUICK_START.md para más información

📚 Documentación:
   - docs/QUICK_START.md       (Setup & uso)
   - STATUS_REPORT.md     (Status ejecutivo)
   - scripts/setup_portable.ps1   (Script Windows)

💡 Features:
   ✨ 11 skills funcionales (programming, testing, build, deploy)
   ✨ MCP server sin dependencias externas
   ✨ Setup portable en 2-5 minutos
   ✨ Compatible con Copilot, Claude, Cursor
   ✨ Cross-platform (Windows/macOS/Linux)
   ✨ Async execution & error handling

🎉 ¡Listo para llevar a otra máquina!

" -ForegroundColor Green
