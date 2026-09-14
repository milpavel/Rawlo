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

  // V9: rebuilt 17-screen carousel. Every screenshot has an explicit numbered control.
  const gallery = document.getElementById('app-screens');
  if (gallery) {
    const shell = gallery.closest('.preview-shell');
    const prev = shell?.querySelector('.preview-prev');
    const next = shell?.querySelector('.preview-next');
    const count = shell?.querySelector('.preview-count');
    const figures = Array.from(gallery.querySelectorAll(':scope > figure'));
    const total = figures.length;

    figures.forEach((figure, i) => {
      figure.dataset.slide = `SCREEN ${String(i + 1).padStart(2, '0')}`;
      figure.dataset.index = String(i);
    });

    // Visible, numbered access to all 17 screenshots. This is deliberately explicit,
    // so there can be no ambiguity that the gallery contains more than the first four.
    const jump = document.createElement('div');
    jump.className = 'gallery-jump';
    jump.setAttribute('aria-label', `Choose one of ${total} screenshots`);
    const jumpButtons = figures.map((_, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = String(i + 1).padStart(2, '0');
      b.setAttribute('aria-label', `Show screenshot ${i + 1} of ${total}`);
      b.addEventListener('click', () => goTo(i));
      jump.appendChild(b);
      return b;
    });
    shell?.appendChild(jump);

    const progress = document.createElement('div');
    progress.className = 'gallery-progress';
    progress.setAttribute('aria-hidden', 'true');
    progress.innerHTML = '<span></span>';
    shell?.appendChild(progress);
    const progressBar = progress.firstElementChild;

    let activeIndex = 0;
    let raf = 0;

    function slideLeft(i) {
      const f = figures[i];
      if (!f) return 0;
      return f.offsetLeft - gallery.offsetLeft;
    }

    function goTo(i, behavior = 'smooth') {
      const target = Math.max(0, Math.min(total - 1, i));
      gallery.scrollTo({ left: slideLeft(target), behavior });
      activeIndex = target;
      renderState();
    }

    function nearestIndex() {
      const x = gallery.scrollLeft;
      let best = 0;
      let bestDistance = Infinity;
      figures.forEach((f, i) => {
        const d = Math.abs(slideLeft(i) - x);
        if (d < bestDistance) { best = i; bestDistance = d; }
      });
      return best;
    }

    function visibleCount() {
      if (!figures[0]) return 1;
      const w = figures[0].getBoundingClientRect().width;
      const style = getComputedStyle(gallery);
      const gap = parseFloat(style.columnGap || style.gap || '18') || 18;
      return Math.max(1, Math.floor((gallery.clientWidth + gap) / (w + gap)));
    }

    function renderState() {
      const visible = visibleCount();
      const last = Math.min(total, activeIndex + visible);
      if (count) count.innerHTML = `<b>${activeIndex + 1}–${last}</b> of ${total} screens`;
      if (prev) prev.disabled = activeIndex <= 0;
      if (next) next.disabled = activeIndex >= total - 1;
      jumpButtons.forEach((b, i) => b.classList.toggle('is-active', i === activeIndex));
      jumpButtons[activeIndex]?.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      if (progressBar) progressBar.style.width = `${((activeIndex + 1) / total) * 100}%`;
    }

    prev?.addEventListener('click', () => goTo(activeIndex - 1));
    next?.addEventListener('click', () => goTo(activeIndex + 1));

    gallery.addEventListener('scroll', () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        activeIndex = nearestIndex();
        renderState();
      });
    }, { passive: true });

    gallery.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(activeIndex - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); goTo(activeIndex + 1); }
      if (e.key === 'Home') { e.preventDefault(); goTo(0); }
      if (e.key === 'End') { e.preventDefault(); goTo(total - 1); }
    });

    let drag = null;
    gallery.addEventListener('pointerdown', (e) => {
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      drag = { x: e.clientX, left: gallery.scrollLeft, moved: false, pointerId: e.pointerId };
      gallery.setPointerCapture?.(e.pointerId);
    });
    gallery.addEventListener('pointermove', (e) => {
      if (!drag) return;
      const dx = e.clientX - drag.x;
      if (Math.abs(dx) > 4) drag.moved = true;
      gallery.scrollLeft = drag.left - dx;
    });
    const finishDrag = () => {
      if (!drag) return;
      const i = nearestIndex();
      drag = null;
      goTo(i);
    };
    gallery.addEventListener('pointerup', finishDrag);
    gallery.addEventListener('pointercancel', finishDrag);

    window.addEventListener('resize', () => {
      goTo(activeIndex, 'auto');
    }, { passive: true });

    activeIndex = 0;
    renderState();
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
