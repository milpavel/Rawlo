'use strict';
(() => {
  const payload = document.querySelector('#tour-data');
  if (!payload) return;
  const steps = JSON.parse(payload.textContent);
  const tabs = Array.from(document.querySelectorAll('[data-tour-index]'));
  const panel = document.querySelector('#tour-panel');
  const image = document.querySelector('.tour-phone img');
  const caption = document.querySelector('[data-tour-label]');
  const title = document.querySelector('[data-tour-title]');
  const body = document.querySelector('[data-tour-body]');
  const count = document.querySelector('[data-tour-count]');
  const link = document.querySelector('[data-tour-gallery]');
  function selectStep(index, focus = false) {
    if (!Number.isInteger(index) || index < 0 || index >= steps.length) return;
    const step = steps[index];
    tabs.forEach((tab, i) => { tab.setAttribute('aria-selected', String(i === index)); tab.tabIndex = i === index ? 0 : -1; });
    panel.setAttribute('aria-labelledby', tabs[index].id);
    image.src = step.image; image.alt = step.name + ' — RAWLO';
    caption.textContent = step.name; title.textContent = step.title; body.textContent = step.body;
    count.textContent = String(index + 1).padStart(2, '0') + ' / 04';
    link.dataset.showCategory = ['planner','navigation','map','community'][index];
    document.querySelectorAll('[data-route-point]').forEach((point, i) => point.classList.toggle('active', i === index));
    if (focus) tabs[index].focus();
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => selectStep(index));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) { event.preventDefault(); selectStep(next, true); }
    });
  });
  document.querySelectorAll('[data-tour-start]').forEach(link => link.addEventListener('click', () => selectStep(Number(link.dataset.tourStart))));
  selectStep(0);
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if ('IntersectionObserver' in window && !reduced) {
    document.documentElement.classList.add('motion-ready');
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('visible'); observer.unobserve(entry.target); } });
    }, {threshold: .08, rootMargin: '0px 0px -15px 0px'});
    document.querySelectorAll('.benefit-intro, .mosaic, .community-story-copy, .tour-heading, .preview .section-heading, .access-layout').forEach(el => { el.classList.add('reveal'); observer.observe(el); });
  }
  let pending = false;
  function updateProgress() {
    const distance = document.documentElement.scrollHeight - innerHeight;
    document.documentElement.style.setProperty('--scroll-progress', distance > 0 ? Math.min(1, Math.max(0, scrollY / distance)) : 0);
    pending = false;
  }
  addEventListener('scroll', () => { if (!pending) { pending = true; requestAnimationFrame(updateProgress); } }, {passive: true});
  addEventListener('resize', updateProgress);
  updateProgress();
  const stage = document.querySelector('.product-stage');
  if (stage && !reduced && matchMedia('(hover: hover) and (pointer: fine)').matches) {
    stage.addEventListener('pointermove', event => { const bounds = stage.getBoundingClientRect(); const ratio = (event.clientX - bounds.left) / bounds.width - .5; stage.style.setProperty('--phone-y', `${ratio * 10}deg`); });
    stage.addEventListener('pointerleave', () => stage.style.setProperty('--phone-y', '0deg'));
  }
})();
