import { expect, test } from '@playwright/test';

const collectPageErrors = (page) => {
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  return errors;
};

const expectNoHorizontalOverflow = async (page) => {
  const hasOverflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
  expect(hasOverflow).toBe(false);
};

test('a prémium nyitóoldal, navigáció és CTA működik', async ({ page, isMobile }) => {
  const errors = collectPageErrors(page);
  await page.goto('./');
  await expect(page.getByRole('heading', { name: /A történelem nem évszámok sora/ })).toBeVisible();
  await expect(page.getByRole('link', { name: /Athéni demokrácia indítása/ })).toHaveAttribute('href', './learn.html');
  if (isMobile) {
    await page.getByRole('button', { name: 'Menü megnyitása' }).click();
  }
  await expect(page.getByRole('navigation', { name: 'Fő navigáció' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Válassz tanulási útvonalat' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Földrajzi felfedezések' })).toBeVisible();
  await expectNoHorizontalOverflow(page);
  expect(errors).toEqual([]);
});

test('a sötét mód megmarad navigáció után', async ({ page }) => {
  await page.goto('./');
  await page.getByRole('button', { name: 'Sötét mód bekapcsolása' }).click();
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
  await page.goto('./library.html');
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
  await expect(page.getByRole('button', { name: 'Világos mód bekapcsolása' })).toBeVisible();
});

test('a digitális könyvtár keresése és szűrése működik', async ({ page }) => {
  const errors = collectPageErrors(page);
  await page.goto('./library.html');
  await expect(page.getByRole('heading', { name: 'Építs biztos történelmi tudást.' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Athéni demokrácia' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Földrajzi felfedezések' })).toBeVisible();
  await page.getByPlaceholder('Keress témakörre vagy korszakra…').fill('nincs ilyen');
  await expect(page.getByRole('heading', { name: 'Nincs ilyen tananyag' })).toBeVisible();
  await page.getByRole('button', { name: 'Szűrők törlése' }).click();
  await expect(page.getByRole('heading', { name: 'Athéni demokrácia' })).toBeVisible();
  await expectNoHorizontalOverflow(page);
  expect(errors).toEqual([]);
});

test('a H5P Interactive Book betöltődik és 30 oldalas', async ({ page }) => {
  const errors = collectPageErrors(page);
  await page.goto('./learn.html');
  await expect(page.getByRole('heading', { name: 'Athéni demokrácia' }).first()).toBeVisible();
  await expect(page.locator('#h5p-container')).toHaveAttribute('data-state', 'ready', { timeout: 45_000 });
  await expect(page.locator('#error-state')).toBeHidden();
  await expect(page.locator('iframe.h5p-iframe').first()).toBeVisible();
  await expect(page.getByText('30 oldal', { exact: true })).toBeVisible();
  const contentResponse = await page.request.get('./h5p/atheni-demokracia/content/content.json');
  expect(contentResponse.ok()).toBe(true);
  const content = await contentResponse.json();
  expect(content.chapters).toHaveLength(30);
  expect(JSON.stringify(content)).toContain('Ki döntött Athénban – és ki maradt kívül?');
  await page.waitForTimeout(500);
  expect(errors).toEqual([]);
});

test('a Földrajzi felfedezések H5P könyv betöltődik és 30 oldalas', async ({ page }) => {
  const errors = collectPageErrors(page);
  await page.goto('./learn.html?module=foldrajzi-felfedezesek');
  await expect(page.getByRole('heading', { name: 'Földrajzi felfedezések' }).first()).toBeVisible();
  await expect(page.locator('#h5p-container')).toHaveAttribute('data-state', 'ready', { timeout: 45_000 });
  await expect(page.locator('#error-state')).toBeHidden();
  await expect(page.locator('iframe.h5p-iframe').first()).toBeVisible();
  const contentResponse = await page.request.get('./h5p/foldrajzi-felfedezesek/content/content.json');
  expect(contentResponse.ok()).toBe(true);
  const content = await contentResponse.json();
  expect(content.chapters).toHaveLength(30);
  expect(JSON.stringify(content)).toContain('Egy felfedezés kinek jelentett lehetőséget');
  await page.waitForTimeout(500);
  expect(errors).toEqual([]);
});

test('a tananyag fókusz módja működik', async ({ page }) => {
  await page.goto('./learn.html');
  const toggle = page.locator('[data-focus-toggle]');
  await toggle.click();
  await expect(page.locator('body')).toHaveClass(/is-focus-mode/);
  await expect(page.locator('.course-sidebar')).toBeHidden();
  await expect(toggle).toHaveAttribute('aria-pressed', 'true');
});

test('az alapvető akadálymentességi szerkezet érvényes', async ({ page }) => {
  await page.goto('./');
  await expect(page.locator('html')).toHaveAttribute('lang', 'hu');
  await expect(page.getByRole('link', { name: 'Ugrás a tartalomhoz' })).toHaveAttribute('href', '#main');
  expect(await page.locator('main').count()).toBe(1);
  expect(await page.locator('[id]').evaluateAll((nodes) => new Set(nodes.map((node) => node.id)).size)).toBe(await page.locator('[id]').count());
  expect(await page.locator('img:not([alt])').count()).toBe(0);
  expect(await page.locator('button:not([type])').count()).toBe(0);
});

test('a mobilnézetek nem okoznak vízszintes túlcsordulást', async ({ page, isMobile }) => {
  test.skip(!isMobile, 'Csak a mobilprojektben fut.');
  for (const path of ['./', './library.html', './learn.html', './learn.html?module=foldrajzi-felfedezesek']) {
    await page.goto(path);
    if (path.endsWith('learn.html')) {
      await expect(page.locator('#h5p-container')).toHaveAttribute('data-state', 'ready', { timeout: 45_000 });
      await expect(page.locator('iframe.h5p-iframe').first()).toBeVisible();
    }
    await expectNoHorizontalOverflow(page);
  }
});
