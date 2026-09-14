# 🚀 Phase 1: Monorepo Migration Guide

**Status:** Foundation complete, ready for code migration  
**Time to Complete:** ~30 minutes  
**Difficulty:** Medium  

---

## 📋 Overview

This guide walks through moving the current React application from a single-package structure into the `packages/web/` directory of the monorepo, while maintaining all functionality.

## ✅ What's Already Done

The monorepo foundation is complete:

```
✅ pnpm-workspace.yaml configured
✅ root package.json with scripts
✅ tsconfig.base.json with path aliases
✅ @mportafolio/core package created with:
   - CV data (cv-data.ts)
   - Type definitions
   - Export structure
✅ @mportafolio/web package scaffolding created
```

## 🎯 What Needs to Happen Now

Move the current application code into the new structure and update import paths.

---

## 🔄 Step-by-Step Migration

### STEP 1: Run Migration Script (Auto-copy files)

**Time:** 2 minutes

```bash
# From root directory
node scripts/migrate-to-monorepo.js
```

This will:
- Copy `src/` → `packages/web/src/`
- Copy `public/` → `packages/web/public/`
- Copy config files → `packages/web/`

**Expected Output:**
```
🚀 Phase 1: Monorepo Migration

📁 Step 1: Copying src/ directory...
✅ Copied: utils
✅ Copied: components
✅ Copied: types
✅ Copied: App.tsx
✅ Copied: index.tsx
✅ src/ migrated to packages/web/src/

[... more files ...]

✅ PHASE 1 MIGRATION COMPLETE!
```

### STEP 2: Update Import Paths in packages/web/src/

**Time:** 10 minutes

#### 2.1 Find all imports of cv-data

```bash
# From packages/web/ directory
grep -r "from.*cv-data" src/
# or use your IDE's find & replace
```

#### 2.2 Replace all cv-data imports

**OLD:**
```typescript
import { CV_DATA } from '@/utils/cv-data';
import { CV_DATA } from '../utils/cv-data';
```

**NEW:**
```typescript
import { CV_DATA, PROJECTS } from '@mportafolio/core';
```

#### 2.3 Find and update project imports

**OLD:**
```typescript
import { PROJECTS } from '@/types/projects';
import { PROJECTS } from '../utils/cv-data';
```

**NEW:**
```typescript
import { CV_DATA, PROJECTS } from '@mportafolio/core';
```

#### 2.4 Example Files to Check

Files that likely import CV data:

```
packages/web/src/components/About.tsx          ← Check
packages/web/src/components/Skills.tsx         ← Check
packages/web/src/components/Experience.tsx     ← Check
packages/web/src/components/Education.tsx      ← Check
packages/web/src/components/Certificates.tsx   ← Check
packages/web/src/components/CVDownloads.tsx    ← Check
packages/web/src/components/Hero.tsx           ← Check
packages/web/src/App.tsx                       ← Check
```

**Sample replacement for About.tsx:**

```typescript
// BEFORE
import { CV_DATA } from '@/utils/cv-data';

// AFTER
import { CV_DATA } from '@mportafolio/core';
```

### STEP 3: Update TypeScript Configuration in packages/web/

**Time:** 3 minutes

Ensure `packages/web/tsconfig.json` references base config:

**Current (should already be set):**
```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

✅ This is already configured, no changes needed.

### STEP 4: Verify package.json in packages/web/

**Time:** 2 minutes

Check that `@mportafolio/core` is in devDependencies:

```json
{
  "devDependencies": {
    "@mportafolio/core": "workspace:*",
    ...
  }
}
```

✅ This is already configured.

### STEP 5: Install Dependencies (Monorepo-wide)

**Time:** 5 minutes

```bash
# From root directory
pnpm install
```

This will:
1. Install all root dependencies
2. Install all packages/core dependencies
3. Install all packages/web dependencies
4. Create symlinks between packages

**Expected output:**
```
packages synced
 +145 packages in 15s
```

### STEP 6: Test Development Build

**Time:** 5 minutes

```bash
# From root directory
pnpm dev
```

or specifically:

```bash
pnpm -F @mportafolio/web dev
```

**Expected:**
- Dev server starts at http://localhost:5173
- No TypeScript errors
- Application renders correctly

**Verify:**
1. Open http://localhost:5173 in browser
2. Check that profile loads correctly
3. Check that skills section renders
4. Check console for errors

### STEP 7: Run Tests

**Time:** 5 minutes

```bash
# Run all tests
pnpm test

# Run E2E tests
pnpm test:e2e

# Run with UI (helpful for debugging)
pnpm test:ui
```

**Expected:**
```
✓ 65+ unit tests pass
✓ 30+ E2E tests pass
✓ No TypeScript errors
✓ 0 failing tests
```

### STEP 8: Build for Production

**Time:** 3 minutes

```bash
pnpm build
```

**Expected:**
```
packages/web: vite v8.3.0 building for production...
...
✓ 245 modules transformed
dist/index.html          0.45 kB
dist/index.js            125.34 kB (gzipped: 42.1 kB)
...
✓ build completed
```

### STEP 9: Verify Synchronization

**Time:** 2 minutes

```bash
pnpm sync:verify
```

This script will:
1. Extract data from web app
2. Verify structure matches CV_DATA
3. Generate sync report

**Expected:**
```
✅ Web application in sync
✅ Data structure valid
✅ All fields present
✅ No discrepancies detected
```

---

## 📊 Verification Checklist

After completing all steps, verify:

### Code Structure
- [ ] `packages/web/src/` contains all React components
- [ ] `packages/web/public/` contains static assets
- [ ] `packages/core/src/data/cv-data.ts` is the single source
- [ ] Config files copied to `packages/web/`

### Imports
- [ ] All `cv-data` imports use `@mportafolio/core`
- [ ] All `projects` imports use `@mportafolio/core`
- [ ] No broken relative imports remain
- [ ] TypeScript compiler shows 0 errors

### Tests
- [ ] Unit tests pass: `pnpm test` ✅
- [ ] E2E tests pass: `pnpm test:e2e` ✅
- [ ] Coverage maintained: >80%
- [ ] No new TypeScript errors

### Build
- [ ] Development build works: `pnpm dev`
- [ ] Production build works: `pnpm build`
- [ ] Build output correct size
- [ ] No warnings during build

### Functionality
- [ ] Application loads at http://localhost:5173
- [ ] All pages render correctly
- [ ] Navigation works
- [ ] Data displays correctly
- [ ] Responsive design works

---

## 🆘 Troubleshooting

### Issue: "Module not found: @mportafolio/core"

**Solution:**
1. Run `pnpm install` again
2. Clear `node_modules`: `rm -rf node_modules packages/*/node_modules`
3. Reinstall: `pnpm install`

### Issue: TypeScript errors about CV_DATA

**Solution:**
1. Check import path: should be `import { CV_DATA } from '@mportafolio/core'`
2. Verify `tsconfig.base.json` paths are correct
3. Run `tsc --noEmit` to see detailed errors

### Issue: Tests failing with import errors

**Solution:**
1. Update all import paths in test files
2. Clear test cache: `pnpm test -- --clearCache`
3. Run tests again: `pnpm test`

### Issue: Dev server not starting

**Solution:**
1. Check Node.js version: `node --version` (should be >=20)
2. Check PNPM version: `pnpm --version` (should be >=9)
3. Check that `packages/web/vite.config.mjs` exists
4. Run `pnpm install --force`

### Issue: Build fails with type errors

**Solution:**
1. Run type check: `pnpm -F @mportafolio/web lint`
2. Fix any errors reported
3. Clear build cache: `rm -rf packages/web/dist`
4. Build again: `pnpm build`

---

## 📝 Summary of Changes

### Before (Single package)
```
MiPortafolio/
├── src/
├── public/
├── package.json
└── vite.config.mjs
```

### After (Monorepo)
```
MiPortafolio/
├── packages/
│   ├── core/              ← Shared data & types
│   └── web/               ← React app (migrated here)
├── pnpm-workspace.yaml    ← Monorepo config
├── package.json           ← Root scripts
└── tsconfig.base.json     ← Shared TS config
```

### Behavior
- **Same functionality** ✅
- **Better organization** ✅
- **Easier to scale** ✅
- **Central data source** ✅
- **Type safety** ✅

---

## 🎯 Success Criteria

Phase 1 is complete when:

✅ All code migrated to `packages/web/`
✅ All imports updated to use `@mportafolio/core`
✅ `pnpm install` succeeds
✅ `pnpm dev` starts development server
✅ `pnpm test` passes all tests (65+ unit, 30+ E2E)
✅ `pnpm build` creates production build
✅ Application looks and behaves identically to before

---

## 🚀 Next Steps

Once Phase 1 is complete:

1. **Phase 2:** Build Python backend
   - DOCX generator
   - PDF generator
   - Excel generator
   - FastAPI endpoints
   - Estimated: 8-10 hours

2. **Phase 3:** Integration & Testing
   - Sync validator service
   - Integration tests
   - End-to-end workflows
   - Estimated: 4-6 hours

3. **Phase 4:** Deploy & Verify
   - Final testing
   - Deployment
   - Monitoring
   - Estimated: 2-4 hours

---

## 📞 Questions?

Refer to:
- [PHASE_1_STATUS.md](../PHASE_1_STATUS.md) - Current status
- [docs/MONOREPO_IMPLEMENTATION.md](../docs/MONOREPO_IMPLEMENTATION.md) - Full implementation guide
- [QUICK_REFERENCE.md](../QUICK_REFERENCE.md) - Quick lookup
- [.agent/ARCHITECTURE.md](../.agent/ARCHITECTURE.md) - System architecture

---

**Ready to migrate? Start with:** `node scripts/migrate-to-monorepo.js`

**Estimated total time:** ~30 minutes ⏱️
