import { readFile, stat } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(fileURLToPath(new URL('..', import.meta.url)));
const output = join(root, '_site');
const config = JSON.parse(await readFile(join(output, 'data', 'modules.json'), 'utf8'));
const modules = config.modules.filter((module) => module.status === 'available');
const requiredFiles = [
  'index.html', 'library.html', 'learn.html', '404.html', '.nojekyll', 'data/modules.json',
  'player/main.bundle.js', 'player/frame.bundle.js', 'player/styles/h5p.css',
  ...modules.flatMap((module) => [
    `h5p/${module.slug}/h5p.json`,
    `h5p/${module.slug}/content/content.json`
  ])
];

const failures = [];
for (const file of requiredFiles) {
  try {
    if (!(await stat(join(output, file))).isFile()) failures.push(`${file}: nem fájl`);
  } catch {
    failures.push(`${file}: hiányzik`);
  }
}

let declaredDependencies = 0;
let referencedAssets = 0;
const inspectPaths = (value, collector) => {
  if (Array.isArray(value)) return value.forEach((item) => inspectPaths(item, collector));
  if (!value || typeof value !== 'object') return;
  for (const [key, child] of Object.entries(value)) {
    if (key === 'path' && typeof child === 'string' && !/^https?:/i.test(child)) collector.push(child);
    else inspectPaths(child, collector);
  }
};

for (const module of modules) {
  const contentRoot = join(output, 'h5p', module.slug);
  const manifest = JSON.parse(await readFile(join(contentRoot, 'h5p.json'), 'utf8'));
  const content = JSON.parse(await readFile(join(contentRoot, 'content', 'content.json'), 'utf8'));
  if (manifest.mainLibrary !== 'H5P.InteractiveBook') failures.push(`${module.slug}: hibás mainLibrary.`);
  if (content.chapters?.length !== module.pages) failures.push(`${module.slug}: hibás oldalszám: ${content.chapters?.length ?? 'nincs'}.`);
  if (!JSON.stringify(content).includes(module.contentProbe)) failures.push(`${module.slug}: a várt tartalmi ellenőrzőszöveg nem található.`);
  if (manifest.license !== module.license) failures.push(`${module.slug}: hibás vagy hiányzó licencmetaadat.`);
  if (manifest.authors?.[0]?.name !== module.author) failures.push(`${module.slug}: hibás vagy hiányzó szerzőmetaadat.`);
  if (manifest.version !== module.version) failures.push(`${module.slug}: hibás vagy hiányzó verziómetaadat.`);

  for (const dependency of manifest.preloadedDependencies ?? []) {
    declaredDependencies += 1;
    const folder = `${dependency.machineName}-${dependency.majorVersion}.${dependency.minorVersion}`;
    try { await stat(join(contentRoot, folder, 'library.json')); }
    catch { failures.push(`${module.slug}: hiányzó runtime-függőség: ${folder}`); }
  }
  const assets = [];
  inspectPaths(content, assets);
  referencedAssets += new Set(assets).size;
  for (const asset of [...new Set(assets)]) {
    try { await stat(join(contentRoot, 'content', asset)); }
    catch { failures.push(`${module.slug}: hiányzó tartalmi asset: ${asset}`); }
  }
}

if (config.platformVersion !== '1.1.0') failures.push('A platformverzió nem 1.1.0.');
if (failures.length) {
  console.error(failures.map((failure) => `- ${failure}`).join('\n'));
  process.exit(1);
}
const pageCount = modules.reduce((sum, module) => sum + module.pages, 0);
console.log(`Build verified: ${modules.length} modules, ${pageCount} pages, ${declaredDependencies} declared dependencies, ${referencedAssets} referenced content assets.`);
