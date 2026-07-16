import { chromium } from '@playwright/test';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';

const baseURL = process.env.DTEA_SCREENSHOT_BASE_URL || 'http://127.0.0.1:4173';
const executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH;
const output = path.resolve('docs/screenshots/gsi-02');
await mkdir(output, { recursive: true });

const browser = await chromium.launch({ headless: true, ...(executablePath ? { executablePath } : {}) });
try {
  const desktop = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  await desktop.goto(`${baseURL}/`);
  const cardHeading = desktop.getByRole('heading', { name: 'Géza fejedelem és I. (Szent) István' });
  await cardHeading.scrollIntoViewIfNeeded();
  await cardHeading.locator('xpath=ancestor::article').screenshot({ path: path.join(output, '01-home-module-card-desktop.png') });

  await desktop.goto(`${baseURL}/learn.html?module=geza-fejedelem-szent-istvan`);
  await desktop.locator('#h5p-container').waitFor({ state: 'visible' });
  await desktop.locator('#h5p-container[data-state="ready"]').waitFor({ timeout: 45_000 });
  await desktop.frameLocator('iframe.h5p-iframe').getByText('Két nemzedék, egy államalapítási fordulat', { exact: true }).first().waitFor();
  await desktop.screenshot({ path: path.join(output, '02-book-first-page-desktop.png'), fullPage: true });

  const book = desktop.frameLocator('iframe.h5p-iframe');
  const finalButton = book.getByRole('button', { name: /Záróteszt/ }).first();
  await finalButton.click();
  await book.getByRole('heading', { name: 'Záróteszt', exact: true }).first().waitFor();
  await desktop.screenshot({ path: path.join(output, '03-final-test-desktop.png'), fullPage: true });
  await desktop.close();

  const mobile = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
  await mobile.goto(`${baseURL}/learn.html?module=geza-fejedelem-szent-istvan`);
  await mobile.locator('#h5p-container[data-state="ready"]').waitFor({ timeout: 45_000 });
  await mobile.frameLocator('iframe.h5p-iframe').getByText('Két nemzedék, egy államalapítási fordulat', { exact: true }).first().waitFor();
  await mobile.screenshot({ path: path.join(output, '04-book-first-page-mobile.png'), fullPage: true });
  await mobile.close();
} finally {
  await browser.close();
}

console.log(`GSI-02 screenshots: ${output}`);
