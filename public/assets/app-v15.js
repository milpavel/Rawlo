'use strict';
(() => {
 const supported=['en','cs','sk','pl','de','fr','es','pt','it','nl','hu','ro','hr','sl','bg','fi','sv','et','lv','lt','da','el'];
 const chooseLanguage=code=>{if(!supported.includes(code))return;try{localStorage.setItem('rawlo-lang',code);}catch(_){}location.assign((code==='en'?'/':`/${code}/`)+location.search+location.hash);};
 document.querySelector('[data-language-select]')?.addEventListener('change',event=>chooseLanguage(event.target.value));
 document.querySelectorAll('[data-language]').forEach(link=>link.addEventListener('click',()=>{try{localStorage.setItem('rawlo-lang',link.dataset.language);}catch(_){}}));
 const button=document.querySelector('.menu-toggle'),menu=document.querySelector('.main-nav');
 const closeMenu=()=>{menu.classList.remove('open');button.setAttribute('aria-expanded','false');};
 button?.addEventListener('click',()=>button.setAttribute('aria-expanded',String(menu.classList.toggle('open'))));
 menu?.querySelectorAll('a').forEach(link=>link.addEventListener('click',closeMenu));
 document.addEventListener('keydown',event=>{if(event.key==='Escape')closeMenu();});
 document.addEventListener('click',event=>{if(!event.target.closest('.site-header'))closeMenu();});
 const gallery=document.querySelector('.gallery'),filters=Array.from(document.querySelectorAll('[data-filter]'));
 function filter(category){filters.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.filter===category)));gallery.querySelectorAll('figure').forEach(figure=>{figure.hidden=category!=='all'&&figure.dataset.category!==category;});gallery.scrollLeft=0;}
 filters.forEach(button=>button.addEventListener('click',()=>filter(button.dataset.filter)));
 document.querySelectorAll('[data-show-category]').forEach(link=>link.addEventListener('click',()=>filter(link.dataset.showCategory)));
 const move=direction=>gallery.scrollBy({left:direction*Math.max(210,gallery.clientWidth*.75),behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
 document.querySelector('[data-gallery-prev]')?.addEventListener('click',()=>move(-1));
 document.querySelector('[data-gallery-next]')?.addEventListener('click',()=>move(1));
 gallery?.addEventListener('keydown',event=>{if(event.target!==gallery)return;if(event.key==='ArrowRight'||event.key==='ArrowLeft'){event.preventDefault();move(event.key==='ArrowRight'?1:-1);}});
 const dialog=document.querySelector('.lightbox');
 document.querySelectorAll('[data-shot]').forEach(button=>button.addEventListener('click',()=>{if(typeof dialog.showModal!=='function'){window.open(button.dataset.shot,'_blank','noopener');return;}const image=dialog.querySelector('[data-lightbox-image]');image.src=button.dataset.shot;image.alt=button.dataset.caption+' — RAWLO';dialog.querySelector('[data-lightbox-caption]').textContent=button.dataset.caption;dialog.showModal();}));
 dialog?.querySelector('[data-lightbox-close]').addEventListener('click',()=>dialog.close());
 dialog?.addEventListener('click',event=>{const rect=dialog.getBoundingClientRect();if(event.target===dialog&&(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom))dialog.close();});
})();
