import { expect, test } from '@playwright/test';

test('a nyitóoldal és az indítógomb működik', async ({ page }) => {
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  await page.goto('./');
  await expect(page.getByRole('heading', { name: 'Athéni demokrácia' })).toBeVisible();
  await expect(page.getByRole('link', { name: 'Tananyag indítása' })).toHaveAttribute('href', './learn.html');
  expect(errors).toEqual([]);
});

test('a H5P Interactive Book betöltődik és 30 oldalas', async ({ page }) => {
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  await page.goto('./learn.html');
  await expect(page.locator('#h5p-container')).toHaveAttribute('data-state', 'ready', { timeout: 45_000 });
  await expect(page.locator('#error-state')).toBeHidden();
  const iframe = page.locator('iframe.h5p-iframe').first();
  await expect(iframe).toBeVisible();
  const contentResponse = await page.request.get('./h5p/atheni-demokracia/content/content.json');
  expect(contentResponse.ok()).toBe(true);
  const content = await contentResponse.json();
  expect(content.chapters).toHaveLength(30);
  expect(JSON.stringify(content)).toContain('Ki döntött Athénban – és ki maradt kívül?');
  await page.waitForTimeout(500);
  expect(errors).toEqual([]);
});

test('a mobilnézet nem okoz vízszintes túlcsordulást', async ({ page, isMobile }) => {
  test.skip(!isMobile, 'Csak a mobilprojektben fut.');
  await page.goto('./learn.html');
  await expect(page.locator('#h5p-container')).toHaveAttribute('data-state', 'ready', { timeout: 45_000 });
  await expect(page.locator('iframe.h5p-iframe').first()).toBeVisible();
  const hasOverflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
  expect(hasOverflow).toBe(false);
});
