---
description: "Automatización de pruebas E2E para validar funcionalidades del portafolio"
keywords: ["testing", "playwright", "E2E", "automation", "QA"]
---

# Skill: Testing Automatizado

## Descripción
Automatiza pruebas E2E del portafolio usando Playwright para validar:
- ✅ Navegación responsiva
- ✅ Descargas de CV (ATS y Visual)
- ✅ Menú hamburguesa móvil
- ✅ Ausencia de redes sociales eliminadas
- ✅ Funcionalidad de todos los componentes

## Ubicación
- Tests: `tests/portfolio.spec.ts`
- Configuración: `playwright.config.ts`
- Reports: `playwright-report/`

## Suite de Tests

### 1. Navegación
```bash
npm run test -- Portfolio
```
- Validar título de página
- Verificar header con navegación
- Botones de descarga visibles
- Enlaces de navegación funcionales

### 2. Navegación Móvil
```bash
npm run test -- "Mobile Navigation"
```
- Hamburguesa visible en móvil (375px)
- Toggle del menú funciona
- Menú colapsa al seleccionar sección

### 3. Descarga de CV
```bash
npm run test -- "CV Download"
```
- Botón ATS descarga PDF/DOCX
- Botón Visual descarga PDF/DOCX
- Archivos generados con nombre correcto

### 4. Responsividad
```bash
npm run test -- "Responsive Design"
```
- Desktop (1920x1080)
- Tablet (768x1024)
- Mobile (375x667)

### 5. Validaciones de Requisitos
```bash
npm run test -- "No Facebook"
```
- Verifica que NO hay link de Facebook
- Verifica que NO hay link de Instagram
- Verifica que LinkedIn sí existe

## Comandos

### Ejecutar todos los tests
```bash
npm run test
```

### UI interactivo
```bash
npm run test:ui
```
Abre navegador para debug interactivo.

### Tests específicos
```bash
npm run test -- portfolio.spec.ts
npm run test -- --project=chromium
npm run test -- --project=firefox
```

### Generar reporte
```bash
npm run test
npx playwright show-report
```

## Integración con Agente

**El agente debe:**
1. Ejecutar tests antes de cada PR
2. Validar que todos pasen
3. Incluir reporte en comentario de PR
4. Fallar build si tests fallan

**Comando de verificación rápida:**
```bash
npm run test 2>&1 | tee test-results.log
```

## Elementos Críticos a Validar

| Elemento | Mobil | Tablet | Desktop | Estado |
|----------|-------|--------|---------|--------|
| Hamburguesa | ✅ | ✅ | ❌ | Oculto |
| Botones descargas | ✅ | ✅ | ✅ | Siempre |
| LinkedIn | ✅ | ✅ | ✅ | Visible |
| Facebook | ❌ | ❌ | ❌ | Eliminado |
| Instagram | ❌ | ❌ | ❌ | Eliminado |

## Estructura de Test

```typescript
test.describe('Portfolio Navigation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })
  
  test('should have correct functionality', async ({ page }) => {
    // Arrange: preparar
    // Act: ejecutar acción
    // Assert: validar resultado
  })
})
```

## Debugging

### Ver logs
```bash
PWDEBUG=1 npm run test
```

### Video de pruebas
El `playwright.config.ts` graba automáticamente videos en fallos.

### Trace
```bash
npx playwright show-trace trace.zip
```

## Links Relacionados
- HV Generator: `.agent/hv-generator.md`
- Deployment: `.agent/deployment.md`
- Playwright Docs: https://playwright.dev/docs/intro
