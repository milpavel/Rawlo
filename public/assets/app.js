(() => {
  const select = document.getElementById('lang-select');
  if (select) {
    select.addEventListener('change', (e) => {
      const code = e.target.value;
      try { localStorage.setItem('rawlo-lang', code); } catch (_) {}
      const target = code === 'en' ? '/' : `/${code}/`;
      location.href = target + location.hash;
    });
  }

  const reveal = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.11, rootMargin: '0px 0px -35px' });
    reveal.forEach((el) => observer.observe(el));
  } else {
    reveal.forEach((el) => el.classList.add('is-visible'));
  }

  const header = document.querySelector('.site-header');
  const updateHeader = () => header?.classList.toggle('is-scrolled', window.scrollY > 24);
  updateHeader();
  addEventListener('scroll', updateHeader, { passive: true });

  const menu = document.querySelector('.menu-btn');
  menu?.addEventListener('click', () => {
    const open = header.classList.toggle('menu-open');
    menu.setAttribute('aria-expanded', String(open));
  });
  header?.querySelectorAll('nav a').forEach((a) => a.addEventListener('click', () => header.classList.remove('menu-open')));

  const scroller = document.getElementById('app-screens');
  const controls = [...document.querySelectorAll('[data-preview]')];
  if (scroller && controls.length) {
    const figures = [...scroller.querySelectorAll('figure')];
    controls.forEach((btn) => btn.addEventListener('click', () => {
      const idx = Number(btn.dataset.preview || 0);
      figures[idx]?.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }));
    const markActive = () => {
      const center = scroller.scrollLeft + scroller.clientWidth / 2;
      let active = 0, best = Infinity;
      figures.forEach((fig, i) => {
        const c = fig.offsetLeft + fig.offsetWidth / 2;
        const d = Math.abs(c - center);
        if (d < best) { best = d; active = i; }
      });
      controls.forEach((b, i) => b.classList.toggle('active', i === active));
    };
    scroller.addEventListener('scroll', markActive, { passive: true });
    markActive();
  }

  const links = [...document.querySelectorAll('.site-header nav a')];
  const sections = links.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  if ('IntersectionObserver' in window && sections.length) {
    const sectionObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach(a => a.classList.toggle('active', a.getAttribute('href') === `#${entry.target.id}`));
      });
    }, { rootMargin: '-30% 0px -62%', threshold: 0 });
    sections.forEach(s => sectionObserver.observe(s));
  }
})();
