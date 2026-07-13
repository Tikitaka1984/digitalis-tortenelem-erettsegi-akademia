(function () {
  'use strict';

  const container = document.getElementById('h5p-container');
  const loading = document.getElementById('loading-state');
  const error = document.getElementById('error-state');
  const retry = document.getElementById('retry-load');
  const progress = document.querySelector('[data-course-progress]');
  const progressLabel = document.querySelector('[data-progress-label]');
  const progressKey = 'academy-athens-progress';

  const setProgress = (value, label) => {
    const safeValue = Math.max(0, Math.min(100, Number(value) || 0));
    if (progress) progress.style.width = `${safeValue}%`;
    if (progressLabel) progressLabel.textContent = label || `${safeValue}% teljesítve`;
    localStorage.setItem(progressKey, String(safeValue));
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
        id: 'atheni-demokracia-v2',
        h5pJsonPath: './h5p/atheni-demokracia',
        contentJsonPath: './h5p/atheni-demokracia/content',
        librariesPath: './h5p/atheni-demokracia',
        frameJs: './player/frame.bundle.js',
        frameCss: './player/styles/h5p.css',
        frame: true,
        copyright: true,
        export: false,
        icon: false,
        fullScreen: true,
        reportingIsEnabled: true
      });
      loading.hidden = true;
      container.dataset.state = 'ready';
      container.focus({ preventScroll: true });
      const storedProgress = Number(localStorage.getItem(progressKey));
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
      const current = Number(localStorage.getItem(progressKey)) || 3;
      setProgress(Math.min(95, current + 3));
    }
  });
  loadContent();
})();

