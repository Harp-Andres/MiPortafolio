# 🚀 Hoja de Vida SDET - Andrés Rodríguez Pisa

[![Build Status](https://img.shields.io/github/actions/workflow/status/Harp-Andres/MiPortafolio/deploy.yml?branch=main)](https://github.com/Harp-Andres/MiPortafolio/actions)
[![React](https://img.shields.io/badge/React-18-blue)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-Strict-blue)](https://www.typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-v4-38B2AC)](https://tailwindcss.com)
[![Testing](https://img.shields.io/badge/Testing-Vitest%20%2B%20Playwright-45ba4b)](https://playwright.dev)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**Autor:** Andrés Rodríguez Pisa | **SDET Senior | QA Automation Engineer**  
**Versión:** 2.0.0 (React Router + Portfolio Projects) | **[🌐 Live Demo](https://harp-andres.github.io/MiPortafolio/)**

---

## 📋 Descripción

Hoja de Vida profesional **SDET** construida con **React 18 + TypeScript + Tailwind CSS v4** y **Vite**.  
Plataforma completa para gestionar CV profesional con:
- ✅ Generación dual de CV (ATS-optimized + Visual PDF)
- ✅ Página de Proyectos con GitHub integration
- ✅ Testing exhaustivo (65+ unit tests + E2E tests)
- ✅ CI/CD pipeline con GitHub Actions
- ✅ Responsive design (mobile-first)
| **Playwright E2E** | Tests de funcionalidad y responsivo |
| **GitHub Actions CI/CD** | Lint → Build → Tests → Deploy automatizado |
| **Responsive Design** | Mobile-first, tested en 3+ viewports |
| **GitHub Pages Deploy** | Publicación automática en push a main |
| **Agent Skills Docs** | 10 skills documentadas para automatización futura |

---

## 🏗️ Stack Tecnológico

### Frontend
```
React 18.3.1           # UI framework
TypeScript 5.6         # Type safety (strict mode)
Tailwind CSS v4        # Utility-first styling
Vite 8.3.0            # Build tool (ESM, no CommonJS)
Lucide React          # Icon components
```

### Backend & Generación
```
Node.js 20+           # Runtime
docx                  # DOCX file generation
```

### Testing & QA
```
Playwright            # E2E browser automation
GitHub Actions        # CI/CD pipeline
ESLint / Prettier     # Code quality
```

### Deployment
```
GitHub Pages          # Static hosting
GitHub Actions        # Auto-deploy on push
```

---

## 📁 Estructura del Proyecto

```
MiPortafolio/
├── src/
│   ├── components/          # 8 componentes React reutilizables
│   │   ├── Navigation.tsx   # Nav responsiva + hamburger
│   │   ├── Hero.tsx         # Sección hero
│   │   ├── About.tsx        # About SDET profile
│   │   ├── Skills.tsx       # Grid 3-columns (16 categorías)
│   │   ├── Experience.tsx   # 4 trabajos recientes
│   │   ├── Education.tsx    # 2 formaciones académicas
│   │   ├── Certificates.tsx # 7 categorías + 2 oficiales (LPI, CertMind)
│   │   ├── CVDownloads.tsx  # Modal descarga CV
│   │   └── Footer.tsx       # Footer
│   ├── utils/
│   │   └── cv-data.ts       # 🎯 SINGLE SOURCE OF TRUTH (CV centralizado)
│   ├── types/
│   │   └── index.ts         # TypeScript interfaces
│   ├── App.tsx              # Root component
│   ├── main.tsx             # Entry point
│   └── index.css            # Tailwind @import "tailwindcss"
│
├── scripts/
│   └── hv/
│       └── generate-cv-sdet.mjs    # 📄 DOCX CV generation script
│
├── docs/
│   ├── AGENT_SKILLS.md             # 📚 10 agent skills documentadas
│   └── CV_MANAGEMENT_WORKFLOW.md   # 🔄 E2E workflow (10 pasos)
│
├── Hoja De Vida/
│   └── HV_2026_ATS_AndesRodriguez.docx  # Generated CV
│
├── .github/
│   └── workflows/
│       ├── lint-build.yml          # ESLint + TypeScript + Vite
│       ├── e2e-tests.yml           # Playwright E2E tests
│       └── deploy-pages.yml        # GitHub Pages deploy
│
├── vite.config.mjs                 # ESM-only (NO CommonJS)
├── tailwind.config.js              # Tailwind v4 config
├── tsconfig.json                   # TypeScript strict mode
├── playwright.config.ts            # Playwright test config
└── package.json                    # Dependencies & scripts
```

---

## 🚀 Inicio Rápido

### Requisitos
```bash
Node.js 20+    (LTS recomendado)
npm 10+        (O yarn/pnpm compatible)
Git            (Para versionamiento)
```

### Instalación & Setup

```bash
# 1. Clonar repositorio
git clone https://github.com/Harp-Andres/MiPortafolio.git
cd MiPortafolio

# 2. Instalar dependencias
npm install

# 3. Iniciar servidor desarrollo
npm run dev
# ✅ Abre: http://localhost:5176 (o puerto auto-asignado)
# ✅ HMR activo: cambios en tiempo real

# 4. Abrir en navegador
# Browser auto-opens con Vite
```

---

## 📦 Scripts & Comandos

### Desarrollo Local
```bash
# Servidor dev con HMR (hot reload)
npm run dev

# Build para producción (0 TS errors required)
npm run build

# Preview del build producción
npm run preview
```

### CV & Documentos
```bash
# Generar DOCX CV (ATS optimizado)
node scripts/hv/generate-cv-sdet.mjs
# Output: Hoja De Vida/HV_2026_ATS_AndesRodriguez.docx

# Exportar a PDF (manual en WPS Office por ahora)
# Abrir DOCX → Archivo → Exportar PDF
```

### Testing & QA
```bash
# Ejecutar Playwright E2E tests
npm run test

# Tests en modo UI (debug interactivo)
npm run test:ui

# Ver report de último test
npm run test:report
```

### Linting & Formato
```bash
# Verificar tipos TypeScript
npx tsc --noEmit

# Lint con ESLint
npm run lint

# Formato automático con Prettier
npm run format
```

### Git & Deployment
```bash
# Ver status y cambios
git status
git diff src/

# Commit + push a rama feature
git add .
git commit -m "type: descripción"
git push origin feat/rama

# Deploy (automático en merge a main via GitHub Actions)
# No requiere comando manual
```

---

## 🎯 Workflow SDET (Caso de Uso)

### Actualizar CV → Test → Deploy

```bash
┌─────────────────────────────────────────────────────┐
│ 1. Editar datos CV                                  │
│    → src/utils/cv-data.ts                          │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 2. Validar localmente                               │
│    → npm run dev                                    │
│    → Abrir http://localhost:5176                   │
│    → Verificar cambios visibles                    │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 3. Testing E2E (Playwright)                         │
│    → npm run test                                   │
│    → Validar: layout, responsivo, data binding     │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 4. Build producción                                 │
│    → npm run build                                  │
│    → Verificar: 0 TS errors, dist/ generado       │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 5. Commit + Push                                    │
│    → git add .                                      │
│    → git commit -m "feat: actualizar CV"           │
│    → git push origin feat/rama                     │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 6. GitHub Actions CI/CD                             │
│    → ESLint + TypeScript check                     │
│    → Vite build validation                         │
│    → Playwright E2E tests                          │
│    → Status: ✅ All checks passed                 │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 7. Create PR                                        │
│    → GitHub: Create pull request                   │
│    → Base: main ← Compare: feat/rama               │
│    → Esperar checks verdes                         │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 8. Merge PR                                         │
│    → Merge pull request                            │
│    → GitHub Actions auto-triggers deploy          │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 9. Deploy a GitHub Pages                            │
│    → Vite build                                     │
│    → Push dist/ a GitHub Pages                     │
│    → Esperar 30-60 segundos                        │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 10. Validar en Producción ✅                         │
│     → https://harp-andres.github.io/MiPortafolio/ │
│     → Verificar cambios visibles                   │
│     → Testing final responsivo                     │
└─────────────────────────────────────────────────────┘
```

**Documentación completa:** [CV_MANAGEMENT_WORKFLOW.md](docs/CV_MANAGEMENT_WORKFLOW.md)

---

## 🏛️ Secciones Principales

### 1️⃣ Navigation
- ✅ Desktop: Menú horizontal + botón "Descargar HV"
- ✅ Mobile: Hamburger menu colapsable
- ✅ Responsive: Tailwind breakpoints (sm, md, lg)

### 2️⃣ Hero Section
- Nombre, título SDET, ubicación
- Links: LinkedIn, GitHub, Email
- CTA: Descargar CV en 2 formatos

### 3️⃣ About (Perfil SDET)
- Descripción profesional completa (3+ años expertise)
- Enfoque: QA Automation, Playwright, API Testing, CI/CD
- Palabras clave SDET para ATS

### 4️⃣ Skills (16 Categorías)
- **Grid 3 columnas uniforme** (h-80, auto-rows-fr)
- Categorías:
  - Automatización Web (Playwright, Selenium, Cypress)
  - Testing API (RestAssured, Postman, Thunder Client)
  - Lenguajes (Java, Python, JavaScript, TypeScript)
  - Frameworks QA (Jest, Mocha, Playwright)
  - DevOps & CI/CD (GitHub Actions, Jenkins, Docker)
  - Cloud (AWS, Azure, GCP)
  - Y 10 más...

### 5️⃣ Experience (4 Trabajos Recientes)
- Empresa, título, período, tecnologías
- 3-5 bullet points por experiencia
- Enfoque en automatización y testing

### 6️⃣ Education
- 2 formaciones académicas
- Grado, institución, año

### 7️⃣ Certificates & Trainings
**Subsección 1: Certificaciones Oficiales** (2 items)
  - 🐧 Linux Essentials (LPI)
  - ⚡ Scrum Practitioner (CertMind)

**Subsección 2: Cursos de Formación** (7 categorías, 3-column grid)
  - DevOps & Cloud (Udemy)
  - Calidad & QA (Udemy)
  - Automatización Web & Mobile (Udemy/LinkedIn)
  - Playwright & API Testing (Udemy)
  - Otros Frameworks (Udemy)
  - IA & Productividad (Anthropic, Microsoft)
  - Programación & Desarrollo (Oracle, Cymetria)

### 8️⃣ CV Downloads Modal
- Botón: "🗂️ Hoja de Vida Descargable"
- Modal con 2 opciones:
  - **Formato ATS** (DOCX optimizado para sistemas)
  - **Formato Visual** (Diseño ejecutivo)
- Cierre: Botón X o click fuera del modal

---

## 🧪 Testing & QA

### Estrategia de Testing (SDET Approach)

```typescript
// tests/portfolio.spec.ts (Ejemplo Playwright)

import { test, expect } from '@playwright/test';

test.describe('Portfolio SDET Tests', () => {
  test('Navigation hamburger visible on mobile', async ({ page }) => {
    await page.goto('http://localhost:5176');
    await page.setViewportSize({ width: 375, height: 667 }); // Mobile
    
    const hamburger = page.locator('[data-testid="hamburger-menu"]');
    await expect(hamburger).toBeVisible();
  });

  test('CV data renders correctly', async ({ page }) => {
    await page.goto('http://localhost:5176');
    
    // Validar nombre visible
    const name = page.locator('h1');
    await expect(name).toContainText('ANDRES RODRIGUEZ PISA');
    
    // Validar skills en grid 3 columnas
    const skillsGrid = page.locator('[data-testid="skills-grid"]');
    const columns = await skillsGrid.evaluate(el => 
      getComputedStyle(el).gridTemplateColumns
    );
    expect(columns).toMatch(/auto auto auto/); // 3 columnas
  });

  test('CVDownloads modal abre y cierra', async ({ page }) => {
    await page.goto('http://localhost:5176');
    
    // Abrir modal
    await page.locator('button:has-text("Hoja de Vida Descargable")').click();
    
    const modal = page.locator('[data-testid="cv-downloads-modal"]');
    await expect(modal).toBeVisible();
    
    // Cerrar modal
    await page.locator('button:has-text("×")').click();
    await expect(modal).not.toBeVisible();
  });

  test('Responsive design: Desktop, Tablet, Mobile', async ({ page }) => {
    const viewports = [
      { width: 1920, height: 1080, name: 'Desktop' },
      { width: 768, height: 1024, name: 'Tablet' },
      { width: 375, height: 667, name: 'Mobile' }
    ];

    for (const viewport of viewports) {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.goto('http://localhost:5176');
      
      // Validar que no hay scroll horizontal
      const bodyWidth = await page.evaluate(() => document.body.scrollWidth);
      expect(bodyWidth).toBeLessThanOrEqual(viewport.width);
      
      console.log(`✅ ${viewport.name} responsive OK`);
    }
  });
});
```

### Ejecutar Tests
```bash
# Todos los tests
npm run test

# Modo UI (debug interactivo)
npm run test:ui

# Modo headed (ve el navegador)
npm run test:headed

# Reporte HTML
npm run test:report
```

---

## 🔄 CI/CD Pipeline (GitHub Actions)

Documentado en `.github/workflows/`:

### 1. **lint-build.yml** - Code Quality
```yaml
✅ ESLint check
✅ TypeScript compile (strict mode, 0 errors required)
✅ Vite build (bundle size validation)
```

### 2. **e2e-tests.yml** - Playwright Tests
```yaml
✅ Run on: Node 20
✅ Browsers: Chromium, Firefox, WebKit
✅ Screenshots en caso de fallo
```

### 3. **deploy-pages.yml** - GitHub Pages Deploy
```yaml
✅ Build: npm run build
✅ Deploy: Push dist/ a gh-pages branch
✅ URL: https://harp-andres.github.io/MiPortafolio/
```

**Ver estado:** [Actions](https://github.com/Harp-Andres/MiPortafolio/actions)

---

## 📚 Documentación Agent Skills

**Para automatización futura del CV workflow:**

- **[AGENT_SKILLS.md](docs/AGENT_SKILLS.md)** - 10 skills reutilizables
  1. CV Data Management
  2. React Component Development (Tailwind CSS v4)
  3. CV Document Generation (DOCX)
  4. Local Testing & Validation
  5. Git Workflow & Version Control
  6. GitHub Actions & CI/CD Validation
  7. GitHub Pages Deployment
  8. Browser Automation & Screenshots
  9. Responsive Design Testing
  10. Production Build & Distribution

- **[CV_MANAGEMENT_WORKFLOW.md](docs/CV_MANAGEMENT_WORKFLOW.md)** - E2E workflow de 10 pasos
  - Desde cambios en CV data hasta deploy en producción
  - Comandos exactos, troubleshooting, checklist

---

## 🔧 Patrón Crítico: Grid Uniforme 3-Columnas

**Problema:** Espacio inconsistente entre cards en grids responsivos.

**Solución (Tailwind v4):**
```tsx
// ✅ CORRECTO
<div className="grid grid-cols-3 gap-4 auto-rows-fr">
  {items.map(item => (
    <div className="h-80 border-2 rounded-lg p-6 flex flex-col">
      {content}
    </div>
  ))}
</div>

// Explicación:
// grid-cols-3       → Siempre 3 columnas (SIN breakpoints md:/lg:)
// gap-4             → Espaciado consistente (1rem)
// auto-rows-fr      → Filas distribuyen altura uniformemente
// h-80              → Altura fija (320px)
// flex flex-col     → Contenido fluye verticalmente
// overflow-y-auto   → Scroll si contenido > h-80
```

**Lecciones aprendidas:**
- NO usar `grid-cols-1 md:grid-cols-2 lg:grid-cols-3` (causa desalineación)
- Usar `grid-cols-3` de forma fija
- `auto-rows-fr` es clave para filas uniformes

---

## 🌐 Deployment & Hosting

### GitHub Pages
```
Repositorio: https://github.com/Harp-Andres/MiPortafolio
Live URL:    https://harp-andres.github.io/MiPortafolio/
Branch:      main (automático)
```

### Deploy Process
1. Cambios en local → `git push origin feat/rama`
2. Crea PR → Validación GitHub Actions (lint, build, tests)
3. Merge a `main` → Auto-triggers deploy workflow
4. Espera 30-60 segundos → Cambios visibles en URL pública

### Validar Deploy
```bash
# 1. Abrir navegador
https://harp-andres.github.io/MiPortafolio/

# 2. Limpiar cache si no ve cambios
Ctrl+Shift+R (Windows) o Cmd+Shift+R (Mac)

# 3. Verificar en modo incógnito
Ctrl+Shift+N

# 4. Ver logs de deploy
GitHub → Actions → Deploy Pages workflow
```

---

## 🛠️ Troubleshooting

| Problema | Causa | Solución |
|---|---|---|
| `npm run dev` falla | Dependencias no instaladas | `npm install` |
| Cambios no se ven | HMR no funciona | Refresh página (F5) |
| Build error TS | Typo o tipo incorrecto | Revisar línea, usar `unknown[]` si es necesario |
| Tests fallan | Selector obsoleto | Actualizar `data-testid` en componentes |
| Deploy no se ve | Cache browser | `Ctrl+Shift+R` + esperar 60s |
| GitHub Actions falla | ESLint errors | `npm run lint` local |

**Más detalles:** [CV_MANAGEMENT_WORKFLOW.md#troubleshooting](docs/CV_MANAGEMENT_WORKFLOW.md)

---

## 📖 Referencia Rápida

```bash
# Setup
npm install
npm run dev

# Desarrollo
# Editar src/utils/cv-data.ts
# Cambios se ven en tiempo real
# F12 para DevTools

# Testing
npm run test
npm run test:ui

# Build
npm run build

# Deploy (automático en push a main)
git add .
git commit -m "feat: cambio"
git push origin feat/rama
# Crear PR en GitHub
# Merge cuando checks pasen ✅

# Validar en producción
https://harp-andres.github.io/MiPortafolio/
```

---

## 📄 Licencia

MIT © 2026 Andrés Rodríguez Pisa

---

## 🤝 Contribuir

1. Fork el repositorio
2. Crear rama feature: `git checkout -b feat/mejora`
3. Commit cambios: `git commit -m "feat: descripción"`
4. Push: `git push origin feat/mejora`
5. Crear Pull Request
6. Esperar validación GitHub Actions
7. Merge cuando checks pasen ✅

**Guía completa:** [CV_MANAGEMENT_WORKFLOW.md](docs/CV_MANAGEMENT_WORKFLOW.md)

---

## 🎓 Ejemplo: Agregar Nueva Habilidad

### 1. Editar CV data
```typescript
// src/utils/cv-data.ts
export const CV_DATA = {
  // ...
  skills: [
    {
      category: 'Automatización Web',
      items: [
        'Playwright',
        'Selenium',
        'Cypress',
        'Puppeteer', // ← Nueva
      ]
    },
    // ...
  ]
}
```

### 2. Validar localmente
```bash
npm run dev
# Abrir http://localhost:5176
# Verificar que "Puppeteer" aparece en Skills
```

### 3. Testing
```bash
npm run test:ui
# Validar elemento visible en grid
```

### 4. Commit & Deploy
```bash
git add src/utils/cv-data.ts
git commit -m "feat: agregar Puppeteer a habilidades"
git push origin feat/add-puppeteer
# Crear PR → Merge → Auto-deploy ✅
```

---

## 📞 Contacto & Links

- **Portfolio:** https://harp-andres.github.io/MiPortafolio/
- **LinkedIn:** [Andrés Rodríguez](https://linkedin.com/in/your-profile)
- **GitHub:** [@Harp-Andres](https://github.com/Harp-Andres)
- **Email:** andrés@example.com

---

**Última actualización:** 2026-09-11  
**Versión:** 2.0.0 (Modernización React + TypeScript + Tailwind)  
**Estado:** ✅ Production Ready
- Sobre Mí
- Habilidades Técnicas
- Experiencia Laboral
- Educación
- Certificaciones
- Contacto

### 4. Modernidad Visual
- Animaciones suave
- Gradientes y sombras
- Colores profesionales
- Tipografía moderna

## 🧪 Testing

```bash
# Ejecutar todos los tests
npm run test

# Tests específicos
npm run test -- portfolio.spec.ts

# Interfaz interactiva
npm run test:ui

# Ver reporte detallado
npm run test
npx playwright show-report
```

**Suite de tests valida:**
- ✅ Navegación y menús
- ✅ Descargas de CV
- ✅ Responsividad
- ✅ Ausencia de redes sociales eliminadas
- ✅ Funcionalidad de enlaces

## 📤 Deployment

### GitHub Pages Automático
Cada push a `main` o `develop` dispara:
1. Instalación de dependencias
2. Linting y validaciones
3. Tests E2E
4. Build
5. Deploy automático

**URL:** https://Harp-Andres.github.io/MiPortafolio

### Deploy Manual
```bash
npm run build
npx gh-pages -d dist
```

## 🔧 Stack Técnico

| Categoría | Tecnología |
|-----------|-----------|
| **Frontend** | React 19 + TypeScript |
| **Build** | Vite |
| **Estilos** | Tailwind CSS |
| **Iconos** | Lucide React |
| **Testing** | Playwright |
| **Configuración** | ESLint, TypeScript strict |

## 📊 Generador de Hoja de Vida

### Datos Centralizados
Archivo: `src/utils/cv-data.ts`

Contiene toda la información del CV en un único lugar:
```typescript
export const CV_DATA = {
  name: 'HARDWARE ANDRES RODRIGUEZ PISA',
  title: 'Ingeniero De Calidad De Software',
  email: '...',
  // ... más datos
}
```

### Generar CV
```bash
npm run generate:cv
```

Genera:
- `public/cv/HV_2026_2_ATS_AndesRodriguez.docx`
- `public/cv/HV_2026_2_Visual_AndresRodriguez.docx`

## 🤖 Agente de Automatización

El proyecto usa el sistema **Maestro** (`@maestro`), un agente orquestador multi-nivel definido en [.agent/AGENTS.md](.agent/AGENTS.md), con agentes especializados para:

- **CV/Hoja de Vida**: `portfolio-cv-manager`
- **Testing E2E/Unitario**: `portfolio-test-manager`
- **Deployment**: `portfolio-deployment-manager`
- **CI/CD**: `github-cicd-manager`

Ver [.agent/AGENTS.md](.agent/AGENTS.md) para la jerarquía completa y [docs/MAESTRO_REFERENCE.md](docs/MAESTRO_REFERENCE.md) para la guía de uso.

## 🔒 Consideraciones de Seguridad

✅ Realizadas:
- TypeScript strict mode
- No console.logs en producción
- Validación de descargas
- HTTPS en GitHub Pages
- Headers de seguridad

## 📱 Responsividad

| Dispositivo | Ancho | Menú | Botones |
|-------------|-------|------|---------|
| Mobile | 320-480px | ☰ Hamburguesa | Apilados |
| Tablet | 768-1024px | Horizontal | Lado a lado |
| Desktop | 1920px+ | Completo | Visible |

## 🔄 Flujo de Trabajo Recomendado

```bash
# 1. Crear rama
git checkout -b feat/descripcion

# 2. Hacer cambios
# ... editar archivos ...

# 3. Validar localmente
npm run lint && npm run test && npm run build

# 4. Commit y push
git add .
git commit -m "feat: descripcion de cambios"
git push origin feat/descripcion

# 5. Crear PR en GitHub
# (automático con validaciones)

# 6. Merge cuando todo ✅
# (deploy automático)
```

## 📝 Estándares de Commits

```
feat: agregar nueva funcionalidad
fix: corregir un bug
docs: cambios en documentación
style: cambios de formato/estilos
refactor: refactorizar código
test: agregar/actualizar tests
chore: cambios en build/dependencias
```

## 🤝 Contribuciones

Este proyecto está configurado para:
- Validación automática en PRs
- Tests obligatorios
- Linting automático
- Deploy automático en main

Asegurate de:
1. ✅ Tests pasando
2. ✅ Código sin linting errors
3. ✅ Commit con mensajes claros
4. ✅ PR con descripción

## 📞 Contacto

- **Email:** andresrdrgzps05@gmail.com
- **LinkedIn:** [Andrés Rodríguez Pisa](https://www.linkedin.com/in/AndresRodriguezPisa-CalidadDeSoftware)
- **Ubicación:** Bogotá - Colombia

## 📄 Licencia

ISC

---

**Última actualización:** 2026-09-11  
**Estado:** ✅ Producción  
**Rama principal:** main
