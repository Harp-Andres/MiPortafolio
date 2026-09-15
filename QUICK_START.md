# 🚀 QUICK START - Maestro Agent Setup (Portable)

**Setup completo en otra máquina: 2-5 minutos**

## 1️⃣ Clonar Repositorio

```bash
git clone https://github.com/YOUR_USERNAME/MiPortafolio.git
cd MiPortafolio
```

## 2️⃣ Instalar Dependencias (Una sola vez)

### Windows (PowerShell):
```powershell
cd agent
# Instalar uv (gestor de paquetes Python)
pip install uv

# Sincronizar dependencias
uv sync

# Verificar instalación
uv run python --version
```

### macOS/Linux:
```bash
cd agent
pip3 install uv
uv sync
uv run python --version
```

## 3️⃣ Verificar Que Todo Funciona

```bash
# Opción A: Ejecutar CLI
uv run agent --help

# Opción B: Ejecutar MCP Server (se ejecuta indefinidamente)
uv run python -m agent.1_interface.mcp_server_standalone
# Press Ctrl+C para detener
```

**Resultado esperado:**
```
✅ Maestro MCP Server (Standalone)
Python: 3.11.x ...
Root: /path/to/agent
Waiting for connections on stdin...
```

## 4️⃣ Integrar con GitHub Copilot (VS Code)

### Opción A: Configuración Automática
Abre `.vscode/settings.json` y verifica que esté configurado:

```json
{
  "github.copilot.chat.agentAccess": true,
  "modelContext.mcp.maestro": {
    "enabled": true,
    "command": "cd ${workspaceFolder}/agent && uv run python -m agent.1_interface.mcp_server_standalone"
  }
}
```

### Opción B: Configuración Manual en VS Code
1. **Abre Settings** (Ctrl+,)
2. **Busca**: "MCP" o "Model Context Protocol"
3. **Agregar servidor MCP**:
   - Nombre: `maestro`
   - Comando: `cd ${workspaceFolder}/agent && uv run python -m agent.1_interface.mcp_server_standalone`
   - Tipo: `stdio`

## 5️⃣ Usar el Agente Maestro en Copilot

### En el Chat de Copilot:

**Ejecutar Quality Gate:**
```
@maestro skill-quality-gate
```

**Ejecutar Tests:**
```
@maestro skill-unit-test-runner {"path": "tests"}
```

**Ejecutar Build:**
```
@maestro skill-build {"target": "all"}
```

**Ejecutar Full Pipeline:**
```
@maestro maestro {"workflow": "full-pipeline"}
```

## 6️⃣ Skills Disponibles

### 🔧 Programación & Testing
| Skill | Descripción | Comando |
|-------|-------------|---------|
| `skill-code-formatter` | Formato y linting | `@maestro skill-code-formatter` |
| `skill-type-checker` | Verificación de tipos | `@maestro skill-type-checker` |
| `skill-unit-test-runner` | Tests unitarios | `@maestro skill-unit-test-runner` |
| `skill-e2e-test-runner` | Tests E2E | `@maestro skill-e2e-test-runner` |
| `skill-test-coverage` | Cobertura de tests | `@maestro skill-test-coverage` |
| `skill-code-analyzer` | Análisis de código | `@maestro skill-code-analyzer` |

### 🏗️ Infraestructura
| Skill | Descripción |
|-------|-------------|
| `skill-build` | Compilación TypeScript + Python |
| `skill-quality-gate` | Checks completos (format+type+lint+test) |

### 🚀 Deploy & CI/CD
| Skill | Descripción |
|-------|-------------|
| `skill-git-workflow` | Gestión de Git |
| `skill-deploy` | Despliegue a producción |

### 🎼 Maestro Orchestrator
| Skill | Descripción |
|-------|-------------|
| `maestro` | Orquestador maestro (coordina workflows) |

## 7️⃣ Troubleshooting

### ❌ "python-mcp not found"
✅ **Solución**: Ya está corregido. El servidor standalone NO necesita ese paquete.

### ❌ "Command not found: uv"
✅ **Solución**:
```bash
pip install uv
uv --version
```

### ❌ "ModuleNotFoundError: No module named 'agent'"
✅ **Solución**: Asegúrate de estar en la carpeta `agent/` y ejecutar con `uv run`:
```bash
cd agent
uv run python -m 1_interface.mcp_server_standalone
```

### ❌ "MCP Server no aparece en Copilot"
✅ **Solución**:
1. Cierra VS Code completamente
2. Elimina `.vscode/settings.json` (se regenerará)
3. Reabre VS Code
4. Presiona Ctrl+Shift+P → "Reload Window"

## 8️⃣ Workflow Recomendado

### Desarrollo Diario
```bash
# En terminal abierta:
cd agent
uv run agent ci

# En Copilot:
@maestro skill-unit-test-runner {"path": "tests"}
@maestro skill-code-formatter {"files": ["src/app.ts"]}
```

### Pre-Commit
```bash
uv run agent quality
```

### Deploy
```bash
uv run agent deploy
```

## 9️⃣ Actualizar Agente

Para traer cambios del repositorio:
```bash
git pull origin main
cd agent
uv sync  # Actualiza dependencias
```

## 📚 Documentación Adicional

- **Arquitectura**: [docs/MAESTRO_SPECIFICATION.md](docs/MAESTRO_SPECIFICATION.md)
- **Agent System**: [.agent/AGENTS.md](.agent/AGENTS.md)
- **Skills**: [docs/AGENT_SKILLS.md](docs/AGENT_SKILLS.md)
- **Testing**: [docs/E2E_TESTING.md](docs/E2E_TESTING.md)

## ✨ Características

✅ **Portable**: Funciona en Windows, macOS, Linux  
✅ **Rápido**: Setup en 2-5 minutos  
✅ **Sin dependencias externas**: MCP server standalone  
✅ **Integrado con Copilot**: Úsalo directamente en Chat  
✅ **Múltiples skills**: 11 skills para programación, testing, deployment  
✅ **Orkestración**: Maestro coordina workflows complejos  

---

**¿Preguntas?** Revisa `.agent/AGENTS.md` o abre un issue en GitHub.
