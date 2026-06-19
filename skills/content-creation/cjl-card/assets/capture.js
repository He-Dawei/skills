#!/usr/bin/env node

const path = require('path');
const http = require('http');

async function serveHtml(htmlPath) {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(require('fs').readFileSync(htmlPath));
    });
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      resolve(`http://127.0.0.1:${port}`);
      // Keep server alive - will be closed when browser closes
    });
  });
}

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

  const browser = await chromium.launch({
    args: [
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-font-subsetting',
      '--font-render-hinting=none',
      '--allow-profiles-outside-user-dir',
    ],
  });
  const page = await browser.newPage();
  await page.setViewportSize({ width, height: fullpage ? 800 : height });

  // Serve via HTTP instead of file:// to allow web fonts to load (CORS)
  const url = await serveHtml(path.resolve(htmlPath));
  await page.goto(url, { waitUntil: 'networkidle' });
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
