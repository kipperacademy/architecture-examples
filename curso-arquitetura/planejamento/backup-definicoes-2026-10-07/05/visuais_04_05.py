from visual_engine import *

def chip(x,y,txt,color='blue',w=210,h=70):return box(x,y,w,h,txt,color)
def table(x,y,title,rows,color='blue',w=500):
 out=[note(x,y,title,27,BLACK)]
 for i,row in enumerate(rows):out.append(box(x,y+48+i*75,w,65,row,color))
 return out

def packet(x,y,txt,color='blue'):return chip(x,y,txt,color,200,90)
D={}
D['04-monolito-modular']=[
slide('Uma aplicação, duas capacidades','Módulos reúnem regras e dados; monólito define o que é implantado junto.',[
 box(160,280,1240,330,'','gray'),note(200,300,'processo da escola',27,BLACK),
 box(220,370,430,170,'','blue'),note(250,395,'Financeiro',32,BLACK),note(250,448,'confirmadas = {pedido-ana}',23),
 box(950,370,390,170,'','green'),note(980,395,'Acadêmico',32,BLACK),note(980,448,'alunas = [Ana]',26),
 arrow(930,430,670,430,'consulta local'),
 chip(250,665,'alteração no Financeiro','yellow',390),arrow(660,700,820,700,'build'),chip(840,665,'1 artefato → 1 deploy','purple',510)],
 'Mudar um módulo recompila a aplicação; não cria uma chamada de rede.'),
slide('Uma regra atravessa o contrato','Pagamento confirmado permite a matrícula; o Financeiro responde sem expor seu conjunto.',[
 packet(100,300,'pedido-ana'),packet(100,570,'pedido-bia'),
 box(430,275,660,390,'','blue'),note(460,302,'Cobrancas.estaConfirmado(pedido)',28,BLACK),
 note(475,380,'confirmadas',24,GRAY),chip(480,425,'pedido-ana','blue',310),
 arrow(300,335,420,335,'consulta'),arrow(300,605,420,605,'consulta'),
 arrow(1100,355,1250,355,'true'),chip(1260,310,'adiciona Ana','green',245,90),
 arrow(1100,585,1250,585,'false'),chip(1260,540,'não adiciona Bia','red',245,100)],
 'Resultado observado em DemoModulos: Matrículas: [Ana]. A regra vive no Acadêmico.'),
slide('A fronteira também aparece no código','O cliente recebe uma resposta; o estado mutável continua privado no módulo.',[
 box(110,285,590,360,'','green'),note(140,315,'Matriculas.java',29,BLACK),
 note(140,395,'if (cobrancas\n    .estaConfirmado(pedido))\n    alunas.add(aluna);',27,BLACK,font=3),
 box(900,285,600,360,'','blue'),note(930,315,'Cobrancas.java',29,BLACK),
 note(930,395,'private final Set<String>\n    confirmadas = new HashSet<>();',24,BLACK,font=3),
 arrow(720,420,880,420,'chamada'),arrow(880,595,720,595,'boolean'),
 note(240,710,'Pode mudar a estrutura interna → o retorno boolean continua igual.',28)],
 'Contrato concreto desta demo: dependência de Cobrancas. Separar módulos não elimina toda dependência.'),
slide('Banco compartilhado, escritas com dono','Uma fronteira de módulo evita que outra capacidade altere seus dados por fora.',[
 chip(130,275,'Financeiro','blue',480,85),chip(990,275,'Acadêmico','green',480,85),
 box(100,475,1400,230,'','gray'),
 *table(140,490,'financeiro_recebimentos',['pedido-ana'],'blue',500),
 *table(940,490,'academico_matriculas',['pedido-ana | Ana | vaga 1'],'green',510),
 arrow(350,375,350,465,'INSERT próprio'),arrow(1230,375,1230,465,'INSERT próprio'),
 arrow(670,330,950,330,'contrato público'),note(645,650,'mesmo banco físico',24,GRAY)],
 'Prefixos de tabela documentam a propriedade. Controle de acesso exige configuração adicional.'),
slide('Autocommit deixa um resultado parcial','A primeira escrita confirma antes de a segunda descobrir que a vaga está ocupada.',[
 note(110,250,'ANTES',25,GRAY),note(625,250,'1. INSERT recebimento',25,BLACK),note(1120,250,'2. INSERT matrícula',25,BLACK),
 *table(100,305,'Recebimentos',['pedido-ana'],'blue',380),
 *table(610,305,'Recebimentos',['pedido-ana','pedido-bia ✓'],'blue',380),
 *table(1110,305,'Recebimentos',['pedido-ana','pedido-bia ✓'],'blue',380),
 arrow(495,420,595,420,'commit'),arrow(1010,420,1095,420),
 *table(1100,570,'Matrículas',['Ana | vaga 1'],'green',390),
 chip(100,595,'Bia pede vaga 1','yellow',380,90),arrow(500,640,780,640,'tenta gravar'),chip(805,595,'UNIQUE falha','red',255,90)],
 'Observado sem-transacao: recebimentos [pedido-ana, pedido-bia]; matrículas [Ana].'),
slide('BEGIN faz as escritas participarem da mesma unidade','A falha desfaz também o recebimento que ainda não foi confirmado.',[
 note(110,250,'ANTES',25,GRAY),note(580,250,'BEGIN → escritas',25,BLACK),note(1110,250,'ROLLBACK',25,BLACK),
 *table(100,305,'Recebimentos',['pedido-ana'],'blue',360),
 box(555,285,470,430,'','gray'),note(590,300,'mesma conexão',26,BLACK),chip(590,360,'pedido-ana ✓ prévio','blue',390,70),note(590,445,'nova escrita pendente',23,GRAY),chip(590,485,'pedido-bia','yellow',390,65),
 chip(590,565,'vaga 1: UNIQUE falha','red',390,80),
 *table(1120,305,'Recebimentos',['pedido-ana'],'blue',360),*table(1120,555,'Matrículas',['Ana | vaga 1'],'green',360),
 arrow(475,420,540,420),arrow(1040,420,1100,420,'desfaz')],
 'Observado com-transacao: só Ana permanece nas duas tabelas. Mesma conexão, mesma transação.'),
slide('O mesmo limite permite confirmar as duas escritas','Se ambas forem aceitas, COMMIT torna a unidade confirmada.',[
 box(180,275,760,420,'','yellow'),note(215,300,'UMA TRANSAÇÃO',28,BLACK),
 chip(230,390,'INSERT recebimento: aceita','blue',650,90),chip(230,535,'INSERT matrícula: aceita','green',650,90),
 arrow(960,500,1120,500,'COMMIT'),
 box(1150,345,340,295,'','green'),note(1180,390,'recebimento ✓\n\nmatrícula ✓',29,BLACK)],
 'Caminho de sucesso ilustrativo. Na demo executada, a vaga 1 já existe e o caminho é ROLLBACK.'),
slide('Rollback local não alcança a cobrança externa','A resposta remota não faz parte do commit do seu banco.',[
 box(120,290,710,365,'','gray'),note(160,310,'banco da escola',28,BLACK),
 chip(170,405,'INSERT matrícula','green',290,90),chip(500,405,'ROLLBACK','red',260,90),
 box(1040,290,460,365,'','yellow'),note(1070,310,'provedor remoto',28,BLACK),chip(1080,425,'cobrança confirmada','yellow',380,100),
 arrow(840,390,1020,390,'HTTP: cobrar'),note(885,540,'✕',45,'#c92a2a'),
 note(245,710,'A linha local desaparece.',27),note(1000,710,'O efeito remoto continua.',27)],
 'Cenário ilustrativo: compensação/reconciliação é outra operação. A demo SQL não cobra dinheiro.'),
slide('Preveja o estado final, depois execute','Mesma Bia, mesma vaga ocupada: muda somente o limite da transação.',[
 note(120,270,'AUTOCOMMIT',28,BLACK),note(900,270,'BEGIN + ROLLBACK',28,BLACK),
 *table(120,335,'Recebimentos após erro',['pedido-ana','pedido-bia ?'],'blue',560),
 *table(900,335,'Recebimentos após erro',['pedido-ana','pedido-bia ?'],'blue',560),
 chip(120,620,'Matrícula: Ana na vaga 1','green',560,95),chip(900,620,'Matrícula: Ana na vaga 1','green',560,95)],
 'Rode sem-transacao e com-transacao. Aponte qual escrita já havia sido confirmada em cada caso.')]

D['05-localhost-producao']=[
slide('Código precisa virar um processo acessível','A requisição só recebe resposta se alcançar um processo escutando naquela porta.',[
 chip(100,350,'Servidor.java','blue',330,110),arrow(450,405,580,405,'javac'),chip(600,350,'Servidor.class','purple',350,110),
 arrow(970,405,1100,405,'java'),box(1120,290,370,250,'','green'),note(1150,325,'processo JVM',30,BLACK),note(1150,400,'escuta :8080',28),
 packet(150,625,'GET /curso'),arrow(360,660,1280,660,'requisição pela rede'),arrow(1300,650,1300,550),
 note(670,725,'resposta: instancia=local | visitas=1',28)],
 'Código é o programa; processo é a execução que guarda estado e atende requisições.'),
slide('Localhost volta para a própria máquina','O mesmo endereço não atravessa da máquina da aluna até a sua.',[
 box(100,290,620,405,'','blue'),note(130,315,'computador da professora',30,BLACK),packet(145,400,'navegador'),chip(445,400,'JVM :8080','green',235,90),arrow(345,445,420,445,'local'),
 box(880,290,620,405,'','purple'),note(910,315,'computador da aluna',30,BLACK),packet(920,400,'navegador'),chip(1210,400,'porta vazia','red',235,90),arrow(1125,445,1195,445,'local'),
 note(150,590,'127.0.0.1:8080\nresposta da professora',27),note(935,590,'127.0.0.1:8080\nninguém escutando aqui',27)],
 'Para acessar outra máquina, é preciso o endereço dela e um caminho de rede permitido.'),
slide('Uma VM recebe seu próprio sistema operacional','O hipervisor distribui recursos da máquina física para ambientes separados.',[
 box(130,270,1340,440,'','gray'),
 box(180,310,550,285,'','blue'),chip(215,345,'processo Java','blue',475,75),chip(215,475,'SO convidado A + kernel A','purple',475,80),
 box(870,310,550,285,'','green'),chip(905,345,'outro processo','green',475,75),chip(905,475,'SO convidado B + kernel B','purple',475,80),
 chip(180,635,'HIPERVISOR → CPU, memória e disco físicos','gray',1240,60),
 arrow(445,575,445,620),arrow(1130,575,1130,620),note(500,602,'usa recursos',22),note(1190,602,'usa recursos',22)],
 'VM A e VM B têm kernels próprios. Servidor pode nomear a máquina ou o processo que atende.'),
slide('A imagem inicia processos; não guarda a execução','Dois containers usam a mesma imagem e mantêm memórias distintas.',[
 chip(100,345,'imagem\nclasses + JRE','yellow',335,160),
 box(650,270,850,440,'','gray'),
 box(700,310,325,250,'','blue'),note(730,335,'container A',28,BLACK),note(730,420,'JVM\nvisitas = 2',29),
 box(1125,310,325,250,'','green'),note(1155,335,'container B',28,BLACK),note(1155,420,'JVM\nvisitas = 0',29),
 arrow(455,365,680,365,'run A'),arrow(350,515,350,590),arrow(350,590,1280,590),note(410,540,'run B',24),arrow(1280,590,1280,570),
 chip(700,625,'kernel Linux compartilhado','purple',750,60)],
 'No Mac, Docker Desktop fornece o host Linux em uma VM. Imagem não é um contador persistido.'),
slide('Publicar a porta liga dois endereços diferentes','O host recebe em 8081 e encaminha para o processo na porta 8080 do container.',[
 box(100,285,1400,410,'','gray'),note(135,310,'HOST',28,BLACK),
 packet(150,425,'curl /curso'),chip(465,405,'127.0.0.1\nporta 8081','blue',300,130),
 box(1000,370,430,230,'','green'),note(1030,390,'CONTAINER',27,BLACK),note(1030,455,'Java escuta\n0.0.0.0:8080',29),
 arrow(355,465,445,465),arrow(785,465,980,465,'publish'),
 note(240,630,'-p 127.0.0.1:8081:8080',32,PURPLE,font=3)],
 'EXPOSE 8080 registra a intenção na imagem; o mapeamento é criado por -p ao iniciar.'),
slide('A configuração entra antes de atender','O mesmo código lê o ambiente e identifica qual processo respondeu.',[
 chip(130,280,'PORT=8080\nINSTANCE=A','blue',430,130),chip(980,280,'PORT=8081\nINSTANCE=B','green',430,130),
 chip(650,315,'mesmo\nServidor.class','purple',270,150),
 arrow(345,430,345,515,'inicia A'),arrow(1195,430,1195,515,'inicia B'),
 chip(130,540,'GET :8080/curso\ninstancia=A | visitas=1','blue',540,140),chip(890,540,'GET :8081/curso\ninstancia=B | visitas=1','green',570,140)],
 'Escolher a porta manualmente não é balanceamento. A configuração muda, o handler permanece igual.'),
slide('Reiniciar cria um contador novo','AtomicInteger pertence à memória do processo que acabou de nascer.',[
 box(100,290,650,410,'','blue'),note(135,320,'processo A',29,BLACK),
 chip(145,420,'GET 1 → visitas=1','blue',540,80),chip(145,555,'GET 2 → visitas=2','blue',540,80),
 arrow(775,460,1000,460,'encerra → inicia'),
 box(1040,290,460,410,'','green'),note(1070,320,'novo processo',29,BLACK),
 note(1090,405,'memória começa em 0',25),chip(1080,555,'GET 1 → visitas=1','green',370,80)],
 'Resultado esperado para o ensaio HTTP. Reempacotar em container não muda a vida útil dessa memória.'),
slide('Build e execução têm papéis separados','O estágio de build compila; a imagem final recebe classes e o runtime.',[
 box(100,285,620,380,'','blue'),note(130,310,'build · JDK 21',30,BLACK),
 chip(150,390,'Servidor.java','blue',490,75),arrow(395,480,395,535,'javac'),chip(150,550,'out/Servidor.class','purple',490,75),
 box(940,285,560,380,'','green'),note(970,310,'imagem final · JRE 21',30,BLACK),
 chip(990,420,'/app/Servidor.class','purple',450,90),chip(990,555,'java -cp /app Servidor','green',450,75),
 arrow(735,470,925,470,'COPY --from')],
 'O Dockerfile usa dois estágios. A imagem final não precisa carregar o compilador nem o fonte.'),
slide('Do nome público até a aplicação','DNS resolve o nome; HTTPS e roteamento levam a requisição até a aplicação.',[
 packet(100,310,'nome do site'),arrow(305,345,450,345,'consulta'),chip(475,290,'DNS\nendereço do serviço','yellow',500,110),
 arrow(660,415,250,470),note(355,395,'IP resolvido',24),arrow(250,480,250,520),packet(100,535,'GET /curso'),arrow(305,570,530,570,'HTTPS'),chip(560,510,'entrada pública\nproxy / roteamento','purple',420,140),
 arrow(1000,580,1120,580,'encaminha'),chip(1140,510,'JVM\n/curso','green',330,140),
 arrow(1300,490,1300,390),note(1330,420,'/health',23),chip(1140,290,'200 · ok','green',330,80)],
 'Topologia conceitual: esta aula não implantou um serviço público. Logs, acesso e persistência também precisam de operação.'),
slide('Encontre onde a requisição parou','A mesma sequência permite localizar falhas sem adivinhar.',[
 chip(100,310,'endereço','blue',300,100),chip(650,310,'porta','purple',300,100),chip(1200,310,'processo','green',300,100),
 arrow(425,360,620,360,'roteia'),arrow(975,360,1175,360,'entrega'),
 chip(100,520,'localhost da aluna\n≠ máquina da professora','red',390,140),
 chip(600,520,'sem -p\nsem porta publicada','red',390,140),
 chip(1100,520,'processo encerrado\nninguém atende','red',390,140)],
 'Faça a aluna apontar a etapa que falha e explicar por que reiniciar também zera visitas.')]

import textwrap
for slides in D.values():
 for _,_,items,_ in slides:
  for item in items:
   if item['kind']=='box' and item['text']:
    limit=int((item['w']-50)/(22*.62))
    item['text']='\n'.join('\n'.join(textwrap.wrap(line,limit)) for line in item['text'].split('\n'))

if __name__=='__main__':
 for folder,slides in D.items():generate(folder,slides)
