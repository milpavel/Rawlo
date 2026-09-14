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

  // V8: explicit 17-screen horizontal gallery. Show visible range, strong arrows and drag/swipe.
  const gallery = document.getElementById('app-screens');
  if (gallery) {
    const shell = gallery.closest('.preview-shell');
    const prev = shell?.querySelector('.preview-prev');
    const next = shell?.querySelector('.preview-next');
    const count = shell?.querySelector('.preview-count');
    const figures = [...gallery.querySelectorAll('figure')];
    const step = () => (figures[0]?.getBoundingClientRect().width || 300) + 18;
    const visibleSlots = () => Math.max(1, Math.floor((gallery.clientWidth + 18) / step()));
    const updateCount = () => {
      if (!figures.length) return;
      const first = Math.max(0, Math.min(figures.length - 1, Math.round(gallery.scrollLeft / step())));
      const last = Math.min(figures.length, first + visibleSlots());
      if (count) count.textContent = `${first + 1}–${last} / ${figures.length} SCREENSHOTS`;
      const atStart = gallery.scrollLeft <= 4;
      const atEnd = gallery.scrollLeft + gallery.clientWidth >= gallery.scrollWidth - 4;
      if (prev) prev.disabled = atStart;
      if (next) next.disabled = atEnd;
      shell?.classList.toggle('gallery-at-end', atEnd);
    };
    prev?.addEventListener('click', () => gallery.scrollBy({ left: -step() * Math.max(1, visibleSlots() - 1), behavior: 'smooth' }));
    next?.addEventListener('click', () => gallery.scrollBy({ left: step() * Math.max(1, visibleSlots() - 1), behavior: 'smooth' }));
    gallery.addEventListener('scroll', () => requestAnimationFrame(updateCount), { passive: true });
    gallery.addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft') gallery.scrollBy({ left: -step(), behavior: 'smooth' });
      if (e.key === 'ArrowRight') gallery.scrollBy({ left: step(), behavior: 'smooth' });
    });
    let drag = null;
    gallery.addEventListener('pointerdown', e => { drag = { x: e.clientX, left: gallery.scrollLeft }; gallery.setPointerCapture?.(e.pointerId); });
    gallery.addEventListener('pointermove', e => { if (drag) gallery.scrollLeft = drag.left - (e.clientX - drag.x); });
    gallery.addEventListener('pointerup', () => { drag = null; });
    gallery.addEventListener('pointercancel', () => { drag = null; });
    window.addEventListener('resize', updateCount, { passive: true });
    updateCount();
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
