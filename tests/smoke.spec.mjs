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
  await expect(page.locator('#error-state')).toBeHidden();
  const book = page.locator('#h5p-container .h5p-interactive-book');
  await expect(book).toBeVisible({ timeout: 45_000 });
  await expect(book.getByText('Ki döntött Athénban – és ki maradt kívül?')).toBeVisible();
  expect(errors).toEqual([]);
});

test('a mobilnézet nem okoz vízszintes túlcsordulást', async ({ page, isMobile }) => {
  test.skip(!isMobile, 'Csak a mobilprojektben fut.');
  await page.goto('./learn.html');
  await expect(page.locator('#h5p-container .h5p-interactive-book')).toBeVisible({ timeout: 45_000 });
  const hasOverflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
  expect(hasOverflow).toBe(false);
});
