import { chromium } from '@playwright/test';
import fs from 'fs';

const viewports = [
  { name: 'Samsung S24 (360px)', width: 360, height: 800 },
  { name: 'Tablet (768px)', width: 768, height: 1024 },
  { name: 'Desktop (1920px)', width: 1920, height: 1080 }
];

(async () => {
  for (const viewport of viewports) {
    const browser = await chromium.launch();
    const context = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height } });
    const page = await context.newPage();
    
    try {
      await page.goto('http://localhost:5173', { waitUntil: 'networkidle' });
      await page.screenshot({ path: `screenshot-${viewport.width}px.png` });
      
      // Obtener info del grid
      const skillsInfo = await page.locator('#skills .grid').evaluate(el => ({
        computedStyle: window.getComputedStyle(el).gridTemplateColumns,
        width: el.offsetWidth,
        childCount: el.children.length,
        childWidths: Array.from(el.children).map(c => c.offsetWidth)
      }));
      
      console.log(`\n✅ ${viewport.name}:`);
      console.log(`   Grid Template Columns: ${skillsInfo.computedStyle}`);
      console.log(`   Container Width: ${skillsInfo.width}px`);
      console.log(`   Cards per row: ${skillsInfo.childCount}`);
      console.log(`   Individual card widths: [${skillsInfo.childWidths.join(', ')}]px`);
    } catch (err) {
      console.log(`❌ ${viewport.name}: ${err.message}`);
    }
    
    await context.close();
    await browser.close();
  }
})();
