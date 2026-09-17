# Guía de Uso del Agente Maestro

Esta guía está ubicada en `agent/docs/` para respetar la arquitectura de 7 capas y mantener la documentación operativa junto al runtime del agente.

## Objetivo

Inicializar, validar y operar el ecosistema agéntico de forma rápida en otro equipo (por ejemplo, VS Code en una máquina nueva), sin implementar manualmente la lógica interna de Phase 2.

## Requisitos mínimos

- Python 3.11+
- uv instalado
- Git instalado
- Variables de entorno configuradas en `.env` a partir de `.env.example`

## Flujo recomendado (máquina nueva)

Desde la carpeta `agent/` ejecuta:

```bash
# 0) Instalar dependencias
uv sync

# 1) Inicializar el ecosistema
uv run agent --setup-init

# 2) Verificar estado
uv run agent --setup-status

# 3) Ver arquitectura completa
uv run agent --setup-show-architecture

# 4) Ejecutar pipeline CI/CD
uv run agent --ci

# 5) Ver todos los skills disponibles
uv run agent --setup-list-skills
```

## Modo Setup Agent para Phase 2 (sin implementación)

Tu estrategia queda soportada con comandos de scaffold y verificación, sin construir aún la lógica de negocio de Orchestrator/Memory/Guardrails/Telemetry/State.

```bash
# Crear plan + scaffold base de archivos faltantes
uv run agent --setup-phase2-agent

# Verificar que el scaffold mínimo de Phase 2 existe
uv run agent --setup-phase2-verify
```

## Qué hace y qué NO hace

### Sí hace

- Inicializa estructura portable
- Valida arquitectura de 7 capas
- Verifica integración MCP para IDEs
- Prepara scaffold de Phase 2
- Verifica que el scaffold esté completo

### No hace

- No implementa lógica de runtime real para Phase 2
- No reemplaza el diseño detallado de cada capa
- No salta quality gates

## Integración con agentes

- Master: `@maestro`
- Setup especializado: `@setup-manager`

Casos típicos:

- `@setup-manager prepara bootstrap para equipo nuevo en VS Code`
- `@setup-manager verifica que el scaffold de phase 2 esté completo`
- `@maestro ejecuta workflow ci`

## Solución de problemas rápida

1. Si falla `uv run agent ...` revisa `agent/pyproject.toml` y vuelve a ejecutar `uv sync`.
2. Si falla MCP, ejecuta `uv run agent --setup-mcp-check`.
3. Si CI falla, ejecuta `uv run agent --ci` y corrige primero pruebas/lint.

## Ubicación de referencia

- Esta guía: `agent/docs/GUIA_USO_AGENTE.md`
- Setup agent base: `agent/setup_agent.py`
- CLI bootstrap: `agent/setup_bootstrap_cli.py`
- Agente especializado definido: `.agent/AGENTS.md`
