(async function () {
  'use strict';

  const container = document.getElementById('h5p-container');
  const loading = document.getElementById('loading-state');
  const error = document.getElementById('error-state');
  const retry = document.getElementById('retry-load');
  const progress = document.querySelector('[data-course-progress]');
  const progressLabel = document.querySelector('[data-progress-label]');
  let course;
  let retryCount = 0;
  let frameObserver;
  let syncTimer;

  const setText = (selector, value) => document.querySelectorAll(selector).forEach((node) => { node.textContent = value; });
  const loadConfig = async () => {
    const response = await fetch('./data/modules.json', { cache: 'no-store' });
    if (!response.ok) throw new Error(`A modulkonfiguráció nem tölthető be (${response.status}).`);
    return response.json();
  };

  const readStoredProgress = () => {
    try {
      const value = JSON.parse(localStorage.getItem(course.progressKey) || '{}');
      return Number.isInteger(value.chapter) ? value : { chapter: 1, completed: false };
    } catch {
      return { chapter: 1, completed: false };
    }
  };

  const setChapterProgress = (chapter, completed = false) => {
    const safeChapter = Math.max(1, Math.min(course.pages, Number(chapter) || 1));
    const percent = completed ? 100 : Math.round((safeChapter / course.pages) * 1000) / 10;
    if (progress) {
      progress.style.width = `${percent}%`;
      progress.parentElement?.setAttribute('aria-valuenow', String(Math.round(percent)));
    }
    if (progressLabel) progressLabel.textContent = completed ? 'Tananyag teljesítve' : `${safeChapter} / ${course.pages} oldal`;
    localStorage.setItem(course.progressKey, JSON.stringify({ chapter: safeChapter, completed, updatedAt: new Date().toISOString() }));
  };

  const configureFrame = (config) => {
    const era = config.taxonomy.find((item) => item.id === course.era)?.label || course.era;
    const level = course.levels.map((id) => config.levels.find((item) => item.id === id)?.label || id).join(' + ');
    const available = config.modules.filter((item) => item.status === 'available');
    const position = available.findIndex((item) => item.slug === course.slug) + 1;
    const nextCourse = config.modules.find((item) => item.slug === course.next);
    document.title = `${course.title} · Digitális Történelem Érettségi Akadémia`;
    document.querySelector('meta[name="description"]')?.setAttribute('content', `${course.title} interaktív H5P-tananyaga.`);
    setText('[data-module-title]', course.title);
    setText('[data-module-era]', `${era} · ${String(course.sequence).padStart(2, '0')}`);
    setText('[data-module-description]', course.description);
    setText('[data-module-duration]', course.duration);
    setText('[data-module-difficulty]', course.difficulty);
    setText('[data-module-level]', level);
    setText('[data-module-pages]', `${course.pages} oldal`);
    setText('[data-module-loading]', `A ${course.pages} oldalas interaktív könyv betöltése folyamatban…`);
    setText('[data-module-position]', `${String(position).padStart(2, '0')} / ${available.length}`);
    setText('[data-module-status]', 'Elérhető modul');
    const objectiveList = document.querySelector('[data-module-objectives]');
    if (objectiveList) objectiveList.replaceChildren(...course.objectives.map((item) => Object.assign(document.createElement('li'), { textContent: item })));
    container.setAttribute('aria-label', `${course.title} interaktív tananyag`);
    const next = document.querySelector('[data-next-module]');
    if (next && nextCourse) {
      next.href = `./learn.html?module=${nextCourse.slug}`;
      next.querySelector('strong').textContent = nextCourse.title;
    }
    setChapterProgress(readStoredProgress().chapter, readStoredProgress().completed);
  };

  const chapterFromFrame = (frameDocument) => {
    const current = frameDocument.querySelector('[aria-current="page"], .h5p-interactive-book-navigation-current');
    const candidates = [current?.textContent, frameDocument.body?.innerText];
    for (const value of candidates) {
      const match = String(value || '').match(new RegExp(`(?:^|\\s)(\\d{1,3})\\s*\\/\\s*${course.pages}(?:\\s|$)`));
      if (match) return Number(match[1]);
    }
    return null;
  };

  const syncProgressFromFrame = (frameDocument) => {
    clearTimeout(syncTimer);
    syncTimer = setTimeout(() => {
      const chapter = chapterFromFrame(frameDocument);
      if (chapter) setChapterProgress(chapter);
    }, 80);
  };

  const handleStatement = (statement, frameDocument) => {
    const verb = statement?.verb?.id || statement?.verb || '';
    if (typeof verb === 'string' && (verb.includes('completed') || verb.includes('passed'))) {
      setChapterProgress(course.pages, true);
      return;
    }
    if (frameDocument) syncProgressFromFrame(frameDocument);
  };

  const attachProgressTracking = async () => {
    const iframe = container.querySelector('iframe.h5p-iframe, iframe');
    if (!iframe) return;
    const attach = () => {
      try {
        const frameWindow = iframe.contentWindow;
        const frameDocument = iframe.contentDocument;
        if (!frameDocument?.body) return;
        frameObserver?.disconnect();
        frameObserver = new MutationObserver(() => syncProgressFromFrame(frameDocument));
        frameObserver.observe(frameDocument.body, { subtree: true, childList: true, attributes: true, characterData: true });
        frameDocument.addEventListener('click', () => syncProgressFromFrame(frameDocument), true);
        frameWindow?.H5P?.externalDispatcher?.on?.('xAPI', (event) => handleStatement(event?.data?.statement || event?.data, frameDocument));
        syncProgressFromFrame(frameDocument);
      } catch (reason) {
        console.warn('A fejezetszintű haladásfigyelés nem csatlakozott:', reason);
      }
    };
    iframe.addEventListener('load', attach, { once: true });
    attach();
  };

  const showError = (reason) => {
    console.error('H5P betöltési hiba:', reason);
    loading.hidden = true;
    container.replaceChildren();
    error.hidden = false;
    container.dataset.state = 'error';
    retry.textContent = retryCount ? 'Oldal teljes újratöltése' : 'Runtime újratöltése';
  };

  const reloadRuntime = () => new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = `./player/main.bundle.js?retry=${Date.now()}`;
    script.charset = 'UTF-8';
    script.onload = resolve;
    script.onerror = () => reject(new Error('A H5P runtime ismételt letöltése sikertelen.'));
    document.head.append(script);
  });

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
      await attachProgressTracking();
    } catch (reason) {
      showError(reason);
    }
  };

  retry.addEventListener('click', async () => {
    if (retryCount > 0) {
      window.location.reload();
      return;
    }
    retryCount += 1;
    retry.disabled = true;
    retry.textContent = 'Runtime újratöltése…';
    try {
      await reloadRuntime();
      await loadContent();
    } catch (reason) {
      showError(reason);
    } finally {
      retry.disabled = false;
    }
  });

  window.addEventListener('message', (event) => {
    if (!event.data || typeof event.data !== 'object') return;
    const iframe = container.querySelector('iframe.h5p-iframe, iframe');
    handleStatement(event.data.statement || event.data, iframe?.contentDocument);
  });

  try {
    const config = await loadConfig();
    const requested = new URLSearchParams(window.location.search).get('module') || 'atheni-demokracia';
    course = config.modules.find((item) => item.slug === requested && item.status === 'available')
      || config.modules.find((item) => item.slug === 'atheni-demokracia');
    configureFrame(config);
    await loadContent();
  } catch (reason) {
    showError(reason);
  }
})();
