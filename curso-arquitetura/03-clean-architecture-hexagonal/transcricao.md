# Transcrição — Aula 3: Clean Architecture e arquitetura hexagonal
Fonte: [aula3_Bananecos FHD - Cam Extra - 11-36-08.mp4](https://drive.google.com/file/d/1Ueu5kF6520nl4EHeyTB7UTM_osaiVmsA/view), gravação FHD da pasta compartilhada no Google Drive. Duração falada: 32min31s. Transcrição automática em português pelo ElevenLabs Scribe. Timestamps agrupados em blocos de 30 segundos a partir dos tempos por palavra. O texto não foi revisado palavra a palavra.
Fonte: `aula3_Bananecos FHD - Cam Extra - 11-36-08.mp4` na pasta compartilhada do Google Drive. Duração falada: 32min31s. Transcrição automática em português pelo ElevenLabs Scribe; timestamps agrupados em blocos de 30 segundos a partir dos tempos por palavra. O texto não foi revisado palavra a palavra.

## Texto com timestamps

### 00:00
Esse vídeo faz parte da nossa série de vídeos de arquitetura de software aqui do nosso canal e no vídeo de hoje a gente vai discutir as duas arquiteturas mais emblemáticas e discutidas aqui na nossa comunidade, que é arquitetura limpa e arquitetura hexagonal. Pra você conseguir entender esse conteúdo por completo, eu recomendo que você já tenha assistido aulas de Solid, inversão de dependê-- pra você conseguir, pra você conseguir compreender esse conteúdo

### 00:30
por completo, eu recomendo que você já tenha assistido os nossos vídeos sobre Solid e Design Patterns, que vão te ajudar a te dar a base fundamental pra gente compreender como que essas arquiteturas são implementadas. Mas, caso você não tenha assistido esses vídeos e já tenha esse conhecimento, tá tudo certo e vai conseguir seguir no vídeo por aqui. Vai funcio-- e a nossa aula vai funcionar... E a nossa aula, e a nossa aula vai funcionar da seguinte maneira: eu vou dividir a primeira parte.

### 01:00
E a nossa aula vai funcionar da seguinte maneira: a gente vai dividir a primeira parte pra ser a nossa parte teórica e depois a gente vai pular pra parte prática, onde eu vou mostrar os dois exemplos de arquitetura hexagonal e arquitetura limpa lado a lado pra você entender como que essas arquiteturas funcionam na prática. Então, sem mais enrolações, bora pro vídeo. Bom, bom, bom, bom, quando a gente fala de arquitetura

### 01:30
limpa ou arquitetura hexagonal, a gente tá falando sobre decisões de arquitetura que vão viver no nível de design de código. Então quando a gente for implementar, seja a Clean Architecture ou a arquitetura hexagonal, a gente tá falando de modificações que a gente vai fazer no nosso código e não na infraestrutura que tá rodando por volta. Então aqui a gente ainda não tá falando sobre microsserviços, não tá falando sobre Event Driven Architecture, sobre conectar diferentes provedores. Não, aqui

### 02:00
a gente tá falando sobre como a gente vai estruturar o nosso código, como que a gente vai fazer o design dele pra evitar acoplamento, pra ajudar na matune-- pra ajudar na ma-- pra ajudar na manutenção a longo prazo e fazer com que ele evolu-- e prazer-- e fazer com que ele tenha uma, e fazer com que ele tenha um ciclo de vida mais saudável. Então, quando a gente fala sobre Clean Architecture, a gente fala sobre uma arquitetura que defende muito a gente proteger a decisão das implementações. Então quando a

### 02:30
gente fala, então quando a gente fala de Clean Architecture, a gente tá falando... Então quando a gente, então quando a gente fala sobre Clean Architecture, a gente tá falando sobre uma arquitetura que defende muito que a gente proteja a decisão da tecnologia e da implementação. Então, quando a gente vê assim uma aplicação web, por exemplo, uma aplicação React, uma aplicação que foi construída com Next.js ou com o próprio Spring no Java, a gente vai ver uma aplicação que tá totalmente acoplada ao funcionamento

### 03:00
dos frameworks na qual ela foi construída, tá? E qual que é o problema? O problema é que a nossa decisão, que seria as nossas regras de negócio, os casos de uso que a nossa aplicação tem, né, as funcionalidades de fato, elas estão totalmente independentes da tecnologia. Seja essa tecnologia o React, seja o Next, seja o Java Spring, né. E aí eu tenho qual problema? O problema é, se eu for mudar a tecnologia, né, se eu for mudar ali o framework que eu tô utilizando, por exemplo, do React pro Angular, eu não vou mudar

### 03:30
só a tecnologia de fora. Eu vou ter que mudar todo o núcleo da minha aplicação, né, todas as regras, todo o funcionamento, porque tá tudo acoplado. Agora, se a gente trabalhar com arquitetura limpa, né, com o Clean Architecture, a gente teria uma aplicação onde o núcleo da decisão e as regras de negócio estão protegidos da tecnologia que tá rodando por fora e que tá dando a vida pra aquela aplicação, tá? Aí eu trouxe aqui um, uma imagem que vai ficar muito mais fácil de entender.

### 04:00
Então, na Clean Architecture, as nossas responsabilidades, elas vão ficar divididas em camadas, tá? E a gente vai separar isso em, a, seguindo algumas políticas, tá? Então olha só, mais por fora, então, hã... Então olha só, a gente consegue enxergar a Clean Architecture como o formato de uma cebola mesmo, né? Mais por fora, né, na borda, a gente vai ter os frameworks e os drivers. Frameworks seria ali o React, o, o Next, como eu falei, o NestJS, o Spring, ou se você tá

### 04:30
usando o Python, pode ser o Django, sei lá. Então aqui por fora a gente teria os frameworks e os drivers seriam, hã, hã, e os drivers... E os drivers, e os drivers seriam as classes que no-- e os drivers seriam as classes que nos permitem utilizar as ferramentas externas, né, adaptando elas pros nossos casos de uso, tá? E aí, e aí, e aí, e aí,

### 05:00
e aí, e aí o que que isso quer diz, e aí o que que isso quer dizer? Isso significa que nenhuma regra e nenhum contrato da minha aplicação vai ficar definido dentro da minha camada de framework, tá? Então se eu tô utilizando ali, por exemplo, o Spring, é pra eu deixar na camada de coisas do Spring somente as responsabilidades do Spring, que é a tecnologia que vai fazer com que aquele servidor rode, né, e execute. Agora, onde eu defino ali o, qual desconto eu vou dar pro cliente, como que eu vou liberar a matrícula do aluno,

### 05:30
quais são as minhas regras de negócio mesmo, isso vão ficar nas camadas mais internas, que estão bem protegidas das camadas externas. E aí, quando a gente enxerga essa cebola, a gente tem que enxergar da seguinte maneira: o que tá mais no miolo, o que tá mais dentro, não conhece o que tá pra fora, tá? Então esse framework aqui, ele sabe tudo que tem pra dentro, né, depois vendo o código vai ficar muito mais claro, mas ele conhece as camadas mais internas. Só que a camada mais interna de todas, que seria a camada mais valiosa, mais preciosa, ela não conhece tudo que tá rodando por fora dela. Ué,

### 06:00
ela E quando eu digo, e quando eu digo que ela não conhece, isso literalmente significa que ela não tem contato direto com ela, né. Ela não, não se relaciona com essas outras classes ou com essas outras funções. Dessa maneira, ela não tem nenhuma dependência com essas camadas externas. O que que isso significa? Significa que dessa maneira eu posso literalmente recortar essa parte aqui e passar pra rodar em outro framework, desde que esse framework crie os adaptadores necessários pra se conectar com essa minha camada interna e eu consigo fazer, né,

### 06:30
a-a transferência desse meu núcleo pra qualquer tecnologia que eu queira. Por que que isso aqui é interessante? Não só por causa dos frameworks, mas também pra-pra serviços externos que eu vou tá utilizando ou até o próprio banco de dados. Então digamos que eu tô utilizando ali o banco de dados da AWS e por algum motivo eu vou precisar trocar esse banco, seja por custo, seja por alguma diretriz da minha empresa, alguma política, encerramento de contrato, e a gente vai migrar agora pra GCP. Se eu tivesse criado uma aplicação que tá totalmente acoplada ao formato de funcionamento

### 07:00
da AWS, da forma como eles controlam o banco de dados, como eu tenho que montar as requisições, etc, etc, etc, quando eu fosse mudar esse banco de dados, eu ia ter uma puta dor de cabeça, ia ter que mudar em vários lugares. Se eu tivesse seguido a arquitetura limpa, eu ia ter que só tirar o driver da AWS e conectar o driver do GCP, e todo o resto da minha aplicação ia continuar funcionando. Então agora... Então... Então pra

### 07:30
resumir... Então pra resumir, então pra re-- então pra resumir, o núcleo da na-- então pra resumir, o núcleo da nossa arqui-- então pra resumir, o núcleo da nossa arquitetura vai aplicar as decisões e vai concentrar as regras de negócio. Os adaptadores vão atender esses contratos internos e os frameworks, né, ou os files aqui, vão realizar os acessos internos e as conexões com as tecnologias externas, tá? Então vamo passar de camada em camada, começando

### 08:00
com a camada das entidades. A re-- a-- Então vamo passar, então vamo passar, então vamo passar de camada em camada, começando com a camada das entidades. As entidades, elas vão representar os conceitos do domínio e vão preservar suas regras sem depender de interface ou armazenamento. Quando eu digo aqui ou armazenamento, é o seguinte: a minha entidade, por exemplo, a minha entidade aluno, eu tô criando uma classe que representa o meu aluno dentro da minha aplicação, ela não tem que se preocupar

### 08:30
e não precisa saber se eu tô usando um banco SQL ou NoSQL, né? Se eu tô salvando essa informação num JSON ou se eu tô salvando no banco de dados SQL. Não me importa onde eu tô salvando essa informação, não me importa o que é o armazenamento. Aqui eu tô falando da entidade. A entidade é o aluno. O aluno tem o quê? O aluno tem uma matrícula, o aluno tem um nome, o aluno tem um CPF. É isso que diz respeito ao aluno, né? Não me importa se aquilo ali depois tá sendo salvado num arquivo direto na minha máquina, num CSV, numa planilha, ou se eu tô salvando lá no banco de dados no Neon

### 09:00
ou se eu tô salvando na AWS, tá? Então aqui a-a regra vai viver dentro desses dados. E aí depois que eu tenho as minhas entidades, eu vou ter também os meus casos de uso. Os casos de uso vão coordenar as ações. Então eles vão coordenar as-as ações aplicadas às minhas entidades. Eles vão aplicar a regra, eles vão aplicar regras, vão solicitar colaboradores, ou seja, integrar diferentes, né, entidades e devolver um resultado, tá? Então aqui

### 09:30
na entidade vai morar o meu dado, né, e as ações desse dado. Então, por exemplo, um aluno, ele tem nome, CPF e toda a matrícula, todo pedido pode permitir uma matrícula, né? Isso ali seria a minha entidade. E então eu vou ter um caso de uso, onde o aluno é criado, depois o pagamento é confirmado e depois uma matrícula é gerada, né? Isso aqui vai morar dentro de um caso de uso. O caso de uso seria literalmente a coordenação de uma ação, aplicando as regras e as ações

### 10:00
em cima das entidades. Depois dos casos de uso, a gente vai ter os adaptadores, né. Os adaptadores, eles vão fazer só a tradução. Inclusive, a gente já falou do design pattern de adapters na nossa última aula que a gente falou sobre design patterns. A gente discutiu quatro design patterns e um deles foi o design pattern de adapters, que é os adaptadores que a gente tá chamando aqui. Se você quiser assistir essa aula, eu vou deixar linkado aqui no card, mas se você já conhece esse design pattern, vai entender do que eu tô falando. Então os adaptadores, eles vão converter protocolos, ou seja,

### 10:30
interfaces e contratos e formatos externos para os dados e as operações esperados pela aplicação. Então a minha aplicação vai depender somente de um contrato bem definido, né, duma interface, e aí os adaptadores vão fazer essa conversão de protocolos e formatos externos para os dados e as operações esperadas pela minha aplicação. Então é como se eu traduzisse o mundo de fora pelo que a minha aplicação tá esperando, né. Eu crio essa ponte, o adaptador, ele cri-- o adaptador, ele cria

### 11:00
essa ponte. Só que aí eu faço com que os meus casos de uso e as minhas entidades não dependam de nada externo, né. Eles vão depender de uma interface que eles definiram lá dentro, né, que eu defini, na verdade. Eu vou ter tomado essa decisão do que que eles dependem. E aí eu vou usar o adaptador pra traduzir o mundo externo pra o que a minha aplicação tá dependendo, né. Tudo pensando naquele formatinho de cebola, onde o domínio aqui de dentro não conhece, né, os casos de uso, que não conhece o que tá sendo por fora, né, o que

### 11:30
tá sendo colocado por fora pra ser... Que não conhece o que tá sendo colocado por fora, né, pra permitir que essas ações aqui sejam realizadas, tá? E aí, por fim, a gente tem os nossos frameworks e drivers, que são os mecanismos que vão rodar na borda, tá? Então os frameworks e os drivers são os mecanismos externos de execução, aquilo que eu falei pra vocês. Então é o que vai permitir a gente executar essa aplicação num servidor web, é o que vai permitir comunicação com serviços externos, a persistência dos dados, né, pra eu salvar um banco de dados ou

### 12:00
algum, hã, mecanismo ali de armazenamento e memória, ou o próprio armazenamento em storage. É o que vai conectar, né, a E é o que vai conectar a nossa aplicação ao mundo externo, tá? E aí ela vai ser co-- e é o que vai conectar a nossa aplicação ao mundo externo. E pra que essa conexão dos frameworks e dos drivers com o nosso núcleo aconteça, quem vai tá morando ali no meio são os adaptadores que a gente acabou de ver, tá?

### 12:30
E quem, quem vai tá morando ali no meio são os adaptadores que a gente acabou de ver, tá? E agora vamos partir pra arquitetura hexagonal.

### 13:00
Então a arquitetura, então a arquitetura, então a arquitetura hexagonal vai ter um objetivo muito alinhado com o objetivo da arquitetura limpa, que é proteger as camadas de domínio e as decisões da minha aplicação de serviços e tecnologias externos que a gente não tem controle, né, pra que eu proteja o que é meu, o que são as minhas regras de negócio e o que são regras do mundo externo que eu tô só utilizando como um meio, né, pra

### 13:30
fazer com que a minha aplicação rode, mas que de fato não é o núcleo ali da minha aplicação. A única diferença da arquitetura hexagonal pra arquitetura limpa é a maneira como isso vai ser implementado. Mas o objetivo, no final, é praticamente o mesmo, né, é a gente proteger o nosso núcleo das ferramentas externas, pra que o nosso núcleo da nossa aplicação não fique dependente de ferramentas que eu tô utilizando. Porque quando eu tô dependente, caso eu precise fazer modificações, eu vou ter que mudar por tudo quanto é lado. Caso a tecnologia externa

### 14:00
mude e não funcione mais como a forma que eu queria, eu também vou ter que me adaptar pra, hã, né, encarar essa nova realidade, o que não é o correto. O correto seria: beleza, isso aqui não me atende mais, eu jogo fora e troco por uma outra tecnologia, porque isso aqui não é a minha tecnologia core. O meu core tá aqui no meu domínio, né, nas minhas regras de negócio, nos meus casos de uso. E essa tecnologia eu tô usando somente como um meio de execução, como um meio de comunicação, e caso ela não me atenda mais, eu jogo fora e troco por outra, sem precisar refatorar todo o meu núcleo. Mas vamo ver como é que isso aqui

### 14:30
vai funcionar na hexagonal, tá? Na hexagonal vai ser o seguinte: a gente vai dividir a nossa aplicação entre portas de entrada e de saída, né, entrada pro núcleo e saída do núcleo, né, pra eu conectar com o mundo externo, atendidas por adaptadores. Então quando vocês forem ver, hã, artigos e outros vídeos sobre arquitetura hexagonal, vocês vão ver as pessoas falarem muito sobre ports and adapters, né, que seria, hã, portas e adaptadores. Então a gente vai ter porta de entrada e saída e os adaptadores que tão no meio, fazendo essa entrada

### 15:00
e essa saída, né. Aí a gente vai ter aqui o nosso núcleo, que concentra as regras, né, e o domínio. E então esse núcleo se comunica com o mundo de fora através das portas de saída e ele recebe os resultados do mundo de fora através das portas de entradas, né. Então, a saída, o núcleo tá solicitando alguma coisa e a entrada, o exterior tá iniciando alguma coisa e mandando pro núcleo. E quem vai morar ali no meio são os meus adaptadores, tá? E o que que vai acontecer?

### 15:30
Aí o que que vai acontecer? Aí o que que vai acontecer? Na arquite-- aí o que que vai acontecer? Na arquitetura hexagonal, o... Aí o que que vai acontecer? Na arquitetura hexagonal, os casos de uso vão ser mantidos dentro do nosso núcleo, tá? E as portas, que a gente vai chamar aqui, vão definir as conversas entre o nosso núcleo com o mundo externo.

### 16:00
Quando eu digo definir conversa, é literalmente definir o contrato. É o que o meu núcleo vai esperar que o mundo externo mande pra ele, e é o que o meu núcleo vai mandar pro mundo externo, se-seja mandar pra salvar no banco de dados, mandar pra um serviço de mensageria, e etc. E quem vai fazer essa adaptação da comunicação vai ser o adaptador. Então a gente consegue imaginar o adaptador como um tradutor. Digamos que a gente tem alguém que fala, hã, português e outra pessoa que fala mandarim. E o adaptador é o cara no meio que fala português e mandarim. O cara de português fala uma frase, o do,

### 16:30
o tradutor traduz e explica pra pessoa de mandarim. A pessoa de mandarim fala uma outra frase, o tradutor traduz e fala pra pessoa do português. Esse é o papel do adaptador. E o adaptador aqui é bem parecido com o adaptador lá que a gente viu na arquitetura limpa. A diferença é que lá na arquitetura limpa eu tinha mais camadas. Aqui na arquitetura hexagonal eu só tenho o núcleo e eu tenho as portas de entrada e saída, e o adaptador que mora ali no meio, né, que é o cara que vai ficar fazendo, hã, essa tradução. E aí agora...

### 17:00
E aí agora, e aí agora já podemos ir aqui para o nosso código.

### 18:00
E agora, e agora, e agora já podemos, e agora

### 18:30
já podemos ir aqui pro nosso código. Então imagina o seguinte: imagina que a gente tá trabalhando numa aplicação que consiste em um sistema de matrículas, né, de uma instituição, hã, de ensino, seja um curso, seja uma universidade, uma escola, enfim, não importa. E o, o que importa aqui é que a gente tem os pedidos, que são os pedidos de matrícula, né, pra gente fazer ali a liberação duma matrícula de um aluno, e a gente tem também os nossos, hã, status de pagamento. Essas informações, como quais são os status de pagamento

### 19:00
que a minha aplicação contém, são informações que moram no meu núcleo, entende? Eu não tenho que fazer com que os meus status de pagamento sejam acoplados ao provedor de pagamento que eu tô utilizando, se é cartão de crédito, se eu tô cobrando via Stripe, se eu tô vo-- cobrando via AbacatPay, se eu tô cobrando via UV, via Transfera, não importa aqui, tá? O que eu quero fazer aqui...

### 19:30
Então, então o status de pagamento, então o status de pagamento é uma coisa, então os-- então o status atual de pagamento da matrícula do aluno é uma coisa que interfere em, é uma coisa que interfere... Então o status de pagamento da matrícula do meu aluno é uma coisa que vai interferir diretamente no funcionamento das minhas regras, né. Dependendo se o pagamento tá confirmado ou pendente, eu vou liberar ou não a matrícula desse aluno. Então isso faz parte da minha regra de negócio.

### 20:00
E esse status é uma coisa que tem que viver dentro do meu domínio, né, dentro do núcleo ali da minha aplicação. Então aqui não me importa se eu tô usando AbacatPay, se eu tô usando AppMax, se eu tô usando Stripe, né. O que eu quero saber aqui dentro é somente o status dentro do domínio da minha aplicação. Depois eu vou conectar com o mundo de fora e ver como que esses provedores, digamos, como que a AppMax me retorna quando o pagamento tá pendente, ou quando foi aprovado, ou quando foi recusado. E eu vou criar um adaptador pra adaptar o mundo,

### 20:30
o meu mundo interno aqui com o mundo da AppMax, né, pra fazer essa conexão. Então, isso aqui, esses, esses status é uma coisa que tem que viver dentro do meu domínio, né, do pacote do meu domínio. O pedido é uma coisa que tem que viver dentro do pacote do meu domínio também, né, a, o, o record de pedido. Então o pedido recebe uma aluna ali, digamos que é o nome da aluna e o status do pagamento, né? Tudo isso aqui, ó, sem conectar com nada de fora, isso aqui é só o núcleo da minha aplicação. E aí, dentro aqui de aplicação...

### 21:30
E aí... E aí... E aí... E aí depois...

### 22:00
E aí depois, e aí depois de defi-- e aí depois de definir essa minha camada de domínio, eu vou começar a definir minhas camadas de casos de uso, né. Então eu já tenho o meu domínio, que é os status do pagamento. Obviamente, isso aqui seria algo muito mais completo, tá? Eu criei um, um tipo muito simples, só pra que a gente consiga entender. Então dentro do meu domínio, eu tenho somente status de pagamento, nem é pagamento dentro do min-- do domínio, é só status e pedido. E eu começo a criar os casos de uso, que é o caso de uso de matrícula. Então matrícula, ela vai ser executada, né,

### 22:30
recebendo uma aluna e um status de pagamento. E aí quando eu for criar uma matrícula, eu vou criar uma matrícula do aluno, que vai implementar ali a minha interface matricular, né? Que seria matricular aquele aluno. Essa minha interface matric-- essa minha, esse meu caso de uso de matricular aluno, ele vai ter que criar um novo pedido pra esse aluno, passando o nome do aluno e o pagamento, sendo o pedido aqui a minha entidade principal, né? Esse pedido, eu vou ver se ele permite matrícula ou não. Se permitir matrícula, eu vou

### 23:00
salvar isso em algum lugar, né, vou persistir esses dados, vou salvar num repositório. Só que percebam que esse repositório aqui não é um repositório JPA, eu não tô integrando direto com o schema do Prisma, eu não tô fazendo essa integração direta. O repositório é só uma interface também, uma interface que me expõe os métodos salvar, listar. Tudo isso aqui, ó, vivendo num núcleo totalmente desacoplado com o mundo de fora. Fê, mas isso aqui não funciona, né, não tá funcionando, tu só criou um monte de classe que, que define interface, define interface.

### 23:30
Pois é, a gente vai criando várias camadas, até que chegue na camada mais de fora, que é quem vai pegar tudo isso que eu defini e executar, que é a camada de fora, né, de frameworks e, e drivers, que vai ser responsável por essa execução e por essa comunicação com o mundo de fora. Depois que eu faço isso, eu começo a criar os meus adaptadores, né, que vão adaptar, por exemplo, o meu repositório de matrículas prum repositório, hã, do J-- do JPA, ou vão adaptar prum repositório do, usando o

### 24:00
Prisma, né, como ORM, se eu tivesse aqui numa aplicação TypeScript. Então isso aqui seria o funcionamento do, da arquitetura limpa, né, de maneira simples. A arquitetura hexagonal, ela vai dividida aí entre entradas e saídas. Então digamos que essa minha aplicação, então digamos que essa minha aplicação, então digamos que essa minha aplicação, ela su-- ela, então digamos que essa minha aplicação, ela fosse Então digamos que essa minha aplicação, ela fosse salvar essas matrículas em dois possíveis,

### 24:30
hããã, repositórios, né, em du-duas possíveis memórias. Poderia ser em arquivo, então vou exportar um arquivo CSV ou TXT, sei lá, ou em memória mesmo, né, salvar aqui na memória do meu computador. É, o que que eu poderia fazer? Eu poderia criar aqui uma entrada, que seria a entrada CSV ou a entrada via terminal, né, que é quando eu vou digitar esses dados. E aí essa entrada aqui, ó, cês tão vendo que eu, hã, recebo uma dependência de matrícula, que eu sei que matrícula executa, né? Eu leio esse meu CSV, vou quebrando

### 25:00
os dados e vou passando, né, essa informação pra matrícula.executar. Então tu perceba que a matrícula lá dentro do núcleo dela, né, ela nem sabe o que tá acontecendo por volta. Ela nem sabe que tá rodando um CSV ou que eu tô lendo isso de arquivo ou que eu tô buscando do banco de dados. Ela tá lá bem bela, presinha no seu núcleo e só sabendo o que ela precisa fazer, né, que é matricular o aluno e salvar isso num repositório depois e aplicar as regras que tivesse que aplicar, que no caso aqui eu não, não botei nenhuma regras, mas pensem que ali vai ter várias regras de matrícula que vamos ver

### 25:30
dentro da, do meu núcleo, tá? E aí eu crio uma porta de entrada, né, que é o, a entrada do mundo exterior pra se conectar com meu mú-- com meu núcleo. Essa entrada tá lendo um arquivo na minha máquina, files.readfiles, fazendo a quebra, né, das linhas, processando o CSV e chamando matrícula pra matrícula executar, né? E eu posso fazer essa entrada tanto via CSV, quanto via terminal, que eu poderia, né, literalmente ir digitando aqui no terminal e ch-chamando a minha classe de matrículas, e essa matrícula fosse

### 26:00
recebendo e fazendo de novo matrícula.executar. Então isso aqui seria minha camada de entrada, né? Uma porta de entrada. E uma porta de saída seria a seguinte: repositório em arquivo, que implementa o repositório em matrícula. Opa, o que que é isso daqui? Isso daqui é um adapter, né? Então isso aqui eu tô adaptando a, o meu repositório matrículas, que é uma coisa que vive lá dentro do meu núcleo, né, pra uma integração externa, que é o repositório em arquivo, pra eu salvar isso aqui

### 26:30
num arquivo, né? Transformar isso aqui num arquivo que eu vou salvar na minha máquina. Eu vou pegando cada uma das alunas, hã, adicionando ela numa lista, criando um diretório, escrevendo num arquivo e salvando esse arquivo, né? E aí a gente pode olar, olhar lá em matrícula, ó, na, aqui na matrícula do aluno, que ela recebe uma instância de repositório e chama esse repositório salvar, mas ela não sabe o que tá acontecendo por volta. E eu poderia salvar essas informações tanto em um arquivo, quanto em memória também, né? Então salvar aqui uma cópia, por exemplo,

### 27:00
né? E de novo, o meu núcleo lá não ia conhecer isso. E aí, obviamente, a gente tem uma camada que tá por fora de tudo, né? Vocês já devem tá se perguntando, tipo, tá beleza, monte de classe, mas nada se conecta. Quem que vai conectar? A camada mais de fora. Então, se a gente olhar aqui a nossa demo de arquitetura limpa, como é que vai funcionar isso daqui, tá? Em arquitetura limpa, eu vou ter o seguinte: eu vou ter a definição de um novo repositório em arquivo, que é do tipo repositório matrículas. Per-pe-percebam aqui que eu não tô dizendo que isso aqui é do tipo repositório em arquivo, eu não tô

### 27:30
criando essa dependência direta com o meu formato de armazenamento. Eu tô usando aqui a minha, hã, interface que... repositório matrículas, né? Eu tô usando essa minha interface aqui que define esse contrato. Depois, eu crio uma nova matrícula do aluno. Aí eu executo as matrículas, executo a matrícula da Ana, com status de pagamento confirmado, matrícula da Bia, etc, né? E aí tudo aqui roda sem, hã, dependência. E aí todo o meu núcleo aqui roda sem dependência

### 28:00
com as coisas de fora, né, com as camadas, os frameworks de fora, os drivers e etc, né? Aí eu posso tranquilamente trocar esse repositório em arquivo por um repositório em memória, né? O código vai só instanciar, ao invés do repositório em arquivo, o repositório em memória. E aí tudo vai continuar funcionando. No caso da arquitetura hexagonal, o que que eu vou fazer? Eu vou... No caso da arquitetura, no caso da-- no caso,

### 28:30
no caso, no caso da arquitetura hexagonal, a única diferença que teve foi que eu criei esse formato de portinhas, né? Porta de entrada e porta de saída. Mas no final das contas, o, o formato ali da matrícula, né, e do domínio continua sendo o mesmo. Olha só, vou botar aqui lado a lado pra que vocês consigam enxergar isso daqui. Então, se a gente observar esse código... A gente-- se a gente observar esse código, a gente vai ver que a diferença aqui foi

### 29:00
que a parte da execução, que eu deixei aqui na minha classe principal, no caso da arquitetura limpa, foi movida pra dentro de uma parte de entrada, né. Então quem vai controlar a execução e, hã, chamar ali quem vai ser matriculado, lendo isso de um arquivo fonte, foi o meu entrada.csv, que poderia ser aqui também um, um, que poderia, que poderia ser aqui também substituído pela minha entrada em arquivo, né, que eu tenho aqui o meu entrada

### 29:30
termina-- a minha-- que poderia ser aqui também substituído pela minha entrada terminal, né? Deixa eu achar aqui, entrada. Que poderia ser substi- que poderia ser substituído aqui também pelo meu entrada terminal, né? Aqui, trocar por entrada terminal, entrada terminal, pronto. E aí eu faço aqui, na verdade, eu já vou ter um exemplo disso pronto pra mostrar pra vocês, que eu faço aqui o meu new entrada terminal,

### 30:00
terminal.receberargumentos e então printar as matrículas salvas. E aí, ao invés de deixar isso exposto na minha classe principal, que é quem tá chamando tudo e orquestrando tudo, eu boto isso pro, pra dentro de uma camadinha de porta de entrada. E a porta de saída seria o que a minha matrícula, hã, faz pra se conectar com o repositório externo, tá? Se você quiser aprofundar ainda mais a prática da arquitetura limpa e da arquitetura hexagonal, porque aqui eu dei só uma passada, né, por

### 30:30
s-- porque aqui eu dei Agora, agora, agora, agora se você, agora se você, agora se você ainda tá com dúvida e quiser aprofundar ainda mais essa parte pra... Agora se você ainda tá com dúvida e quiser aprofundar ainda mais essa parte pra... Agora se você ainda tá com dúvida e quiser aprofundar ainda mais essa parte prática da arquitetura limpa e da arquitetura hexagonal, eu recomendo que você assista esse vídeo que tá aparecendo aqui no card, porque eu peguei uma aplicação do zero e implementei

### 31:00
utilizando essas arquiteturas, tá? Porque aqui nesse vídeo a ideia é ser mais um formato de aula da gente ver a teoria e comparar com a prática pra que você consiga consumir esse conteúdo de maneira mais rápida. Agora, se você quiser entrar a fundo mesmo e implementar um código do zero usando essas arquiteturas, eu recomendo que você assista esse vídeo que eu já fiz aqui no canal, onde a gente vai construir uma aplicação ali digitando linha por linha, né, implementando essas arquiteturas discutidas aqui no vídeo. E se você se sente

### 31:30
perdido no momento de estudar e gostaria de um acompanhamento, e se você se, e se você, e se, e se além disso, e se além disso, e voc-- e se além disso você ainda se sente, e se além disso você ainda se sente meio perdido em qual assunto estudar, qual ordem seguir, e entender quais são os seus pontos fortes e fracos e construir um roadmap pra você, e, e se além disso, e se além disso, e se além, e se além desses conteúdos gratuitos, você

### 32:00
quiser uma ajuda extra pra entender o que estudar, quais são os seus pontos fortes e fracos e criar um roadmap de estudos personalizado pra você, ter acesso a plantão de dúvidas e aulas ao vivo, e além disso participar de prese-- e além disso participar de eventos presenciais da nossa comunidade, eu recomendo que você dê uma olhada no link que eu deixei aqui na descrição. No Keeper Academy a gente tá construindo algo muito legal aqui pra nossa comunidade e se você tiver interesse, é só dar uma olhadinha ali naquele link. Esse vídeo vai ficando por aqui e te vejo na próxima live

### 32:30
ou no próximo vídeo, falou!
