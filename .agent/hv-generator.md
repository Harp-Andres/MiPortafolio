---
description: "Gestor de generación automática de Hoja de Vida en múltiples formatos"
keywords: ["CV generator", "ATS", "document generation", "automation"]
---

# Skill: Generador de Hoja de Vida

## Descripción
Este skill permite al agente generar automáticamente la hoja de vida en múltiples formatos (ATS y Visual) desde datos centralizados, sincronizando con el portafolio web.

## Ubicación
- Script principal: `scripts/hv/generate-cv.mjs`
- Datos centralizados: `src/utils/cv-data.ts`
- Datos externos: `E:\UnidadPrincipal\Escritorio\INGENIERIA DE SISTEMAS UNAD\Andres Trabajo\Hojas de vida\HV-Generativa`

## Flujo de Negocio

```
1. Usuario actualiza datos de HV (localmente con IA)
   ↓
2. Agente detecta cambios en cv-data.ts
   ↓
3. Ejecuta: npm run generate:cv
   ↓
4. Genera DOCX en formato ATS y Visual
   ↓
5. Convierte a PDF (opcional, si pdftk disponible)
   ↓
6. Copia archivos a carpeta de destino
   ↓
7. Crea commit automático
   ↓
8. Prepara para PR y deploy
```

## Comandos Disponibles

### Generar CV
```bash
npm run generate:cv
```
Genera dos archivos DOCX:
- `public/cv/HV_2026_2_ATS_AndesRodriguez.docx` (formato ATS)
- `public/cv/HV_2026_2_Visual_AndresRodriguez.docx` (formato Visual)

### Usar datos del generador
El agente debe:
1. Leer datos de `src/utils/cv-data.ts`
2. Mantener sincronizado con la carpeta HV-Generativa
3. Ejecutar generación automáticamente después de cambios

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
