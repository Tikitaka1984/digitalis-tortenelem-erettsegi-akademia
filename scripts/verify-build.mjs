import { readFile, readdir, stat } from 'node:fs/promises';
import { join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(fileURLToPath(new URL('..', import.meta.url)));
const output = join(root, '_site');
const contentRoot = join(output, 'h5p', 'atheni-demokracia');

const requiredFiles = [
  'index.html',
  'learn.html',
  '404.html',
  '.nojekyll',
  'player/main.bundle.js',
  'player/frame.bundle.js',
  'player/styles/h5p.css',
  'h5p/atheni-demokracia/h5p.json',
  'h5p/atheni-demokracia/content/content.json'
];

const failures = [];
for (const file of requiredFiles) {
  try {
    if (!(await stat(join(output, file))).isFile()) failures.push(`${file}: nem fájl`);
  } catch {
    failures.push(`${file}: hiányzik`);
  }
}

const manifest = JSON.parse(await readFile(join(contentRoot, 'h5p.json'), 'utf8'));
const content = JSON.parse(await readFile(join(contentRoot, 'content', 'content.json'), 'utf8'));
if (manifest.mainLibrary !== 'H5P.InteractiveBook') failures.push('Hibás mainLibrary.');
if (content.chapters?.length !== 30) failures.push(`Hibás oldalszám: ${content.chapters?.length ?? 'nincs'}.`);

for (const dependency of manifest.preloadedDependencies ?? []) {
  const folder = `${dependency.machineName}-${dependency.majorVersion}.${dependency.minorVersion}`;
  try {
    await stat(join(contentRoot, folder, 'library.json'));
  } catch {
    failures.push(`Hiányzó runtime-függőség: ${folder}`);
  }
}

const missingAssets = [];
const inspectPaths = (value) => {
  if (Array.isArray(value)) return value.forEach(inspectPaths);
  if (!value || typeof value !== 'object') return;
  for (const [key, child] of Object.entries(value)) {
    if (key === 'path' && typeof child === 'string' && !/^https?:/i.test(child)) {
      missingAssets.push(child);
    } else {
      inspectPaths(child);
    }
  }
};
inspectPaths(content);
for (const asset of [...new Set(missingAssets)]) {
  try {
    await stat(join(contentRoot, 'content', asset));
  } catch {
    failures.push(`Hiányzó tartalmi asset: ${asset}`);
  }
}

if (failures.length) {
  console.error(failures.map((failure) => `- ${failure}`).join('\n'));
  process.exit(1);
}

console.log(`Build verified: 30 pages, ${manifest.preloadedDependencies.length} declared dependencies, ${new Set(missingAssets).size} referenced content assets.`);
