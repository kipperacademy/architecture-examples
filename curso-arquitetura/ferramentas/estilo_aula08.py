"""Estilo do board de referência Archictecture: ícones editáveis e traços leves."""
import copy,uuid,html
from pathlib import Path

def apply_style(doc):
    elements=doc['elements'];frames={e['id']:e for e in elements if e['type']=='frame'}
    added=[]
    for e in elements:
        if e['type']=='frame':continue
        f=frames[e['frameId']];ry=e['y']-f['y'];rx=e['x']-f['x']
        if e['type']=='rectangle':
            if e['width']==10 and e['height']==130:e['isDeleted']=True;continue
            if e['width']==1600:continue
            e['backgroundColor']='#f8f9fa' if e['width']<900 else 'transparent'
            e['strokeWidth']=1.4;e['roughness']=1
        if e['type']=='text':
            if ry==70:
                e['strokeColor']='#9c36b5';e['fontFamily']=1
            else:
                e['fontFamily']=2 if e.get('fontFamily')!=3 else 3
                e['strokeColor']='#343a40' if ry==145 else e['strokeColor']
                if ry not in [145,785,855]:e['fontSize']=max(23,e['fontSize']*.92)
        if e['type']=='arrow':
            i=f['customData']['slidesOrder']
            e['strokeColor']='#1971c2' if i==0 else '#e67700'
            e['strokeWidth']=1.5;e['roughness']=1
            if i in [2,3,4]:e['strokeStyle']='dashed'
    for b in list(elements):
        if b['type']!='rectangle' or b.get('isDeleted') or b['width']>=1500:continue
        txt=next((t for t in elements if t['type']=='text' and t.get('frameId')==b.get('frameId') and abs(t['x']-b['x']-25)<1 and b['y']<t['y']<b['y']+b['height']),None)
        if not txt:continue
        isapp=any(a in txt['text'] for a in ['APP ','APLICAÇÃO ','API ESTOQUE','WORKER ESTOQUE'])
        if not isapp:continue
        x=b['x']+b['width']-37;y=b['y']+12
        icon=copy.deepcopy(b);icon.update(id=uuid.uuid4().hex[:20],x=x,y=y,width=23,height=42,strokeColor='#495057',backgroundColor='#f1f3f5',roundness=None,boundElements=[],roughness=1)
        added.append(icon)
        for yy in [7,13,19,25]:
            line=copy.deepcopy(icon);line.update(id=uuid.uuid4().hex[:20],type='line',x=x+4,y=y+yy,width=15,height=0,points=[[0,0],[15,0]],backgroundColor='transparent',startArrowhead=None,endArrowhead=None);added.append(line)
    doc['elements']=[e for e in elements if not e.get('isDeleted')]+added
    return doc

def render_svgs(doc,directory):
    frames=sorted([e for e in doc['elements'] if e['type']=='frame'],key=lambda f:f['customData']['slidesOrder'])
    for i,f in enumerate(frames):
        svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">']
        for e in doc['elements']:
            if e.get('frameId')!=f['id']:continue
            x=e['x']-f['x'];y=e['y']-f['y'];c=e['strokeColor'];fill=e['backgroundColor'];w=e['width'];h=e['height']
            if e['type']=='rectangle':svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{c}" stroke-width="{e["strokeWidth"]}"/>')
            elif e['type']=='text':
                size=e['fontSize'];font='Courier New,monospace' if e['fontFamily']==3 else 'Arial,sans-serif'
                for j,line in enumerate(e['text'].split('\n')):svg.append(f'<text x="{x}" y="{y+size+j*size*1.25}" fill="{c}" font-family="{font}" font-size="{size}">{html.escape(line)}</text>')
            elif e['type'] in ['arrow','line']:
                dx,dy=e['points'][-1];dash='stroke-dasharray="8 6"' if e.get('strokeStyle')=='dashed' else ''
                svg.append(f'<path d="M{x} {y} L{x+dx} {y+dy}" stroke="{c}" stroke-width="{e["strokeWidth"]}" fill="none" {dash}/>')
                if e['type']=='arrow':
                    import math
                    a=math.atan2(dy,dx);xx=x+dx;yy=y+dy
                    svg.append(f'<path d="M{xx-14*math.cos(a-.4)} {yy-14*math.sin(a-.4)} L{xx} {yy} L{xx-14*math.cos(a+.4)} {yy-14*math.sin(a+.4)}" stroke="{c}" fill="none"/>')
        svg.append('</svg>');(Path(directory)/f'{i+1:02d}.svg').write_text(''.join(svg))
