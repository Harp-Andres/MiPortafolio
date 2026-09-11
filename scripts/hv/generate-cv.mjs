#!/usr/bin/env node

/**
 * Script de Generación de Hoja de Vida
 * Genera CV en formato ATS y Visual desde datos centralizados
 * Integración con el agente de automatización
 * 
 * Uso: npm run generate:cv
 */

import { Document, Packer, Paragraph, TextRun, PageBreak, Table, TableCell, TableRow, VerticalAlign, BorderStyle, convertInchesToTwip } from 'docx'
import * as fs from 'fs'
import * as path from 'path'

const CV_DATA = {
  name: 'HARDWARE ANDRES RODRIGUEZ PISA',
  title: 'Ingeniero De Calidad De Software | QA Automation',
  email: 'andresrdrgzps05@gmail.com',
  phone: '(+57) 3012119295 - (+57) 320245988',
  location: 'Bogota - Colombia',
  linkedin: 'https://www.linkedin.com/in/AndresRodriguezPisa-CalidadDeSoftware',
  summary: 'Ingeniero de Software con especialización en Automatización de Pruebas y Control de Calidad. Experiencia en diseño e implementación de estrategias de testing, frameworks de automatización y metodologías ágiles.',
  
  experience: [
    {
      position: 'Senior QA Automation Engineer',
      company: 'Current Organization',
      period: '2025 - Presente',
      responsibilities: [
        'Diseño y desarrollo de frameworks de automatización',
        'Implementación de pruebas E2E con Playwright y Cypress',
        'Liderazgo técnico de equipo de QA'
      ]
    },
  ],
  
  skills: {
    'Automatización': ['Selenium', 'Cypress', 'Playwright', 'Appium', 'Serenity BDD'],
    'Lenguajes': ['Java', 'Python', 'JavaScript', 'TypeScript', 'SQL'],
    'Herramientas': ['Postman', 'SoapUI', 'JIRA', 'GitLab', 'Jenkins'],
    'Metodologías': ['Scrum', 'Kanban', 'BDD', 'TDD'],
  },
  
  education: [
    { degree: 'Tecnólogo en Gestión de Redes de Datos', institution: 'SENA', year: '2016' },
  ],
  
  certifications: [
    { name: 'Automation Testing with Selenium', issuer: 'Udemy', year: '2024' },
    { name: 'Advanced Cypress Testing', issuer: 'Coursera', year: '2024' },
  ]
}

// Función para generar CV en formato ATS
function generateATSCV() {
  const sections: Paragraph[] = []

  // Header
  sections.push(
    new Paragraph({
      text: CV_DATA.name,
      bold: true,
      size: 28,
      spacing: { after: 100 },
    })
  )

  sections.push(
    new Paragraph({
      text: `${CV_DATA.title} | ${CV_DATA.location}`,
      spacing: { after: 100 },
    })
  )

  sections.push(
    new Paragraph({
      text: `Email: ${CV_DATA.email} | Phone: ${CV_DATA.phone}`,
      spacing: { after: 200 },
    })
  )

  // Summary
  sections.push(
    new Paragraph({
      text: 'RESUMEN PROFESIONAL',
      bold: true,
      size: 24,
      spacing: { before: 100, after: 100 },
    })
  )

  sections.push(
    new Paragraph({
      text: CV_DATA.summary,
      spacing: { after: 200 },
    })
  )

  // Experience
  sections.push(
    new Paragraph({
      text: 'EXPERIENCIA LABORAL',
      bold: true,
      size: 24,
      spacing: { before: 100, after: 100 },
    })
  )

  CV_DATA.experience.forEach(exp => {
    sections.push(
      new Paragraph({
        text: exp.position,
        bold: true,
        spacing: { after: 50 },
      })
    )
    sections.push(
      new Paragraph({
        text: `${exp.company} | ${exp.period}`,
        spacing: { after: 50 },
      })
    )
    exp.responsibilities.forEach(resp => {
      sections.push(
        new Paragraph({
          text: `• ${resp}`,
          spacing: { after: 50 },
        })
      )
    })
    sections.push(new Paragraph({ text: '', spacing: { after: 100 } }))
  })

  // Skills
  sections.push(
    new Paragraph({
      text: 'HABILIDADES',
      bold: true,
      size: 24,
      spacing: { before: 100, after: 100 },
    })
  )

  Object.entries(CV_DATA.skills).forEach(([category, skills]) => {
    sections.push(
      new Paragraph({
        text: `${category}: ${skills.join(', ')}`,
        spacing: { after: 100 },
      })
    )
  })

  // Education
  sections.push(
    new Paragraph({
      text: 'EDUCACIÓN',
      bold: true,
      size: 24,
      spacing: { before: 100, after: 100 },
    })
  )

  CV_DATA.education.forEach(edu => {
    sections.push(
      new Paragraph({
        text: edu.degree,
        bold: true,
        spacing: { after: 50 },
      })
    )
    sections.push(
      new Paragraph({
        text: `${edu.institution} | ${edu.year}`,
        spacing: { after: 100 },
      })
    )
  })

  // Certifications
  sections.push(
    new Paragraph({
      text: 'CERTIFICACIONES',
      bold: true,
      size: 24,
      spacing: { before: 100, after: 100 },
    })
  )

  CV_DATA.certifications.forEach(cert => {
    sections.push(
      new Paragraph({
        text: `• ${cert.name} - ${cert.issuer} (${cert.year})`,
        spacing: { after: 100 },
      })
    )
  })

  return new Document({ sections })
}

// Función para generar CV en formato Visual
function generateVisualCV() {
  const sections: Paragraph[] = []

  // Header con estilos
  sections.push(
    new Paragraph({
      text: CV_DATA.name,
      bold: true,
      size: 32,
      spacing: { after: 50 },
      border: {
        bottom: {
          color: '0066CC',
          space: 1,
          style: BorderStyle.DOUBLE,
          size: 12,
        },
      },
    })
  )

  sections.push(
    new Paragraph({
      text: CV_DATA.title,
      size: 24,
      color: '0066CC',
      spacing: { after: 100 },
    })
  )

  sections.push(
    new Paragraph({
      text: `📍 ${CV_DATA.location} | ✉️ ${CV_DATA.email} | 📞 ${CV_DATA.phone}`,
      spacing: { after: 200 },
    })
  )

  // Summary con highlight
  sections.push(
    new Paragraph({
      text: 'RESUMEN PROFESIONAL',
      bold: true,
      size: 26,
      color: '0066CC',
      spacing: { before: 100, after: 100 },
      border: {
        bottom: {
          color: 'CCCCCC',
          space: 1,
          style: BorderStyle.SINGLE,
          size: 6,
        },
      },
    })
  )

  sections.push(
    new Paragraph({
      text: CV_DATA.summary,
      spacing: { after: 200 },
    })
  )

  // Rest similar a ATS pero con más estilos
  sections.push(
    new Paragraph({
      text: 'EXPERIENCIA LABORAL',
      bold: true,
      size: 26,
      color: '0066CC',
      spacing: { before: 100, after: 100 },
      border: {
        bottom: {
          color: 'CCCCCC',
          space: 1,
          style: BorderStyle.SINGLE,
          size: 6,
        },
      },
    })
  )

  CV_DATA.experience.forEach(exp => {
    sections.push(
      new Paragraph({
        text: exp.position,
        bold: true,
        size: 22,
        spacing: { after: 50 },
      })
    )
    sections.push(
      new Paragraph({
        text: `${exp.company} | ${exp.period}`,
        italics: true,
        spacing: { after: 50 },
      })
    )
    exp.responsibilities.forEach(resp => {
      sections.push(
        new Paragraph({
          text: `▸ ${resp}`,
          spacing: { after: 50 },
        })
      )
    })
    sections.push(new Paragraph({ text: '', spacing: { after: 100 } }))
  })

  sections.push(
    new Paragraph({
      text: 'HABILIDADES TÉCNICAS',
      bold: true,
      size: 26,
      color: '0066CC',
      spacing: { before: 100, after: 100 },
      border: {
        bottom: {
          color: 'CCCCCC',
          space: 1,
          style: BorderStyle.SINGLE,
          size: 6,
        },
      },
    })
  )

  Object.entries(CV_DATA.skills).forEach(([category, skills]) => {
    sections.push(
      new Paragraph({
        text: category,
        bold: true,
        spacing: { after: 50 },
      })
    )
    sections.push(
      new Paragraph({
        text: skills.join(' • '),
        spacing: { after: 100 },
        color: '333333',
      })
    )
  })

  return new Document({ sections })
}

// Main execution
async function main() {
  try {
    console.log('🚀 Iniciando generación de CV...\n')

    // Crear directorio de salida si no existe
    const outputDir = './public/cv'
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true })
    }

    // Generar ATS
    console.log('📄 Generando CV en formato ATS...')
    const atsDoc = generateATSCV()
    const atsPath = path.join(outputDir, 'HV_2026_2_ATS_AndesRodriguez.docx')
    await Packer.toFile(atsDoc, atsPath)
    console.log(`✅ CV ATS generado: ${atsPath}\n`)

    // Generar Visual
    console.log('🎨 Generando CV en formato Visual...')
    const visualDoc = generateVisualCV()
    const visualPath = path.join(outputDir, 'HV_2026_2_Visual_AndresRodriguez.docx')
    await Packer.toFile(visualDoc, visualPath)
    console.log(`✅ CV Visual generado: ${visualPath}\n`)

    console.log('✨ Generación de CV completada exitosamente!')
  } catch (error) {
    console.error('❌ Error durante la generación:', error)
    process.exit(1)
  }
}

main()
