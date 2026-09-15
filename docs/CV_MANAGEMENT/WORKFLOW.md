# CV Management Workflow - End-to-End

**Alcance:** Desde cambios en datos CV hasta despliegue productivo

---

## 🎯 Flujo Completo (10 Pasos)

### PASO 1: Identificar Cambio Necesario
```
Tipos de cambios:
├── Datos CV (cv-data.ts)
│   ├── Agregar/actualizar habilidad
│   ├── Nueva experiencia laboral
│   ├── Nuevo certificado
│   └── Actualizar información personal
├── UI/UX (componentes React)
│   ├── Cambiar colores
│   ├── Ajustar spacing
│   ├── Reorganizar layout
│   └── Mejorar responsive
└── Documentos (scripts/hv/)
    ├── Generar nuevo DOCX
    ├── Actualizar plantilla CV
    └── Exportar a PDF
```

**Decisión:** ¿Qué tipo de cambio necesitas?

---

### PASO 2: Crear Rama Feature
```bash
git checkout -b feat/descripcion-cambio

# Ejemplos:
git checkout -b feat/agregar-certificado-aws
git checkout -b feat/fix-responsive-skills
git checkout -b feat/mejorar-cv-docx-template
```

**Por qué:** Aislamiento de cambios, fácil revertir, limpio para PR

---

### PASO 3: Hacer Cambios + Validación Local

#### Si es cambio de DATOS:
```bash
# 1. Editar src/utils/cv-data.ts
nano src/utils/cv-data.ts
# Agregar skill, certificado, experiencia, etc.

# 2. Iniciar dev server
npm run dev
# Dev server en http://localhost:5176 (o puerto asignado)

# 3. Validar en navegador
# Abrir http://localhost:5176
# Verificar que datos se ven correctamente
# Probar responsive (F12 → Device toggle)

# 4. Commit
git add src/utils/cv-data.ts
git commit -m "feat: agregar certificado AWS"
```

#### Si es cambio de UI/UX:
```bash
# 1. Editar componentes React
# src/components/*.tsx
nano src/components/Skills.tsx

# 2. Vite auto-reload (HMR), verificar cambios en tiempo real
# http://localhost:5176 se actualiza automáticamente

# 3. Tomar screenshot
# DevTools (F12) → Captura pantalla
# Verificar: colores, spacing, alineación

# 4. Validar responsive
# DevTools → Device toggle → Mobile/Tablet/Desktop
# Confirmar layout en diferentes tamaños

# 5. Commit
git add src/components/
git commit -m "chore: ajustar spacing en grid skills"
```

#### Si es cambio de DOCUMENTOS:
```bash
# 1. Editar script de generación
nano scripts/hv/generate-cv-sdet.mjs

# 2. Ejecutar script
node scripts/hv/generate-cv-sdet.mjs

# 3. Validar output
# Abrir Hoja De Vida/HV_2026_ATS_AndesRodriguez.docx
# Verificar: estructura, contenido, formato

# 4. Si necesario, exportar a PDF (manual)
# Abrir en WPS Office
# Archivo → Exportar a PDF
# Guardar como: HV_2026_ATS_AndesRodriguez.pdf

# 5. Commit
git add scripts/hv/ Hoja\ De\ Vida/
git commit -m "docs: actualizar template CV DOCX"
```

---

### PASO 4: Build Producción
```bash
npm run build

# Valida:
# ✅ TypeScript compile: 0 errores
# ✅ Vite bundling: exitoso
# ✅ Output: dist/ folder generado
# ✅ Size: dist/ contiene index.html + assets

# Si hay errores:
# 1. Leer error message
# 2. Revisar archivo mencionado
# 3. Corregir typo/tipo
# 4. Intentar npm run build nuevamente
```

---

### PASO 5: Testing Local Completo

#### Checklist Visual
```bash
npm run dev
# Luego en navegador:

✅ Navegación
  - Header visible
  - Links internos funcionan
  - Hamburger menu en mobile

✅ Datos actualizados
  - Todas habilidades visibles
  - Experiencias mostradas correctamente
  - Certificados en categorías correctas

✅ Layout
  - Grid skills: 3 columnas uniforme
  - Grid certificates: 3 columnas uniforme
  - Spacing consistente

✅ Responsive
  - Mobile: single-column, hamburger visible
  - Tablet: 2 columnas donde aplique
  - Desktop: 3 columnas, espaciado máximo

✅ Modales & Interactivos
  - CVDownloads modal: abre/cierra
  - Descargas: ATS y Visual funcionan
  - Hover effects visibles

✅ Colores & Emojis
  - Skills: colores correctos por categoría
  - Certificates: emojis presentes
  - Certificados oficiales: LPI 🐧, CertMind ⚡
```

#### Testing Programático (Opcional)
```bash
# Si tienes Playwright instalado:
npm test
# O ejecutar tests de componentes

# Validaciones automáticas:
# - Elementos presentes (querySe lector)
# - Textos correctos
# - Links no rotos
# - Responsive funcionando
```

---

### PASO 6: Commit y Push
```bash
# Ver cambios pendientes
git status

# Agregar cambios (específicos o todos)
git add .
# o
git add src/utils/cv-data.ts src/components/Skills.tsx

# Commit con mensaje descriptivo
git commit -m "type: descripción clara

Descripción más larga si es necesario
- Cambio 1
- Cambio 2
"

# Tipos de commit recomendados:
# feat:     Nueva feature/funcionalidad
# fix:      Corrección de bug
# docs:     Cambios en documentación
# chore:    Cambios de build/dependencias
# refactor: Reorganizar código sin cambiar funcionalidad

# Push a rama remota
git push origin feat/descripcion-cambio
```

---

### PASO 7: Crear Pull Request en GitHub

#### URL para crear PR
```
https://github.com/Harp-Andres/MiPortafolio/compare/main...feat/descripcion
```

#### Contenido de PR (Descripción Recomendada)
```markdown
## 📝 Descripción
Breve descripción de qué cambia

## ✨ Cambios
- ✅ Cambio 1
- ✅ Cambio 2
- ✅ Cambio 3

## 📸 Screenshots (si hay cambios UI)
[Adjuntar screenshots antes/después]

## ✓ Checklist
- [ ] Build pasa: `npm run build`
- [ ] 0 errores TypeScript
- [ ] Responsive validado (mobile, tablet, desktop)
- [ ] Datos correctos en componentes
- [ ] Links funcionan
- [ ] Documentación actualizada

## 🔗 Referencias
Relacionado con: [issue #X]
```

---

### PASO 8: GitHub Actions Validation

GitHub Actions automáticamente ejecuta:
```
Pipeline:
1. Checkout código
2. Install dependencias (npm install)
3. Lint: ESLint, Prettier
4. Build: tsc, Vite bundle
5. Tests: si existen
6. Resultado: ✅ PASS o ❌ FAIL
```

#### Esperar resultado (típicamente 2-5 minutos)
```
Estado en PR:
- 🟡 Pending: Validando...
- ✅ All checks passed: Listo para merge
- ❌ Some checks failed: Necesita fix
```

#### Si falla:
1. Haz click en "Details" junto al check fallido
2. Lee error message
3. Corrige en local (`npm run build`, etc.)
4. Commit + push
5. GitHub Actions se vuelve a ejecutar automáticamente

---

### PASO 9: Merge Pull Request
```
Esperar hasta:
✅ Todos checks pasan (verde)
✅ Revisor aprueba (si hay política de review)
✅ Ni conflictos de merge

Opción 1: Merge directamente desde GitHub
- Abrir PR
- Botón "Merge pull request"
- Seleccionar "Create a merge commit"
- Confirmar

Opción 2: Merge desde terminal
git checkout main
git pull origin main
git merge feat/descripcion-cambio
git push origin main
```

---

### PASO 10: Validar Deploy en Producción

#### GitHub Pages Deploy (automático)
```
Después de merge a main:
1. GitHub Actions dispara "Deploy" workflow
2. Vite build genera dist/
3. GitHub Pages publica contenido
4. Esperar 30-60 segundos
5. Verificar https://harp-andres.github.io/MiPortafolio/
```

#### Checklist Post-Deploy
```bash
# 1. Abrir navegador
https://harp-andres.github.io/MiPortafolio/

# 2. Validar cambios se ven
✅ Datos actualizados
✅ UI cambios aplicados
✅ No hay broken links

# 3. Si no se ve
- Esperar 60 segundos adicionales
- Limpiar cache: Ctrl+Shift+R (Windows) o Cmd+Shift+R (Mac)
- Abrir en incógnito: Ctrl+Shift+N

# 4. Verificar versión
- Abrir DevTools (F12)
- Console
- Ver si hay errores

# 5. Testing final
- Probar responsive (mobile, tablet)
- Descargar CV (ATS y Visual)
- Verificar links internos
```

---

## 📋 Resumen Comandos Rápidos

```bash
# Crear rama
git checkout -b feat/cambio

# Editar + validar
# (usar editor favorito)
nano src/utils/cv-data.ts
npm run dev  # Ver cambios en tiempo real

# Build producción
npm run build

# Commit + push
git add .
git commit -m "feat: descripción"
git push origin feat/cambio

# Merge (desde terminal)
git checkout main
git pull origin main
git merge feat/cambio
git push origin main

# Ver estado
git status
git log --oneline -5
git branch -a
```

---

## 🎯 Casos de Uso Comunes

### Caso 1: Agregar Nueva Certificación
```bash
git checkout -b feat/add-aws-certification
# Editar: src/utils/cv-data.ts
# Agregar a certificatesByCategory o officialCertifications
npm run dev  # Verificar se ve
git add src/utils/cv-data.ts
git commit -m "feat: agregar certificación AWS Solutions Architect"
git push origin feat/add-aws-certification
# Create PR en GitHub
# Esperar GitHub Actions
# Merge cuando pase
```

### Caso 2: Mejorar Responsive Design
```bash
git checkout -b feat/improve-mobile-layout
# Editar: src/components/Navigation.tsx (o cualquier componente)
# Cambiar clases Tailwind
npm run dev
# Validar en mobile (F12 → Device toggle)
git add src/components/
git commit -m "chore: mejorar layout mobile en Navigation"
git push origin feat/improve-mobile-layout
# Create PR, merge cuando pase
```

### Caso 3: Actualizar Información Personal
```bash
git checkout -b feat/update-profile-2026
# Editar: src/utils/cv-data.ts
# Cambiar: nombre, título, perfil, última experiencia
npm run dev  # Verificar se ve
git add src/utils/cv-data.ts
git commit -m "chore: actualizar perfil 2026"
git push origin feat/update-profile-2026
# PR + Merge
```

### Caso 4: Exportar nuevo DOCX
```bash
git checkout -b feat/update-cv-docx
# Editar: scripts/hv/generate-cv-sdet.mjs
# Ejecutar: node scripts/hv/generate-cv-sdet.mjs
# Validar: Hoja De Vida/HV_2026_ATS_AndesRodriguez.docx
git add scripts/hv/ Hoja\ De\ Vida/
git commit -m "docs: regenerate CV DOCX with updated content"
git push origin feat/update-cv-docx
# PR + Merge
```

---

## ⚠️ Troubleshooting Común

| Problema | Causa | Solución |
|----------|-------|----------|
| `npm run build` falla con error TS | Typo o tipo incorrecto | Revisar línea mencionada, agregar tipos si es necesario |
| Dev server no inicia | Puerto ocupado | Esperar, o ejecutar en puerto diferente |
| Git merge conflict | Cambios en mismo archivo | Editar archivo, resolver conflicto, git add/commit |
| GitHub Actions falla | Lint o build error | Ver logs en GitHub Actions, corregir en local, push |
| Deploy no se ve | Cache browser | Limpiar cache (Ctrl+Shift+R) u abrir en incógnito |
| Grid desalineado | Breakpoints incorrectos | Usar `grid-cols-3 h-80` (ver patrón en Skills.md) |

---

## 🎓 Mejor Práctica: Branch Management

```bash
# Siempre trabaja en rama feature
git checkout -b feat/cambio  # ← Trabajar aquí

# NO trabajar directamente en main
# git checkout main && git commit -m "..." # ❌ Evitar esto

# Mantener main limpio y deployable
# Siempre main debe estar en estado "production ready"

# Después de merge, limpiar rama local
git branch -d feat/cambio-completado
git push origin --delete feat/cambio-completado
```

---

## 📚 Referencias
- GitHub Documentation: https://docs.github.com
- Vite Guide: https://vitejs.dev
- React Docs: https://react.dev
- Tailwind CSS: https://tailwindcss.com
- Git Tutorial: https://git-scm.com/book

---

**Última actualización:** 2026-09-11  
**Fase:** MVP Completo (10 pasos)
