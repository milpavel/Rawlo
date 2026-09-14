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


  // V10: rebuilt carousel - all 17 screenshots are in one track, 4 visible on desktop.
  const gallery = document.getElementById('app-screens');
  if (gallery) {
    const shell = gallery.closest('.preview-shell');
    shell?.classList.add('v10-gallery');

    // Build an isolated viewport so the track can translate independently.
    if (!gallery.parentElement?.classList.contains('preview-viewport')) {
      const viewport = document.createElement('div');
      viewport.className = 'preview-viewport';
      gallery.parentNode.insertBefore(viewport, gallery);
      viewport.appendChild(gallery);
    }
    const viewport = gallery.parentElement;
    const figures = [...gallery.querySelectorAll('figure')];
    const controls = shell?.querySelector('.preview-controls');
    const prev = shell?.querySelector('.preview-prev');
    const next = shell?.querySelector('.preview-next');
    const count = shell?.querySelector('.preview-count');

    // Keep arrows grouped on the right.
    if (controls && prev && next && !controls.querySelector('.preview-buttons')) {
      const buttons = document.createElement('div');
      buttons.className = 'preview-buttons';
      controls.appendChild(buttons);
      buttons.append(prev, next);
    }

    // 17 explicit numbered controls: a visible proof that every supplied screen is present.
    let thumbs = shell?.querySelector('.preview-thumbs');
    if (!thumbs) {
      thumbs = document.createElement('div');
      thumbs.className = 'preview-thumbs';
      thumbs.setAttribute('aria-label', 'All 17 RAWLO screenshots');
      figures.forEach((_, i) => {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'preview-thumb';
        b.textContent = String(i + 1).padStart(2, '0');
        b.dataset.galleryIndex = String(i);
        b.setAttribute('aria-label', `Show screenshot ${i + 1} of ${figures.length}`);
        thumbs.appendChild(b);
      });
      viewport.insertAdjacentElement('afterend', thumbs);
    }
    const thumbButtons = [...thumbs.querySelectorAll('.preview-thumb')];

    let index = 0;
    const gap = () => parseFloat(getComputedStyle(gallery).gap || '18') || 18;
    const cardWidth = () => figures[0]?.getBoundingClientRect().width || 300;
    const visible = () => {
      const w = viewport?.clientWidth || 1;
      return Math.max(1, Math.min(figures.length, Math.floor((w + gap()) / (cardWidth() + gap()))));
    };
    const maxIndex = () => Math.max(0, figures.length - visible());
    const clamp = n => Math.max(0, Math.min(maxIndex(), n));

    function update() {
      index = clamp(index);
      const x = index * (cardWidth() + gap());
      gallery.style.transform = `translate3d(${-x}px,0,0)`;
      const last = Math.min(figures.length, index + visible());
      if (count) count.innerHTML = `<strong>${figures.length}</strong> screenshots <span>· showing ${index + 1}–${last}</span>`;
      if (prev) prev.disabled = index === 0;
      if (next) next.disabled = index >= maxIndex();
      thumbButtons.forEach((b, i) => b.classList.toggle('active', i >= index && i < last));
      thumbButtons[index]?.scrollIntoView?.({block:'nearest', inline:'nearest', behavior:'smooth'});
    }
    function goTo(n) { index = clamp(n); update(); }
    function page(dir) { goTo(index + dir * Math.max(1, visible() - 1)); }

    thumbButtons.forEach((button, i) => {
      const target = Number.parseInt(button.dataset.galleryIndex ?? String(i), 10);
      button.addEventListener('click', () => goTo(Number.isFinite(target) ? target : i));
    });
    prev?.addEventListener('click', () => page(-1));
    next?.addEventListener('click', () => page(1));
    gallery.addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(index - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); goTo(index + 1); }
    });

    let drag = null;
    gallery.addEventListener('pointerdown', e => {
      drag = {x:e.clientX, index};
      gallery.style.transition = 'none';
      gallery.setPointerCapture?.(e.pointerId);
    });
    gallery.addEventListener('pointermove', e => {
      if (!drag) return;
      const base = drag.index * (cardWidth()+gap());
      gallery.style.transform = `translate3d(${-(base - (e.clientX-drag.x))}px,0,0)`;
    });
    const finishDrag = e => {
      if (!drag) return;
      const dx = e.clientX - drag.x;
      gallery.style.transition = '';
      if (Math.abs(dx) > 45) index = clamp(drag.index + (dx < 0 ? 1 : -1));
      else index = drag.index;
      drag = null;
      update();
    };
    gallery.addEventListener('pointerup', finishDrag);
    gallery.addEventListener('pointercancel', () => { drag=null; gallery.style.transition=''; update(); });
    window.addEventListener('resize', update, {passive:true});
    requestAnimationFrame(update);
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
