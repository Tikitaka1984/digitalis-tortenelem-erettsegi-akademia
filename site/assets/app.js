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
  document.querySelectorAll('[data-theme-toggle]').forEach((button) => button.addEventListener('click', () => setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark')));

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

  const normalize = (value) => value.toLocaleLowerCase('hu-HU').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  const escapeHtml = (value) => String(value).replace(/[&<>'"]/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' })[character]);
  const labelFor = (items, id) => items.find((item) => item.id === id)?.label || id;

  let configPromise;
  const getConfig = () => {
    if (!configPromise) {
      configPromise = fetch('./data/modules.json', { cache: 'no-store' }).then((response) => {
        if (!response.ok) throw new Error('A tananyagjegyzék nem tölthető be.');
        return response.json();
      });
    }
    return configPromise;
  };

  const renderFeaturedModules = async () => {
    const host = document.querySelector('[data-featured-modules]');
    if (!host) return;
    const config = await getConfig();
    const available = config.modules.filter((module) => module.status === 'available');
    host.innerHTML = available.map((module) => {
      const era = labelFor(config.taxonomy, module.era);
      const levels = module.levels.map((id) => labelFor(config.levels, id)).join(' + ');
      const decoration = module.slug === 'atheni-demokracia' ? '<div class="greek-grid"></div>' : '<div class="route-lines"></div>';
      const discoveryClass = module.slug === 'foldrajzi-felfedezesek' ? 'course-art-discoveries' : '';
      return `<article class="featured-course reveal"><div class="course-art ${discoveryClass}" aria-hidden="true"><span class="course-era">${escapeHtml(module.period)}</span>${decoration}<strong>${escapeHtml(module.artLabel)}</strong></div><div class="course-body"><div class="card-meta"><span class="badge badge-live">Elérhető</span><span>${escapeHtml(era)}</span><span>${escapeHtml(levels)}</span></div><h3>${escapeHtml(module.title)}</h3><p>${escapeHtml(module.description)}</p><div class="course-facts"><span><b>${module.pages}</b> oldal</span><span><b>${escapeHtml(module.duration)}</b></span></div><a class="button button-primary" href="./learn.html?module=${escapeHtml(module.slug)}">Tananyag indítása <span aria-hidden="true">→</span></a></div></article>`;
    }).join('');
  };

  const renderLibrary = async () => {
    const grid = document.querySelector('[data-library-grid]');
    if (!grid) return;
    const config = await getConfig();
    grid.innerHTML = config.modules.map((module) => {
      const available = module.status === 'available';
      const era = labelFor(config.taxonomy, module.era);
      const levels = module.levels.map((id) => labelFor(config.levels, id)).join(' + ');
      const tags = [module.era, ...(module.tags || [])].join(' ');
      const link = available ? `<a class="lesson-card-link" href="./learn.html?module=${escapeHtml(module.slug)}" aria-label="${escapeHtml(module.title)} tananyag megnyitása"><span class="sr-only">Tananyag megnyitása</span></a>` : '';
      const stats = available
        ? `<span>${module.pages} oldal</span><span>${escapeHtml(module.duration)}</span><span>${escapeHtml(levels)}</span>`
        : '<span>Tervezés alatt</span>';
      return `<article class="lesson-card ${available ? 'lesson-card-live' : 'is-coming'}" data-library-item data-era="${escapeHtml(tags)}" data-level="${escapeHtml(module.levels.join(' '))}" data-search="${escapeHtml(`${module.title} ${era} ${module.searchTerms}`)}">${link}<div class="lesson-art ${escapeHtml(module.artClass)}"><span class="badge ${available ? 'badge-live' : ''}">${available ? 'Elérhető' : 'Hamarosan'}</span><strong>${escapeHtml(module.artLabel)}</strong><small>${escapeHtml(module.period)}</small></div><div class="lesson-card-body"><div class="card-meta"><span>${escapeHtml(era)}</span><span>${String(module.sequence).padStart(2, '0')}</span></div><h3>${escapeHtml(module.title)}</h3><p>${escapeHtml(module.shortDescription)}</p><div class="lesson-stats">${stats}</div>${available ? '<div class="lesson-card-action">Tananyag indítása <span aria-hidden="true">→</span></div>' : ''}</div></article>`;
    }).join('');

    const availableCount = config.modules.filter((module) => module.status === 'available').length;
    document.querySelector('[data-library-total]')?.replaceChildren(document.createTextNode(String(availableCount)));
    const params = new URLSearchParams(window.location.search);
    const validEras = new Set(config.taxonomy.map((item) => item.id));
    const validLevels = new Set(config.levels.map((item) => item.id));
    const state = {
      era: validEras.has(params.get('era')) ? params.get('era') : 'all',
      level: validLevels.has(params.get('level')) ? params.get('level') : 'all'
    };
    const search = document.querySelector('[data-library-search]');
    const items = [...document.querySelectorAll('[data-library-item]')];
    const emptyState = document.querySelector('[data-empty-state]');
    const resultCount = document.querySelector('[data-result-count]');

    const renderFilterButtons = (target, values, kind, allLabel) => {
      const host = document.querySelector(target);
      if (!host) return;
      const entries = [{ id: 'all', label: allLabel }, ...values];
      host.replaceChildren(...entries.map((entry) => {
        const button = document.createElement('button');
        button.className = 'chip';
        button.type = 'button';
        button.dataset.filterKind = kind;
        button.dataset.filterValue = entry.id;
        button.textContent = entry.label;
        return button;
      }));
    };
    renderFilterButtons('[data-era-filters]', config.taxonomy, 'era', 'Összes korszak');
    renderFilterButtons('[data-level-filters]', config.levels, 'level', 'Minden szint');
    const filterButtons = [...document.querySelectorAll('[data-filter-kind]')];

    const updateUrl = () => {
      const next = new URL(window.location.href);
      for (const kind of ['era', 'level']) state[kind] === 'all' ? next.searchParams.delete(kind) : next.searchParams.set(kind, state[kind]);
      window.history.replaceState({}, '', `${next.pathname}${next.search}${next.hash}`);
    };
    const syncButtons = () => filterButtons.forEach((button) => {
      const selected = state[button.dataset.filterKind] === button.dataset.filterValue;
      button.classList.toggle('is-selected', selected);
      button.setAttribute('aria-pressed', String(selected));
    });
    const updateLibrary = () => {
      const query = normalize(search?.value.trim() || '');
      let visible = 0;
      items.forEach((item) => {
        const eraMatch = state.era === 'all' || item.dataset.era.split(' ').includes(state.era);
        const levelMatch = state.level === 'all' || item.dataset.level.split(' ').includes(state.level);
        const queryMatch = !query || normalize(item.dataset.search || '').includes(query);
        item.hidden = !(eraMatch && levelMatch && queryMatch);
        if (!item.hidden) visible += 1;
      });
      if (emptyState) emptyState.hidden = visible !== 0;
      if (resultCount) resultCount.textContent = `${visible} találat`;
      syncButtons();
    };
    search?.addEventListener('input', updateLibrary);
    filterButtons.forEach((button) => button.addEventListener('click', () => {
      state[button.dataset.filterKind] = button.dataset.filterValue;
      updateUrl();
      updateLibrary();
    }));
    document.querySelector('[data-clear-filters]')?.addEventListener('click', () => {
      state.era = 'all';
      state.level = 'all';
      if (search) search.value = '';
      updateUrl();
      updateLibrary();
      search?.focus();
    });
    updateLibrary();
  };
  renderLibrary().catch((reason) => {
    console.error(reason);
    const emptyState = document.querySelector('[data-empty-state]');
    if (emptyState) {
      emptyState.hidden = false;
      emptyState.querySelector('h3').textContent = 'A tananyagjegyzék nem tölthető be';
      emptyState.querySelector('p').textContent = 'Frissítsd az oldalt, majd próbáld újra.';
    }
  });
  renderFeaturedModules().catch((reason) => console.error(reason));

  document.querySelector('[data-focus-toggle]')?.addEventListener('click', (event) => {
    const active = document.body.classList.toggle('is-focus-mode');
    event.currentTarget.setAttribute('aria-pressed', String(active));
    event.currentTarget.setAttribute('aria-label', active ? 'Fókusz mód kikapcsolása' : 'Fókusz mód bekapcsolása');
  });
  document.querySelector('[data-scroll-top]')?.addEventListener('click', () => document.getElementById('h5p-container')?.scrollIntoView({ behavior: 'smooth', block: 'start' }));
})();
