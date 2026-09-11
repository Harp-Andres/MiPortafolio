#!/usr/bin/env node

/**
 * Script de Generación de Hoja de Vida SDET
 * Genera CV en formato ATS Puro y ATS + Visual desde datos centralizados
 * Integración con el agente de automatización
 * 
 * Uso: node scripts/hv/generate-cv-sdet.mjs
 */

import {
  Document, Packer, Paragraph, TextRun, HeadingLevel,
  AlignmentType, BorderStyle, Table, TableRow, TableCell,
  WidthType, ShadingType, VerticalAlign, convertInchesToTwip,
} from "docx";
import { writeFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const OUTPUT_DIR = join(__dirname, "../../Hoja De Vida");

// ─────────────────────────────────────────────
// DATOS CENTRALIZADOS (Importados de cv-data.ts)
// ─────────────────────────────────────────────
const DATA = {
  name: "ANDRES RODRIGUEZ PISA",
  title: "SDET | Senior QA Automation Engineer | API · Backend · Mobile · Web | Entornos DevOps | IA aplicada a QA",
  location: "Bogotá, Colombia",
  phone1: "(+57) 320 324 5988",
  phone2: "(+57) 301 211 9295",
  email: "andresrdrgzps05@gmail.com",
  linkedin: "linkedin.com/in/andresrodriguezpisa-qa/",
  github: "github.com/Harp-Andres",

  profile: `Ingeniero de Sistemas especializado en aseguramiento de calidad de software, con expertise en arquitectura de frameworks de automatización multiplataforma (Web, API, Mobile) y prácticas DevOps de clase empresarial. Sólida experiencia en diseño e implementación de estrategias QA con patrones avanzados (Screenplay, POM), CI/CD (GitHub Actions, GitLab CI, Jenkins, Azure DevOps), ecosistema Azure (Pipelines YAML, ACR, Blob Storage, Docker) y validación de servicios REST/SOAP con trazabilidad de calidad. Liderazgo técnico demostrado en estandarización de prácticas QA, gobierno de automatización, arquitectura de frameworks mantenibles bajo principios SOLID, y capacitación continua de equipos. Activamente integro herramientas de IA (GitHub Copilot, MCP Playwright) para optimizar diseño de escenarios, refactorización y cobertura de pruebas. Enfoque senior en calidad continua, automatización inteligente, entrega de valor medible y cultura DevOps.`,

  skills: [
    { cat: "Mobile Automation", items: "Appium, Appium Server, Appium Inspector, Android/iOS, ADB" },
    { cat: "Web Automation", items: "Selenium WebDriver, Playwright, Cypress, HTML, CSS" },
    { cat: "API / Backend Testing", items: "REST Assured, Karate, Postman, SoapUI, Swagger, validación de contratos, pruebas de integración" },
    { cat: "Performance", items: "JMeter, Gatling (básico)" },
    { cat: "BDD / Frameworks", items: "Cucumber, Reqnroll (.NET), Serenity BDD, JUnit, TestNG, Katalon Studio" },
    { cat: "Arquitectura / Patrones", items: "Screenplay, Page Object Model (POM), POO, DTO, Entities, IA & Productividad" },
    { cat: "CI/CD & DevOps", items: "GitHub Actions, GitLab CI/CD, Jenkins, Azure DevOps (YAML, Release, Repos, Boards), Docker, Git, SonarQube" },
    { cat: "Cloud & Plataformas", items: "Azure, Azure Blob Storage, Azure Container Registry (ACR), BrowserStack, AWS Device Farm, Sauce Labs" },
    { cat: "Lenguajes", items: "Java, JavaScript, TypeScript, C#, SQL" },
    { cat: "Build Tools", items: "Gradle, Maven, Node.js, dotenv" },
    { cat: "Reporting", items: "Allure Report, Cucumber HTML, GitHub Pages Reports Hub" },
    { cat: "Bases de Datos", items: "SQL Server, MySQL, Oracle, PostgreSQL, MongoDB" },
    { cat: "Gestión / Colaboración", items: "Jira, Kanban, Azure Boards, liderazgo técnico, capacitación" },
    { cat: "IA & Productividad", items: "GitHub Copilot, MCP Playwright, MCP AppMod, prompting avanzado" },
    { cat: "Scripting / Consola", items: "PowerShell, Bash, CMD" },
    { cat: "Virtualización", items: "VirtualBox, VMware, Linux, WPS Office, Microsoft Office, IntelliJ IDEA, VS Code" },
  ],

  experience: [
    {
      company: "GFT Technologies",
      role: "Test Automation Analyst III",
      period: "Feb 2026 – Actualidad",
      bullets: [
        "Lidero la estrategia de automatización QA en entornos CI/CD para pruebas de servicios y front-end.",
        "Diseño y ejecuto pruebas de performance para validar estabilidad y comportamiento bajo carga.",
        "Gestiono DoD, Test Plan y trazabilidad de calidad.",
        "Implemento pruebas de aceptación con Karate y automatización web con Serenity.",
        "Desarrollo automatizaciones inteligentes con IA integrada.",
      ],
    },
    {
      company: "Bizagi Latam SAS",
      role: "Senior QA Engineer L1",
      period: "Ago 2025 – Dic 2025",
      bullets: [
        "Diseñé e implementé arquitecturas de automatización para pruebas API, Web y Mobile.",
        "Implementé soluciones en Azure para optimizar tiempos de ejecución.",
        "Establecí estándares de calidad técnica y patrones de diseño.",
        "Diseñé soluciones con IA para validación visual.",
        "Lideré capacitación QA y revisión de código.",
      ],
    },
    {
      company: "Tata Consultancy Services (TCS)",
      role: "Domain Consultant – QA Automation",
      period: "Dic 2024 – Ago 2025",
      bullets: [
        "Orquesté marcos de automatización QA alineados a pipelines CI/CD corporativos.",
        "Analicé y reestructuré soluciones de automatización de alta complejidad.",
        "Mejoré mantenibilidad mediante estandarización técnica.",
        "Administré pipelines en YAML y Azure DevOps.",
        "Brindé capacitación continua al equipo QA.",
      ],
    },
    {
      company: "Banco de Occidente",
      role: "QA Automation Engineer",
      period: "Abr 2023 – Dic 2024",
      bullets: [
        "Diseñé estrategias de pruebas automatizadas multiplataforma.",
        "Implementé pipelines CI/CD con GitHub Actions y GitLab CI.",
        "Optimicé flujos de trabajo QA.",
        "Capacité continuamente al equipo QA.",
      ],
    },
  ],

  education: [
    { title: "Ingeniero de Sistemas", inst: "Universidad Nacional Abierta y a Distancia (UNAD)", year: "2024" },
    { title: "Tecnólogo en Gestión de Redes de Datos", inst: "SENA", year: "2018" },
  ],

  certs: [
    "AI Fluency: Framework & Foundations — Anthropic",
    "Introduction to Claude Cowork — Anthropic",
    "Claude 101 — Anthropic",
    "Linux Essentials — LPI",
    "Programa Oracle Next Education (7 formaciones) — Oracle + Alura",
    "JavaScript — Cymetria Group",
    "Scrum Practitioner — CertMind",
    "Introducción a Automatización de Pruebas con Puppeteer — Platzi",
    "Automatización de Pruebas API Rest con Playwright — Udemy",
    "Curso de Playwright con JavaScript — Udemy",
    "Dominando Playwright con TypeScript: E2E Testing moderno — Udemy",
    "Master Class de Appium 2 con Java — Udemy",
    "Configuración básica con Appium+Serenity — Udemy",
    "Cypress: Master en Automatización Test QA — Udemy",
    "Master: Pruebas de Rendimiento con Apache JMeter — Udemy",
    "Master: Katalon Studio Test QA Automation — Udemy",
    "Selenium WebDriver y Grid — Udemy",
    "Docker Compose with Selenium — Udemy",
    "DevOps y Cloud con Azure DevOps — Udemy",
    "La Guía de Jenkins: De Cero a Experto — Udemy",
    "ISTQB Certified Tester Foundation Level (CTFL 4.0) — Udemy",
    "Selenium Essential Training — LinkedIn Learning",
  ],

  microsoftStudies: [
    "Escriba indicaciones eficaces para lograr resultados óptimos — Microsoft",
    "Introducción a Microsoft Copilot Studio — Microsoft",
    "Introducción a Microsoft 365 Copilot Chat (básico) — Microsoft",
  ],

  languages: [
    { lang: "Español", level: "Nativo" },
    { lang: "Inglés", level: "B1 (en progreso)" },
  ],
};

// ─────────────────────────────────────────────
// ESTILOS COMPARTIDOS
// ─────────────────────────────────────────────
const COLOR_PRIMARY = "1F4E79";
const COLOR_ACCENT  = "2E75B6";
const COLOR_LIGHT   = "D6E4F0";
const COLOR_RULE    = "ADB9CA";
const COLOR_TEXT    = "1A1A1A";

function sectionTitle(text) {
  return new Paragraph({
    children: [
      new TextRun({ text: text.toUpperCase(), bold: true, size: 24, color: COLOR_PRIMARY }),
    ],
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: COLOR_ACCENT } },
    spacing: { before: 220, after: 120 },
  });
}

function bullet(text, indent = 360) {
  return new Paragraph({
    bullet: { level: 0 },
    indent: { left: indent },
    children: [new TextRun({ text, size: 20, color: COLOR_TEXT })],
    spacing: { before: 30, after: 30 },
  });
}

function keyValue(key, value) {
  return new Paragraph({
    children: [
      new TextRun({ text: key + ": ", bold: true, size: 20, color: COLOR_PRIMARY }),
      new TextRun({ text: value, size: 20, color: COLOR_TEXT }),
    ],
    spacing: { before: 40, after: 40 },
  });
}

// ─────────────────────────────────────────────
// VERSIÓN 1 — ATS PURO
// ─────────────────────────────────────────────
function buildATS() {
  const children = [];

  // ENCABEZADO
  children.push(new Paragraph({
    children: [new TextRun({ text: DATA.name, bold: true, size: 48, color: COLOR_PRIMARY })],
    alignment: AlignmentType.CENTER,
    spacing: { after: 60 },
  }));
  children.push(new Paragraph({
    children: [new TextRun({ text: DATA.title, bold: false, size: 22, color: COLOR_ACCENT })],
    alignment: AlignmentType.CENTER,
    spacing: { after: 60 },
  }));
  children.push(new Paragraph({
    children: [
      new TextRun({ text: `${DATA.location}  |  ${DATA.phone1}  |  ${DATA.phone2}`, size: 19, color: COLOR_TEXT }),
    ],
    alignment: AlignmentType.CENTER,
    spacing: { after: 40 },
  }));
  children.push(new Paragraph({
    children: [
      new TextRun({ text: `${DATA.email}  |  ${DATA.linkedin}  |  ${DATA.github}`, size: 19, color: COLOR_TEXT }),
    ],
    alignment: AlignmentType.CENTER,
    spacing: { after: 100 },
  }));

  // PERFIL
  children.push(sectionTitle("Perfil Profesional"));
  children.push(new Paragraph({
    children: [new TextRun({ text: DATA.profile, size: 20, color: COLOR_TEXT })],
    spacing: { before: 60, after: 60 },
  }));

  // HABILIDADES
  children.push(sectionTitle("Competencias Técnicas"));
  for (const s of DATA.skills) {
    children.push(keyValue(s.cat, s.items));
  }

  // EXPERIENCIA
  children.push(sectionTitle("Experiencia Profesional"));
  for (const exp of DATA.experience) {
    children.push(new Paragraph({
      children: [
        new TextRun({ text: exp.company, bold: true, size: 22, color: COLOR_PRIMARY }),
        new TextRun({ text: "  —  ", size: 22, color: COLOR_TEXT }),
        new TextRun({ text: exp.role, bold: true, size: 22, color: COLOR_TEXT }),
        new TextRun({ text: `    ${exp.period}`, italics: true, size: 20, color: "555555" }),
      ],
      spacing: { before: 120, after: 40 },
    }));
    for (const b of exp.bullets) {
      children.push(bullet(b));
    }
  }

  // EDUCACIÓN
  children.push(sectionTitle("Educación"));
  for (const e of DATA.education) {
    children.push(new Paragraph({
      children: [
        new TextRun({ text: e.title, bold: true, size: 21, color: COLOR_PRIMARY }),
        new TextRun({ text: `  —  ${e.inst}  (${e.year})`, size: 20, color: COLOR_TEXT }),
      ],
      spacing: { before: 80, after: 40 },
    }));
  }

  // CERTIFICACIONES
  children.push(sectionTitle("Certificaciones"));
  for (const c of DATA.certs) {
    children.push(bullet(c));
  }

  // CAPACITACIÓN MICROSOFT
  if (DATA.microsoftStudies && DATA.microsoftStudies.length > 0) {
    children.push(sectionTitle("Capacitación Microsoft"));
    for (const m of DATA.microsoftStudies) {
      children.push(bullet(m));
    }
  }

  // IDIOMAS
  children.push(sectionTitle("Idiomas"));
  for (const l of DATA.languages) {
    children.push(keyValue(l.lang, l.level));
  }

  return new Document({
    sections: [{
      properties: {
        page: {
          margin: {
            top: convertInchesToTwip(0.75),
            bottom: convertInchesToTwip(0.75),
            left: convertInchesToTwip(0.85),
            right: convertInchesToTwip(0.85),
          },
        },
      },
      children,
    }],
  });
}

// ─────────────────────────────────────────────
// GENERAR ARCHIVOS
// ─────────────────────────────────────────────
async function main() {
  console.log("📄 Generando CV en formato ATS...");
  const atsDoc = buildATS();
  const atsBuffer = await Packer.toBuffer(atsDoc);
  const atsPath = `${OUTPUT_DIR}/HV_2026_ATS_AndesRodriguez.docx`;
  writeFileSync(atsPath, atsBuffer);
  console.log(`✅ ${atsPath}`);

  console.log("\n🎉 Archivos generados correctamente.");
  console.log("📁 Ubicación: " + OUTPUT_DIR);
  console.log("\n📝 Próximo paso: Convertir DOCX a PDF usando WPS Office o libreoffice");
}

main().catch(err => {
  console.error("❌ Error:", err);
  process.exit(1);
});
