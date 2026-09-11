# Agent Skills - MiPortafolio CV Management

## Skill 1: CV Data Management

### Cuando usar
- Actualizar perfil SDET, habilidades, experiencia o certificaciones
- Agregar nuevos cursos o certificaciones
- Reorganizar categorías de datos

### Archivo centralizado
`src/utils/cv-data.ts` - Single Source of Truth para todo el CV

### Estructura de datos
```typescript
export const CV_DATA = {
  // Información personal
  name, title, email, phone1, phone2, location, linkedin, github,
  birthDate, profile,
  
  // Profesional
  skills: Array<{category, items}>,
  experience: Array<{company, role, period, technologies, bullets}>,
  education: Array<{degree, institution, year}>,
  
  // Certificaciones
  certificatesByCategory: {[category]: [items]},
  officialCertifications: [{title, issuer, color, icon}],
  certificates: [array],
  microsoftStudies: [array],
  
  // Otros
  languages: Array<{lang, level}>,
}
```

### Validaciones
- ✅ Cambios en `CV_DATA` deben reflejarse en componentes
- ✅ Todas las categorías skills deben tener items
- ✅ Certificaciones oficiales: solo LPI y CertMind
- ✅ Cursos organizados en 7 categorías

### Patrón de actualización
```bash
1. Editar src/utils/cv-data.ts
2. npm run dev
3. Validar en http://localhost:5176
4. git commit -m "feat: actualizar CV con ..."
5. git push origin feat/...
```

---

## Skill 2: React Component Development (Tailwind CSS v4)

### Cuando usar
- Crear nuevos componentes
- Actualizar estilos existentes
- Mejorar responsive design

### Stack tecnológico
- React 18 + TypeScript + Tailwind CSS v4
- Build: Vite 8.3.0
- Dev server: `npm run dev`

### Patrón de grid uniforme (CRÍTICO)
```tsx
// ✅ CORRECTO - Tabla perfecta
<div className="grid grid-cols-3 gap-4 auto-rows-fr">
  {items.map(item => (
    <div className="h-80 border-l-4 rounded-lg p-6 flex flex-col">
      {/* contenido */}
    </div>
  ))}
</div>

// ❌ INCORRECTO - Filas desordenadas
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Breakpoints causan desalineación */}
</div>
```

### Tailwind v4 Syntax
```css
/* src/index.css */
@import "tailwindcss";
```
NO usar `@tailwind directives`, v4 usa `@import`

### Componentes disponibles
- Navigation (responsive hamburger)
- Hero, About, Skills, Experience, Education
- Certificates (2 subsecciones), CVDownloads

### Testing visual
```bash
1. npm run dev
2. open_browser_page('http://localhost:5176')
3. screenshot_page()
4. Validar: layout, spacing, colores, responsive
```

---

## Skill 3: CV Document Generation (DOCX)

### Cuando usar
- Generar CV en formato DOCX para ATS
- Actualizar plantilla de documentos
- Exportar a PDF (manual con WPS Office)

### Script de generación
```bash
# Ubicación
scripts/hv/generate-cv-sdet.mjs

# Ejecutar
node scripts/hv/generate-cv-sdet.mjs

# Output
Hoja De Vida/HV_2026_ATS_AndesRodriguez.docx
```

### Librerías usadas
- `docx`: Generar documento DOCX
- `packer`: Convertir a bytes para guardar
- `Document`, `Packer`, `Paragraph`, `TextRun`: API de docx

### Formato ATS
- Texto simple, sin gráficos complejos
- Estructura: Contacto → Perfil → Habilidades → Experiencia → Educación → Certificaciones
- Fuente estándar (Calibri, Arial)
- Sin formatos especiales (colores, emojis, bordes)

### Conversión DOCX → PDF
**Método actual:** Manual
1. Abrir `HV_2026_ATS_AndesRodriguez.docx` en WPS Office
2. Archivo → Exportar a PDF
3. Guardar como `HV_2026_ATS_AndesRodriguez.pdf`

**Automatización futura:** Investigar `docx2pdf`, `libreoffice --headless`, o API externa

---

## Skill 4: Local Testing & Validation

### Cuando usar
- Validar cambios antes de commit
- Testing de layout responsivo
- Verificar integración datos → componentes
- Testing de descarga de CV

### Checklist local
```
✅ Build exitoso: npm run build (0 errores TS)
✅ Dev server: npm run dev activo
✅ Navegación: Links internos funcionan
✅ Responsive: Mobile, tablet, desktop
✅ Data binding: Todos items desde cv-data.ts se ven
✅ Modales: CVDownloads abre/cierra
✅ Grid layout: Skills y Certificates 3 columnas uniformes
✅ Certificaciones: Sección oficial separada de cursos
✅ Descargas: CV ATS y Visual funcionan
```

### Herramientas
```typescript
// Browser automation (Playwright)
await page.goto('http://localhost:5176');
await page.screenshot();
await page.locator('#skills').isVisible();
await page.locator('#certificates').isVisible();

// Scroll a sección específica
await page.evaluate(() => {
  document.querySelector('#skills').scrollIntoView();
});
```

### Validación responsivo
- Desktop (1920x1080)
- Tablet (768x1024)
- Mobile (375x667)

### Validación de datos
Confirmar:
- 16 categorías skills se renderizan
- 7 categorías certificados + 2 oficiales (LPI, CertMind)
- 4 experiencias laborales visibles
- 2 educaciones mostradas
- Emojis y colores en categorías correctos

---

## Skill 5: Git Workflow & Version Control

### Cuando usar
- Hacer cambios de código
- Sincronizar con remoto
- Crear y mergear PRs

### Workflow estándar
```bash
# 1. Verificar rama actual
git status

# 2. Crear/cambiar a rama feature
git checkout -b feat/descripcion
# o
git checkout feat/descripcion

# 3. Hacer cambios, validar en local
# ... editar archivos ...
npm run dev
# Verificar en navegador

# 4. Commit pequeños y frecuentes
git add <archivos>
git commit -m "type: descripción"
# Types: feat, fix, chore, refactor, docs

# 5. Push a remoto
git push origin feat/descripcion

# 6. En GitHub: Create PR main ← feat/...
# Descripción: cambios, checklist, screenshots si es UI

# 7. Esperar GitHub Actions (lint, build, tests)
# Status: All checks must pass

# 8. Merge PR (merge commit o squash)
git fetch origin
git checkout main
git pull origin main

# 9. Verificar deploy en GitHub Pages
# https://harp-andres.github.io/MiPortafolio/
```

### Ramas disponibles
- `master`: Legacy (NO usar)
- `main`: Producción (base para deploy)
- `feat/modernizacion-hv-2026`: Desarrollo actual
- `feat/*`: Nuevas features

### Comandos útiles
```bash
git log --oneline -10              # Ver últimos 10 commits
git diff src/                      # Ver cambios pendientes
git status                         # Estado actual
git branch -a                      # Ver todas ramas
git rebase origin/main             # Sincronizar con main
git push origin --force-with-lease # Push forzado (seguro)
```

---

## Skill 6: GitHub Actions & CI/CD Validation

### Cuando usar
- Validar que CI/CD pase antes de merge
- Monitorear build y tests automáticos
- Resolver errores de GitHub Actions

### Pipeline configurado
**Archivos:** `.github/workflows/*.yml`

Típicamente:
- **Lint:** ESLint, Prettier
- **Build:** TypeScript compile, Vite bundle
- **Tests:** Unit tests (si los hay)
- **Deploy:** GitHub Pages (manual o automático)

### Validaciones requeridas
```
✅ ESLint/Prettier: Código sigue estándares
✅ TypeScript: 0 errores, strict mode
✅ Build: Bundled exitosamente
✅ Tests: Todos pasan (si hay)
```

### Troubleshooting
| Error | Solución |
|-------|----------|
| TypeScript errors | Revisar tipos, usar `unknown[]` si es necesario |
| Build fails | `npm run build` local para debuggear |
| Lint errors | Ejecutar formatter: `npm run format` |
| Deploy pending | Esperar 30-60 segundos, es normal |

---

## Skill 7: GitHub Pages Deployment

### Cuando usar
- Publicar cambios a producción
- Validar despliegue exitoso
- URL pública: https://harp-andres.github.io/MiPortafolio/

### Deploy flow
```
1. PR merged a main
2. GitHub Actions auto-triggers deploy workflow
3. Vite build genera dist/
4. Contenido de dist/ se publica a GitHub Pages
5. URL actualiza en ~30-60 segundos
```

### Validación post-deploy
```bash
# Esperar 60 segundos
# Abrir navegador
https://harp-andres.github.io/MiPortafolio/

# Validar:
✅ Layout correcto
✅ Datos actualizados
✅ Responsive funciona
✅ Links funcionan
✅ CVDownloads modal existe
```

### Troubleshooting
- Cambios no se ven: Limpiar cache (Ctrl+Shift+R)
- Deploy no inicia: Revisar GitHub Actions tab
- Build falla: Ver logs en GitHub Actions
- 404 en subpáginas: Revisar `vite.config.mjs` SPA config

---

## Skill 8: Browser Automation & Screenshots (Playwright)

### Cuando usar
- Validar cambios visuales antes de deploy
- Testing responsivo
- Automatizar screenshots para documentación
- Validar que elementos estén visibles

### Patrón básico
```typescript
// Abrir página
const page = await open_browser_page('http://localhost:5176');

// Navegar a sección
await page.evaluate(() => {
  document.querySelector('#skills').scrollIntoView();
});

// Tomar screenshot
await page.screenshot({ path: 'skills-screenshot.png' });

// Validar elemento visible
const isVisible = await page.locator('#certificates').isVisible();

// Cerrar
await page.close();
```

### Estrategia de testing visual
1. Tomar screenshot después de cambios CSS
2. Comparar con anterior
3. Validar: colores, spacing, alineación, responsive

### Helpers útiles
```javascript
// Scroll a elemento
await page.evaluate(() => {
  document.querySelector('#selector').scrollIntoView({ behavior: 'auto' });
});

// Esperar a que cargue
await page.waitForTimeout(500);

// Buscar botones
const buttons = await page.locator('button').all();

// Validar contenido
const text = await page.locator('h2').textContent();
```

---

## Skill 9: Responsive Design Testing

### Cuando usar
- Validar layout en diferentes pantallas
- Testing mobile-first
- Verificar breakpoints Tailwind

### Viewports estándar
```
Desktop:  1920x1080
Tablet:   768x1024
Mobile:   375x667
```

### Validaciones por viewport
```
Mobile:
  ✅ Hamburger menu visible
  ✅ Componentes single-column
  ✅ Texto legible
  ✅ Botones clickeables

Tablet:
  ✅ Layout 2 columnas donde aplique
  ✅ Spacing adecuado
  ✅ Imágenes escaladas

Desktop:
  ✅ 3 columnas (grids)
  ✅ Espaciado máximo
  ✅ Hover effects funcionen
```

### Herramientas
- Chrome DevTools (F12)
- Playwright viewport config
- Tailwind breakpoints: sm, md, lg, xl

---

## Skill 10: Production Build & Distribution

### Cuando usar
- Generar build final para deploy
- Optimizar bundle size
- Validar cero errores

### Build process
```bash
npm run build
# Output: dist/
# Incluye:
# - HTML minificado
# - CSS optimizado
# - JS bundled (Vite)
# - Assets comprimidos

# Validar
npm run preview
# Abre http://localhost:4173 con build producción
```

### Checklist build
```
✅ 0 TypeScript errors
✅ Build completa sin warnings
✅ dist/ folder generado
✅ index.html presente
✅ Assets cargan correctamente
✅ No hay archivos innecesarios
```

### Optimizaciones
- Tree-shaking: ESM modules
- Code splitting: Dynamic imports
- Minificación: Terser
- CSS purging: Tailwind solo estilos usados

---

## Matriz de Decisión: Cuál Skill Usar

| Situación | Skill | Acción |
|-----------|-------|--------|
| Agregar certificación | #1 CV Data | Editar `cv-data.ts` + componentes |
| Cambiar colores/layout | #2 React | Modificar CSS Tailwind |
| Crear nuevo CV formato | #3 Doc Gen | Actualizar script DOCX |
| Validar antes de push | #4 Testing | screenshots + responsive |
| Hacer commit/push | #5 Git | git add/commit/push |
| Revisar CI/CD errors | #6 Actions | GitHub Actions logs |
| Deploy a producción | #7 Pages | Merge a main, esperar 60s |
| Validar visualmente | #8 Browser | Playwright screenshots |
| Testing mobile | #9 Responsive | DevTools viewport |
| Generar producción | #10 Build | `npm run build` |

---

**Última actualización:** 2026-09-11  
**Versión:** 1.0 - MVP Complete
