# Instrucciones para Usar el Agente de Actualización de CV & Portafolio

## � RESTRICCIÓN CRÍTICA - LEE PRIMERO

### ⚠️ REGLA SUPREMA
**Si actualizas un artefacto (Web, PDF, Word), DEBES actualizar TODOS simultáneamente.**

❌ **PROHIBIDO:**
- Actualizar solo la web sin actualizar PDF y Word
- Cambiar skills en portafolio sin cambiarlos en PDF
- Agregar proyecto sin actualizar Word

✅ **OBLIGATORIO:**
- Web + PDF + Word IDÉNTICOS siempre
- El agente VERIFICARÁ sincronización antes de commit
- Si falta sincronizar → NO hace commit

---

## �🚀 Cómo Invocar el Agente desde VS Code

### **Opción 1: Usar Slash Command (RECOMENDADO)**
En el chat de Copilot, escribe:
```
@cv-update-agent Agrega Python y TypeScript a "Programación & Desarrollo"
```

### **Opción 2: Mencionar en el Chat
En cualquier chat de Copilot:
```
@cv-update-agent
Quiero agregar estas nuevas skills:
- Python
- Docker avanzado
- GraphQL
```

### **Opción 3: Crear una Tarea
1. Abre VS Code Command Palette (Ctrl+Shift+P)
2. Escribe: "Copilot: Agents"
3. Selecciona "CV & Portfolio Update Agent"

---

## 📋 Ejemplos de Órdenes para CV

### Agregar Skills Individuales
```
@cv-update-agent
Agrega "Python" a la categoría "Programación & Desarrollo"
```

### Agregar Múltiples Skills
```
@cv-update-agent
Agrega estos skills a "Programación & Desarrollo":
- Python
- Go
- Rust
```

### Crear Nueva Categoría
```
@cv-update-agent
Crea una nueva categoría "Bases de Datos" con:
- PostgreSQL
- MongoDB
- Redis
- Cassandra
```

### Agregar Certificado
```
@cv-update-agent
Agrega un nuevo certificado a "DevOps & Cloud":
- Título: "Kubernetes Advanced - Linux Academy"
- Horas: 35
- Archivo: /certificados/Kubernetes/advanced.pdf
```

---

## 🎯 Ejemplos de Órdenes para Portafolio

### Agregar Nuevo Proyecto al Portafolio
```
@cv-update-agent
Agrega este nuevo proyecto como "featured":
- Nombre: "TaskFlow - Task Management"
- GitHub: https://github.com/usuario/taskflow
- Descripción: "Modern task management with real-time sync"
- Tecnologías: React, TypeScript, Node.js, MongoDB
- Highlights: 
  * Real-time synchronization
  * Collaborative features
  * Dark mode support
```

### Actualizar Proyecto Existente
```
@cv-update-agent
Actualiza el proyecto "buscar-cruceros":
- Agrega "TypeScript" a las tecnologías
- Cambiar tipo a "featured"
- Actualizar link de deployment: https://buscar-cruceros-demo.com
```

### Cambiar Tipo de Proyecto
```
@cv-update-agent
Cambia el proyecto "literalura" de "secondary" a "featured"
```

### Agregar Sitio en Vivo a Proyecto
```
@cv-update-agent
Agrega el link de deployment al proyecto "automation-test-reports-hub":
https://reports-automation.dev
```

### Mover Proyecto a Nueva Categoría
```
@cv-update-agent
Crea un nuevo proyecto "supporting":
- Nombre: "Config Templates"
- GitHub: https://github.com/usuario/config-templates
- Descripción: "Reutilizable configuration templates"
```

---

## ✅ El Agente Automáticamente:

1. ✅ Actualiza `src/utils/cv-data.ts` (CV) y/o `src/types/projects.ts` (Portafolio)
2. ✅ Verifica TypeScript: `npm run lint`
3. ✅ Compila: `npm run build`
4. ✅ Ejecuta tests: `npm test`
5. ✅ Hace commit: `git commit -m "feat: actualizar CV/Portafolio..."`
6. ✅ Despliega: `git push` → GitHub Pages

---

## 🎯 Ubicación del Agente en VS Code

1. **Command Palette**: Ctrl+Shift+P → "Agents"
2. **Copilot Chat**: Usa `@cv-update-agent`
3. **Archivo de config**: `.vscode/cv-update-agent.md`

---

## 📝 Archivos Principales que Modifica

**CV Data:**
- `src/utils/cv-data.ts` - Skills, certificados, educación

**Portafolio:**
- `src/types/projects.ts` - Todos los proyectos

---

## 🔍 Ver Configuración del Agente

En VS Code:
1. Ctrl+Shift+P
2. "Agent Customizations"
3. Selecciona "CV & Portfolio Update Agent"

---

## 📚 Tipos de Proyectos en Portafolio

- **featured** (3 máximo visible) - Proyectos principales
- **secondary** - Proyectos complementarios  
- **supporting** - Proyectos de apoyo

---

## 💡 Tip: Combinar con Mensajes Normales

Puedes combinar el agente con mensajes normales:

```
Acabo de terminar un proyecto nuevo en React con TypeScript.
Se llama "ChatApp" y está en https://github.com/usuario/chatapp

@cv-update-agent
Agrega este proyecto al portafolio como "featured"
e incluye Node.js y Socket.io en las tecnologías
```

El agente entenderá el contexto y hará los cambios.

---

## 🔗 Proyectos Existentes

**Featured (3):**
- `automation-test-reports-hub` - CI/CD Test Reporting
- `buscar-cruceros` - E2E Automation with Playwright  
- `portfolio-site` - This Portfolio Site (https://harp-andres.github.io/MiPortafolio/)

**Secondary (1):**
- `literalura` - Java Spring Boot Backend

---

## ⚡ Comandos Rápidos

```bash
# Ver estado actual
npm run build

# Ejecutar tests
npm test

# Ver linting errors
npm run lint
```

