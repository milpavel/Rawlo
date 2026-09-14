(() => {
  // Keep clean page loads at the top. Anchored URLs (#preview, #features, ...) keep native anchor behavior.
  if (!location.hash) {
    try { if ('scrollRestoration' in history) history.scrollRestoration = 'manual'; } catch (_) {}
    window.scrollTo({ top: 0, left: 0, behavior: 'auto' });
    window.addEventListener('pageshow', () => {
      if (!location.hash) window.scrollTo({ top: 0, left: 0, behavior: 'auto' });
    }, { once: true });
  }

  const picker = document.querySelector('[data-locale-picker]');
  if (picker) {
    const trigger = picker.querySelector('.locale-trigger');
    const popover = picker.querySelector('.locale-popover');
    const search = picker.querySelector('.locale-search');
    const featuredSection = picker.querySelector('.locale-featured');
    const cards = [...picker.querySelectorAll('.locale-card')];
    const allCards = [...picker.querySelectorAll('.locale-grid .locale-card')];
    const empty = picker.querySelector('.locale-empty');
    const autoButton = picker.querySelector('[data-lang-auto]');
    const supported = cards.map(card => card.dataset.lang).filter((v, i, a) => a.indexOf(v) === i);

    const navigate = (code) => {
      if (!supported.includes(code)) return;
      try { localStorage.setItem('rawlo-lang', code); } catch (_) {}
      const target = code === 'en' ? '/' : `/${code}/`;
      location.href = target + location.hash;
    };

    const filterLocales = () => {
      const query = (search?.value || '').trim().toLocaleLowerCase();
      let visible = 0;
      featuredSection?.toggleAttribute('hidden', Boolean(query));
      allCards.forEach(card => {
        const match = !query || (card.dataset.search || '').includes(query);
        card.hidden = !match;
        if (match) visible += 1;
      });
      if (empty) empty.hidden = visible !== 0;
    };

    const openPicker = () => {
      if (!popover) return;
      popover.hidden = false;
      picker.classList.add('open');
      trigger?.setAttribute('aria-expanded', 'true');
      requestAnimationFrame(() => search?.focus({preventScroll:true}));
    };

    const closePicker = ({restoreFocus = false} = {}) => {
      if (!popover || popover.hidden) return;
      popover.hidden = true;
      picker.classList.remove('open');
      trigger?.setAttribute('aria-expanded', 'false');
      if (search) search.value = '';
      filterLocales();
      if (restoreFocus) trigger?.focus();
    };

    trigger?.addEventListener('click', (event) => {
      event.stopPropagation();
      popover?.hidden ? openPicker() : closePicker();
    });
    cards.forEach(card => card.addEventListener('click', () => navigate(card.dataset.lang)));
    search?.addEventListener('input', filterLocales);
    search?.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') {
        const first = allCards.find(card => !card.hidden);
        if (first) navigate(first.dataset.lang);
      }
    });
    autoButton?.addEventListener('click', () => {
      try { localStorage.removeItem('rawlo-lang'); } catch (_) {}
      const browserLanguages = navigator.languages?.length ? navigator.languages : [navigator.language || 'en'];
      let chosen = 'en';
      for (const raw of browserLanguages) {
        const candidate = String(raw).toLowerCase().split('-')[0];
        if (supported.includes(candidate)) { chosen = candidate; break; }
      }
      navigate(chosen);
    });
    document.addEventListener('click', (event) => {
      if (!picker.contains(event.target)) closePicker();
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && !popover?.hidden) closePicker({restoreFocus:true});
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
      // Never use scrollIntoView here: it can vertically move the whole page to #preview on load.
      // Keep the active number visible by scrolling only the thumbnail strip horizontally.
      const activeThumb = thumbButtons[index];
      if (activeThumb && thumbs) {
        const thumbLeft = activeThumb.offsetLeft;
        const thumbRight = thumbLeft + activeThumb.offsetWidth;
        const viewLeft = thumbs.scrollLeft;
        const viewRight = viewLeft + thumbs.clientWidth;
        if (thumbLeft < viewLeft) {
          thumbs.scrollTo({ left: thumbLeft, behavior: 'smooth' });
        } else if (thumbRight > viewRight) {
          thumbs.scrollTo({ left: thumbRight - thumbs.clientWidth, behavior: 'smooth' });
        }
      }
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
