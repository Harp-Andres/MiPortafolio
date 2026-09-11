---
description: "Automatización de despliegue en GitHub Pages con validaciones"
keywords: ["deployment", "GitHub Pages", "CI/CD", "GitHub Actions"]
---

# Skill: Deployment Automático

## Descripción
Automatiza el despliegue del portafolio en GitHub Pages después de validar:
- ✅ Build exitoso
- ✅ Todos los tests pasando
- ✅ Linter sin errores
- ✅ PR aprobado

## Ubicación
- Workflow: `.github/workflows/deploy.yml`
- Configuración: `vite.config.ts` (base: '/MiPortafolio')
- Rama deploy: `gh-pages` (automática)

## Flujo de Deployment

```
1. Push a feat/* o main
   ↓
2. GitHub Actions dispara workflow
   ↓
3. Validaciones:
   - npm install ✅
   - npm run lint ✅
   - npm run build ✅
   - npm run test ✅
   ↓
4. Build genera /dist
   ↓
5. Deploy a gh-pages branch
   ↓
6. GitHub Pages actualizará automáticamente
   ↓
7. URL: https://Harp-Andres.github.io/MiPortafolio
```

## Configuración

### GitHub Pages Settings
```
Repository → Settings → Pages
→ Source: Deploy from a branch
→ Branch: gh-pages
→ Folder: / (root)
```

### Vite Config
```typescript
export default defineConfig({
  base: '/MiPortafolio/',  // IMPORTANTE para GitHub Pages
  // ...
})
```

## Comandos Locales

### Build para producción
```bash
npm run build
```
Genera carpeta `/dist` optimizada.

### Preview local
```bash
npm run preview
```
Simula servidor de producción.

### Deploy manual (si necesario)
```bash
npm run build
npx gh-pages -d dist
```

## Workflow GitHub Actions

### Trigger
- Push a `feat/*` o `main`
- PR hacia `main`
- Manual (workflow_dispatch)

### Jobs
```yaml
1. install
   - Setup Node 20
   - npm ci (install robusto)

2. lint
   - npm run lint
   - Falla si hay errores TypeScript

3. test
   - npm run test
   - Falla si tests fallan

4. build
   - npm run build
   - Valida que dist/ se genere

5. deploy
   - Solo si todo pasó
   - Deploy a gh-pages
   - Crea/actualiza rama automáticamente
```

## Integración con Agente

**El agente debe:**
1. ✅ Crear rama: `git checkout -b feat/nombre`
2. ✅ Hacer cambios y commits
3. ✅ Ejecutar tests: `npm run test`
4. ✅ Verificar build: `npm run build`
5. ✅ Push a remoto: `git push origin feat/nombre`
6. ✅ Crear PR (manual o con gh CLI)
7. ✅ Esperar validaciones de Actions
8. ✅ Merge solo si todo ✅
9. ✅ Deploy automático después del merge

## Comandos de Agente

### Verificar todo antes de PR
```bash
npm run lint && npm run test && npm run build
```

### Crear rama y preparar PR
```bash
git checkout -b feat/descripcion
# ... cambios ...
git add .
git commit -m "feat: descripción"
git push origin feat/descripcion
# Crear PR desde GitHub
```

### Revisar logs de Actions
```
GitHub → Actions → workflow → job
Ver logs en tiempo real
```

## Troubleshooting

### Build falla
```bash
npm run build
# Ver error detallado
```

### Tests fallan en Actions pero no local
```bash
# Usar la misma versión de Node
node -v  # Should be 20.x
npm ci   # Clean install
```

### Deploy no actualiza GitHub Pages
```
1. Verificar rama gh-pages existe
2. Verificar Settings → Pages → Deploy from branch
3. Esperar 1-2 minutos después del merge
4. Invalidar cache del navegador (Ctrl+Shift+R)
```

## Monitoreo

### Verificar deploy exitoso
1. Ir a: https://Harp-Andres.github.io/MiPortafolio
2. Verificar versión con `?v=timestamp`
3. Abrir DevTools → Network → clear cache

### Ver historial de deployments
```
GitHub → Deployments → github-pages
Ver fecha/hora del último deploy
```

## Mejores Prácticas

✅ **DO:**
- Hacer PR antes de merge
- Esperar validaciones de Actions
- Revisar logs si algo falla
- Mantener ramas actualizadas

❌ **DON'T:**
- Push directamente a main
- Ignorar fallos de tests
- Dejar PRs sin revisar
- Cambiar base de Vite sin razón

## Environment Variables
(Si se necesitan en futuro)
```yaml
# .github/workflows/deploy.yml
env:
  NODE_VERSION: '20'
  NPM_CACHE: 'true'
```

## Links Relacionados
- HV Generator: `.agent/hv-generator.md`
- Testing: `.agent/testing.md`
- GitHub Pages: https://pages.github.com/
- GitHub Actions: https://docs.github.com/en/actions
