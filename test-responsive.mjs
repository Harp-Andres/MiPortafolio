import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  
  console.log('🔍 Verificando responsive en portafolio desplegado...\n');
  
  // Test Samsung S24 (360px)
  await page.setViewport({ width: 360, height: 800 });
  await page.goto('https://harp-andres.github.io/MiPortafolio/', { waitUntil: 'networkidle2' });
  
  const skillsGrid360 = await page.evaluate(() => {
    const grid = document.querySelector('section#skills .grid');
    if (grid) {
      const colCount = window.getComputedStyle(grid).gridTemplateColumns.split(' ').length;
      return { viewport: '360px', columns: colCount, childCount: grid.children.length };
    }
    return { viewport: '360px', error: 'Skills grid not found' };
  });
  
  console.log('📱 Samsung S24 (360px):', skillsGrid360);
  
  // Test Tablet (768px)
  await page.setViewport({ width: 768, height: 1024 });
  const skillsGrid768 = await page.evaluate(() => {
    const grid = document.querySelector('section#skills .grid');
    if (grid) {
      const colCount = window.getComputedStyle(grid).gridTemplateColumns.split(' ').length;
      return { viewport: '768px', columns: colCount, childCount: grid.children.length };
    }
    return { viewport: '768px', error: 'Skills grid not found' };
  });
  
  console.log('📱 Tablet (768px):', skillsGrid768);
  
  // Test Desktop (1920px)
  await page.setViewport({ width: 1920, height: 1080 });
  const skillsGrid1920 = await page.evaluate(() => {
    const grid = document.querySelector('section#skills .grid');
    if (grid) {
      const colCount = window.getComputedStyle(grid).gridTemplateColumns.split(' ').length;
      return { viewport: '1920px', columns: colCount, childCount: grid.children.length };
    }
    return { viewport: '1920px', error: 'Skills grid not found' };
  });
  
  console.log('📱 Desktop (1920px):', skillsGrid1920);
  
  // Verify Education grid
  console.log('\n📚 Education Section:');
  
  await page.setViewport({ width: 360, height: 800 });
  const eduGrid360 = await page.evaluate(() => {
    const grid = document.querySelector('section#education .grid');
    if (grid) {
      const colCount = window.getComputedStyle(grid).gridTemplateColumns.split(' ').length;
      return { viewport: '360px', columns: colCount };
    }
    return { viewport: '360px', error: 'Education grid not found' };
  });
  
  console.log('📱 Samsung S24 (360px):', eduGrid360);
  
  await page.setViewport({ width: 768, height: 1024 });
  const eduGrid768 = await page.evaluate(() => {
    const grid = document.querySelector('section#education .grid');
    if (grid) {
      const colCount = window.getComputedStyle(grid).gridTemplateColumns.split(' ').length;
      return { viewport: '768px', columns: colCount };
    }
    return { viewport: '768px', error: 'Education grid not found' };
  });
  
  console.log('📱 Tablet (768px):', eduGrid768);
  
  await browser.close();
  
  // Resumen
  console.log('\n✅ RESUMEN RESPONSIVE:\n');
  console.log('SKILLS (esperado: 1 col → 2 cols → 3 cols):');
  console.log(`  ✓ 360px  (Mobile):   ${skillsGrid360.columns || '?'} columnas`);
  console.log(`  ✓ 768px  (Tablet):   ${skillsGrid768.columns || '?'} columnas`);
  console.log(`  ✓ 1920px (Desktop):  ${skillsGrid1920.columns || '?'} columnas`);
  
  console.log('\nEDUCATION (esperado: 1 col → 2 cols):');
  console.log(`  ✓ 360px  (Mobile):   ${eduGrid360.columns || '?'} columnas`);
  console.log(`  ✓ 768px  (Tablet):   ${eduGrid768.columns || '?'} columnas`);
})();
