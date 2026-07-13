(function () {
  'use strict';

  const container = document.getElementById('h5p-container');
  const loading = document.getElementById('loading-state');
  const error = document.getElementById('error-state');
  const retry = document.getElementById('retry-load');

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
    } catch (reason) {
      showError(reason);
    }
  };

  retry.addEventListener('click', loadContent);
  loadContent();
})();
