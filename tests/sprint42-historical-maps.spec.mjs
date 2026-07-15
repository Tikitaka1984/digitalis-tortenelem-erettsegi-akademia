import { expect, test } from '@playwright/test';

const phase = process.env.DTEA_SCREENSHOT_PHASE;
const chapters = [
  ['07-bartolomeu-dias', 6, 'Bartolomeu Dias útja'],
  ['08-vasco-da-gama', 7, 'Vasco da Gama útja'],
  ['09-kolumbusz', 8, 'Kolumbusz és 1492'],
  ['10-tordesillas', 9, 'A tordesillasi megállapodás'],
  ['11-magellan', 10, 'Magellán expedíciója'],
  ['24-utvonalak', 23, 'Térkép és topográfia'],
];

async function openBook(page) {
  await page.goto('./learn.html?module=foldrajzi-felfedezesek');
  await expect(page.locator('#h5p-container')).toHaveAttribute('data-state', 'ready', { timeout: 45_000 });
  return page.frameLocator('iframe.h5p-iframe');
}

async function openChapter(book, index, title) {
  const button = book.locator('.h5p-interactive-book-navigation-chapter-button').nth(index);
  await expect(button).toHaveCount(1);
  await button.evaluate((element) => element.click());
  await expect(book.getByRole('heading', { name: title, exact: true }).first()).toBeVisible();
  await button.evaluate((_, delay) => new Promise((resolve) => setTimeout(resolve, delay)), 350);
}

test('Sprint 4.2 hiteles térképek vizuális bizonyítékai', async ({ page }, testInfo) => {
  test.skip(!phase, 'A képernyőképek csak a DTEA_SCREENSHOT_PHASE környezeti változóval készülnek.');

  const book = await openBook(page);
  for (const [filename, index, title] of chapters) {
    await openChapter(book, index, title);
    await page.screenshot({
      path: `docs/screenshots/sprint-4-2/${phase}/${testInfo.project.name}/${filename}.png`,
      fullPage: true,
    });
  }
});
