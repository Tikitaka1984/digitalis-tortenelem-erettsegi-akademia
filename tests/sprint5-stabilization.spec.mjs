import { expect, test } from '@playwright/test';

test('a központi modulkonfiguráció teljes és verziózott', async ({ request }) => {
  const response = await request.get('./data/modules.json');
  expect(response.ok()).toBe(true);
  const config = await response.json();
  expect(config.platformVersion).toBe('1.1.0');
  expect(config.taxonomy.map((item) => item.id)).toEqual([
    'okor', 'kozepkor', 'kora-ujkor', 'ujkor', 'huszadik-szazad', 'jelenkor'
  ]);
  expect(config.modules.filter((item) => item.status === 'available')).toHaveLength(2);
});

test('a könyvtár era és level mélylinkjei működnek', async ({ page }) => {
  await page.goto('./library.html?era=kora-ujkor&level=kozep');
  await expect(page.getByRole('heading', { name: 'Földrajzi felfedezések' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Athéni demokrácia' })).toBeHidden();
  await expect(page.getByRole('button', { name: 'Kora újkor' })).toHaveAttribute('aria-pressed', 'true');
  await expect(page.getByRole('button', { name: 'Középszint' })).toHaveAttribute('aria-pressed', 'true');
  await page.getByRole('button', { name: 'Szűrők törlése' }).click();
  await expect(page).toHaveURL(/library\.html$/);
  await expect(page.getByRole('heading', { name: 'Athéni demokrácia' })).toBeVisible();
});

test('a haladásjelző a H5P aktuális fejezetét követi', async ({ page }) => {
  await page.goto('./learn.html?module=foldrajzi-felfedezesek');
  await expect(page.locator('#h5p-container')).toHaveAttribute('data-state', 'ready', { timeout: 45_000 });
  await expect(page.locator('[data-progress-label]')).toHaveText('1 / 30 oldal');
  const book = page.frameLocator('iframe.h5p-iframe');
  await book.getByRole('button', { name: /Portugál kezdeményezés/i }).click();
  await expect(page.locator('[data-progress-label]')).not.toHaveText('1 / 30 oldal', { timeout: 5_000 });
  await expect(page.locator('[data-course-progress]')).not.toHaveCSS('width', '0px');
});

test('a publikált H5P-manifesztumok licencet, szerzőt és verziót tartalmaznak', async ({ request }) => {
  for (const slug of ['atheni-demokracia', 'foldrajzi-felfedezesek']) {
    const response = await request.get(`./h5p/${slug}/h5p.json`);
    expect(response.ok(), slug).toBe(true);
    const manifest = await response.json();
    expect(manifest.license, slug).toBeTruthy();
    expect(manifest.authors?.[0]?.name, slug).toBeTruthy();
    expect(manifest.version, slug).toMatch(/^\d+\.\d+\.\d+$/);
  }
});

test('a kezdőlap nem mutat jelöletlen demóadatot', async ({ page }) => {
  await page.goto('./');
  await expect(page.getByText('40%', { exact: true })).toHaveCount(0);
  await expect(page.getByText('12 / 30', { exact: true })).toHaveCount(0);
  await expect(page.getByText('Demófelület', { exact: true })).toBeVisible();
});

test('a platform desktop, tablet és mobil nézetben nem csordul túl', async ({ page }) => {
  for (const path of ['./', './library.html?era=okor&level=kozep', './learn.html?module=atheni-demokracia', './learn.html?module=foldrajzi-felfedezesek']) {
    await page.goto(path);
    if (path.includes('learn.html')) await expect(page.locator('#h5p-container')).toHaveAttribute('data-state', 'ready', { timeout: 45_000 });
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
    expect(overflow, path).toBe(false);
  }
});
