(function () {
  'use strict';

  const root = document.documentElement;
  const themeMeta = document.querySelector('meta[name="theme-color"]');
  const savedTheme = localStorage.getItem('academy-theme');
  const preferredDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

  const setTheme = (theme) => {
    root.dataset.theme = theme;
    root.style.colorScheme = theme;
    localStorage.setItem('academy-theme', theme);
    if (themeMeta) themeMeta.content = theme === 'dark' ? '#0d120f' : '#f7f5ef';
    document.querySelectorAll('[data-theme-toggle]').forEach((button) => {
      button.setAttribute('aria-label', theme === 'dark' ? 'Világos mód bekapcsolása' : 'Sötét mód bekapcsolása');
      button.setAttribute('aria-pressed', String(theme === 'dark'));
    });
  };

  setTheme(savedTheme || (preferredDark ? 'dark' : 'light'));
  document.querySelectorAll('[data-theme-toggle]').forEach((button) => {
    button.addEventListener('click', () => setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark'));
  });

  const header = document.querySelector('[data-header]');
  if (header) {
    const syncHeader = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
    syncHeader();
    window.addEventListener('scroll', syncHeader, { passive: true });
  }

  const menuToggle = document.querySelector('[data-menu-toggle]');
  const nav = document.querySelector('[data-nav]');
  if (menuToggle && nav) {
    menuToggle.addEventListener('click', () => {
      const open = nav.classList.toggle('is-open');
      menuToggle.setAttribute('aria-expanded', String(open));
      menuToggle.querySelector('[aria-hidden]')?.replaceChildren(document.createTextNode(open ? '×' : '☰'));
    });
    nav.addEventListener('click', (event) => {
      if (event.target.closest('a')) {
        nav.classList.remove('is-open');
        menuToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  const search = document.querySelector('[data-library-search]');
  const items = [...document.querySelectorAll('[data-library-item]')];
  const filters = [...document.querySelectorAll('[data-filter]')];
  const emptyState = document.querySelector('[data-empty-state]');
  const resultCount = document.querySelector('[data-result-count]');
  let activeFilter = 'all';

  const normalize = (value) => value.toLocaleLowerCase('hu-HU').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  const updateLibrary = () => {
    if (!items.length) return;
    const query = normalize(search?.value.trim() || '');
    let visible = 0;
    items.forEach((item) => {
      const eraMatch = activeFilter === 'all' || item.dataset.era.split(' ').includes(activeFilter);
      const queryMatch = !query || normalize(item.dataset.search || '').includes(query);
      item.hidden = !(eraMatch && queryMatch);
      if (!item.hidden) visible += 1;
    });
    if (emptyState) emptyState.hidden = visible !== 0;
    if (resultCount) resultCount.textContent = `${visible} találat`;
  };

  search?.addEventListener('input', updateLibrary);
  filters.forEach((button) => button.addEventListener('click', () => {
    activeFilter = button.dataset.filter;
    filters.forEach((item) => {
      const selected = item === button;
      item.classList.toggle('is-selected', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
    updateLibrary();
  }));
  document.querySelector('[data-clear-filters]')?.addEventListener('click', () => {
    activeFilter = 'all';
    if (search) search.value = '';
    filters.forEach((item) => {
      const selected = item.dataset.filter === 'all';
      item.classList.toggle('is-selected', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
    updateLibrary();
    search?.focus();
  });

  document.querySelector('[data-focus-toggle]')?.addEventListener('click', (event) => {
    const active = document.body.classList.toggle('is-focus-mode');
    event.currentTarget.setAttribute('aria-pressed', String(active));
    event.currentTarget.setAttribute('aria-label', active ? 'Fókusz mód kikapcsolása' : 'Fókusz mód bekapcsolása');
  });

  document.querySelector('[data-scroll-top]')?.addEventListener('click', () => {
    document.getElementById('h5p-container')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
})();

