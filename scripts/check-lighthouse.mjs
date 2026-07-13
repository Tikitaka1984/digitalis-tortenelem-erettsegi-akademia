import { readFile } from "node:fs/promises";

const reportPath = process.argv[2] ?? "lighthouse-report.json";
const report = JSON.parse(await readFile(reportPath, "utf8"));

const thresholds = {
  performance: 0.95,
  accessibility: 0.95,
  "best-practices": 0.9,
  seo: 0.9,
};

let failed = false;
for (const [category, minimum] of Object.entries(thresholds)) {
  const score = report.categories?.[category]?.score;
  if (typeof score !== "number") {
    console.error(`Missing Lighthouse category: ${category}`);
    failed = true;
    continue;
  }

  const percent = Math.round(score * 100);
  console.log(`${category}: ${percent} (minimum ${Math.round(minimum * 100)})`);
  if (score < minimum) failed = true;
}

if (failed) process.exit(1);

