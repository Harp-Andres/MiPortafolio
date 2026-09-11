---
description: "Generador automático de Hoja de Vida SDET en formatos ATS y PDF, sincronizado con portafolio web"
keywords: ["CV generator", "DOCX", "PDF", "ATS", "SDET", "document generation"]
---

# Skill: Generador de Hoja de Vida SDET

## Descripción
Automatiza la generación de Hoja de Vida en formatos DOCX y PDF desde una fuente única de datos (`src/utils/cv-data.ts`), manteniendo sincronización con el portafolio web React y la carpeta local HV-Generativa.

## Ubicaciones Críticas

### Fuente Única de Datos
- **Archivo**: `src/utils/cv-data.ts`
- **Estructura**: Objeto exportado `CV_DATA` con:
  - Información personal (name, title, email, phone1, phone2, location, linkedin, github, birthDate)
  - Perfil profesional (profile - texto largo de 200+ palabras)
  - Skills (array con 16 categorías, cada una con items como string separados por comas)
  - Experience (array con 4+ experiencias, cada una con company, role, period, technologies, bullets[])
  - Education (array con título, institución, año)
  - Certificates (array de strings con todas las certificaciones)
  - MicrosoftStudies (array de strings)
  - Languages (array con lang y level)

### Scripts de Generación
- **DOCX Generator**: `scripts/hv/generate-cv-sdet.mjs`
- **Output**: `Hoja De Vida/HV_2026_ATS_AndesRodriguez.docx`

### Sincronización Web
- **App Principal**: `src/App.tsx`
- **Componentes**:
  - `src/components/Experience.tsx` - Últimas 4 experiencias
  - `src/components/Skills.tsx` - TODAS las 16 categorías
  - `src/components/Certificates.tsx` - TODAS las certificaciones + Microsoft Studies
  - `src/components/Education.tsx` - TODA la educación
  - `src/components/About.tsx` - Información personal

## Flujo de Actualización

### Escenario 1: Usuario agrega nuevas certificaciones
```
1. Usuario dice: "Agregué 3 nuevos certificados de Udemy"
2. Agente actualiza `src/utils/cv-data.ts` → certificates[]
3. Ejecuta: node scripts/hv/generate-cv-sdet.mjs
4. Genera: Hoja De Vida/HV_2026_ATS_AndesRodriguez.docx
5. Commit + Push
6. Portafolio web muestra certificaciones automáticamente (recarga en npm run dev)
```

### Escenario 2: Nuevo trabajo agregado
```
1. Usuario: "Empecé en empresa X como QA Senior desde Febrero"
2. Agente:
   - Actualiza experience[] en cv-data.ts (agregar al inicio)
   - Actualiza skills[] si hay nuevas tecnologías
   - Ejecuta generación DOCX
   - Commit + Push
3. Resultado:
   - DOCX actualizado en Hoja De Vida/
   - Web muestra últimas 4 experiencias (automático)
```

### Escenario 3: Exportar a PDF
```
1. Agente genera DOCX con generate-cv-sdet.mjs
2. Abre manualmente en WPS Office o LibreOffice
3. Archivo → Exportar a PDF
4. Guardar como: Hoja De Vida/HV_2026_ATS_AndesRodriguez.pdf
5. Usuario puede descargar desde web (botones [ATS] [Visual])
```

## Comandos Agente

### Generar DOCX desde datos actuales
```bash
node scripts/hv/generate-cv-sdet.mjs
```
**Salida**: `Hoja De Vida/HV_2026_ATS_AndesRodriguez.docx`

### Verificar que datos están sincronizados
1. Comparar `src/utils/cv-data.ts` con Portafolio web
2. Verificar que `Experience`, `Skills`, `Certificates` muestran contenido correcto
3. Asegurar que últimas 4 experiencias se muestran correctamente

### Crear PR después de actualizar HV
```bash
git add src/utils/cv-data.ts scripts/hv/
git commit -m "feat: actualizar HV con nuevos datos [certificaciones/experiencia]"
git push origin feat/actualizar-hv
# Crear PR en GitHub
```

## Validación Post-Actualización

Después de ejecutar cualquier actualización, el agente DEBE:

1. ✅ Verificar que `scripts/hv/generate-cv-sdet.mjs` se ejecutó sin errores
2. ✅ Confirmar que `Hoja De Vida/HV_2026_ATS_AndesRodriguez.docx` fue creado/actualizado
3. ✅ Revisar que `src/utils/cv-data.ts` tiene estructura válida
4. ✅ Hacer commit de cambios
5. ✅ Crear PR (si aplica)
6. ✅ Informar al usuario dónde puede descargar PDFs

## Restricciones Importantes

- **NO** modificar la estructura de `CV_DATA` sin actualizar también componentes React
- **NO** agregar experiencias antiguas (mantener solo últimas 4 en web)
- **SÍ** incluir TODAS las certificaciones sin límite
- **SÍ** mostrar TODAS las skills (16 categorías)
- **SÍ** mantener sincronización bidireccional: cambios en cv-data.ts → web automático

## Integración Futura

- [ ] Automatizar conversión DOCX → PDF (LibreOffice CLI)
- [ ] Endpoint GET `/api/cv` para descargar PDF dinámicamente
- [ ] Validación de schema JSON para cv-data.ts
- [ ] Versionado de CVs en Git con timestamps


## Estructura de Datos

```typescript
interface CVData {
  name: string
  title: string
  email: string
  phone: string
  location: string
  linkedin: string
  birthDate: string
  about: string
  skills: SkillCategory[]
  experience: Experience[]
  education: Education[]
  certificates: Certificate[]
}
```

## Consideraciones de Agente

**Cuando el usuario o el agente actualice la HV:**
1. ✅ Verificar cambios en `cv-data.ts`
2. ✅ Ejecutar `npm run generate:cv`
3. ✅ Validar que se generaron archivos
4. ✅ Copiar archivos a destino externo
5. ✅ Crear commit con mensaje descriptivo
6. ✅ Reportar éxito/error

**Restricciones:**
- ❌ No modificar estructura de directorios
- ❌ No eliminar datos históricos
- ❌ No usar datos de fuentes no validadas
- ✅ Siempre hacer backup antes de cambios masivos

## Testing
```bash
npm run test
# Verifica que los CV se descarguen correctamente
# Valida formatos ATS y Visual
```

## Links Relacionados
- Testing: `.agent/testing.md`
- Deployment: `.agent/deployment.md`
- CV Data: `src/utils/cv-data.ts`
