import { expect, test } from '@playwright/test';

const slug = 'geza-fejedelem-szent-istvan';

test('a GSI-02 modulkártya, borítókép és útvonal elérhető', async ({ page }) => {
  await page.goto('./');
  const card = page.getByRole('heading', { name: 'Géza fejedelem és I. (Szent) István' }).locator('..').locator('..');
  await expect(card.getByRole('img', { name: 'I. István ábrázolása az 1031-ben készült koronázási paláston.' })).toBeVisible();
  await expect(card.getByRole('link', { name: /Tananyag indítása/ })).toHaveAttribute('href', `./learn.html?module=${slug}`);
  await page.goto('./library.html?era=kozepkor');
  await expect(page.getByRole('heading', { name: 'Géza fejedelem és I. (Szent) István' })).toBeVisible();
  await expect(page.getByRole('img', { name: 'I. István ábrázolása az 1031-ben készült koronázási paláston.' })).toBeVisible();
});

test('a GSI-02 Interactive Book 30 oldallal és magyar felülettel betöltődik', async ({ page }) => {
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  await page.goto(`./learn.html?module=${slug}`);
  await expect(page.getByRole('heading', { name: 'Géza fejedelem és I. (Szent) István' }).first()).toBeVisible();
  await expect(page.locator('#h5p-container')).toHaveAttribute('data-state', 'ready', { timeout: 45_000 });
  await expect(page.locator('#error-state')).toBeHidden();
  const frame = page.frameLocator('iframe.h5p-iframe');
  await expect(frame.getByText('Két nemzedék, egy államalapítási fordulat', { exact: true }).first()).toBeVisible();
  const visibleText = await frame.locator('body').innerText();
  expect(visibleText).toMatch(/1\s*\/\s*30/);
  expect(visibleText).not.toMatch(/\b(Check|Retry|Submit|Previous|Next|Finish|Correct|Incorrect)\b|Show Solution|Your result|Summary & submit/i);
  expect(errors).toEqual([]);
});

test('a GSI-02 csomag oldalszerkezete, assetjei és zárótesztje teljes', async ({ page }) => {
  await page.goto(`./learn.html?module=${slug}`);
  await expect(page.locator('#h5p-container')).toHaveAttribute('data-state', 'ready', { timeout: 45_000 });
  const response = await page.request.get(`./h5p/${slug}/content/content.json`);
  expect(response.ok()).toBe(true);
  const content = await response.json();
  expect(content.chapters).toHaveLength(30);
  expect(content.showCoverPage).toBe(false);
  expect(content.behaviour.displaySummary).toBe(false);
  const serialized = JSON.stringify(content);
  for (let number = 1; number <= 30; number += 1) {
    expect(serialized).toContain(`${slug}--pg-${String(number).padStart(3, '0')}`);
  }
  for (const asset of ['kingdom-hungary-1000.svg', 'hungary-11th-century.png', 'stephen-coronation-pall.jpg', 'pannonhalma-charter.jpg', 'stephen-monogram.svg']) {
    const assetResponse = await page.request.get(`./h5p/${slug}/content/images/${asset}`);
    expect(assetResponse.ok(), asset).toBe(true);
  }
  const finalSet = content.chapters[29].params.content
    .map((item) => item.content)
    .find((item) => item.library === 'H5P.QuestionSet 1.20');
  expect(finalSet.params.questions).toHaveLength(10);
  expect(finalSet.params.passPercentage).toBe(60);
  expect(finalSet.params.questions.map((question) => question.params.answers.filter((answer) => answer.correct).length)).toEqual(Array(10).fill(2));
  expect(serialized).not.toMatch(/PLACEHOLDER|TODO|FIXME|Forrásnyom|Helyes válasz:|Gyakori hiba:/i);
});

test('a GSI-02 tananyag mobilon és tableten sem okoz vízszintes túlcsordulást', async ({ page }) => {
  await page.goto(`./learn.html?module=${slug}`);
  await expect(page.locator('#h5p-container')).toHaveAttribute('data-state', 'ready', { timeout: 45_000 });
  const hasOverflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
  expect(hasOverflow).toBe(false);
});
