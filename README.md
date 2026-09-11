# 🚀 Portafolio Profesional & Generador de Hoja de Vida

**Autor:** Andrés Rodríguez Pisa  
**Especialidad:** QA Automation | Software Quality Engineer  
**Versión:** 2.0.0 (Modernizado 2026)

## 📋 Descripción

Portafolio profesional moderno y responsivo construido con **React + TypeScript + Tailwind CSS**. 
Integrado con generador automático de hojas de vida en formato **ATS** y **Visual**.

**Características:**
- ✅ Diseño moderno y profesional
- ✅ 100% responsivo (mobile, tablet, desktop)
- ✅ Navegación con menú hamburguesa
- ✅ Descarga dual de CV (ATS + Visual)
- ✅ Tests E2E automatizados con Playwright
- ✅ Deploy automático en GitHub Pages
- ✅ Hoja de vida centralizada y sincronizada
- ✅ Agente profesional para automatización

## 🏗️ Estructura del Proyecto

```
MiPortafolio/
├── src/                    # Código React
│   ├── components/         # Componentes reutilizables
│   ├── hooks/             # Custom React hooks
│   ├── types/             # TypeScript types
│   ├── utils/             # Funciones de utilidad
│   ├── App.tsx            # Componente raíz
│   ├── main.tsx           # Entry point
│   └── index.css          # Estilos globales
├── public/cv/             # CVs generados
├── scripts/hv/            # Scripts de generación
├── tests/                 # Tests E2E Playwright
├── .agent/                # Skills del agente
│   ├── hv-generator.md
│   ├── testing.md
│   └── deployment.md
├── .github/workflows/     # GitHub Actions
├── vite.config.ts         # Configuración Vite
├── tailwind.config.ts     # Configuración Tailwind
├── tsconfig.json          # Configuración TypeScript
└── playwright.config.ts   # Configuración tests
```

## 🚀 Inicio Rápido

### Requisitos
- Node.js 20+
- npm 10+

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/Harp-Andres/MiPortafolio.git
cd MiPortafolio

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

El sitio estará disponible en `http://localhost:5173`

## 📦 Scripts Disponibles

```bash
# Desarrollo
npm run dev              # Inicia servidor Vite
npm run build            # Build para producción
npm run preview          # Vista previa del build

# Hoja de Vida
npm run generate:cv      # Genera CV en ATS y Visual

# Testing
npm run test             # Ejecuta tests E2E
npm run test:ui          # Tests en modo interactivo

# Calidad de código
npm run lint             # Verifica TypeScript
```

## 🎯 Características Principales

### 1. Navegación Responsiva
- Desktop: menú horizontal completo
- Tablet: menú comprimido
- Mobile: menú hamburguesa

### 2. Descarga Dual de CV
- **Formato ATS**: Optimizado para sistemas de rastreo
- **Formato Visual**: Diseño ejecutivo con estilos

### 3. Secciones
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

El proyecto incluye skills especializados para un agente profesional:

- **HV Generator** (`.agent/hv-generator.md`): Generación automática de CVs
- **Testing** (`.agent/testing.md`): Suite E2E completamente automatizada
- **Deployment** (`.agent/deployment.md`): Deploy seguro con validaciones

Ver `.instructions.md` para flujo completo del agente.

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
