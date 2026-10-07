from pathlib import Path
import json, shutil
base=Path.cwd()
out=base/'studio/audio'
lessons=sorted(p for p in base.glob('0*') if p.is_dir())
scripts={}
scripts[1]=(lessons[0]/'preparacao-para-gravar.txt').read_text().replace('A classe Demo escolhe o canal','O main de cada demo escolhe o canal').replace('A montagem muda na Demo.','A montagem muda no main.')
start=scripts[1].index('Na prática, comece por')
end=scripts[1].index('Tudo é uma simulação local.')
scripts[1]=scripts[1][:start]+'''Na prática, deixe os mains separados em abas. Abra Demo Acoplamento e Matriculas Acopladas para mostrar a ordem: consultar, enviar, liberar. Antes da falha, rode Demo Email. Com e-mail disponível, a versão organizada libera três acessos e não deixa avisos pendentes.

Peça a previsão e execute Demo Acoplamento: com os três pagamentos confirmados e o e-mail indisponível, ficam zero acessos. Depois execute Demo Desacoplamento: mesmos pedidos, mesma indisponibilidade, três acessos e três avisos pendentes. Abra Matriculas e explique a causa: ela registra o acesso antes do envio e trata a falha esperada. Interfaces sozinhas não produzem tolerância a falhas. A versão acoplada também poderia tratar corretamente essa exceção.

Na Demo Desacoplamento, mostre o tipo Notificador e a construção de Email com falso. Troque somente essa linha pela criação de WhatsApp; preserve a montagem de Matriculas. Preveja, execute e mostre três acessos, agora sem pendências. Demo WhatsApp já oferece essa alternativa preparada. Por fim, rode Demo Pagamento Pendente: zero acessos e zero avisos pendentes. A exigência do pagamento continua válida.

'''+scripts[1][end:]
scripts[3]='''Fernanda, esta aula tem quatro blocos de cinco minutos: fundamentos de Clean Architecture, prática de Clean, fundamentos de Hexagonal e prática de Hexagonal. Comece pelos modelos gerais e só depois apresente a escola. Quem chegou diretamente a este vídeo precisa entender o contexto antes de ouvir os nomes das classes.

Clean organiza a aplicação para preservar políticas de negócio quando mudam mecanismos externos. Entidades reúnem estado e comportamento do domínio; não significam necessariamente tabelas de banco. Casos de uso representam intenções realizadas pela aplicação e coordenam regras e colaboradores. Adaptadores traduzem formatos entre exterior e aplicação. Frameworks e drivers ficam na borda, como servidor web, sistema de arquivos e biblioteca de banco. O modelo não exige determinado número de pastas.

A regra de dependência é o ponto principal: o código externo conhece as políticas e contratos internos. O núcleo não importa detalhes técnicos externos. Separe isso da direção das chamadas em execução. Injeção entrega um colaborador pelo construtor; inversão organiza quem conhece o contrato de quem.

Agora apresente a escola: recebe nome e situação do pagamento e só registra matrículas confirmadas. Ana e Clara estão confirmadas; Bia está pendente. O desafio é trocar armazenamento sem reescrever essa decisão. Abra Pedido, Matricular Aluno e Repositório Matrículas. Mostre a condição do domínio, o retorno antecipado e a chamada para salvar.

Em Demo Clean Memória, a lista contém Ana e Clara. Peça a previsão sobre uma nova instância do repositório: ela começa vazia. Depois abra Demo Clean Arquivo. Mesmos pedidos e caso de uso; muda a implementação escolhida. Outra instância recupera Ana e Clara. Abra o arquivo real de matrículas na tela. A persistência vem da implementação com arquivo, não da existência da interface. Prepare a saída limpa antes de gravar para evitar duplicatas de execuções anteriores.

Na segunda teoria, Hexagonal organiza o núcleo e suas conversas com o exterior. Os seis lados são visuais, não exigem seis portas. Porta de entrada expressa uma capacidade que agentes externos acionam. Porta de saída expressa uma necessidade iniciada pelo núcleo. Entrada e saída indicam quem começa a conversa; ambas podem retornar dados. Adaptadores traduzem tecnologias e formatos para esses contratos.

Aplicando à escola, Matricular é a porta de entrada; Matricular Aluno a implementa. Terminal e CSV a chamam. Repositório Matrículas é a porta de saída; memória e arquivo atendem ao contrato.

Na prática final, abra Demo Hexagonal Terminal. Ana entra; Bia é recusada. Cada comando começa com memória nova. Depois mostre os três pedidos do CSV e peça uma previsão. Demo Hexagonal CSV registra Ana e Clara, usando a mesma regra. Reconstrua o caminho de Bia: formato válido, chamada válida, rejeição pelo pagamento pendente antes de salvar. Encerre perguntando onde ficariam a conversão de um request HTTP e a decisão do pagamento: tradução no adaptador, decisão no núcleo. As demos são locais e não implementam banco concorrente nem importação atômica.
'''
scripts[4]='''Fernanda, nesta aula o objetivo é separar capacidades de negócio dentro de uma aplicação implantada como uma unidade e mostrar onde uma transação local garante consistência. A proposta é vinte e cinco minutos: dez de conceitos, doze de prática e três de recuperação. Comece apresentando a escola, sem depender das aulas anteriores. Ela registra recebimentos e libera matrículas. Financeiro conhece a confirmação do pedido; Acadêmico decide o acesso.

A pergunta condutora é: como separar responsabilidades sem criar serviços de rede e sem perder consistência entre duas escritas? Monólito significa uma unidade de implantação. Ele pode ter módulos, réplicas e banco externo. Modularização organiza capacidades e suas interfaces. Controller, service e repository são camadas técnicas; podem existir dentro de cada módulo. Nomes de pastas sozinhos não impõem fronteiras.

Mostre a dependência permitida: Matrículas pergunta a Cobranças se um pedido está confirmado. O mapa de confirmações é privado; o consumidor recebe a informação necessária, não a coleção mutável inteira. Esse contrato cria um acoplamento escolhido. Não prometa isolamento completo só por usar pacotes Java.

Depois apresente donos dos dados. Um banco físico pode conter tabelas pertencentes a módulos diferentes. Acadêmico não deveria escrever diretamente nos recebimentos. Prefixos de tabelas documentam propriedade nesta demo, mas não implementam permissões. Em seguida, explique a transação: duas alterações relacionadas podem precisar confirmar juntas. Uma conexão e um banco participam da unidade de trabalho. Estar no mesmo processo ou no mesmo método não gera atomicidade automaticamente.

Na primeira prática, abra Demo Módulos, Matrículas e Cobranças. A montagem instancia Financeiro e o injeta em Acadêmico. Somente o pedido de Ana é confirmado. Peça a previsão para Ana e Bia e rode a opção módulos do script. A lista final contém Ana. Essa execução Java mostra fronteira e visibilidade, com estado em memória; ainda não usa SQLite.

Na segunda prática, abra a estrutura SQL. Existe uma única vaga, já ocupada por Ana. Vamos inserir o recebimento de Bia e tentar colocá-la nessa mesma vaga. A segunda escrita falha pela restrição de unicidade. Pergunte: o recebimento de Bia continua salvo? Abra o bloco da transação no arquivo Python. Ele serve apenas como driver SQLite da biblioteca padrão para executar uma transação real sem baixar dependências Java.

Rode sem transação: autocommit preserva os recebimentos de Ana e Bia, mas a matrícula continua sendo apenas Ana. Rode com transação: a mesma falha leva ao rollback e o recebimento de Bia desaparece. Cada comando usa um banco novo em memória. A mudança é o limite da transação, não a regra de vaga.

Reconstrua a causa sobre as duas escritas. O registro de recebimento é uma linha local fictícia; rollback de SQL não estorna cobrança feita em um provedor por HTTP. A garantia termina na fronteira dessa transação. Termine perguntando: posso ter dez módulos e um deploy? Sim. Dois inserts no mesmo método são sempre atômicos? É preciso localizar a transação e seus participantes. A organização lógica e a distribuição operacional são decisões diferentes.
'''
scripts[5]='''Fernanda, o fio desta aula é acompanhar o caminho entre endereço, porta e processo e entender o que muda quando a aplicação precisa continuar respondendo fora do seu terminal. A proposta é vinte e cinco minutos. Apresente a escola oferecendo uma página de curso. Cada acesso devolve o nome da instância e um contador local de visitas. Não há login, banco ou pagamento.

Comece pelo significado de deploy: disponibilizar e operar uma versão num ambiente acessível aos usuários. Localhost aponta para o ambiente de quem faz a chamada. O localhost da aluna não é seu computador. A porta identifica o serviço naquele endereço, e precisa existir um processo escutando no destino correto.

Servidor pode ser a máquina ou o processo que atende. Uma máquina virtual executa um sistema operacional convidado sobre virtualização. Container é uma execução isolada iniciada a partir de uma imagem. Containers Linux compartilham o kernel do host Linux. No macOS, o Docker Desktop usa um ambiente Linux virtualizado; não diga que o container Linux compartilha diretamente o kernel do Mac. Máquina virtual e container podem ser combinados.

Explique a publicação de portas com dois números visíveis. A aplicação do container escuta em oito mil e oitenta; o computador pode publicar oito mil e oitenta e um. A instrução EXPOSE documenta a porta, mas não a publica sozinha. Configuração pode alterar o nome da instância e a porta sem editar a regra. Imagem também não torna o estado em memória durável.

Na prática, abra Servidor Java e mostre criação do servidor, handler de curso e contador. Num terminal, inicie a instância A na porta oito mil e oitenta pelo script da aula. No outro, faça duas chamadas para curso: visitas um, depois dois. Consulte health: retorna ok. Esse health só comprova que o handler responde, não verifica dependências.

Peça uma previsão antes de parar com control C e reiniciar. O próximo acesso volta a um. A causa é um novo contador em memória no novo processo, não cache do navegador. Em outra porta, inicie a instância B e compare os nomes e contadores independentes. Você escolheu as portas manualmente; essa comparação ainda não demonstra um balanceador.

Para o bloco Docker, abra o Dockerfile: um estágio compila, outro recebe classes e runtime. A execução usa um usuário sem privilégios e escuta nas interfaces do container. Pare a instância B antes de reutilizar a porta oito mil e oitenta e um. Execute build e run apenas se o Docker estiver funcionando e o bloco tiver sido ensaiado. O material atual registra daemon desligado e esse bloco pendente de execução; não apresente uma saída inventada. A primeira construção também pode precisar baixar a imagem.

Conclua com o caminho DNS, HTTPS, proxy e aplicação saudável. O servidor local desta aula não foi publicado na internet. Produção exige ambiente, artefato, rede, configuração, observação, teste da versão e estratégia de retorno. Recupere três perguntas: por que a aluna não abre meu localhost, por que EXPOSE não basta e por que as visitas sumiram no restart? As respostas vêm do endereço, do roteamento e do estado do processo.
'''
scripts[6]='''Fernanda, nesta aula o aluno precisa escolher uma técnica de escala pelo recurso pressionado e reconhecer o custo que ela introduz. A proposta é trinta minutos. Contextualize a escola: há consultas repetidas ao preço de um curso e uma aluna autenticada navegando entre pedidos. Catálogo público e sessão privada têm necessidades distintas.

Escalar significa sustentar mais carga dentro dos objetivos de serviço. Antes de multiplicar instâncias, observe requisições, latência, erros e saturação. A demo contará operações, não medirá um benchmark de tempo. Escala vertical aumenta recursos de uma instância; horizontal distribui entre instâncias. Se o gargalo está na origem compartilhada, mais servidores podem pressioná-la ainda mais.

Cache guarda uma cópia reaproveitável. Na falta da cópia, busca a origem; quando encontra, reutiliza. Esse mesmo mecanismo economiza consultas e pode servir um valor antigo. TTL e invalidação são políticas diferentes; aqui só teremos invalidação explícita. Uma compra que exige preço atual precisa de uma verificação autoritativa apropriada.

CDN entrega conteúdo pela borda segundo regras de cache. Uma imagem pública pode se beneficiar; isso não elimina automaticamente consultas da API de matrícula. Conteúdo privado exige cuidado com personalização. Load balancing distribui requisições entre alvos disponíveis, mas não remove todo gargalo nem garante sucesso por operação.

Stateless significa que a réplica não depende do estado local de uma sessão anterior para atender à próxima requisição. O sistema continua tendo estado. Sticky sessions mantêm afinidade, mas preservam dependência daquela réplica. Rate limiting restringe admissões por chave e intervalo: protege capacidade, não a cria. Três por réplica não significa três no sistema inteiro.

Na prática, abra Catálogo, Cache Preço e os dois mains de cache. Pergunte quantas leituras cinco consultas iguais produzem. Rode Demo Sem Cache: cinco acessos à origem. Rode Demo Cache: apenas um. Mostre que o contador é incrementado na origem. Depois a origem muda de dez mil para doze mil centavos; o cache ainda responde dez mil. Após invalidar, responde doze mil e o contador chega a dois. Relacione economia e desatualização à mesma cópia mantida em memória.

Em Demo Estado Local, destaque duas instâncias de Sessões. A réplica A encontra Ana; B fica sem sessão. Em Demo Estado Compartilhado, ambas recebem o mesmo objeto e encontram Ana. São objetos na mesma JVM, não servidores reais ou Redis. A demo isola a causa lógica; armazenamento entre processos acrescenta rede, latência e falhas.

Por fim, abra Demo Limite e a operação permitir. Ana passa nas três primeiras chamadas; quarta e quinta são recusadas. Bia tem cota própria e Ana volta a passar no tempo sessenta. O relógio é um argumento controlado para não esperar um minuto. O método retorna boolean; um adaptador HTTP poderia traduzi-lo para uma resposta apropriada. O mapa é local e sequencial, sem garantia distribuída.

Feche pedindo técnica, recurso poupado e custo novo. Um exercício útil é criar dois limitadores de três e alternar seis chamadas: cada um tem sua própria cota. Medir, identificar, mudar uma variável e explicar o efeito é mais útil do que decorar nomes de infraestrutura.
'''
scripts[7]='''Fernanda, a pergunta desta aula é se a autonomia de separar uma capacidade em outro serviço compensa os custos da chamada remota e dos dados distribuídos. A proposta é vinte e cinco minutos. Não apresente microserviços como destino obrigatório. Monólito é implantação conjunta; microserviços permitem evolução e implantação independente por capacidades e contratos. Réplicas do mesmo monólito continuam sendo réplicas, não microserviços.

Contextualize a escola vendendo um curso de cem reais. O checkout pede uma cobrança e espera confirmação para liberar matrícula. O provedor pode cobrar e perder a resposta. Esse problema também aparece em um monólito que chama um provedor externo: a causa é atravessar uma fronteira remota.

Desenhe a requisição indo, o efeito acontecendo e a resposta voltando. Cada trecho pode atrasar ou falhar. Timeout indica falta de confirmação dentro do prazo, não pagamento recusado. No experimento, o provedor já confirmou a cobrança enquanto o cliente ficou com resultado desconhecido, marcado como UNKNOWN. O cliente real não conhece o efeito só por olhar a exceção. Precisa reconciliar pela identidade da operação.

Retry precisa preservar a identidade da mesma intenção. Uma chave nova pode representar outra compra. A mesma chave com parâmetros incompatíveis deve ser rejeitada. Contrato inclui semântica e evolução dos dados, não somente a URL ou o formato JSON. Também explique propriedade dos dados: escrever direto na tabela de outro serviço cria dependência do modelo interno. Uma transação local não desfaz automaticamente o commit em outro participante.

Na prática, declare que as demos simulam uma falha remota de forma determinística: não executam HTTP nem serviços independentes. Abra Provedor e mostre a lista recebendo a cobrança antes da exceção. Em Demo Retry, o cliente tenta, perde a resposta e repete o mesmo pedido. Peça a previsão antes de executar. No final, o provedor registra duas cobranças. O contador é derivado dos efeitos na lista; não é um placar impresso sem mecanismo.

Depois abra Provedor Idempotente e Demo Idempotência. Nas duas tentativas, o main mantém a mesma chave de pedido de Ana. O provedor registra a identidade e o valor. A primeira resposta é desconhecida; a segunda é confirmada; fica uma cobrança. A diferença vem da decisão de não reaplicar o efeito já associado à mesma operação, não de uma interface ou de capturar a exceção.

O mapa é local, efêmero e sequencial. Para produção, identidade, parâmetros, efeito e resultado precisam de coordenação e armazenamento adequados. Se o efeito é externo, use a garantia do destino e reconcilie estados incertos. Peça duas novas previsões: chave diferente significa nova operação; mesma chave com valor diferente gera conflito. Não distraia do contraste principal antes de explicar sua causa.

Termine comparando necessidades concretas. Uma equipe pequena que muda matrícula e cobrança juntas pode valorizar um monólito modular. Processamento de vídeos com escala e evolução independentes pode justificar uma separação. O aluno precisa associar benefício a custo operacional, observabilidade e falhas parciais. A ponte para assincronia é adiar trabalho posterior, mantendo explícitas as garantias entre etapas. Eventos não eliminam erros distribuídos.
'''
scripts[8]='''Fernanda, nesta aula acompanhe uma operação entre gravação, publicação, consumo e confirmação. A proposta é trinta e cinco minutos. A escola confirma a matrícula de Ana e um worker registra o aviso depois. A aluna pode ter acesso antes de esse trabalho posterior acabar. Assíncrono muda o momento de execução; não significa que tudo será mais rápido.

Apresente produtor, fila e worker. Se a chegada supera o processamento, cresce o backlog. Mais workers só ajudam enquanto não pressionam ainda mais um recurso comum. Comando pede uma ação, como enviar aviso; evento informa um fato, como matrícula confirmada. Consumidores concorrentes numa fila normalmente dividem trabalho; broadcast exige uma topologia apropriada.

O primeiro risco é salvar a matrícula e publicar o evento em sistemas diferentes. Uma falha entre os dois deixa negócio salvo e evento ausente. Inverter a ordem pode publicar antes do negócio existir. Outbox registra mudança de negócio e intenção de publicar na mesma transação local. Um publicador envia as pendências depois. Se publicar e falhar antes de marcar envio, pode repetir. A transação protege a intenção local, não torna o broker parte dela.

No consumo, registrar o efeito e perder a confirmação também pode provocar repetição. ACK antes do efeito arrisca perda. Confirmação do publicador trata produtor e broker; ACK do consumidor trata broker e consumidor. Evite prometer processamento exatamente uma vez de ponta a ponta. Idempotência exige identidade estável e coordenação entre registro de processamento e efeito. Para um efeito externo, como e-mail, essa coordenação não surge automaticamente de uma tabela local.

Declare o limite das demos antes de rodar: memória, uma thread, nenhum broker, nenhum e-mail real e nenhuma recuperação durável após crash. Em Demo Evento Perdido, a matrícula de Ana fica salva e a fila tem zero eventos porque a publicação foi omitida. Peça previsão antes de mostrar a saída.

Em Demo Outbox, abra Estado e Escola. Um novo estado reúne matrícula e evento, e a referência é trocada uma vez. Isso modela gravação conjunta na execução sequencial; não é transação de banco. Com publicador parado, há uma pendência. Ao retomá-lo, fica um evento na fila. A demo não marca a pendência como enviada; repetir o loop publicaria de novo.

Depois mostre Fila: obter não remove; confirmar remove. Em Demo Entrega Duplicada, o aviso é registrado, mas falta ACK. O mesmo evento volta e a lista contém Ana duas vezes. Em Demo Consumidor Idempotente, o ID já processado evita o segundo registro e a lista contém Ana uma vez. O conjunto em memória não garante atomicidade concorrente nem sobrevive ao reinício.

Use o SQL como modelo da garantia necessária: produtor grava negócio e outbox juntos; consumidor grava identidade e efeito local juntos, com restrição de unicidade, e confirma depois do commit. Retry precisa de atraso e limite. Mensagem inválida exige tratamento; DLQ não corrige sozinha. Saga é outro cenário: reserva de vaga, cobrança recusada e liberação da reserva. Compensar é uma nova ação que também pode falhar, não voltar o tempo. Feche perguntando qual etapa o ACK realmente confirma e onde guardar identidade e efeito para dois workers.
'''
summary={1:'Organizar responsabilidades e dependências; preservar acesso quando o aviso falha.',2:'Distinguir criação, instância compartilhada, política de cálculo e adaptação de interface.',3:'Preservar a regra ao trocar armazenamento e entrada; explicar dependências e portas.',4:'Separar módulos e donos dos dados; observar a fronteira de uma transação local.',5:'Seguir endereço, porta e processo; distinguir execução local, container e produção.',6:'Escolher técnicas por gargalo e observar economia, estado e limites.',7:'Comparar autonomia de implantação com falhas parciais e custo de distribuição.',8:'Localizar perda e repetição entre gravação, publicação, consumo e ACK.'}
points={1:['Usar mains independentes: DemoEmail, DemoAcoplamento, DemoDesacoplamento, DemoWhatsApp e DemoPagamentoPendente.','0/3 versus 3/3 resulta da ordem e tratamento da exceção; interface sozinha não garante resiliência.','Trocar somente a implementação de Notificador no main; não editar Matriculas.'],2:['Simple Factory não é o Factory Method clássico do GoF.','9000 centavos viram 90.00 reais no Adapter; sem conversão, SDK interpreta R$ 9000.','Singleton compartilha identidade nesta execução; não garante persistência ou thread safety.'],3:['Apresentar fundamentos gerais antes de contextualizar escola e nomes de classes.','Clean: memória nova fica vazia; arquivo novo objeto recupera Ana e Clara.','Hexagonal: Bia continua recusada no CSV; comandos de terminal não acumulam memória.'],4:['Java mostra módulos; Python/SQLite executa transação real e efêmera.','Autocommit mantém recebimento de Bia; rollback o remove com a mesma falha UNIQUE.','Rollback local não estorna cobrança HTTP externa.'],5:['Reiniciar volta visitas a 1; duas portas escolhidas manualmente não são balanceamento.','EXPOSE documenta; publicação mapeia portas; Docker Linux no Mac usa VM Linux.','Docker build/run precisa de ensaio; não confundir HTTP local com deploy público.'],6:['Cinco consultas versus uma; preço antigo permanece até invalidar, então origem totaliza duas.','Réplicas modeladas como objetos JVM, sem Redis/CDN/load balancer implantados.','Limite por chave e janela: três de Ana, cota própria de Bia, renovação em t=60.'],7:['Timeout mantém cliente UNKNOWN; o provedor pode já ter aplicado o efeito.','Retry sem identidade produz duas cobranças; mesma chave idempotente produz uma.','Simulação local sequencial não oferece idempotência financeira durável.'],8:['Outbox preserva intenção local; publicação ainda pode repetir.','Efeito antes de ACK produz [Ana, Ana]; ID processado evita repetição na demo.','Demos em memória e SQL-modelo não são broker nem recuperação durável; Saga é compensação.']}
records=[]
for i,lesson in enumerate(lessons,1):
    script=out/f'{i:02d}-preparacao.txt'
    audio=out/f'{i:02d}-preparacao.mp3'
    if i==2:
        shutil.copy2(lesson/'preparacao-para-gravar.txt',script)
        shutil.copy2(lesson/'preparacao-para-gravar.mp3',audio)
    else: script.write_text(scripts[i],encoding='utf-8')
    records.append(dict(id=lesson.name,lessonNumber=i,summary=summary[i],points=points[i],scriptPath=str(script.relative_to(base)),audioPath=str(audio.relative_to(base)),audioStatus='generated' if i==2 else 'pending',durationSeconds=None,generationSource='ElevenLabs · Lucas · Eleven Multilingual v2 · arquivo anterior alinhado ao roteiro atual' if i==2 else 'macOS Speech · Luciana · pt_BR'))
(base/'studio/briefings.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
for r in records: print(r['lessonNumber'],len((base/r['scriptPath']).read_text().split()))
