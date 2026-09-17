# @mportafolio/web

Professional portfolio website built with React 19, TypeScript 7, Vite 8, and Tailwind CSS.

## 🎯 Features

- ⚡ **React 19** with modern hooks and patterns
- 🎨 **Tailwind CSS 4.0** with @import syntax
- 🧪 **Vitest** - 65+ unit tests
- 🎭 **Playwright** - 30+ E2E tests (chromium, firefox, webkit)
- 📱 **Responsive Design** - Mobile, Tablet, Desktop viewports
- 🚀 **GitHub Pages** - Auto-deployed on every commit
- 🤖 **AI-Powered** - Integrated with GitHub Copilot & MCP

## 🚀 Quick Start

### Development
```bash
pnpm install
pnpm dev
```

Server runs at: http://localhost:5173

### Testing

Unit Tests:
```bash
pnpm test              # Run all tests
pnpm test:ui           # Interactive UI
pnpm test:coverage     # Coverage report
```

E2E Tests:
```bash
pnpm test:e2e          # Run all E2E tests
pnpm test:e2e:ui       # Debug UI
```

### Build
```bash
pnpm build
pnpm preview
```

### Linting
```bash
pnpm lint              # Type check
pnpm format            # Format code
```

## 📁 Project Structure

```
src/
├── components/         React components
│   ├── About.tsx
│   ├── Navigation.tsx
│   ├── Hero.tsx
│   ├── Skills.tsx
│   ├── Experience.tsx
│   ├── Education.tsx
│   ├── Certificates.tsx
│   ├── CVDownloads.tsx
│   └── Footer.tsx
├── styles/            CSS and Tailwind styles
├── App.tsx            Main component
└── index.tsx          Entry point
```

## 🔗 Data Source

All data is imported from `@mportafolio/core`:

```typescript
import { CV_DATA, PROJECTS } from '@mportafolio/core';
```

This ensures **100% synchronization** across all platforms:
- Web (React) ✅
- DOCX (python-docx) ✅
- PDF (reportlab) ✅
- Excel (openpyxl) ✅

## 📦 Dependencies

### Core
- react: ^19.3.0
- react-dom: ^19.3.0
- react-router-dom: ^7.18.3

### Styling
- tailwindcss: ^4.0.0
- lucide-react: ^1.45.0

### Development
- typescript: ^7.0.2
- vite: ^8.3.0
- vitest: ^5.0.0
- @playwright/test: ^1.63.0

## 🎨 Styling

Uses Tailwind CSS 4.0 with @import syntax:

```css
@import "tailwindcss";
```

### Color Scheme
- Primary: Blue
- Accent: Cyan
- Background: Gray-900
- Text: Gray-50

## 🧪 Testing

### Unit Tests (Vitest)
- Component rendering tests
- Props validation
- Event handler tests
- Edge cases

### E2E Tests (Playwright)
- User workflows
- Navigation flows
- Form interactions
- Responsive behavior

### Coverage Target
- Minimum: 80% coverage
- Quality gates enforce this

## 🚀 Deployment

Automatically deployed to GitHub Pages on every commit to `main`:

```
https://Harp-Andres.github.io/MiPortafolio
```

Deployment is handled by `.github/workflows/deploy.yml`

## 🔧 Environment Variables

Create `.env.local`:

```env
VITE_BASE_URL=/MiPortafolio/
VITE_API_BASE=https://api.example.com
```

## 📝 Scripts

```json
{
  "dev": "vite",
  "build": "tsc && vite build",
  "preview": "vite preview",
  "test": "vitest",
  "test:ui": "vitest --ui",
  "test:coverage": "vitest --coverage",
  "test:e2e": "playwright test",
  "test:e2e:ui": "playwright test --ui",
  "lint": "tsc --noEmit",
  "format": "prettier --write 'src/**/*.{ts,tsx}'",
  "generate:cv": "node scripts/hv/generate-cv-sdet.mjs"
}
```

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Run tests: `pnpm test`
4. Format code: `pnpm format`
5. Commit with meaningful message
6. Push to trigger deployment

## 📄 License

ISC

---

**Version:** 2.0.0  
**Status:** ✅ Production Ready  
**Tech Stack:** React 19 + TypeScript 7 + Vite 8 + Tailwind CSS 4
