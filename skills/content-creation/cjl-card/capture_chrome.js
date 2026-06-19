#!/usr/bin/env node

const path = require('path');
const fs = require('fs');

async function main() {
  const args = process.argv.slice(2);
  const htmlPath = args[0];
  const outputPath = args[1];
  const width = parseInt(args[2]) || 1200;
  const height = parseInt(args[3]) || 1600;
  const fullpage = args[4] === 'fullpage';

  if (!htmlPath || !outputPath) {
    console.error('Usage: node capture.js <html> <png> [width] [height] [fullpage]');
    process.exit(1);
  }

  let chromium;
  try {
    chromium = require('playwright').chromium;
  } catch {
    console.error('Playwright not found. Run: npx playwright install chromium');
    process.exit(1);
  }

  // Try to use the full Chrome executable on Mac
  const chromePaths = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium'
  ];

  let browser;
  const chromePath = chromePaths.find(p => {
    try {
      require('fs').accessSync(p, fs.constants.X_OK);
      return true;
    } catch { return false; }
  });

  if (chromePath) {
    browser = await chromium.launch({
      executablePath: chromePath,
      headless: true,
      args: [
        '--font-render-hinting=none',
        '--disable-font-subpixel-positioning',
        '--no-sandbox',
        '--disable-setuid-sandbox'
      ]
    });
  } else {
    browser = await chromium.launch({
      headless: true,
      args: [
        '--font-render-hinting=none',
        '--disable-font-subpixel-positioning',
        '--no-sandbox',
        '--disable-setuid-sandbox'
      ]
    });
  }

  const page = await browser.newPage();
  await page.setViewportSize({ width, height: fullpage ? 800 : height });

  const htmlContent = fs.readFileSync(htmlPath, 'utf8');
  await page.setContent(htmlContent, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  if (fullpage) {
    const bodyHeight = await page.evaluate(() => document.body.scrollHeight);
    await page.setViewportSize({ width, height: bodyHeight });
    await page.waitForTimeout(300);
    await page.screenshot({
      path: path.resolve(outputPath),
      type: 'png',
      clip: { x: 0, y: 0, width, height: bodyHeight }
    });
  } else {
    await page.screenshot({
      path: path.resolve(outputPath),
      type: 'png',
      clip: { x: 0, y: 0, width, height }
    });
  }

  await browser.close();
  console.log('OK: ' + path.resolve(outputPath));
}

main().catch(err => {
  console.error(err.message);
  process.exit(1);
});