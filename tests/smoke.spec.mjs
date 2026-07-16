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
  const menuButton = page.getByRole('button', { name: 'Menü megnyitása' });
  if (isMobile && await menuButton.isVisible()) {
    await menuButton.click();
  }
  await expect(page.getByRole('navigation', { name: 'Fő navigáció' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Válassz tanulási útvonalat' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Földrajzi felfedezések' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Géza fejedelem és I. (Szent) István' })).toBeVisible();
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
  await expect(page.getByRole('heading', { name: 'Géza fejedelem és I. (Szent) István' })).toBeVisible();
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
  expect(content.showCoverPage).toBe(false);
  expect(content.behaviour.displaySummary).toBe(false);
  expect(JSON.stringify(content)).toContain('Egy felfedezés kinek jelentett lehetőséget');
  const studentFacing = JSON.stringify(content.chapters.map((chapter) => chapter.params.content
    .filter((item) => item.content.library === 'H5P.AdvancedText 1.1')
    .map((item) => item.content.params.text)));
  expect(studentFacing).not.toMatch(/Tanulói szöveg|Megjelenő szöveg|Akadálymentes alternatíva|VIZUÁLIS ELEM|KÉSŐBB CSERÉLENDŐ|PLACEHOLDER|Pontozás:|Helyes válasz:|Helyes visszajelzés:|Hibás visszajelzés:/i);
  for (const asset of ['cover-atlantic-routes.webp', 'navigation-tools.svg', 'martellus-world-map-1489.jpg', 'cantino-planisphere-1502.jpg', 'juan-de-la-cosa-map-1500.jpg', 'ribero-world-map-1529.jpg', 'agnese-world-map-1544.jpg']) {
    const assetResponse = await page.request.get(`./h5p/foldrajzi-felfedezesek/content/images/${asset}`);
    expect(assetResponse.ok(), asset).toBe(true);
  }
  expect(JSON.stringify(content)).not.toMatch(/dias-route\.svg|da-gama-route\.svg|columbus-route\.svg|tordesillas\.svg|magellan-route\.svg|route-overview\.svg/i);
  expect(JSON.stringify(content)).toContain('Térkép forrása és licence');
  await page.waitForTimeout(500);
  expect(errors).toEqual([]);
});

test('a Földrajzi felfedezések első oldala teljesen magyar és 30 oldalt jelez', async ({ page }) => {
  await page.goto('./learn.html?module=foldrajzi-felfedezesek');
  await expect(page.locator('#h5p-container')).toHaveAttribute('data-state', 'ready', { timeout: 45_000 });
  const book = page.frameLocator('iframe.h5p-iframe');
  await expect(book.getByRole('img', { name: 'Stilizált atlanti térkép tengeri útvonalakkal és egy 15. századi karavellával.' })).toBeVisible();
  const visibleText = await book.locator('body').innerText();
  expect(visibleText).toMatch(/1\s*\/\s*30/);
  expect(visibleText).not.toMatch(/\b(Check|Retry|Submit|Previous|Next|Finish|Correct|Incorrect)\b|Show Solution|Your result|Summary & submit/i);
  expect(visibleText).not.toMatch(/Tanulói szöveg|Megjelenő szöveg|Multiple Choice|Single Choice Set|Question Set|Accordion|VIZUÁLIS ELEM|KÉSŐBB CSERÉLENDŐ|PLACEHOLDER/i);
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
  for (const path of ['./', './library.html', './learn.html', './learn.html?module=foldrajzi-felfedezesek', './learn.html?module=geza-fejedelem-szent-istvan']) {
    await page.goto(path);
    if (path.endsWith('learn.html')) {
      await expect(page.locator('#h5p-container')).toHaveAttribute('data-state', 'ready', { timeout: 45_000 });
      await expect(page.locator('iframe.h5p-iframe').first()).toBeVisible();
    }
    await expectNoHorizontalOverflow(page);
  }
});
