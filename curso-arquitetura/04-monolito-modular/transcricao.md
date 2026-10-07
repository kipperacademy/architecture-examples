# Transcrição — Aula 4: Monólito modular
Fonte: [aula4_Bananecos FHD - Cam Extra - 12-15-46.mp4](https://drive.google.com/file/d/167fHGc4hkvALaiZhys9lWB3jJzuO8DuH/view), gravação FHD da pasta compartilhada no Google Drive. Duração falada: 15min31s. Transcrição automática em português pelo ElevenLabs Scribe. Timestamps agrupados em blocos de 30 segundos a partir dos tempos por palavra. O texto não foi revisado palavra a palavra.
Fonte: `aula4_Bananecos FHD - Cam Extra - 12-15-46.mp4` na pasta compartilhada do Google Drive. Duração falada: 15min31s. Transcrição automática em português pelo ElevenLabs Scribe; timestamps agrupados em blocos de 30 segundos a partir dos tempos por palavra. O texto não foi revisado palavra a palavra.

## Texto com timestamps

### 00:00
Esse vídeo faz parte da nossa série de vídeos de arquitetura de software aqui no canal e a gente vai discutir hoje o quesito ... Esse vídeo faz parte da nossa série de vídeos de arquitetura de software que a gente tá construindo aqui no canal e no vídeo de hoje a gente vai discutir o tema de monolito modular, que é um passo muito importante pra gente entender antes de ir pro conceito de microservices, que muitas pessoas acabam atropelando. E como é que a gente vai fazer o funcionamento dessa aula? Nos primeiros dez minutos,

### 00:30
eu vou te explicar. Nos primeiros cinco minutos, eu vou-- Nos primeiros dez minutos, eu vou te explicar o conceito teórico por trás de um monolito modular e nos últimos minutos do vídeo, a gente vai ver uma parte mais prática. Então, sem mais enrolações, bora pro vídeo. Bom. Bom. Bom, pra gente começar entendendo o conceito de monolito modular, primeiro a gente precisa entender o que que é

### 01:00
o monolito e o que que é o módulo, tá? Então o monolito, ele vai descrever uma única unidade de implantação, tá? Então quando a gente diz que um projeto é um monolito, a gente tá dizendo que aquele projeto, quando ele é, hã, gerado a versão final dele, que vai ser disponibilizada pros usuários, né, que a gente vai fazer o famoso deploy, então aquilo ali vai ser uma única unidade de implementação, aquilo ali vai ser uma única unidade de implantação, né. Então quando eu gerar o build final, aquilo ali vai gerar um único build que vai ser implantado tudo junto.

### 01:30
E o módulo, ele vai dizer respeito a limites internos. Então a gente pode ter uma única unidade de implantação, mas dentro dessa única unidade de implantação, lá no código disso, eu vou ter módulos que vão delimitar limites internos, né, que vão definir contratos e as dependências permitidas entre esses módulos, tá? Então, por exemplo, seguindo aqui o nosso exemplo de escola, né, pra quem assistiu as últimas aulas aqui da nossa série de arquitetura, já tá acostumada com esse exemplo. Pra quem não

### 02:00
assistiu, imagina que você trabalha numa aplicação que consiste em um sistema de uma escola ou de uma universidade ou de um curso, né, que vai controlar ali a parte do financeiro dessa escola, com o status dos pagamentos das matrículas, a parte acadêmica que controla o acesso dos alunos, a parte do registro dos alunos e por aí vai. Isso aqui pode ser um monolito, então isso pode ser uma única aplicação que vai ser implantada junto, né, mas dentro desse monolítolo, mas dentro desse monolítolo, mas dentro desse monolito eu posso

### 02:30
ter módulos apartados, tá? Então eu posso ter o meu módulo do financeiro, que é quem controla os pagamentos, quem controla o status dos boletos, quem faz a cobrança dos meus alunos, e eu posso ter o, a parte, né, o módulo do acadêmico, que vai controlar as aulas, vai controlar os alunos matriculados, as notas, né? Eu posso quebrar isso dentro do meu código de forma bem dividida, tá, com limites bem definidos, responsabilidades bem separadas também. Só que o que que vai acontecer? Apesar

### 03:00
de dentro do código aquilo estar bem segregado e bem separado, com limites definidos e só se comunicando via contratos, quando eu tiver uma alteração no financeiro ou uma alteração no acadêmico, isso aqui vai gerar um novo build. E se eu tenho um novo build, isso gera um único artefato que vai ter um único deploy. Então isso aqui é um monolito, né. Então vai lá no acadêmico, alterei a forma como eu controlo a nota do aluno. Antes eu usava a escala cinco, agora eu uso escala dez. Isso aqui, é, só diz respeito ao acadêmico. Não mudou

### 03:30
nada na parte de cobrança, não mudou nada na matrícula do aluno. Só tô controlando como é que eu controlo ali as notas, né. Mas mesmo assim eu mudei esse código. Isso aqui vai ter que gerar um novo build, né, pra eu disponibilizar aquilo pros meus usuários. E gerando esse novo build eu vou ter um novo artefato que eu vou fazer um único deploy. Isso aqui é um monolito. Agora, se isso aqui fore-fossem aplicações apartadas, se isso aqui fosse uma aplicação Java separada dessa, iam ser microservices, né? Mas daí em outras aulas a gente vai discutir isso aqui com mais detalhe. E aí mesmo que eu mudasse acadêmico,

### 04:00
isso ia gerar só o build novo do acadêmico, e somente a parte do acadêmico ia sofrer deploy, né, ia ser implantado ali. Então, mudar um módulo vai fazer recompilar a aplicação. Então, então no, então no, então, então, então, então no modolito, então no monolito modular, mudar o módulo vai fazer com que eu recompile a minha aplicação, gerando um novo build, gerando um novo deploy. "Fê, eu não consigo

### 04:30
reutilizar, hã, ali builds passados pra não precisar ficar recompilando todos os módulos, né, mesmo que eu só mudei uma única parte?" Sim, eu posso, né. Então eu posso salvar em algum lugar ali um cache dos últimos builds, salvando o último build da parte do financeiro e da parte do acadêmico, né, pra depois eu construir esse artefato de forma personalizada, sem precisar ficar rebuildando módulos que, que não foram modificados. Posso fazer isso. Mas se no final das contas isso aqui vai produzir um único artefato

### 05:00
que vai, né, ser deployado num único lugar tudo junto, isso é um monolito, tá? Eu só tô modularizando esse monolito. Beleza. Então vamo entender isso aqui com mais detalhes, tá? Dentro do monolito eu vou ter um projeto, tá? Imagine o monolito ali como a aplicação React que vocês criaram, a aplicação Next, a aplicação Java Spring, a aplicação Django, aquilo ali é o monolito. Cês até podem, dentro ali do código de vocês, separar em pastas, a parte da matrícula, a parte do pagamento. Beleza, mas aquilo ali é uma única aplicação, certo?

### 05:30
Só que o que eu vou fazer aqui pra isso aqui funcionar de maneira modular? Eu vou fazer com que a, eu tenha regras, né, de, de comunicação entre esses módulos e que a gente não tenha um módulo atravessando os limites do outro, tá? Então se eu tenho aqui o meu módulo de cobrança, que cuida ali os pedidos de matrícula, né. Então se eu tenho aqui o meu módulo de matrícula, que cuida ali os pedidos de matrícula, e eu preciso consultar cobranças, o que eu vou fazer é uma consulta no módulo de cobranças. Eu não vou lá e con-- no módulo de

### 06:00
matrículas, acessar diretamente o banco de dados de cobranças e manipular a entidade de cobranças. Não. Eu vou ter um módulo de matrícula Que vai receber um pedido, o pedido da Ana e da Bia. Com esse pedido eu vou fazer uma consulta no, no módulo de cobranças. Esse módulo de cobranças vai me exportar uma interface, né, vai me expor uma interface que vai ter ali o método está confirmado. Eu vou passar o número do pedido e aí é o cobrança que vai me retornar true ou false, se aquele, se aquela cobrança tá confirmada ou não. E aí através desse resultado

### 06:30
eu vou produzir, né, uma ação ou adicionar a Ana nos alunos matriculados e no caso da Bia, não vou adicioná-la porque retornou false, tá? E aqui pra finalizar, essa fronteira ela também vai aparecer no código, tá? Então aqui a gente tá falando muito dum-dum nível mais macro, mas quando a gente olhar o código vai ficar claro. Então olha só, eu tenho ali meu matrículas.java que precisa saber se a cobrança tá confirmada pra adicionar a aluna, né? Eu só vou adicionar a aluna se a cobrança tiver confirmada. E pra isso eu vou passar o número do meu pedido

### 07:00
pra fazer essa consulta. O meu matrículas.java vai ch-- fazer uma chamada pro meu cobranças.java. Só que aqui eu só vou consumir, né, o cobranças.estar-- está confirmado, ó. Eu tô só acessando um método público que cobranças me expõe, que o módulo de cobranças tá expondo pro mundo externo. As informações internas de cobrança, todos os métodos privados que cobrança tem, todos os dados que ele controla não me importa e não era nem pra eu tá mexendo, tá? Eu só quero fazer uma

### 07:30
consulta. Isso aqui tá sendo escondido por cobranças, né? Tá ali meio que abstraído. E aí dentro do módulo de cobranças eu posso ter várias outras classes, serviços que vão ajudar a fazer essa consulta e esse controle do pagamento das parcelas e tal, mas pro mundo de fora eu só exponho está confirmado, né? Quando eu digo pro mundo de fora é pros outros módulos que vão ter outras classes que vão me consumir, tá? E olha só que legal aqui. O bacana é que eu posso mudar a estrutura interna de cobrança, eu posso refatorar

### 08:00
tudo aqui. Antes eu tava cobrando via, hã, Stripe, agora eu vou mudar pra AppMax. Eu tava antes controlando boleto, agora não vai ter mais boleto, vai ser só Pix. Hã, eu vou fazer uma reconciliação de pagamentos passados pra quem tá devendo matrícula eu vou aplicar desconto, e aí eu vou botar uma nova regra aqui do desconto do aluno que-que entrou em 2027, sei lá, vou botar um monte de coisa aqui de cobrança. Matrículas está nem aí, matrícula só quer saber, tá confirmada a cobrança? Tá. Se tá confirmado eu adiciono o aluno na aula, se não, não tá.

### 08:30
Então eu mudo toda a estrutura interna de cobrança sem afetar os outros módulos, né? O retorno do booleano continua igual. E pra quem tá assistindo todas as nossas aulas aqui da série de vídeos de arquitetura de software, tá vendo que várias coisas se conectam, né? Eu não consigo explicar monólito modular sem eu tá aplicando os design patterns que a gente viu hoje, né, sem eu tá aplicando princípios do Solid, né? Porque tudo isso aqui vai dizer respeito ao design do meu código, a maneira como estrutu-- a maneira como estru-- a maneira como estou,

### 09:00
a maneira como estou estruturando a estrutura desse código, desse projeto, né, dessas classes pra que eu tenha essa aplicação mais saudável, tá? Então isso aqui, hã, é o que a gente fala de, hã, mudanças a nível estrutural do código, né, quando a gente fala de arquitetura. E o que vai unindo todos esses conceitos, conceito de design patterns que provavelmente aqui a gente vai usar uma injeção de dependência ou quem sabe segregação de interfaces lá do Solid, né. Aqui a gente pode trabalhar com

### 09:30
factors também, pode trabalhar com o Singleton, né, pra-pra criar ali as instâncias dos repositórios, pra compartilhar as conexões com o banco de dados. Então todos esses conhecimentos vão se aco-- hã, se acoplando, né, se, hã, se juntando pra que eu consiga produzir no final essa solução mais elegante. E o monólito modular vai ser isso, eu ter uma única aplicação, né, um único projeto, um monólito, que no final é um único artefato com um único deploy. É, obviamente, se eu precisar escalar eu posso fazer mais de deploy numa

### 10:00
mesma máquina, mas o que eu quero dizer é que o artefato é todo deployado junto, né. Esse é o-o, o quesito aqui. Mas internamente esse monolito, mas internamente esse monólito tá todo modularizado, né. E pra finalizar, a gente pode falar aqui do banco de dados também, que eu acho que pode surgir essa dúvida. O banco de dados entre esses módulos pode ser compartilhado. No final das contas a gente tem uma única instância lá do nosso Postgres ou do nosso MySQL, sei lá, um único banco, né? Mas o-o ponto aqui é,

### 10:30
lá dentro do código eu vou estabelecer bem essas regras, esses limites. Então o meu módulo do financeiro ele só pode inserir na sua própria tabela de financeiro, mexer lá nas partes de cobrança, de boleto, só mexe lá. Se por algum motivo o financeiro precisa avisar a matrícula de que aquele aluno não pagou, ele só vai avisar via contrato público aqui no código, né? Vão se comunicar um com o outro com código, mas quem mexe na tabela de matrículas é o módulo do acadêmico. O módulo do financeiro

### 11:00
não pode mexer lá na tabela de matrículas, porque eu tenho responsabilidades bem divididas, né, e limites ali bem, hã, desenhados, tá? Então esse é o ponto que esse, essa limitação vai viver na, na camada lógica, né, na-na, na camada ali do design do código e não necessariamente na tecnologia. Porque na tecnologia-- o que eu quero dizer com tecnologia é, é o mesmo banco de dados que eu tô usando, entende? O mesmo Postgres, tá? Com tabelas, a tabela de matrícula, tabela de boleto, tabela de alunos, a tabela de aulas. A diferença

### 11:30
é que lá no código, no momento de definir como que eu interajo com essas tabelas, eu vou estabelecer bem esses limites. E agora vamos pro exemplo aqui, né, no código pra que fique mais claro pra vocês. Então aqui de novo temos uma classe main que instancia cobranças e matrículas, tá? Eu posso fazer cobranças.confirmar o pedido da Ana, e depois eu posso fazer matrículas.matricularAna e matricular Bia, tá? Digamos que esse cobranças.confirmar fosse ser causado por um evento externo, né, eu só vou confirmar

### 12:00
a cobrança da Ana quando eu receber a notificação da AppMax de que o pagamento da matrícula da Ana foi confirmado, tá? Mas aqui a gente tá chamando diretamente a título de aprendizado. Então a cobrança da Ana foi confirmada, tá confirmado. A da Bia não Quando eu chamar matrículas.matricular, aqui passando o pedido da Ana e a Ana, a matrículas vai consultar cobranças, mas vai consultar cobranças através do, da interface pública

### 12:30
que cobrança expõe, né? Cobrança tá me expondo aqui o, o método está confirmado, tá? Que é um método aqui que retorna esse booleano true ou falso, se tá confirmado ou não. Se isso aqui me retorna que tá confirmado, eu adiciono a aluna na aula, se não, eu não adiciono, né? Mas aqui, imagine, eu quero que vocês usem o exercício da imaginação pra imaginar que aqui dentro de cobrança ia ser algo muito mais complexo, né, não é só isso que tá confirmado. Eu ia confirmar o ID do boleto, eu ia ver se o boleto foi processado, se não foi processado, cadê essa informação? Aí eu ia recuperar,

### 13:00
não, o boleto tá travado ainda, então o retorno não tá confirmado. Ou ah, foi no Pix, mas o Pix tá lá no outro banco de dados, ia ter toda uma lógica pra então eu poder retornar sim ou não, né? Só que tudo isso ficaria dentro somente de cobranças, só cobrança saberia e matrícula não interageria com isso, interageria some-- interageri- ah, interjare- interagira, interagiria, interagiria somente com a interface pública de cobranças, né?

### 13:30
E aí vocês vão ver que essa divisão, ela vive até na defisi-- na, aí vocês vão ver que essa defini... E aí vocês vão ver que essa divisão ela vive até na definição das pastas. Então aqui matrículas vive dentro da pasta, né, e do package acadêmico e vai ficar tudo aqui dentro. A parte de, de cobranças vive dentro do package de financeiro. Aqui dentro eu posso ter várias outras classes e arquivos que matrícula

### 14:00
não faz nem ideia que existe, né? Lá dentro do módulo de matrícula eu nem tô mexendo nisso, eu só tô interagindo aqui com, com essa interface pública de cobranças e todo o resto tá, hã, escondido e, e segregado ali pra mim, tá? Mas no final das contas eu poderia ter aqui a matrícula e cobranças escrevendo no mesmo banco de dados, só que cada um interagirindo, só cara, só cada um interagindo com o seu próprio repositório, né? Sem, hã, mexer um na tabela do outro. E isso aqui seria um monolito modular, tá? É simples

### 14:30
como isso, não tem muito mistério aqui. Muitas pessoas já fazem isso sem nem saber. Tá, muito provavelmente você já criou essa divisão de módulos, de pacotes, sem nem saber que isso se chamava monolito modular. Mas isso aqui é muito importante a gente entender, porque é o primeiro passo antes da gente ir pros microsserviços e entender quando que eles fazem sentido, tá? E aí, se você, e aí, se, e aí, se mesmo assistindo, e aí, se mesmo, e aí, se mesmo assistindo os nossos vídeos, os nossos cursos gratuitos aqui do canal, você ainda sente que

### 15:00
tá meio perdido, não sabe qual o próximo passo do que estudar ou queria saber seus pontos fortes e fracos pra criar um roadmap de estudos personalizado pro seu cenário, ter acesso a plantão de dúvidas e aulas ao vivo e, além disso, participar dos eventos presenciais da nossa comunidade, dá uma olhadinha no link que tá aqui na descrição do nosso vídeo que a gente tá preparando algo muito legal aqui pra Keeper Academy e vai ser um prazer ter você por lá. Então dá uma olhada aqui na descrição do vídeo e vamos encerrando essa nossa aula por aqui e até a próxima live ou o próximo vídeo.

### 15:30
Falou!
