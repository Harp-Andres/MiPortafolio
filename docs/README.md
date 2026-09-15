# 📚 Documentación de Producción - MiPortafolio

Bienvenido a la documentación oficial de **MiPortafolio**. Esta carpeta contiene **guías, referencias y especificaciones para usuarios y desarrolladores**.

> 📝 **Nota**: Para documentación de desarrollo (análisis, reportes internos, experimentación), ve a [`.dev-docs/`](../.dev-docs/README.md)

---

## 🚀 Inicio Rápido

1. **[QUICK_START.md](QUICK_START.md)** - Empieza aquí (2-5 minutos)
2. **[SETUP.md](SETUP.md)** - Instalación detallada
3. **[MAESTRO_REFERENCE.md](MAESTRO_REFERENCE.md)** - Referencia del Agente Maestro

---

## 📖 Documentación Completa

### 🎯 Sistema Maestro
- **[MAESTRO_REFERENCE.md](MAESTRO_REFERENCE.md)** - Guía de uso del Agente Maestro
- **[SKILLS.md](SKILLS.md)** - Catálogo completo de skills disponibles

### 🏗️ Arquitectura & Desarrollo
- **[DEVELOPMENT/MONOREPO.md](DEVELOPMENT/MONOREPO.md)** - Estructura del monorepo
- **[DEVELOPMENT/MONOREPO_IMPLEMENTATION.md](DEVELOPMENT/MONOREPO_IMPLEMENTATION.md)** - Detalles de implementación
- **[DEVELOPMENT/E2E_TESTING.md](DEVELOPMENT/E2E_TESTING.md)** - Guía de testing E2E
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Cómo contribuir al proyecto

### 📄 CV Management
- **[CV_MANAGEMENT/WORKFLOW.md](CV_MANAGEMENT/WORKFLOW.md)** - Flujo de trabajo CV
- **[API.md](API.md)** - Referencia de API

---

## 🛠️ Convenciones de Documentación

### Para Agentes Copilot

**✅ SIEMPRE crear docs de producción en `docs/`:**
- Guías de usuario
- Referencias de API
- Tutoriales
- Especificaciones de arquitectura
- Documentación técnica para desarrolladores

**✅ SIEMPRE crear docs de desarrollo en `.dev-docs/`:**
- Análisis de issues
- Reportes de sesiones
- Planes de fases
- Intentos y experimentación
- Documentación interna

**Si tienes duda, pregunta antes de crear un archivo.**

---

## 📁 Estructura

```
docs/
├── README.md                              # Este archivo
├── QUICK_START.md                        # Guía rápida
├── SETUP.md                              # Instalación
├── MAESTRO_REFERENCE.md                  # Referencia Maestro
├── SKILLS.md                             # Catálogo de skills
├── API.md                                # API reference
├── CONTRIBUTING.md                       # Cómo contribuir
├── DEVELOPMENT/                          # Guías de desarrollo
│   ├── README.md
│   ├── MONOREPO.md
│   ├── MONOREPO_IMPLEMENTATION.md
│   └── E2E_TESTING.md
└── CV_MANAGEMENT/                        # CV workflow
    ├── README.md
    └── WORKFLOW.md
```

---

## 🤖 Para Agentes AI

**Importante:** Cuando crees documentación nueva:

1. ¿Es para **usuarios o desarrolladores externos**?
   → `docs/` ✅

2. ¿Es **análisis interno, reporte o experimentación**?
   → `.dev-docs/` ✅

3. **¿No estás seguro?**
   → Pregunta en el prompt antes de crear

---

## 📞 Soporte

- Documentación no encontrada → Revisa [`.dev-docs/`](../.dev-docs/README.md)
- Bug en documentación → Abre un issue
- Sugerencia → Envía PR

---

**Última actualización:** 2026-09-15
