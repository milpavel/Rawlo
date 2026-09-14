import os,re,glob,json,shutil
from pathlib import Path
from bs4 import BeautifulSoup
root=Path('/mnt/data/rawlo_v7'); public=root/'public'
mp=json.load(open('/mnt/data/rawlo_gallery_fix/scripts/overview_screenshot_map.json'))
files=glob.glob('/mnt/data/Simulator Screenshot - iPhone 17 - 2026-09-14 at *.png')
def sec_name(s):
 m=re.search(r'at (\d+)\.(\d+)\.(\d+)',os.path.basename(s)); return int(m.group(1))*3600+int(m.group(2))*60+int(m.group(3))
def sec_str(s):
 h,m,ss=map(int,s.split('.')); return h*3600+m*60+ss
centers=sorted((sec_str(v),k,v) for k,v in mp.items()); sets={}
for i,(c,k,v) in enumerate(centers):
 lo=(centers[i-1][0]+c)/2 if i else c-180; hi=(c+centers[i+1][0])/2 if i+1<len(centers) else c+180
 cand=sorted([f for f in files if lo<=sec_name(f)<hi],key=sec_name)
 if len(cand)>17: cand=sorted(sorted(cand,key=lambda f:abs(sec_name(f)-c))[:17],key=sec_name)
 if len(cand)<17:
  pool=sorted([f for f in files if f not in cand],key=lambda f:abs(sec_name(f)-c)); cand=sorted(cand+pool[:17-len(cand)],key=sec_name)
 sets[k]=cand[:17]; out=public/'assets/screens/localized'/k; out.mkdir(parents=True,exist_ok=True)
 for n,src in enumerate(sets[k],1): shutil.copy2(src,out/f'gallery-{n:02d}.png')
for lang,path in [(k,public/k/'index.html') for k in mp]+[('en',public/'index.html')]:
 if not path.exists(): continue
 soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser'); section=soup.find('section',id='preview')
 if not section: continue
 shell=section.find(class_='preview-shell'); shell.clear()
 controls=soup.new_tag('div',attrs={'class':'preview-controls','aria-label':'Screenshot gallery controls'})
 for cls,txt,label in [('preview-arrow preview-prev','‹','Previous screenshots'),('preview-count','1 / 17',None),('preview-arrow preview-next','›','Next screenshots')]:
  if 'button' in cls or 'arrow' in cls:
   el=soup.new_tag('button',attrs={'class':cls,'type':'button','aria-label':label}); el.string=txt
  else:
   el=soup.new_tag('div',attrs={'class':cls}); el.string=txt
  controls.append(el)
 shell.append(controls)
 screens=soup.new_tag('div',attrs={'class':'screens','id':'app-screens','tabindex':'0','aria-label':'RAWLO app screenshots'})
 base='../assets' if path.parent!=public else 'assets'
 for n in range(1,18):
  fig=soup.new_tag('figure'); img=soup.new_tag('img',attrs={'src':f'{base}/screens/localized/{lang}/gallery-{n:02d}.png','alt':f'RAWLO app screenshot {n} of 17','loading':'eager' if n<=4 else 'lazy','decoding':'async'}); fig.append(img); screens.append(fig)
 shell.append(screens); path.write_text(str(soup),encoding='utf-8')
css=public/'assets/styles.css'; s=css.read_text(encoding='utf-8'); marker='/* V6: show every app preview at once instead of hiding most of them in a horizontal carousel */'
if marker in s:s=s.split(marker)[0].rstrip()+'\n'
s+=r'''
/* V7: 17 localized app screens in a horizontal carousel, kept inside the original box */
.preview-shell{position:relative;overflow:hidden!important;padding:26px 24px 20px!important;border:1px solid #263640;border-radius:32px;background:linear-gradient(145deg,rgba(18,27,35,.88),rgba(10,16,22,.94));box-shadow:0 34px 80px rgba(0,0,0,.28)}
.preview-shell:before{content:"";position:absolute;width:520px;height:520px;border-radius:50%;background:rgba(18,214,208,.08);filter:blur(90px);top:-300px;left:20%;pointer-events:none}.preview-rail{display:none!important}
.preview-controls{position:relative;z-index:3;display:flex;justify-content:flex-end;align-items:center;gap:10px;margin:0 0 10px}.preview-arrow{width:42px;height:42px;border-radius:50%;border:1px solid #344650;background:#0d171e;color:#eaf4f5;font-size:29px;line-height:1;cursor:pointer;display:grid;place-items:center}.preview-arrow:hover{border-color:#12d6d0;color:#12d6d0}.preview-count{min-width:72px;text-align:center;color:#7e919a;font-weight:800;font-size:12px;letter-spacing:.08em}
.preview .screens{display:flex!important;grid-template-columns:none!important;gap:18px!important;overflow-x:auto!important;overflow-y:hidden!important;padding:10px 8px 20px!important;scroll-snap-type:x mandatory!important;scroll-behavior:smooth;-webkit-overflow-scrolling:touch;scrollbar-width:thin;scrollbar-color:#2d5f66 transparent;position:relative;z-index:2}.preview .screens::-webkit-scrollbar{height:7px}.preview .screens::-webkit-scrollbar-thumb{background:#28545a;border-radius:99px}.preview .screens figure{flex:0 0 clamp(250px,24vw,330px)!important;width:auto!important;min-width:0;margin:0!important;scroll-snap-align:start;display:block!important;overflow:hidden;border:1px solid #263640;border-radius:32px;background:#0c1319;box-shadow:0 18px 45px rgba(0,0,0,.28)}.preview .screens img{display:block;width:100%!important;height:auto!important;max-height:none!important;object-fit:contain!important;border:0!important;border-radius:31px!important;box-shadow:none!important}
@media(max-width:980px){.preview-shell{padding:20px 16px 16px!important}.preview .screens figure{flex-basis:290px!important}}@media(max-width:640px){.preview-shell{padding:14px 8px 12px!important;border-radius:24px}.preview-arrow{width:38px;height:38px}.preview .screens{gap:12px!important;padding:8px 8px 16px!important}.preview .screens figure{flex:0 0 82vw!important;border-radius:26px}.preview .screens img{border-radius:25px!important}}
'''; css.write_text(s,encoding='utf-8')
app=public/'assets/app.js'; js=app.read_text(encoding='utf-8'); js=js.replace('// V6: screenshots are rendered as a full responsive gallery; no carousel JS is needed.',r'''// V7: 17-screen horizontal gallery with arrows, touch/trackpad swipe and live counter.
  const gallery = document.getElementById('app-screens');
  if (gallery) {
    const shell = gallery.closest('.preview-shell'); const prev = shell?.querySelector('.preview-prev'); const next = shell?.querySelector('.preview-next'); const count = shell?.querySelector('.preview-count'); const figures=[...gallery.querySelectorAll('figure')];
    const step=()=> (figures[0]?.getBoundingClientRect().width||300)+18;
    const updateCount=()=>{if(!count||!figures.length)return;const idx=Math.max(0,Math.min(figures.length-1,Math.round(gallery.scrollLeft/step())));count.textContent=`${idx+1} / ${figures.length}`;};
    prev?.addEventListener('click',()=>gallery.scrollBy({left:-step()*3,behavior:'smooth'})); next?.addEventListener('click',()=>gallery.scrollBy({left:step()*3,behavior:'smooth'})); gallery.addEventListener('scroll',()=>requestAnimationFrame(updateCount),{passive:true}); gallery.addEventListener('keydown',e=>{if(e.key==='ArrowLeft')gallery.scrollBy({left:-step(),behavior:'smooth'});if(e.key==='ArrowRight')gallery.scrollBy({left:step(),behavior:'smooth'});}); updateCount();
  }'''); app.write_text(js,encoding='utf-8')
(root/'GALLERY_17_MAPPING.json').write_text(json.dumps({k:[os.path.basename(x) for x in v] for k,v in sets.items()},ensure_ascii=False,indent=2),encoding='utf-8')
print('built',len(sets),'x17')
