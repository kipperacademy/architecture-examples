from pathlib import Path
import json, uuid, hashlib, html, textwrap

ROOT = Path(__file__).resolve().parents[1]
PURPLE='#9c36b5'; BLACK='#1e1e1e'; GRAY='#687078'
COLORS={'blue':('#1971c2','#d0ebff'),'green':('#2b8a3e','#d3f9d8'),'red':('#c92a2a','#ffe3e3'),'purple':(PURPLE,'#e5dbff'),'yellow':('#e67700','#fff3bf'),'gray':('#868e96','#f1f3f5')}

def box(x,y,w,h,text,color='blue'): return {'kind':'box','x':x,'y':y,'w':w,'h':h,'text':text,'color':color}
def arrow(x,y,x2,y2,label=''): return {'kind':'arrow','x':x,'y':y,'x2':x2,'y2':y2,'text':label}
def note(x,y,text,size=28,color=PURPLE,font=1): return {'kind':'text','x':x,'y':y,'text':text,'size':size,'color':color,'font':font}
def flow(labels,colors=None,y=360):
    colors=colors or ['blue','purple','green']; out=[]
    n=len(labels); w=(1360-(n-1)*95)/n
    for i,label in enumerate(labels):
        x=120+i*(w+95);out.append(box(x,y,w,170,label,colors[i%len(colors)]))
        if i<n-1:out.append(arrow(x+w+10,y+85,x+w+85,y+85))
    return out

def compare(left,right,footer_left='',footer_right=''):
    return [note(120,265,'ANTES',26,BLACK),note(850,265,'DEPOIS',26,BLACK),box(120,330,610,230,left,'red'),box(850,330,610,230,right,'green'),note(120,605,footer_left),note(850,605,footer_right)]

def slide(title,subtitle,items,footer):return (title,subtitle,items,footer)

def generate(folder, slides):
    elements=[]; svgs=[]
    def uid(s):return hashlib.sha256((folder+s).encode()).hexdigest()[:20]
    for i,(title,subtitle,items,footer) in enumerate(slides):
        ox=(i%3)*1800;oy=(i//3)*1080;fid=uid(f'frame{i}'); count=0; svg=[]
        def base(t,x,y,w,h,stroke=BLACK,fill='transparent'):
            nonlocal count
            count+=1
            return dict(id=uid(f'{i}:{count}'),type=t,x=ox+x,y=oy+y,width=w,height=h,angle=0,strokeColor=stroke,backgroundColor=fill,fillStyle='solid',strokeWidth=2,strokeStyle='solid',roughness=1 if t!='text' else 0,opacity=100,groupIds=[],frameId=fid,roundness=None,seed=int(uid(f'{i}:{count}:seed')[:7],16),version=1,versionNonce=1,isDeleted=False,boundElements=[],updated=1791288000000,link=None,locked=False)
        frame=base('frame',0,0,1600,900);frame.update(id=fid,frameId=None,name=f'{i+1:02d}. {title}',customData={'slidesOrder':i});elements.append(frame)
        def rect(x,y,w,h,stroke,fill):
            e=base('rectangle',x,y,w,h,stroke,fill);e['roundness']={'type':3};elements.append(e)
            svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        def text(x,y,txt,size=28,color=BLACK,w=None,font=1):
            lines=txt.split('\n'); width=w or max(len(a) for a in lines)*size*.62; height=len(lines)*size*1.25
            assert x+width<=1580,(folder,i,txt,'width',x+width)
            assert y+height<=890,(folder,i,txt,'height')
            e=base('text',x,y,width,height,color);e.update(text=txt,originalText=txt,fontSize=size,fontFamily=font,textAlign='left',verticalAlign='top',containerId=None,autoResize=False,lineHeight=1.25);elements.append(e)
            svg_font = 'Courier New,monospace' if font == 3 else 'Arial,sans-serif'
            for j,line in enumerate(lines):svg.append(f'<text x="{x}" y="{y+size+j*size*1.25}" fill="{color}" font-family="{svg_font}" font-size="{size}">{html.escape(line)}</text>')
        rect(0,0,1600,900,'#ffffff','#ffffff')
        minimal_cover = not subtitle and not items and not footer
        if minimal_cover:
            text(160,360,title,72,w=1320)
        else:
            rect(58,72,10,130,PURPLE,'#e5dbff')
            text(100,70,title,44,w=1420);text(100,145,subtitle,28,GRAY,w=1400)
        for item in items:
            if item['kind']=='box':
                stroke,fill=COLORS[item['color']];rect(item['x'],item['y'],item['w'],item['h'],stroke,fill)
                if item['text']:
                    lines=item['text'].split('\n');size=min(30,(item['w']-50)/max(len(a) for a in lines)/.62)
                    size=min(size,(item['h']-24)/len(lines)/1.25)
                    assert size>=22,(folder,i,item,size)
                    text(item['x']+25,item['y']+(item['h']-len(lines)*size*1.25)/2,item['text'],size,BLACK,w=item['w']-50)
            elif item['kind']=='text':text(item['x'],item['y'],item['text'],item['size'],item['color'],font=item.get('font',1))
            else:
                x,y,x2,y2=item['x'],item['y'],item['x2'],item['y2'];e=base('arrow',x,y,abs(x2-x),abs(y2-y),PURPLE)
                e.update(points=[[0,0],[x2-x,y2-y]],startBinding=None,endBinding=None,startArrowhead=None,endArrowhead='arrow',elbowed=False);elements.append(e)
                svg.append(f'<path d="M{x} {y} L{x2} {y2}" stroke="{PURPLE}" stroke-width="3" fill="none" marker-end="url(#arrow)"/>')
                if item['text']:text(min(x,x2),min(y,y2)-48,item['text'],24,PURPLE)
        if not minimal_cover:
            text(100,785,textwrap.fill(footer,100),25,PURPLE,w=1400)
            text(1430,855,f'{i+1:02d} / {len(slides):02d}',18,GRAY,w=100)
        doc='<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="none" stroke="'+PURPLE+'" stroke-width="1"/></marker></defs>'+''.join(svg)+'</svg>'
        svgs.append(doc)
    data={'type':'excalidraw','version':2,'source':'https://excalidraw.com','elements':elements,'appState':{'viewBackgroundColor':'#ffffff','gridSize':None},'files':{}}
    if folder == '08-arquitetura-assincrona':
        from estilo_aula08 import apply_style
        data = apply_style(data)
    target=ROOT/folder; (target/'teoria.excalidraw').write_text(json.dumps(data,ensure_ascii=False,indent=2))
    preview=target/'previas';preview.mkdir(exist_ok=True)
    for i,svg in enumerate(svgs):(preview/f'{i+1:02d}.svg').write_text(svg)
    (preview/'index.html').write_text('<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>'+html.escape(slides[0][0])+'</title><style>body{margin:0;background:#eee;font-family:sans-serif}figure{margin:24px auto;max-width:1200px}img{width:100%;box-shadow:0 2px 16px #ccc}figcaption{margin:12px}</style>'+''.join(f'<figure><img src="{i+1:02d}.svg"><figcaption>{i+1:02d}. {html.escape(s[0])}</figcaption></figure>' for i,s in enumerate(slides))+'</html>')
    if folder == '08-arquitetura-assincrona':
        from estilo_aula08 import render_svgs
        render_svgs(data, preview)
    imp=ROOT/'planejamento/importar';imp.mkdir(exist_ok=True)
    (imp/(f'Aula {folder[:2]} — '+slides[0][0]+'.excalidraw')).write_text(json.dumps(data,ensure_ascii=False))
    print(folder,len(slides),'slides',len(elements),'elementos')

