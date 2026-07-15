import { expect, test } from '@playwright/test';

const screenshotDir = 'docs/screenshots/sprint-4-1';

async function openBook(page) {
  await page.goto('./learn.html?module=foldrajzi-felfedezesek');
  await expect(page.locator('#h5p-container')).toHaveAttribute('data-state', 'ready', { timeout: 45_000 });
  return page.frameLocator('iframe.h5p-iframe');
}

async function openChapter(book, title) {
  const button = book.getByRole('button', { name: new RegExp(title, 'i') });
  await expect(button).toHaveCount(1);
  await button.click();
  await expect(book.getByRole('heading', { name: title, exact: true }).first()).toBeVisible();
  await button.first().evaluate((_, delay) => new Promise((resolve) => setTimeout(resolve, delay)), 500);
}

test('@visual-desktop Sprint 4.1 asztali vizuális bizonyítékok és feladatállapotok', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'desktop-chromium', 'Az asztali képernyőképek csak a desktop projektben készülnek.');
  const book = await openBook(page);

  await expect(book.getByRole('img', { name: 'Stilizált atlanti térkép tengeri útvonalakkal és egy 15. századi karavellával.' })).toBeVisible();
  await page.screenshot({ path: `${screenshotDir}/01-cover-real-image-desktop.png`, fullPage: true });

  await openChapter(book, 'Portugál kezdeményezés');
  await expect(book.getByText('Portugália az Atlanti-óceán partján feküdt', { exact: false })).toBeVisible();
  await page.screenshot({ path: `${screenshotDir}/02-clean-student-text.png`, fullPage: true });

  await openChapter(book, 'Miért indultak útnak?');
  const feedback = book.getByText('Helyes. A közvetlen út csökkenthette a közvetítők szerepét, és nagyobb hasznot ígért.', { exact: true });
  await expect(feedback).toBeHidden();
  await page.screenshot({ path: `${screenshotDir}/03-task-before-check.png`, fullPage: true });
  const correct = book.getByRole('radio', { name: /Közvetlenebb és jövedelmezőbb kapcsolatot kerestek/ });
  await expect(correct).toHaveCount(1);
  await correct.check();
  const check = book.locator('.h5p-question-check-answer:visible');
  await expect(check).toHaveCount(1);
  await check.click();
  await expect(feedback).toBeVisible();
  await page.screenshot({ path: `${screenshotDir}/04-task-after-check.png`, fullPage: true });

  await openChapter(book, 'A tordesillasi megállapodás');
  await expect(book.getByRole('img', { name: /Diego Ribero 1529-es világtérképe/i })).toBeVisible();
  await page.screenshot({ path: `${screenshotDir}/05-tordesillas-page.png`, fullPage: true });

  await openChapter(book, 'Borító és motiváció');
  await page.screenshot({ path: `${screenshotDir}/07-table-of-contents.png`, fullPage: true });

  await openChapter(book, 'Záróteszt, 20 pont');
  await expect(book.getByText('Válaszolj a kérdésekre, majd ellenőrizd a megoldást!', { exact: true })).toBeVisible();
  await page.locator('#h5p-container').screenshot({ path: `${screenshotDir}/08-final-test.png` });
});

test('@visual-mobile Sprint 4.1 mobil képernyőkép 390×844 méretben', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'mobile-chromium', 'A mobil képernyőkép csak a mobilprojektben készül.');
  const book = await openBook(page);
  await expect(book.getByRole('img', { name: 'Stilizált atlanti térkép tengeri útvonalakkal és egy 15. századi karavellával.' })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1)).toBe(false);
  await page.screenshot({ path: `${screenshotDir}/06-mobile-390x844.png`, fullPage: true });
});
