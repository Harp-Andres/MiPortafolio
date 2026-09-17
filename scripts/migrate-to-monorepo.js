#!/usr/bin/env node

/**
 * Phase 1: Monorepo Migration Script
 * Moves current project structure into packages/web/
 * 
 * Usage: node scripts/migrate-to-monorepo.js
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rootDir = path.join(__dirname, '..');
const srcDir = path.join(rootDir, 'src');
const publicDir = path.join(rootDir, 'public');
const configFiles = [
  'vite.config.mjs',
  'vitest.config.ts',
  'playwright.config.ts',
  'tailwind.config.ts',
  'postcss.config.js',
];

const webDir = path.join(rootDir, 'packages', 'web');
const webSrcDir = path.join(webDir, 'src');
const webPublicDir = path.join(webDir, 'public');

console.log('🚀 Phase 1: Monorepo Migration\n');

// Function to copy directory recursively
function copyDirRecursive(src, dest) {
  if (!fs.existsSync(src)) {
    console.log(`⚠️  Source not found: ${src}`);
    return;
  }

  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  const files = fs.readdirSync(src);
  files.forEach(file => {
    const srcPath = path.join(src, file);
    const destPath = path.join(dest, file);

    if (fs.statSync(srcPath).isDirectory()) {
      copyDirRecursive(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
      console.log(`✅ Copied: ${file}`);
    }
  });
}

// Function to copy single file
function copyFile(src, dest) {
  const fileName = path.basename(src);
  if (!fs.existsSync(src)) {
    console.log(`⚠️  File not found: ${fileName}`);
    return;
  }

  const destDir = path.dirname(dest);
  if (!fs.existsSync(destDir)) {
    fs.mkdirSync(destDir, { recursive: true });
  }

  fs.copyFileSync(src, dest);
  console.log(`✅ Copied: ${fileName}`);
}

try {
  // 1. Copy src/ to packages/web/src/
  console.log('\n📁 Step 1: Copying src/ directory...');
  if (fs.existsSync(srcDir)) {
    copyDirRecursive(srcDir, webSrcDir);
    console.log('✅ src/ migrated to packages/web/src/\n');
  } else {
    console.log('⚠️  src/ directory not found\n');
  }

  // 2. Copy public/ to packages/web/public/
  console.log('📁 Step 2: Copying public/ directory...');
  if (fs.existsSync(publicDir)) {
    copyDirRecursive(publicDir, webPublicDir);
    console.log('✅ public/ migrated to packages/web/public/\n');
  } else {
    console.log('⚠️  public/ directory not found\n');
  }

  // 3. Copy configuration files
  console.log('⚙️  Step 3: Copying configuration files...');
  configFiles.forEach(file => {
    const src = path.join(rootDir, file);
    const dest = path.join(webDir, file);
    copyFile(src, dest);
  });
  console.log('✅ Configuration files copied\n');

  // 4. Summary
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('✅ PHASE 1 MIGRATION COMPLETE!');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('\n📋 Next Steps:\n');
  console.log('1. Update import paths in packages/web/src/');
  console.log('   OLD: import { CV_DATA } from "@/utils/cv-data"');
  console.log('   NEW: import { CV_DATA } from "@mportafolio/core"');
  console.log('\n2. Install dependencies:');
  console.log('   $ pnpm install');
  console.log('\n3. Test the setup:');
  console.log('   $ pnpm dev              # Start dev server');
  console.log('   $ pnpm test             # Run tests');
  console.log('\n4. Verify synchronization:');
  console.log('   $ pnpm sync:verify');
  console.log('\n✨ You are ready to continue with Phase 2!');
  
} catch (error) {
  console.error('❌ Migration failed:', error.message);
  process.exit(1);
}
