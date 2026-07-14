(function () {
  'use strict';

  const modules = {
    'atheni-demokracia': {
      id: 'atheni-demokracia-v2', title: 'Athéni demokrácia', era: 'Ókor · 01',
      description: 'Az athéni államszervezet és működése a demokrácia virágkorában',
      duration: '35–45 perc', difficulty: 'Közepes', level: 'Közép + emelt', pages: 30,
      path: './h5p/atheni-demokracia', progressKey: 'academy-athens-progress', position: '01 / 50+',
      status: 'Első pilot modul',
      objectives: ['A demokrácia kialakulásának áttekintése', 'A reformerek szerepének elkülönítése', 'Az államszervezet működésének megértése', 'Érettségi feladatok gyakorlása'],
      next: { slug: 'foldrajzi-felfedezesek', title: 'Földrajzi felfedezések' }
    },
    'foldrajzi-felfedezesek': {
      id: 'foldrajzi-felfedezesek-v1', title: 'Földrajzi felfedezések', era: 'Kora újkor · 02',
      description: 'Új tengeri utak, gyarmatosítás és a korai kapitalizmus kialakulása',
      duration: '82–117 perc', difficulty: 'Közepes', level: 'Középszint', pages: 30,
      path: './h5p/foldrajzi-felfedezesek', progressKey: 'academy-discoveries-progress', position: '02 / 50+',
      status: 'Második interaktív modul',
      objectives: ['A felfedezőutak okainak és feltételeinek megértése', 'A fő útvonalak és személyek elkülönítése', 'A gyarmatosítás következményeinek elemzése', 'A gazdasági átalakulás összefüggéseinek felismerése'],
      next: { slug: 'atheni-demokracia', title: 'Athéni demokrácia' }
    }
  };

  const requested = new URLSearchParams(window.location.search).get('module') || 'atheni-demokracia';
  const course = modules[requested] || modules['atheni-demokracia'];
  const container = document.getElementById('h5p-container');
  const loading = document.getElementById('loading-state');
  const error = document.getElementById('error-state');
  const retry = document.getElementById('retry-load');
  const progress = document.querySelector('[data-course-progress]');
  const progressLabel = document.querySelector('[data-progress-label]');

  const setText = (selector, value) => document.querySelectorAll(selector).forEach((node) => { node.textContent = value; });
  const configureFrame = () => {
    document.title = `${course.title} · Digitális Történelem Érettségi Akadémia`;
    document.querySelector('meta[name="description"]')?.setAttribute('content', `${course.title} interaktív H5P-tananyaga.`);
    setText('[data-module-title]', course.title);
    setText('[data-module-era]', course.era);
    setText('[data-module-description]', course.description);
    setText('[data-module-duration]', course.duration);
    setText('[data-module-difficulty]', course.difficulty);
    setText('[data-module-level]', course.level);
    setText('[data-module-pages]', `${course.pages} oldal`);
    setText('[data-module-loading]', `A ${course.pages} oldalas interaktív könyv betöltése folyamatban…`);
    setText('[data-module-position]', course.position);
    setText('[data-module-status]', course.status);
    const objectiveList = document.querySelector('[data-module-objectives]');
    if (objectiveList) objectiveList.replaceChildren(...course.objectives.map((item) => Object.assign(document.createElement('li'), { textContent: item })));
    container.setAttribute('aria-label', `${course.title} interaktív tananyag`);
    const next = document.querySelector('[data-next-module]');
    if (next) {
      next.href = `./learn.html?module=${course.next.slug}`;
      next.querySelector('strong').textContent = course.next.title;
    }
  };

  const setProgress = (value, label) => {
    const safeValue = Math.max(0, Math.min(100, Number(value) || 0));
    if (progress) progress.style.width = `${safeValue}%`;
    if (progressLabel) progressLabel.textContent = label || `${safeValue}% teljesítve`;
    localStorage.setItem(course.progressKey, String(safeValue));
  };

  const showError = (reason) => {
    console.error('H5P betöltési hiba:', reason);
    loading.hidden = true;
    container.replaceChildren();
    error.hidden = false;
    container.dataset.state = 'error';
  };

  const loadContent = async () => {
    loading.hidden = false;
    error.hidden = true;
    container.replaceChildren();
    container.dataset.state = 'loading';
    if (!window.H5PStandalone || typeof window.H5PStandalone.H5P !== 'function') {
      showError(new Error('A H5P runtime nem érhető el.'));
      return;
    }
    try {
      await new window.H5PStandalone.H5P(container, {
        id: course.id,
        h5pJsonPath: course.path,
        contentJsonPath: `${course.path}/content`,
        librariesPath: course.path,
        frameJs: './player/frame.bundle.js',
        frameCss: './player/styles/h5p.css',
        frame: true, copyright: true, export: false, icon: false, fullScreen: true, reportingIsEnabled: true
      });
      loading.hidden = true;
      container.dataset.state = 'ready';
      container.focus({ preventScroll: true });
      const storedProgress = Number(localStorage.getItem(course.progressKey));
      setProgress(storedProgress > 0 ? storedProgress : 3, storedProgress > 0 ? `${storedProgress}% teljesítve` : 'Tananyag megnyitva');
    } catch (reason) {
      showError(reason);
    }
  };

  retry.addEventListener('click', loadContent);
  window.addEventListener('message', (event) => {
    if (!event.data || typeof event.data !== 'object') return;
    const statement = event.data.statement || event.data;
    const verb = statement?.verb?.id || statement?.verb || '';
    if (typeof verb !== 'string') return;
    if (verb.includes('completed') || verb.includes('passed')) setProgress(100, 'Tananyag teljesítve');
    else if (verb.includes('answered') || verb.includes('progressed')) {
      const current = Number(localStorage.getItem(course.progressKey)) || 3;
      setProgress(Math.min(95, current + 3));
    }
  });

  configureFrame();
  loadContent();
})();
