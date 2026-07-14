import { readFile, readdir, stat } from 'node:fs/promises';
import { join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(fileURLToPath(new URL('..', import.meta.url)));
const output = join(root, '_site');
const modules = [
  { slug: 'atheni-demokracia', pages: 30, title: 'Ki döntött Athénban – és ki maradt kívül?' },
  { slug: 'foldrajzi-felfedezesek', pages: 30, title: 'Földrajzi felfedezések' }
];

const requiredFiles = [
  'index.html',
  'learn.html',
  '404.html',
  '.nojekyll',
  'player/main.bundle.js',
  'player/frame.bundle.js',
  'player/styles/h5p.css',
  'h5p/atheni-demokracia/h5p.json',
  'h5p/atheni-demokracia/content/content.json',
  'h5p/foldrajzi-felfedezesek/h5p.json',
  'h5p/foldrajzi-felfedezesek/content/content.json'
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
    if (key === 'path' && typeof child === 'string' && !/^https?:/i.test(child)) {
      collector.push(child);
    } else {
      inspectPaths(child, collector);
    }
  }
};
for (const module of modules) {
  const contentRoot = join(output, 'h5p', module.slug);
  const manifest = JSON.parse(await readFile(join(contentRoot, 'h5p.json'), 'utf8'));
  const content = JSON.parse(await readFile(join(contentRoot, 'content', 'content.json'), 'utf8'));
  if (manifest.mainLibrary !== 'H5P.InteractiveBook') failures.push(`${module.slug}: hibás mainLibrary.`);
  if (content.chapters?.length !== module.pages) failures.push(`${module.slug}: hibás oldalszám: ${content.chapters?.length ?? 'nincs'}.`);
  if (!JSON.stringify(content).includes(module.title)) failures.push(`${module.slug}: a várt cím/tartalom nem található.`);

  for (const dependency of manifest.preloadedDependencies ?? []) {
    declaredDependencies += 1;
    const folder = `${dependency.machineName}-${dependency.majorVersion}.${dependency.minorVersion}`;
    try {
      await stat(join(contentRoot, folder, 'library.json'));
    } catch {
      failures.push(`${module.slug}: hiányzó runtime-függőség: ${folder}`);
    }
  }

  const missingAssets = [];
  inspectPaths(content, missingAssets);
  referencedAssets += new Set(missingAssets).size;
  for (const asset of [...new Set(missingAssets)]) {
    try {
      await stat(join(contentRoot, 'content', asset));
    } catch {
      failures.push(`${module.slug}: hiányzó tartalmi asset: ${asset}`);
    }
  }
}

if (failures.length) {
  console.error(failures.map((failure) => `- ${failure}`).join('\n'));
  process.exit(1);
}

console.log(`Build verified: ${modules.length} modules, 60 pages, ${declaredDependencies} declared dependencies, ${referencedAssets} referenced content assets.`);
