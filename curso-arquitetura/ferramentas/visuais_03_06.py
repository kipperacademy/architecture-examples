import textwrap
from visual_engine import box, arrow, note, slide, generate
D={}
G={}
def add(folder,title,sub,items,footer,question,path,result):
    D.setdefault(folder,[]).append(slide(title,sub,items,footer))
    G.setdefault(folder,[]).append((title,question,path,result))
def row(labels,y=360,colors=None):
    colors=colors or ['blue','purple','green'];out=[];n=len(labels);w=(1360-(n-1)*70)/n
    for i,t in enumerate(labels):
        x=120+i*(w+70);out.append(box(x,y,w,150,t,colors[i%len(colors)]))
        if i<n-1:out.append(arrow(x+w+8,y+75,x+w+62,y+75))
    return out
F='03-clean-architecture-hexagonal'
add(F,'Clean Architecture: proteger a decisão','Clean Architecture organiza políticas no núcleo e detalhes na borda, com\ndependências de código apontando para dentro.',
    row(['ENTRADA\nnome + pagamento','POLÍTICA\npagamento confirmado?','RESULTADO\nregistrar ou recusar'])+[box(650,620,420,90,'Arquivo ou memória?','yellow'),arrow(840,510,840,610,'detalhe substituível')],
    'A regra fica estável enquanto os mecanismos externos podem mudar.', 'O que deve permanecer igual quando trocamos armazenamento?','Entrada → condição de pagamento → decisão; depois aponte o detalhe abaixo.','A decisão deve continuar igual; o modo de guardar pode mudar.')
add(F,'Entidades: a regra vive nos dados','Entidades representam conceitos do domínio e preservam suas regras, sem\ndepender de interface ou armazenamento.',
    [box(130,310,340,130,'Ana\nCONFIRMADO','blue'),box(130,540,340,130,'Bia\nPENDENTE','blue'),box(610,370,400,200,'Pedido\npermiteMatricula()','purple'),arrow(485,375,595,410),arrow(485,600,595,490),box(1160,325,310,100,'true','green'),box(1160,555,310,100,'false','red'),arrow(1020,410,1145,380),arrow(1020,500,1145,600)],
    'Nenhum Path, Files ou SDK participa deste critério.', 'O armazenamento deveria decidir quem pode se matricular?','Compare os mesmos campos Ana/Bia entrando na mesma operação.','O status muda a decisão; o mecanismo de persistência não entra na regra.')
add(F,'Caso de uso: coordenar a ação','Um caso de uso coordena uma ação da aplicação: aplica regras, solicita\ncolaboradores e devolve um resultado.',
    row(['Bia + PENDENTE','permiteMatricula()\nfalse','return false\nSEM salvar'],300,['blue','purple','red'])+row(['Ana + CONFIRMADO','permiteMatricula()\ntrue','salvar("Ana")\nreturn true'],560),
    'O retorno antecipado explica por que Bia não chega ao repositório.', 'Qual caminho não toca o armazenamento?','Linha de Bia até return; depois linha de Ana até salvar.','Recusar acontece antes da persistência.')
add(F,'Adaptadores: traduzir, não duplicar a regra','Adaptadores convertem protocolos e formatos externos para os dados e operações\nesperados pela aplicação.',
    row(['"Bia;PENDENTE"\nlinha do CSV','split(";")\nStatusPagamento','executar("Bia",\nPENDENTE)'],330)+[note(180,590,'texto externo',28),arrow(400,620,1150,620,'conversão de formato'),note(1120,660,'tipo interno',28)],
    'O adaptador converte os dados; a regra continuará recusando o pagamento pendente.', 'Uma linha bem formada significa matrícula permitida?','Texto → campos e enum → operação interna.','Formato válido permite processar; elegibilidade ainda depende da regra.')
add(F,'Frameworks e drivers: o mecanismo na borda','Frameworks e drivers são mecanismos externos de execução, comunicação e\npersistência, conectados ao núcleo por adaptadores.',
    [box(120,330,420,180,'salvar("Ana")\nnecessidade interna','purple'),box(800,250,610,150,'MEMÓRIA\ncoleção recebe Ana','blue'),box(800,530,610,150,'ARQUIVO\nFiles escreve "Ana"','yellow'),arrow(555,385,780,325,'uma implementação'),arrow(555,440,780,605,'outra implementação')],
    'Trocar a tecnologia exige integração; não exige reescrever o critério do pagamento.', 'Quem precisa conhecer o caminho do arquivo?','Necessidade salvar → coleção ou Files → armazenamento concreto.','O adaptador de arquivo e a montagem externa conhecem o caminho.')
add(F,'Dependência de código ≠ fluxo de execução','A regra de dependência orienta quem conhece quais tipos; o fluxo de execução\ndescreve quem chama quem em tempo de execução.',
    [note(120,250,'NO CÓDIGO: quem conhece qual tipo?',26),box(120,320,550,160,'RepositorioEmArquivo\nimplements ...','yellow'),box(940,320,530,160,'RepositorioMatriculas\ncontrato interno','purple'),arrow(690,390,920,390,'depende do tipo'),note(120,525,'NA EXECUÇÃO: quem solicita trabalho?',26),box(120,600,550,100,'caso de uso: salvar("Ana")','purple'),box(940,600,530,100,'arquivo: escreve Ana','yellow'),arrow(690,650,920,650,'chamada em execução')],
    'MatricularAluno conhece o contrato; não importa Files nem o adaptador concreto.', 'As duas setas descrevem a mesma coisa?','Primeiro implements no código; depois salvar na execução.','A dependência do adaptador vai para a abstração; a solicitação chega ao detalhe.')
add(F,'Injeção: mostrar quem monta os objetos','Injeção de dependência entrega um colaborador ao objeto; inversão faz a\npolítica depender de um contrato, não do detalhe.',
    [note(140,280,'var repositorio = new RepositorioEmMemoria();',26,font=3),note(140,340,'var matricular = new MatricularAluno(repositorio);',26,font=3),box(160,490,450,160,'OBJETO repositório\ncoleção: []','blue'),box(950,490,470,160,'OBJETO caso de uso\nrepositorio → referência','purple'),arrow(630,565,925,565,'passado no construtor')],
    'Injeção entrega o objeto; inversão orienta o conhecimento pelo contrato.', 'Quem cria o colaborador? Quem o recebe?','new na montagem → objeto → parâmetro do construtor.','Não é preciso um framework para injetar a referência.')
add(F,'A escola: três pedidos, uma política','Uma regra de negócio decide o que é permitido com base nos dados do domínio,\nindependentemente do canal de entrada.',
    [box(130,290,370,120,'Ana · CONFIRMADO','blue'),box(130,460,370,120,'Bia · PENDENTE','blue'),box(130,630,370,120,'Clara · CONFIRMADO','blue'),box(650,380,420,210,'pagamento\n== CONFIRMADO?','purple'),box(1210,335,290,130,'Ana\nClara','green'),box(1210,610,290,100,'Bia: recusada','red'),arrow(515,350,635,415),arrow(515,520,635,485),arrow(515,690,635,560),arrow(1080,430,1195,400),arrow(1080,560,1195,650)],
    'Pagamento já é uma entrada conhecida nesta demo; não há provedor real de cobrança.', 'Quais nomes devem ser guardados?','Três entradas → condição → conjunto aprovado e recusa.','Ana e Clara; Bia retorna antes de salvar.')
add(F,'Memória: um novo objeto começa vazio','Armazenamento em memória mantém dados na coleção de uma instância; uma nova\ninstância cria seu próprio estado.',
    [note(130,250,'t0: instância M1',28),box(130,320,400,170,'M1\n[]','blue'),arrow(550,405,770,405,'salvar Ana e Clara'),box(790,320,600,170,'M1\n[Ana, Clara]','green'),note(130,570,'t1: new RepositorioEmMemoria()',28),box(790,600,600,110,'M2 · []','blue')],
    'Pergunte antes de executar DemoCleanMemoria: o novo objeto encontra quem?', 'Qual será a lista de M2?','Coleção inicial → duas gravações → outro objeto sem ligação a M1.','M1 tem Ana/Clara; M2 tem coleção vazia.')
add(F,'Arquivo: o dado sobrevive à troca do objeto','Persistência em arquivo grava dados fora da memória do objeto, permitindo\nrecuperá-los em uma nova instância.',
    [box(120,310,330,150,'A1\nsalvar Ana / Clara','blue'),box(640,310,360,150,'matriculas.txt\nAna\nClara','yellow'),box(1190,310,310,150,'A2\nlistar()','blue'),arrow(470,385,615,385,'escreve'),arrow(1170,420,1020,420,'lê'),box(1160,595,340,100,'[Ana, Clara]','green'),arrow(1350,475,1350,580,'retorna')],
    'Persistência vem de Files e do arquivo real, não da existência de uma interface.', 'Por que A2 encontra o que A1 salvou?','A1 escreve → arquivo com duas linhas → A2 lê → lista.','O arquivo mantém os dados; o mesmo caso de uso preserva a regra.')
add(F,'Hexagonal: conversas na fronteira','Arquitetura Hexagonal separa o núcleo dos agentes externos por portas de\nentrada e saída, atendidas por adaptadores.',
    [box(120,300,360,140,'AGENTE EXTERNO\nterminal / CSV','blue'),box(650,290,400,200,'NÚCLEO\nexecutar(nome,status)\nregra de matrícula','purple'),box(1190,310,310,130,'ARQUIVO\nAna\nClara','yellow'),arrow(500,370,630,370,'porta de entrada'),arrow(1070,370,1170,370,'porta de saída'),arrow(1170,450,1070,450,'resultado'),note(670,600,'entrada: exterior inicia\nsaída: núcleo solicita',28)],
    'Os seis lados não exigem seis portas nem definem a topologia de deploy.', 'Uma porta de saída pode retornar dados?','Agente inicia executar; núcleo solicita salvar/listar; resultado volta.','Sim. Entrada/saída identifica quem inicia a conversa, não uma via única.')
add(F,'Terminal ou CSV: a mesma operação interna','Uma porta de entrada expõe uma operação da aplicação; adaptadores distintos\npodem acioná-la com a mesma regra.',
    [box(120,290,430,140,'TERMINAL\nBia PENDENTE','blue'),box(120,555,430,140,'CSV\nBia;PENDENTE','blue'),box(750,350,420,200,'mesmo caso de uso\nexecutar("Bia",\nPENDENTE)','purple'),box(1270,390,260,120,'false\nSEM salvar','red'),arrow(565,360,730,400,'argumentos → enum'),arrow(565,620,730,490,'linha → enum'),arrow(1185,445,1255,445)],
    'Uma regra compartilhada de verdade: os dois adaptadores chamam MatricularAluno.', 'Bia pelo CSV consegue escapar?','Duas formas externas → mesmo enum/operação → false.','Não; a recusa vem da mesma regra interna.')
add(F,'Lote versus processos independentes','Processos independentes possuem memórias separadas; um lote sequencial\ncompartilha a instância durante sua execução.',
    [note(120,250,'TERMINAL · um processo por comando',26),box(120,320,420,120,'Ana → true → [Ana]','green'),box(590,320,420,120,'Bia → false → []','red'),box(1060,320,430,120,'Clara → true → [Clara]','green'),note(120,505,'CSV · três linhas no mesmo processo',26)]+row(['Ana → salvar','Bia → recusar','Clara → salvar'],570,['green','red','green']),
    'CSV termina em [Ana, Clara]; os três comandos de terminal não acumulam a memória.', 'Por que o terminal não mostra a lista acumulada?','Compare três coleções separadas com o lote sequencial único.','Cada execução do terminal cria uma memória nova; CSV usa uma instância no lote.')
add(F,'Trocas independentes, regra preservada','Portas preservam as conversas da aplicação enquanto adaptadores de entrada e\narmazenamento podem variar separadamente.',
    [box(120,300,340,140,'CSV / terminal','blue'),box(640,300,450,140,'CONFIRMADO?\nmesma regra','purple'),box(1210,300,310,140,'memória / arquivo','yellow'),arrow(480,370,620,370,'traduz'),arrow(1110,370,1190,370,'salva'),note(180,600,'HTTP futuro: request → adaptador → executar(...)',28),note(180,665,'Bia PENDENTE continua recusada em qualquer entrada.',28)],
    'Clean protege políticas; Hexagonal explicita conversas; injeção monta os colaboradores.', 'Onde ficam conversão HTTP e decisão do pagamento?','Nova entrada à esquerda; condição permanece no centro.','Conversão no adaptador; decisão no domínio/caso de uso.')
# Two responsibility views added without replacing the original mechanisms.
clean_responsibilities = slide('Clean: as responsabilidades ficam em camadas',
    'Clean Architecture separa políticas de detalhes; as dependências de código\napontam para as regras e contratos internos.',[
    box(120,260,1360,490,'','yellow'),note(150,275,'FORA · FRAMEWORKS E DRIVERS',25),
    box(440,330,990,395,'','blue'),note(465,345,'ADAPTADORES · traduzem e persistem',25),
    box(750,405,630,265,'','purple'),note(780,420,'CASOS DE USO · coordenam a ação',24),
    box(950,475,380,105,'','green'),note(975,492,'DOMÍNIO · Pedido',24),note(975,534,'pagamento == CONFIRMADO',22,font=3),
    note(780,590,'MatricularAluno',26),note(780,630,'RepositorioMatriculas · contrato',24),
    note(160,395,'Files / Path',25,font=3),note(160,445,'ler e escrever\no arquivo real',24),
    note(475,485,'Repositorio\nEmArquivo',27),note(475,575,'implementa\no contrato',24),
    note(160,535,'integração\nexterna',24),arrow(685,625,735,625),arrow(895,510,935,510),
    note(725,275,'REGRAS E CONTRATOS NÃO CONHECEM ADAPTADORES',22)
    ],'O núcleo aplica a decisão; adaptadores atendem contratos; Files realiza o acesso ao arquivo.')
hex_responsibilities = slide('Hexagonal: portas delimitam as conversas',
    'Hexagonal mantém os casos de uso no núcleo; portas definem as conversas e\nadaptadores conectam os formatos e tecnologias externos.',[
    box(520,255,620,495,'','gray'),note(560,275,'FRONTEIRA DA APLICAÇÃO',25),
    box(550,325,560,95,'Matricular · entrada\nexecutar(nome, pagamento)','purple'),
    box(595,455,470,150,'MatricularAluno\nPedido: CONFIRMADO?\nrecusa ou solicita salvar','green'),
    box(550,650,560,75,'RepositorioMatriculas · saída','purple'),
    box(110,330,335,215,'EntradaTerminal\nEntradaCsv\ntexto → enum','blue'),
    box(1200,535,300,210,'Repositorio\nEmMemoria\nEmArquivo','yellow'),
    arrow(460,375,535,375),note(140,565,'chamam Matricular',24),
    arrow(830,435,830,445),arrow(830,620,830,635),
    arrow(1135,675,1185,675),arrow(1185,715,1135,715),
    note(1180,420,'FORA · ADAPTADORES',22),
    note(1160,470,'chamada →\ndependência ←',22),
    note(145,670,'mesma entrada:\nBia + PENDENTE\nmesma recusa',26),
    ],'Na execução, o núcleo solicita salvar; no código, o adaptador conhece o contrato interno.')
folder='03-clean-architecture-hexagonal'
for title,newslide,newguide in [
 ('Clean Architecture: proteger a decisão',clean_responsibilities,
  ('Clean: as responsabilidades ficam em camadas','Quem conhece Files? Quem decide o pagamento?',
   'Percorra camadas encaixadas de Files/Path para adaptador, caso de uso e Pedido. Siga as setas de dependência para dentro.',
   'Files pertence à borda; Pedido guarda a regra; MatricularAluno coordena e conhece RepositorioMatriculas.')),
 ('Hexagonal: conversas na fronteira',hex_responsibilities,
  ('Hexagonal: portas delimitam as conversas','Que partes podem mudar quando o pedido chega pelo CSV e é salvo em arquivo?',
   'Aponte fronteira cinza: porta Matricular acima, MatricularAluno dentro e RepositorioMatriculas abaixo; depois os adaptadores fora.',
   'EntradaTerminal/EntradaCsv traduzem; o núcleo decide; repositórios atendem salvar/listar. Chamada e dependência têm sentidos distintos.'))]:
 index=next(i for i,item in enumerate(D[folder]) if item[0]==title)+1
 D[folder].insert(index,newslide);G[folder].insert(index,newguide)

F='06-sistemas-escalaveis'
add(F,'Escalar: localizar o trabalho repetido','Escalabilidade é a capacidade de sustentar mais carga dentro dos objetivos de\nserviço, considerando limites e custos.',
    [box(120,310,400,220,'R1 R2 R3 R4 R5\nGET preço do curso\nmesma consulta','blue'),box(770,320,590,200,'ORIGEM\n5 leituras\n10000 centavos','yellow'),arrow(540,420,745,420,'trabalho repetido'),note(170,640,'Medir: requisições · latência · erros · saturação',28)],
    'Nesta demo contamos operações; não há benchmark de tempo inventado.', 'Qual recurso recebe cinco vezes o mesmo trabalho?','Cinco IDs de request → operação única da origem repetida cinco vezes.','A origem do catálogo; uma técnica deve poupar esse recurso específico.')
add(F,'Vertical ou horizontal: onde vai a carga?','Escala vertical aumenta recursos de uma instância; escala horizontal distribui\na carga entre várias instâncias.',
    [note(120,250,'VERTICAL',28),box(120,330,540,190,'uma instância\nCPU / memória ↑\nR1 R2 R3 R4','blue'),note(850,250,'HORIZONTAL',28),box(850,325,620,100,'A · R1 R3','blue'),box(850,465,620,100,'B · R2 R4','green'),box(850,635,620,95,'mesma origem · 4 leituras','yellow'),arrow(1090,575,1090,620,'ambas consultam')],
    'Mais réplicas web podem manter a mesma pressão na origem compartilhada.', 'Duplicar web reduz automaticamente as consultas ao banco?','Compare uma instância maior com A/B; ambas terminam na mesma origem.','Não. Há mais alvos, mas o trabalho da origem continua.')
add(F,'Sem cache: cinco pedidos, cinco leituras','Sem uma cópia reutilizável, cada consulta repete a leitura na origem, mesmo\nquando o dado solicitado não mudou.',
    [box(120,300,500,330,'R1 → ler → 10000\nR2 → ler → 10000\nR3 → ler → 10000\nR4 → ler → 10000\nR5 → ler → 10000','blue'),box(900,310,540,140,'ORIGEM\npreço = 10000','yellow'),box(900,540,540,110,'contador: 0 → 5','red'),arrow(640,425,880,425,'5 consultas')],
    'O contador aumenta dentro de Catalogo.consultarPreco().', 'Onde contamos o trabalho real?','Cada linha chama ler; depois acompanhe contador0→5.','Na operação de origem, não num total escrito manualmente.')
add(F,'Cache: um miss e quatro hits','Cache guarda uma cópia reutilizável: um miss busca e preenche a cópia; um hit\natende sem consultar a origem.',
    [box(120,290,340,120,'R1 · MISS\ncache vazio','blue'),box(680,290,350,120,'ORIGEM\n10000','yellow'),arrow(480,350,660,350,'ler 1 vez'),box(680,520,350,130,'CACHE\n10000','green'),arrow(850,425,850,500,'preencher'),box(120,525,340,120,'R2 R3 R4 R5\nHIT','blue'),arrow(480,580,660,580,'usar cópia'),box(1160,480,340,160,'5 respostas\n10000\n1 leitura origem','green'),arrow(1045,585,1140,585)],
    'CachePreco usa preco == null para decidir o miss; a demo não implementa TTL.', 'Quantas consultas chegam à origem?','R1 vazio→origem→cópia; R2–R5 param na cópia.','Uma. O reaproveitamento evita quatro leituras.')
add(F,'Cache antigo: econômico e desatualizado','Um dado em cache fica desatualizado quando sua cópia diverge da origem;\natualizar a origem não renova a cópia por si só.',
    [note(120,250,'t0: preenchimento',28),box(120,320,410,150,'CACHE\n10000','green'),box(980,320,490,150,'ORIGEM\n10000 → 12000','yellow'),note(120,545,'t1: consulta seguinte · HIT',28),box(120,605,410,110,'resposta: 10000','red'),arrow(325,490,325,585,'usa cópia'),box(980,605,490,110,'origem atual: 12000','yellow')],
    'TTL limita reutilização conforme política; compra pode exigir preço autoritativo atual.', 'O próximo hit vê12000?','Preço na origem muda à direita; cache à esquerda permanece10000.','Não; o hit não consultou a origem novamente.')
add(F,'Invalidar: remover, buscar, preencher','Invalidação remove uma entrada do cache; a próxima consulta sem cópia busca\nnovamente o dado na origem.',
    row(['invalidar()\n10000 → null','MISS\norigem: 12000','cópia: 12000\nresposta: 12000'],330,['red','yellow','green'])+[box(590,605,500,100,'leituras origem: 1 → 2','purple')],
    'Alteração da origem e invalidação são operações separadas nesta demo.', 'Por que o contador agora chega a dois?','Remover cópia→miss→segunda leitura→novo valor guardado.','O primeiro preenchimento e a consulta após invalidar são as duas leituras.')
add(F,'CDN: hit na borda, miss até a origem','Uma CDN distribui conteúdo por pontos de presença: hits atendem na borda e\nmisses buscam o conteúdo na origem.',
    [note(120,250,'HIT · /curso.png já está na borda',26)]+row(['cliente\nGET /curso.png','BORDA\ncópia curso.png','imagem entregue\norigem não lida'],310,['blue','green','green'])+[note(120,535,'MISS · /nova.png ainda não está na borda',26)]+row(['cliente\nGET /nova.png','BORDA vazia\nconsulta origem','ORIGEM nova.png\npreenche borda'],585,['blue','purple','yellow']),
    'Resposta privada exige política própria; CDN não elimina consultas da API de matrícula.', 'Qual caminho poupa a origem?','Compare mesma posição borda: preenchida no hit, vazia no miss.','Hit termina na borda; miss vai à origem e traz conteúdo.')
add(F,'Balancear: alternar destinos por request','Balanceamento de carga distribui requisições entre alvos disponíveis; round\nrobin alterna os destinos em sequência.',
    [box(120,320,330,180,'R1 R2 R3 R4\nGET /catalogo','blue'),box(590,320,350,180,'BALANCEADOR\nround robin','purple'),arrow(470,405,570,405,'rota igual'),box(1130,280,370,150,'A\nR1 · R3','blue'),box(1130,560,370,150,'B\nR2 · R4','green'),arrow(960,370,1110,350,'1º e 3º'),arrow(960,450,1110,615,'2º e 4º')],
    'Esquema conceitual: sem balanceador real; health checks ajudam a escolher alvos.', 'Qual réplica recebe R3?','Siga IDs em ordem alternada: R1A,R2B,R3A,R4B.','A. Distribuir não elimina gargalo compartilhado nem garante sucesso.')
add(F,'Estado local: a sessão não acompanha a troca','Estado local de sessão pertence a uma réplica; outra réplica com seu próprio\narmazenamento pode não encontrar a mesma chave.',
    [box(120,300,370,160,'login em A\nsessao-ana → Ana','blue'),box(680,270,370,190,'A · mapa local\nsessao-ana: Ana','green'),box(1120,270,370,190,'B · mapa local\n{}','red'),arrow(510,370,660,370,'salvar'),box(120,580,370,120,'pedido seguinte\nchave sessao-ana','blue'),arrow(510,635,1100,635,'consulta B'),arrow(1305,475,1305,575),box(1120,590,370,100,'B: SEM SESSÃO','red')],
    'DemoEstadoLocal cria dois objetos Sessoes separados dentro da mesma JVM.', 'O login em A garante que B encontre Ana?','Chave salva no mapaA; mesmo identificador consultado no mapaB vazio.','Não. Afinidade sticky preserva dependência de A, não compartilhamento.')
add(F,'Estado compartilhado: duas consultas, um registro','Stateless significa atender sem depender do estado local de pedidos\nanteriores; o sistema pode manter estado compartilhado.',
    [box(130,300,360,130,'A\nlogin sessao-ana','blue'),box(1100,300,370,130,'B\nacessar sessao-ana','green'),box(570,550,460,170,'mesmo Sessoes\nsessao-ana → Ana','purple'),arrow(320,445,580,525),arrow(1250,445,1015,525),note(370,520,'salvar',24),note(1110,520,'consultar',24),note(130,650,'A: Ana',30),note(1160,650,'B: Ana',30)],
    'Demo: um objeto na mesma JVM, não Redis. Estado entre processos exige outro mecanismo.', 'Stateless significa que não existe sessão?','A e B apontam para o mesmo registro da chave; retornoAna nas duas.','Existe estado, mas a réplica não depende do mapa local de pedidos anteriores.')
add(F,'Rate limit: chave e janela visíveis','Rate limiting controla quantas operações uma chave pode iniciar em um\nintervalo; janela fixa reinicia a cota na virada.',
    [note(120,250,'tempo: 0s',30),note(800,250,'59s',30),note(995,250,'60s',30),note(935,280,'|',48),arrow(120,325,1460,325),box(120,390,790,140,'Ana · janela 0\nR1 ✓   R2 ✓   R3 ✓   R4 ×   R5 ×','blue'),box(1000,390,480,140,'Ana · janela 1\nR6 ✓','green'),box(120,615,790,110,'Bia · janela 0 · R1 ✓ · cota própria','purple'),box(1000,615,480,110,'virada: contagens limpas','yellow')],
    'Boolean na demo; adaptador HTTP pode gerar 429. Sem concorrência distribuída.', 'Bia perde a cota porque Ana usou três?','ChaveAna0→3→recusa; chaveBia separada; t60 abre nova janela.','Não. A cota é por chave; Ana volta a passar em outra janela.')
add(F,'Limites locais: três mais três não são três','Um limite local usa contadores de uma instância; um limite global precisa\ncoordenar a cota entre as instâncias participantes.',
    [box(120,300,490,180,'limitador A · Ana\nR1 ✓ R3 ✓ R5 ✓\ncontador = 3','blue'),box(990,300,490,180,'limitador B · Ana\nR2 ✓ R4 ✓ R6 ✓\ncontador = 3','green'),arrow(640,580,965,580,'somar admissões'),note(430,650,'MESMA chave · 6 admitidas · limite global não garantido',28)],
    'Janela fixa permite rajadas na virada. Limite protege capacidade; não a cria.', 'Alternar seis pedidos entre A/B aceita quantos?','Três marcas emA e três emB; some os dois contadores independentes.','Seis. Para cota global é necessário coordenar o estado entre processos.')
add(F,'Escolher técnica pelo recurso protegido','Uma técnica de escala atua sobre um recurso específico e introduz custos; a\nescolha depende do gargalo medido.',
    [box(120,280,570,160,'leituras repetidas\ncache → 5 leituras viram 1','green'),box(850,280,620,160,'imagem pública\nCDN → hit para na borda','blue'),box(120,520,570,170,'sessao-ana entre A/B\nestado compartilhado → Ana','purple'),box(850,520,620,170,'rajada por cliente\nrate limit → 3 passam / 2 não','yellow')],
    'Medir → localizar → mudar → observar efeito/custo. Cache não corrige sessão perdida.', 'Qual técnica altera o recurso que realmente está pressionado?','Relacione cada entrada ao efeito concreto; recupere stale/cota/armazenamento como custos.','Cache poupa origem; CDN serve conteúdo; balanceamento distribui; estado e limites exigem coordenação.')

def clear_arrow_labels(items):
    # Keep labels next to their arrows while ensuring no text crosses boxes/notes.
    occupied=[]
    def bounds(item):
        if item['kind']=='box': return (item['x'],item['y'],item['w'],item['h'])
        if item['kind']=='text':
            lines=item['text'].split('\n');return (item['x'],item['y'],max(map(len,lines))*item['size']*.62,len(lines)*item['size']*1.25)
    for item in items:
        b=bounds(item)
        if b:occupied.append(b)
    def free(x,y,w,h):
        return 100<=x and x+w<=1530 and 240<=y and y+h<=760 and not any(x<bx+bw+8 and x+w>bx-8 and y<by+bh+8 and y+h>by-8 for bx,by,bw,bh in occupied)
    extra=[]
    for item in items:
        if item['kind']!='arrow' or not item['text']:continue
        text=item['text'];w=len(text)*24*.62;h=30
        x=min(item['x'],item['x2']);y=min(item['y'],item['y2'])-48
        if abs(item['x2']-item['x']) < abs(item['y2']-item['y']): x+=20
        if not free(x,y,w,h):
            candidates=[(xx,yy) for xx in range(100,int(1530-w),10) for yy in range(240,731,10) if free(xx,yy,w,h)]
            assert candidates, ('no clear label position',text)
            x,y=min(candidates,key=lambda p:(p[0]-x)**2+(p[1]-y)**2)
        item['text']=''
        extra.append(note(x,y,text,24))
        occupied.append((x,y,w,h))
    return items+extra

if __name__=='__main__':
    import sys
    chosen=set(sys.argv[1:])
    for folder,slides in D.items():
        if chosen and folder not in chosen: continue
        slides=[(t,'\n'.join(textwrap.wrap(sub,78)),clear_arrow_labels(items),'\n'.join(textwrap.wrap(footer,86))) for t,sub,items,footer in slides]
        D[folder]=slides
        generate(folder,slides)
        path=__import__('pathlib').Path(__file__).resolve().parents[1]/folder/'roteiro.md'
        original=path.read_text().split('\n## Guia visual revisado — mecanismo por slide')[0]
        guide='\n## Guia visual revisado — mecanismo por slide\n\nEsta sequência substitui os números de slides da preparação anterior. Mantém os conceitos e práticas; os tempos anteriores são referências de condução. Resultados ilustrados acompanham as demos ou estão identificados como esquemas conceituais.\n'
        for i,(title,q,route,result) in enumerate(G[folder],1):
            guide+=f'\n### Slide {i:02d} — {title}\n\n- **Pergunta:** {q}\n- **Apontar:** {route}\n- **Resultado:** {result}\n'
        path.write_text(original+guide)
