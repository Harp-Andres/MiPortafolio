# @mportafolio/core

Central shared data and types for all MiPortafolio applications.

## 🎯 Purpose

This package contains the **single source of truth** for all CV and portfolio data used across:
- 🌐 Web application (React 19)
- 📄 DOCX generation (python-docx)
- 📑 PDF generation (reportlab)
- 📊 Excel generation (openpyxl)

## 📦 Structure

```
src/
├── data/
│   ├── cv-data.ts       ⭐ Core CV and projects data
│   └── index.ts
├── types/
│   ├── cv.ts            CV data types
│   ├── projects.ts      Project types
│   └── index.ts
└── index.ts             Main export
```

## 🚀 Usage

### Import CV Data
```typescript
import { CV_DATA, PROJECTS } from '@mportafolio/core';

// Use the data
console.log(CV_DATA.profile.name);
console.log(PROJECTS[0].name);
```

### Import Types
```typescript
import type { CV_Data, Project } from '@mportafolio/core/types';

const myCV: CV_Data = { /* ... */ };
const myProject: Project = { /* ... */ };
```

## 📝 Updating Data

When you need to update CV information:

1. ✏️ Edit `src/data/cv-data.ts`
2. ✅ Run tests: `pnpm test`
3. ✅ Verify sync: `pnpm sync:verify`
4. 🚀 Deploy: All applications automatically use the new data

## 🔗 Synchronization

This package is the central hub that ensures:
- Web app reads from cv-data.ts ✅
- Backend generators read from cv-data.ts ✅
- All outputs are guaranteed to be in sync ✅

## 📦 Publishing

Build the package:
```bash
pnpm build
```

The package exports are defined in `package.json`:
- Main export: `./dist/index.js`
- Data export: `./dist/data/index.js`
- Types export: `./dist/types/index.js`

---

**Version:** 2.0.0  
**Status:** ⭐ Single Source of Truth  
**Scope:** Enterprise-grade portfolio system
