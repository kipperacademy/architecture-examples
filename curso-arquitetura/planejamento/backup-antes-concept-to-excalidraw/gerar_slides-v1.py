from pathlib import Path
import json, uuid, hashlib, html

ROOT = Path(__file__).resolve().parents[1]
PURPLE='#9c36b5'; BLACK='#1e1e1e'; GRAY='#687078'
COLORS={'blue':('#1971c2','#d0ebff'),'green':('#2b8a3e','#d3f9d8'),'red':('#c92a2a','#ffe3e3'),'purple':(PURPLE,'#e5dbff'),'yellow':('#e67700','#fff3bf'),'gray':('#868e96','#f1f3f5')}

def box(x,y,w,h,text,color='blue'): return {'kind':'box','x':x,'y':y,'w':w,'h':h,'text':text,'color':color}
def arrow(x,y,x2,y2,label=''): return {'kind':'arrow','x':x,'y':y,'x2':x2,'y2':y2,'text':label}
def note(x,y,text,size=28,color=PURPLE): return {'kind':'text','x':x,'y':y,'text':text,'size':size,'color':color}
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

D={}
D['04-monolito-modular']=[
slide('Monólito Modular','Domínios, módulos, dados e transações — uma aplicação.',flow(['Separar\nresponsabilidades','Definir\ncontratos','Preservar\nconsistência']), 'O que precisa mudar junto? O que pode mudar separado?'),
slide('Uma unidade de deploy','Fronteiras internas não exigem processos separados.',[box(150,285,1300,350,'','gray'),note(190,310,'UMA APLICAÇÃO',28,BLACK),box(220,395,480,140,'Financeiro','blue'),box(900,395,480,140,'Acadêmico','green'),arrow(720,465,880,465,'chamada local'),note(400,670,'build → um artefato → deploy')], 'Mais módulos ≠ mais serviços de rede.'),
slide('Uma fronteira por capacidade','A escola registra recebimentos e libera matrículas.',[box(150,325,540,240,'FINANCEIRO\nconfirmar pedido\nconsultar situação','blue'),box(900,325,540,240,'ACADÊMICO\ndecidir acesso\nregistrar matrícula','green'),arrow(880,460,710,460,'consulta'),note(270,650,'Cada capacidade reúne regras + dados relacionados.')], 'Controller / service / repository podem existir dentro de cada módulo.'),
slide('O contrato limita o conhecimento','Acadêmico pede uma informação; não recebe o estado mutável.',flow(['Matriculas\npedido-ana','Cobrancas\nestaConfirmado(id)','true\npermite decidir']), 'private Set confirmadas: quem consulta não recebe o mapa para editar.'),
slide('Um banco, donos explícitos','Compartilhar o banco físico não autoriza qualquer acesso.',[box(180,280,500,115,'Financeiro','blue'),box(920,280,500,115,'Acadêmico','green'),box(120,500,1360,215,'','gray'),box(200,550,470,105,'financeiro_recebimentos','blue'),box(930,550,470,105,'academico_matriculas','green'),arrow(430,410,430,535,'escreve'),arrow(1170,410,1170,535,'escreve'),note(660,675,'UM BANCO',24,BLACK)], 'Os prefixos documentam a propriedade; não criam permissões de banco.'),
slide('Uma transação local','Duas escritas relacionadas confirmam juntas.',flow(['BEGIN\nrecebimento','INSERT\nmatrícula','COMMIT\nambas confirmadas']), 'Falha antes de confirmar → ROLLBACK. Mesma conexão e transação.'),
slide('A vaga já está ocupada','Mesma entrada: Bia tenta a vaga 1, que pertence a Ana.',compare('Autocommit\n1. salva recebimento\n2. matrícula falha\nRecebimento de Bia: ?','Com transação\n1. salva recebimento\n2. matrícula falha\nRecebimento de Bia: ?','Primeira escrita já confirmada.','Rollback da unidade de trabalho.'), 'Preveja → rode sem-transacao → rode com-transacao → compare.'),
slide('Onde a transação termina','Um rollback local não desfaz uma cobrança remota.',[box(120,300,790,340,'','gray'),note(150,320,'TRANSAÇÃO LOCAL',28,BLACK),box(165,410,300,150,'Recebimentos','blue'),box(545,410,320,150,'Matrículas','green'),arrow(470,485,530,485),box(1120,410,360,150,'Provedor\nde pagamento','yellow'),arrow(920,485,1100,485,'HTTP')], 'O recebimento SQL da demo é um registro fictício, sem cobrança externa.'),
slide('Escolher a fronteira','Organização, implantação e consistência são decisões distintas.',flow(['Quem é dono\nda regra?','Quem pode\nconhecer o dado?','O que precisa\nconfirmar junto?']), 'Dois INSERT no mesmo método já são atômicos? Mostre o limite da transação.')]

D['05-localhost-producao']=[
slide('Do localhost à produção','Servidores, máquinas virtuais, containers e deploy.',flow(['Código','Processo\nem execução','Acesso\npela rede']), 'O que precisa existir para continuar atendendo depois do meu terminal?'),
slide('Localhost é relativo a quem chama','O endereço aponta para o próprio contexto de rede.',compare('Computador da professora\nlocalhost:8080\n→ servidor da professora','Computador da aluna\nlocalhost:8080\n→ próprio computador','Funciona se o processo está aqui.','Não aponta para a professora.'), 'Endereço + porta + processo escutando: siga o caminho da requisição.'),
slide('Servidor e máquina virtual','Máquina fornece recursos; processo atende à requisição.',[box(150,280,1300,425,'','gray'),box(220,595,1160,70,'HARDWARE + VIRTUALIZAÇÃO','gray'),box(220,370,540,185,'VM\nSO convidado\nJVM + aplicação','blue'),box(840,370,540,185,'Outra VM\nSO convidado\nseus processos','purple'),note(510,310,'SISTEMAS OPERACIONAIS SEPARADOS',26,BLACK)], 'Servidor pode significar a máquina ou o software que atende.'),
slide('Imagem não é execução','A imagem inicia um container; containers Linux compartilham um kernel.',[box(120,350,370,190,'IMAGEM\nclasses + runtime','yellow'),box(700,285,760,365,'','gray'),box(740,340,300,165,'Container A\nprocesso Java','blue'),box(1110,340,300,165,'Container B\nprocesso Java','green'),box(740,545,670,65,'KERNEL LINUX DO HOST','gray'),arrow(510,445,680,445,'iniciar')], 'No macOS, Docker Desktop fornece esse ambiente Linux em uma VM.'),
slide('A porta de fora e a porta de dentro','Publicar uma porta cria o caminho até o serviço do container.',flow(['curl\n127.0.0.1:8081','publish\n8081 → 8080','Java no container\n0.0.0.0:8080']), 'docker run -p 127.0.0.1:8081:8080 …    |    EXPOSE sozinho não publica.'),
slide('Mesmo código, outra configuração','O ambiente fornece PORT e INSTANCE ao iniciar o processo.',compare('INSTANCE=A\nPORT=8080\nResposta: instancia=A','INSTANCE=B\nPORT=8081\nResposta: instancia=B','O código do handler é o mesmo.','A montagem da execução mudou.'), 'Variáveis da demo não contêm segredos. Observe o nome devolvido pelo servidor.'),
slide('O contador pertence ao processo','Uma nova execução cria uma nova memória.',flow(['Processo A\nvisitas = 2','Parar\ne iniciar','Novo processo\nvisitas = ?'],['blue','red','green']), 'Faça a previsão antes do restart. Empacotar não torna os dados duráveis.'),
slide('O caminho até a produção','Publicar exige conectar rede, processo e operação.',flow(['DNS + HTTPS\nentrada pública','Proxy / roteamento\nalvo saudável','Aplicação\nlogs + health']), 'Este material prepara o pacote. Nenhum deploy público foi executado.'),
slide('Explique a causa','Três perguntas para verificar o modelo mental.',flow(['Por que seu\nlocalhost não é\no meu?','Por que EXPOSE\nnão publica\na porta?','Por que o\ncontador voltou\na 1?']), 'Diferencie: código, imagem, container, processo e estado.')]

D['06-sistemas-escalaveis']=[
slide('Como Construir Sistemas Escaláveis','Cache, CDN, balanceamento, stateless e rate limiting.',flow(['Medir\na pressão','Escolher\num mecanismo','Observar\nefeito + custo']), 'Escalar: sustentar mais carga dentro dos objetivos do serviço.'),
slide('Qual recurso está saturado?','Cinco leituras iguais podem repetir trabalho na mesma origem.',[box(130,355,370,180,'5 requisições\nmesmo preço','blue'),box(660,355,360,180,'API do catálogo','purple'),box(1170,355,300,180,'Origem\n5 leituras','red'),arrow(520,445,640,445),arrow(1040,445,1150,445)], 'Mais réplicas da API não removem automaticamente o gargalo na origem.'),
slide('Cache reaproveita uma cópia','Hit evita consulta; miss busca na origem e preenche.',[box(130,340,330,160,'Pedido\npreço do curso','blue'),box(650,340,330,160,'Cache\n10000 centavos','purple'),box(1180,340,300,160,'Origem\npreço atual','green'),arrow(480,420,630,420),arrow(1000,420,1160,420,'miss'),note(650,570,'hit → devolve a cópia'),note(130,670,'Origem muda para 12000. Cache continua 10000 até invalidar.')], 'A demo mede consultas, não um ganho de latência inventado.'),
slide('CDN: conteúdo perto do cliente','Uma imagem pública pode ser atendida na borda.',flow(['Aluna\npede capa.png','Borda CDN\nhit: entrega cópia','Origem\nconsultada no miss']), 'A capa pública pode ter cache. A matrícula privada exige outra política.'),
slide('Distribuir requisições entre réplicas','O balanceador encaminha para alvos disponíveis.',[box(130,380,330,160,'Balanceador','purple'),box(690,285,320,135,'Réplica A','blue'),box(690,535,320,135,'Réplica B','green'),box(1210,380,290,160,'Banco\ncompartilhado','yellow'),arrow(480,415,670,350,'pedido 1'),arrow(480,500,670,600,'pedido 2'),arrow(1030,350,1190,415),arrow(1030,600,1190,500)], 'Health checks ajudam a escolher alvos; o banco ainda pode ser o gargalo.'),
slide('A próxima chamada pode cair em B','Stateless: a réplica não depende da própria sessão anterior.',compare('Sessões locais\nlogin em A: Ana\nacesso em B: SEM SESSÃO','Armazenamento compartilhado\nlogin em A: Ana\nacesso em B: Ana','Duas memórias diferentes.','As duas consultam a mesma sessão.'), 'Na demo, réplicas e armazenamento são objetos; em produção, cruzam processos.'),
slide('Limitar admissões por chave e tempo','Uma janela permite três pedidos de cada cliente.',[note(130,270,'ANA · MESMA JANELA',26,BLACK)]+[box(130+i*275,365,230,140,str(i+1)+'\n'+('passa' if i<3 else 'limita'),'green' if i<3 else 'red') for i in range(5)]+[note(130,605,'Bia tem sua própria cota. Em t=60, Ana entra em nova janela.')], 'Limite local por réplica não equivale a um limite global.'),
slide('Preveja antes de executar','Cinco consultas idênticas. Depois, uma alteração na origem.',compare('Sem cache\n5 consultas\nLeituras na origem: ?','Com cache\n5 consultas\nLeituras na origem: ?','Observe Catalogo.consultas().','O preço muda sozinho no cache?'), 'Depois: invalide, consulte novamente e explique os dois contadores.'),
slide('Cada técnica resolve uma pressão','Escolha o mecanismo pelo recurso e pelo contrato.',[box(130,290,600,145,'Cache / CDN\nreutilizar uma cópia','blue'),box(870,290,600,145,'Balanceamento\ndistribuir pedidos','green'),box(130,540,600,145,'Stateless\npermitir trocar de réplica','purple'),box(870,540,600,145,'Rate limiting\nlimitar admissões','yellow')], 'Qual problema permanece depois de aplicar cada técnica?')]

D['07-monolito-vs-microservicos']=[
slide('Monólito vs Microserviços','Quando separar implantação, comunicação e dados.',flow(['Necessidade\nconcreta','Fronteira\nindependente','Custo\ndistribuído']), 'Microserviços são uma escolha. Não são uma promoção automática.'),
slide('O que é implantado junto?','A unidade de deploy é diferente da quantidade de módulos.',compare('Um deploy\nFinanceiro + Acadêmico\nchamadas locais','Deploys independentes\nFinanceiro | Acadêmico\ncontratos entre serviços','Pode ter várias réplicas.','Evolução exige compatibilidade.'), 'Separar os processos sem autonomia pode manter o acoplamento e somar rede.'),
slide('A rede acrescenta etapas de falha','A resposta precisa voltar depois que o efeito ocorre.',[box(130,320,350,160,'Checkout','blue'),box(1090,320,390,160,'Provedor','green'),arrow(510,355,1060,355,'1. pedido'),arrow(1060,570,510,570,'3. resposta'),note(1060,520,'2. registra cobrança'),note(160,625,'espera até um limite')], 'Timeout informa ausência de resposta no prazo, não ausência de efeito.'),
slide('Duas visões da mesma operação','A cobrança aconteceu; a confirmação não chegou.',[box(130,320,540,220,'CLIENTE\nUNKNOWN','yellow'),box(940,320,540,220,'PROVEDOR\nCONFIRMADO\n1 cobrança','green'),arrow(920,605,690,605,'resposta perdida'),note(680,560,'X',50,'#c92a2a')], 'O cliente precisa reconciliar ou repetir sob um contrato seguro.'),
slide('A chave preserva a intenção','Repetir pedido-ana deve referir à mesma operação.',flow(['Tentativa 1\npedido-ana','Registro da chave\n+ valor + efeito','Tentativa 2\nmesma chave']), 'Mesmo ID + outro valor: conflito. ID novo pode gerar outro efeito.'),
slide('Cada banco tem seu commit','Rollback no Acadêmico não alcança o Financeiro.',[box(130,300,600,300,'ACADÊMICO\ntransação local\nbanco de matrículas','blue'),box(880,300,600,300,'FINANCEIRO\ntransação local\nbanco de cobranças','green'),arrow(750,450,860,450,'contrato')], 'Uma ação de compensação será outra operação, não um rollback mágico.'),
slide('O benefício paga o custo?','Justifique a separação com uma necessidade observável.',[box(130,305,600,290,'BENEFÍCIO BUSCADO\nimplantação independente\nescala de uma capacidade\nresponsabilidade de equipe','green'),box(880,305,600,290,'CUSTO INTRODUZIDO\nfalhas parciais\ncontratos e observabilidade\ncoordenação de dados','yellow')], 'Qual problema específico não está sendo bem atendido pela estrutura atual?'),
slide('Uma resposta perdida, uma repetição','O provedor registra antes de simular o timeout.',compare('Sem identidade protegida\ncobrar(pedido-ana)\nretry\nCobranças: ?','Com identidade protegida\ncobrar(pedido-ana, 10000)\nretry com mesma chave\nCobranças: ?','Abra DemoRetry.','Abra DemoIdempotencia.'), 'O modelo é sequencial e em memória; não é um provedor de produção.'),
slide('Decidir e explicar a consequência','Compare necessidades, não slogans.',flow(['Mudam juntas?\nQuem implanta?','Escalam diferente?\nQual gargalo?','Qual falha parcial\na divisão cria?']), 'Um monólito também pode enfrentar falhas remotas ao integrar um provedor.')]

D['08-arquitetura-assincrona']=[
slide('Arquitetura Assíncrona','Filas, eventos, workers, outbox, idempotência e sagas.',flow(['Registrar\num fato','Entregar\no trabalho','Aplicar\no efeito']), 'Onde podemos perder trabalho? Onde podemos repeti-lo?'),
slide('Fila separa os momentos','O produtor entrega trabalho para processamento posterior.',flow(['Produtor\npublica','Fila\ntrabalho pendente','Worker\nprocessa + ACK']), 'Se a entrada supera a saída, o backlog cresce.'),
slide('Pedido de ação ou fato ocorrido?','Nomear o contrato ajuda o consumidor a interpretar a mensagem.',compare('COMANDO\nEnviarAviso\n“faça esta ação”','EVENTO\nMatriculaConfirmada\n“este fato ocorreu”','Expressa uma intenção.','Expressa algo que já aconteceu.'), 'Consumidores concorrentes de uma fila não equivalem a broadcast.'),
slide('A janela entre salvar e publicar','Duas operações separadas permitem uma falha no intervalo.',flow(['Salvar matrícula\nAna registrada','FALHA\npublicação não ocorre','Fila vazia\nnenhum aviso'],['green','red','gray']), 'Publicar primeiro também não resolve: o fato pode ainda não ter sido salvo.'),
slide('Outbox guarda a intenção de publicar','Negócio e evento entram na mesma transação local.',[box(120,280,770,340,'','gray'),note(150,310,'UMA TRANSAÇÃO LOCAL',26,BLACK),box(165,415,295,140,'Matrícula\nAna','green'),box(530,415,315,140,'Outbox\nevento-1','purple'),box(1130,415,350,140,'Relay → broker','blue'),arrow(910,480,1110,480,'publica depois')], 'O relay pode publicar de novo se falhar antes de marcar o envio.'),
slide('O efeito veio antes do ACK','Sem confirmação, o broker pode entregar outra vez.',flow(['Worker registra\naviso de Ana','Falha antes\ndo ACK','Redelivery\nevento-1'],['green','red','yellow']), 'Publisher confirm e consumer ACK confirmam etapas diferentes.'),
slide('Reconhecer a mesma mensagem','O efeito local e o ID processado precisam confirmar juntos.',[box(120,350,310,180,'evento-1\nreentregue','yellow'),box(650,275,830,365,'','gray'),note(690,305,'TRANSAÇÃO DO CONSUMIDOR',26,BLACK),box(700,410,330,140,'ID processado\nUNIQUE evento-1','purple'),box(1090,410,330,140,'Aviso local\nAna','green'),arrow(450,440,630,440,'verifica ID')], 'Chamada a e-mail externo continua fora desta transação local.'),
slide('Repetir com uma política','Falha transitória e mensagem inválida pedem tratamentos distintos.',[box(120,365,330,165,'Falhou','red'),box(650,270,360,135,'Pode recuperar?\nretry com atraso','yellow'),box(650,540,360,135,'Limite / inválida\ntratamento ou DLQ','purple'),box(1170,540,310,135,'Observar\ncorrigir → replay','blue'),arrow(470,395,630,335),arrow(470,510,630,605),arrow(1030,605,1150,605)], 'DLQ não corrige o dado. Preserve identidade e evite repetição infinita.'),
slide('Saga compensa uma etapa já confirmada','Outro cenário: reservar vaga e tentar cobrar.',flow(['Reserva\nconfirmada','Cobrança\nrecusada','Liberar reserva\ncompensação'],['green','red','yellow']), 'A compensação é uma nova ação; também pode falhar e exigir recuperação.'),
slide('Localize a falha antes da solução','Reconstrua commit, publicação, efeito e confirmação.',[box(130,285,600,160,'Commit sem publicação\n→ consultar outbox','blue'),box(870,285,600,160,'Publicação sem marcação\n→ possível duplicidade','purple'),box(130,550,600,160,'Efeito sem ACK\n→ reconhecer ID processado','green'),box(870,550,600,160,'Mensagem inválida\n→ política de tratamento','yellow')], 'Demos em memória mostram mecanismos; não provam recuperação durável.')]


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
        def text(x,y,txt,size=28,color=BLACK,w=None):
            lines=txt.split('\n'); width=w or max(len(a) for a in lines)*size*.62; height=len(lines)*size*1.25
            assert x+width<=1580,(folder,i,txt,'width',x+width)
            assert y+height<=890,(folder,i,txt,'height')
            e=base('text',x,y,width,height,color);e.update(text=txt,originalText=txt,fontSize=size,fontFamily=1,textAlign='left',verticalAlign='top',containerId=None,autoResize=False,lineHeight=1.25);elements.append(e)
            for j,line in enumerate(lines):svg.append(f'<text x="{x}" y="{y+size+j*size*1.25}" fill="{color}" font-family="Arial,sans-serif" font-size="{size}">{html.escape(line)}</text>')
        rect(0,0,1600,900,'#ffffff','#ffffff');rect(58,72,10,130,PURPLE,'#e5dbff')
        text(100,70,title,44,w=1420);text(100,145,subtitle,28,GRAY,w=1400)
        for item in items:
            if item['kind']=='box':
                stroke,fill=COLORS[item['color']];rect(item['x'],item['y'],item['w'],item['h'],stroke,fill)
                if item['text']:
                    lines=item['text'].split('\n');size=min(30,(item['w']-50)/max(len(a) for a in lines)/.62)
                    size=min(size,(item['h']-24)/len(lines)/1.25)
                    assert size>=22,(folder,i,item,size)
                    text(item['x']+25,item['y']+(item['h']-len(lines)*size*1.25)/2,item['text'],size,BLACK,w=item['w']-50)
            elif item['kind']=='text':text(item['x'],item['y'],item['text'],item['size'],item['color'])
            else:
                x,y,x2,y2=item['x'],item['y'],item['x2'],item['y2'];e=base('arrow',x,y,abs(x2-x),abs(y2-y),PURPLE)
                e.update(points=[[0,0],[x2-x,y2-y]],startBinding=None,endBinding=None,startArrowhead=None,endArrowhead='arrow',elbowed=False);elements.append(e)
                svg.append(f'<path d="M{x} {y} L{x2} {y2}" stroke="{PURPLE}" stroke-width="3" fill="none" marker-end="url(#arrow)"/>')
                if item['text']:text(min(x,x2),min(y,y2)-48,item['text'],24,PURPLE)
        text(100,790,footer,25,PURPLE,w=1400)
        text(100,855,'CURSO ARQUITETURA  /  '+folder[:2],18,GRAY,w=650);text(1430,855,f'{i+1:02d} / {len(slides):02d}',18,GRAY,w=100)
        doc='<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="none" stroke="'+PURPLE+'" stroke-width="1"/></marker></defs>'+''.join(svg)+'</svg>'
        svgs.append(doc)
    data={'type':'excalidraw','version':2,'source':'https://excalidraw.com','elements':elements,'appState':{'viewBackgroundColor':'#ffffff','gridSize':None},'files':{}}
    target=ROOT/folder; (target/'teoria.excalidraw').write_text(json.dumps(data,ensure_ascii=False,indent=2))
    preview=target/'previas';preview.mkdir(exist_ok=True)
    for i,svg in enumerate(svgs):(preview/f'{i+1:02d}.svg').write_text(svg)
    (preview/'index.html').write_text('<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>'+html.escape(slides[0][0])+'</title><style>body{margin:0;background:#eee;font-family:sans-serif}figure{margin:24px auto;max-width:1200px}img{width:100%;box-shadow:0 2px 16px #ccc}figcaption{margin:12px}</style>'+''.join(f'<figure><img src="{i+1:02d}.svg"><figcaption>{i+1:02d}. {html.escape(s[0])}</figcaption></figure>' for i,s in enumerate(slides))+'</html>')
    imp=ROOT/'planejamento/importar';imp.mkdir(exist_ok=True)
    (imp/(f'Aula {folder[:2]} — '+slides[0][0]+'.excalidraw')).write_text(json.dumps(data,ensure_ascii=False))
    print(folder,len(slides),'slides',len(elements),'elementos')

if __name__=='__main__':
    for folder,slides in D.items():generate(folder,slides)
