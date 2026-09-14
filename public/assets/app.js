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

  // V7: 17-screen horizontal gallery with arrows, touch/trackpad swipe and live counter.
  const gallery = document.getElementById('app-screens');
  if (gallery) {
    const shell = gallery.closest('.preview-shell'); const prev = shell?.querySelector('.preview-prev'); const next = shell?.querySelector('.preview-next'); const count = shell?.querySelector('.preview-count'); const figures=[...gallery.querySelectorAll('figure')];
    const step=()=> (figures[0]?.getBoundingClientRect().width||300)+18;
    const updateCount=()=>{if(!count||!figures.length)return;const idx=Math.max(0,Math.min(figures.length-1,Math.round(gallery.scrollLeft/step())));count.textContent=`${idx+1} / ${figures.length}`;};
    prev?.addEventListener('click',()=>gallery.scrollBy({left:-step()*3,behavior:'smooth'})); next?.addEventListener('click',()=>gallery.scrollBy({left:step()*3,behavior:'smooth'})); gallery.addEventListener('scroll',()=>requestAnimationFrame(updateCount),{passive:true}); gallery.addEventListener('keydown',e=>{if(e.key==='ArrowLeft')gallery.scrollBy({left:-step(),behavior:'smooth'});if(e.key==='ArrowRight')gallery.scrollBy({left:step(),behavior:'smooth'});}); updateCount();
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
