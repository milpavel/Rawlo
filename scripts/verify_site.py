"""Structural release checks. Browser rendering must be verified separately."""
from html.parser import HTMLParser
from pathlib import Path
import json
from generate_site import LANGS, COPY, PUB
class Document(HTMLParser):
    def __init__(self):
        super().__init__(); self.tags=[]
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag,dict(attrs)))
def verify():
    for code in LANGS:
        path=PUB/('index.html' if code=='en' else code+'/index.html')
        source=path.read_text(); page=Document();page.feed(source)
        ids=[a['id'] for tag,a in page.tags if 'id' in a]
        assert len(ids)==len(set(ids)),f'{code}: duplicate IDs'
        assert next(a['lang'] for tag,a in page.tags if tag=='html')==code
        assert sum(tag=='h1' for tag,a in page.tags)==1
        assert sum(tag=='figure' for tag,a in page.tags)==12
        assert sum(tag=='a' and a.get('class','').startswith('europe-lang-card') for tag,a in page.tags)==22
        assert sum(tag=='link' and a.get('rel')=='alternate' for tag,a in page.tags)==23
        expected='https://rawlo.eu/'+('' if code=='en' else code+'/')
        assert next(a['href'] for tag,a in page.tags if tag=='link' and a.get('rel')=='canonical')==expected
        for tag,attrs in page.tags:
            for attribute in ['href','src','data-shot']:
                ref=attrs.get(attribute,'')
                if ref.startswith('#'):assert ref[1:] in ids,(code,ref)
                elif ref.startswith('/'):
                    target=PUB/ref.lstrip('/')
                    assert target.exists(),(code,ref)
                    if target.is_dir():assert (target/'index.html').exists(),(code,ref)
            if tag=='img':assert 'alt' in attrs,(code,'missing alt')
        for retired in ['styles-v13.css','app-v14.js','gallery-01.png','LIVE UI','App Store','rawlo.app']:
            assert retired not in source,(code,retired)
        if code!='en':
            for key in ['intro','navbody','planbody','mapbody','communitybody','servicebody','profilebody','screens']:
                assert COPY[code][key]!=COPY['en'][key],(code,key,'English fallback')
    print('PASS: 22 language pages, anchors/assets, 12 screenshots, 22 country cards, canonical/hreflang and no retired UI.')
if __name__=='__main__':verify()
