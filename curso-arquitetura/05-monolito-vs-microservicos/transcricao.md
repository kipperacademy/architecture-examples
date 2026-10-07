# Transcrição — Aula 5: Monólito versus microsserviços
Fonte: [aula5_Bananecos FHD - Cam Extra - 12-38-20.mp4](https://drive.google.com/file/d/1N0ysFlsS58evMhFoAeRc7aBxML4KYtCm/view), gravação FHD da pasta compartilhada no Google Drive. Duração falada: 18min50s. Transcrição automática em português pelo ElevenLabs Scribe. Timestamps agrupados em blocos de 30 segundos a partir dos tempos por palavra. O texto não foi revisado palavra a palavra.
Fonte: `aula5_Bananecos FHD - Cam Extra - 12-38-20.mp4` na pasta compartilhada do Google Drive. Duração falada: 18min50s. Transcrição automática em português pelo ElevenLabs Scribe; timestamps agrupados em blocos de 30 segundos a partir dos tempos por palavra. O texto não foi revisado palavra a palavra.

## Texto com timestamps

### 00:00
Esse vídeo faz parte da nossa série de vídeos de arquitetura de software aqui no canal e hoje a gente vai discutir a diferença entre a arquitetura de microsserviços versus monólito. Esse é um passo muito importante pra gente começar a pensar na estrutura que roda em volta da nossa aplicação, e não só no design de código, porque nas últimas aulas a gente tava discutindo muito sobre design patterns, solid, monólito monolar, monólito modular,

### 00:30
mas tudo isso vivi, mas tudo-- porque nas últimas aulas a gente tava discutindo muito sobre solid, design patterns, arquitetura limpa e hexagonal, monólito modular, mas tudo isso vivia, mas tudo isso vivia dentro duma única aplicação, né, dentro do nosso projeto, que era respeito ali do design e da estrutura do nosso código. Agora, a gente vai começar a enxergar que existem outras decisões de arquitetura que podem começar a impactar a estrutura que tá rodando por volta, né, e não só o nosso código.

### 01:00
E é justamente o que a gente vai ver na aula de hoje. Então sem mais enrolações, bora pro vídeo. Bom, bom, bom, bom, então pra gente discutir aqui a diferença de monólitos

### 01:30
contra microsserviços, a gente vai seguir naquele nosso exemplo de uma escola ou de uma universidade que tenha o controle, que tenha o seu contro-- que tenha o seu sistema de controle de matrículas e de cobranças. Então imagina o seguinte, que essa escola, ela vende um curso a cem reais, tá? Essa venda do curso é controlada por uma parte de cobrança, que vai controlar o boleto, o Pix, o cartão, vai retentar a cobrança lá no cartão do usuário, vai ter e-mails de cobrança caso o usuário esteja inadimplente na matrícula, enfim, vai ter toda

### 02:00
uma regra, né. Só que isso aqui precisa, né, retornar o usuário pro checkout, caso ele não-não-não tenha pago a matrícula. Então eu não, eu-eu não consigo liberar a aula pro aluno, a matrícula pro aluno, caso ele não esteja, né, pagando a matrícula corretamente. Então são duas coisas que têm dependência, matrícula e cobrança, mas ao mesmo tempo são coisas diferentes, porque dentro da matrícula do aluno eu posso dizer qual a turma que ele tá, as notas que ele tirou, o professor da aula, né. Então,

### 02:30
posso ter toda uma parte acadêmica, hã, rodando em volta da matrícula, que não diz respeito à cobrança e pagamentos e boletos, tá"?. Só que mesmo assim, as duas coisas têm, hã, uma certa dependência, porque fazem parte, né, de uma mesma aplicação, certo? De-de regras de negócio que a gente tá definindo aqui pra essa, pra esse software final funcionar ali pro usuário. Até aí, tudo bem. Só que aí, essas coisas, elas podem começar

### 03:00
a crescer, tomar grandes proporções. Então aqui, eu primeiro tô falando de uma escola de bairro, né, que tem cem alunos. Até aí, tudo bem. Tudo isso viver dentro de um mesmo projeto, dentro de um monólito, né. E agora a gente já vai entender melhor o que seria o conceito de monólito, mas viver dentro ali do meu Next App ou viver dentro do meu Django, né, uma única aplicação, um repositório que tem todos os endpoints, tudo certo. Só que à medida que isso começa a escalar e essa instituição começa a crescer, eu posso ter ali não mais só duas aulas,

### 03:30
três aulas, né, três cursos diferentes. Essa, a instituição pode começar a criar diversos cursos de diversos setores, implementar vários provedores de-de cobrança pra garantir que sempre quando o usuário for fazer uma matrícula, a gente consiga fazer a cobrança, né, não ficar dependente somente de um provedor. E-e as duas coisas começam a evoluir de maneira paralela, tanto o setor de cobrança quanto o setor de matrícula, né, com suas próprias funcionalidades e-e preocupações, etc. E eu começo a ter um código muito grande

### 04:00
mesmo, né, com muitas regras, muitas coisas, certo? E também um time maior, certo? Um time de, maior de desenvolvedores, de POs, né, de pessoas de produto, que vão tá olhando, né, pras decisões, a, da-daqueles produtos em si. Enfim, tudo começa a crescer. E aí quando isso começa a crescer, começa a surgir aquela decisão de implantar junto ou separar essas coisas, né. E isso aqui é uma decisão de arquitetura, tá?

### 04:30
Isso aqui é uma decisão de arquitetu... E é isso aqui é uma decis-- isso aqui é um, isso aqui é uma decisão de arquitetura, tá? Então, de-- isso aqui é uma decisão de arquitetura, tá? Então diferente do que muitas pessoas pensam, muitas vezes a gente vai começar a nossa aplicação como monólito. Inclusive, tem um artigo bem interessante do Martin Fowler que fala sobre isso, que se chama Monolith First. Vai tá aparecendo aqui na tela. Nesse artigo, ele discute que

### 05:00
a gente talvez devesse começar as nossas aplicações como monólitos mesmo, que é aquilo, eu criar um único projeto, né, vou criar o meu Django App, vou criar a aplicação Express, vou criar o meu Nest App, vou criar minha aplicação Spring. Um único projeto. Vou dividindo em módulos, vou separando tudo, mas tudo tá vivendo dentro de um u-- dum mesmo artefato, né, aquilo ali vira um único build que vai ir pra produção. Até aí, tudo bem. À medida que isso começa a crescer, que eu começo a ter, hã, vários módulos caminhando

### 05:30
pra caminhos diferentes, né, aumentando a complexidade desse meu sistema, tendo necessidades de escalar uma parte, porque eu tenho no-no, no-- tendo necessidade de escalar uma parte, porque na Black Friday eu tenho um monte de venda, eu tenho que escalar cobranças, mas eu não necessariamente preciso escalar lá o sistema de aulas, isso começam a ser suspeitas que eu posso ter pra dividir essas aplicações em projetos diferentes, que é o que a gente vai chamar de microsserviços, que é pegar esse meu serviço que eu tinha, esse meu monólito, e quebrar em partezinhas. Então

### 06:00
Eu vou criar uma aplicação NestJS ou uma aplicação Java Spring pra controlar só as matrículas e os alunos. Eu vou criar outra aplicação Java Spring pra controlar só as cobranças e os pagamentos. Eu vou criar outra aplicação Java Spring pra controlar só as aulas e os professores. Poderia fazer isso, caso eu enxergue essa necessidade, tá? Fê, isso significa que eu nunca devo começar com microsserviços, né? Eu nunca devo começar já quebrando tudo? Não! Tem cenários onde pode ser mais inteligente

### 06:30
tu já começar com microsserviço. Quais cenários seriam esses? Bom, se você trabalha já numa empresa, hã, que tem muitos clientes, né, ou muitas pessoas no time e tu já sabe que aquela aplicação vai escalar mesmo e que vai tomar maiores proporções, talvez já, já seja mais inteligente dividir em microsserviços mesmo, porque aí vocês já conseguem dividir entre as diferentes squads, né. Então vou dar o exemplo de vocês, hã, vou dar o exemplo pra vocês entenderem quando eu trabalhava lá no Mercado Livre. A gente começou

### 07:00
desenvolvendo um projeto lá dentro de farma, né, mas a gente já sabia que iam ter outras equipes que iam trabalhar com farma também, né. E cada equipe ia ficar responsável por uma, por uma parte do fluxo de farma, né, do, do fluxo de comprar item farmacêutico, porque aquilo ali não é só, ah, comprar o item, tem várias etapas, tem a etapa de analisar a receita, a etapa de, hã, mandar as informações pro vendedor, né, pra farmácia, tem a etapa de mandar aquilo pro, pro transporte, etc, tá? Então a gente já sabia que iam ter equipes responsáveis por diferentes

### 07:30
partes no futuro, mas no começo a gente era uma única equipe quando tudo começou. Mesmo assim, por saber já desse futuro próximo, a gente já decidiu iniciar como um microsserviço. A gente quebrou a parte de receitas num-num-num microsserviço, a gente quebrou a parte do seller em outro microsserviço, né, pra que depois, quando essas novas equipes chegassem, cada uma ficasse responsável pela sua parte. A equipe grande é o único motivo de eu quebrar uma aplicação em monolito pra microsserviços? Não, tá? E às vezes, m-mesmo

### 08:00
tendo uma equipe grande, eu não precise quebrar. Isso é só uma das razões e também depende do contexto. Outra razão pode ser aquela razão da escala. Então, por exemplo, né, eu trabalho no, na Amazon e eu tenho muita, hã, muito request, né, pra minha parte de busca. Então tem muitas pessoas que vivem buscando, buscando produto na Amazon, buscando, buscando, mas nunca compra, mas a pessoa fica buscando. E no dia da Black Friday então, meu Deus, ou na Cyber Week, Cyber Monday, né, tá todo mundo buscando produto na Amazon, procurando promoção. Então aquela

### 08:30
parte de buscas é um motor que tem muitas requisições e provavelmente precisa escalar, diferente da parte de alterar o nome da sua conta, né. A parte de alterar os dados da conta do usuário pode ser bem menos acessado, receber mem-- bem menos requests. Mas se tudo isso ficasse dentro de uma única aplicação, né, caso precisasse escalar, eu ia ter que fazer a, é, o deploy de novas instâncias daquela aplicação ou colocar mais recurso na máquina que tá rodando aquela aplicação. E

### 09:00
percebam que eu ia ter que escalar tudo. Ah, mesmo que só a parte de, de buscas usasse esses recursos novos, eu escalei tudo, né, de maneira desnecessária. Se isso tivesse quebrado em aplicações separadas, eu só faço deploy de novas instâncias dessa parte de busca e da parte de perfil eu deixo uma única instância rodando porque ela sozinha já aguenta todos esses requests. Então, o, o quesito da escala pode ser um quesito que a gente possa usar como tomada de decisão se eu vou quebrar em monolito ou não. É o único,

### 09:30
o único quesito? Também não. Pode ter também o quesito da complexidade. Então é aquilo que eu falei, a aplicação tá crescendo, tá ficando com um monte de regra, a-as coisas estão caminhando pra caminhos diferentes. Então eu tenho ali um time que tá dedicado só com a parte de buscas, eles tão se preocupando se quando o usuário buscar sobre, hã, sei lá, sobre roupa infantil, se vai aparecer só roupa infantil, se vai aparecer roupa de mulher também. Eles tão, ó, implementando um monte de algoritmo de busca pra regex, nanana. Enquanto os cara lá da parte de perfil tão preocupado com golpe, com conta laranja,

### 10:00
com usuário e-enviar documento de outra pessoa, entende? Então é coisa diferente. Aí eu começo a adicionar um monte de regra de um lado, um monte de regra do outro, a aplicação começa a ficar mu-muito complexa, né, tu vai abrindo aquelas classes, tu já nem sabe mais o que tá acontecendo na parte de perfil, porque tu nem é daquele time, tu nem mexe lá, tu só queria consultar o nome do usuário e a, a aplicação começa a ficar essa, e-essa quantidade absurda de código. Aí talvez possa fazer sentido eu quebrar em microsserviço, vou quebrar a parte de buscas da parte de perfil. Vão ser duas aplicações, né, separadas.

### 10:30
E aí o time de busca mexe lá, e o time de perfil mexe lá. Quando cada um precisar consultar o dado do outro, eles se conversam através de, de comunicação assíncrona, né. Um faz requisição pro outro, posso com-comunicar através de um serviço de mensageria. Enfim, essa pode ser um, um outro motivo, né, no qual eu faria essa quebra do monolito para um microsserviço. Isso pode ser um outro motivo no qual eu faria essa quebra, né, de um monolito para

### 11:00
um microsserviço. Então, cês começam a perceber que são sinais, né, não são regras. E ne-- e, então vocês começam a perceber, né, que são sinais e não são regras. E aqui a gente tem que tomar muito cuidado pra fazer essa quebra, porque isso aqui traz um benefício concreto, mas também paga um outro custo, né, o custo disso estar distribui-- o custo disso estar, o custo disso estar distribuído. Então mesmo que eu diga que uma aplicação cresceu e o monolito ficou muito complexo e quebrar em microsserviço possa ajudar, isso vai trazer uma complexidade

### 11:30
diferente. Antes eu tinha a complexidade ali do código mesmo, código muito grande, muitas classes, eu não sabia onde mexer, nanana. Agora eu tenho isso separado em serviços, beleza, mas aí é uma complexidade diferente. Às vezes o, a pessoa que entrou lá em search, né, na parte de buscas, não saiba que, hã, dependendo da categoria do usuário, pode aparecer, né, é, produtos +18 ou não. Pu-- aí ele vai lá, testa, testa, testa aquilo e, e não encontra regra nenhuma lá em search que, que diga isso. Até que ele

### 12:00
percebe que o objeto que ele tá recebendo lá de perfil, né, na chamada que ele faz de um serviço pro outro, tá mandando aquele, hã, is minor ou não pra ele, lá em algum if tava aquilo, mas ele nem, mas aí ele tá com uma conta de usuário que não era, né A, maior de 18. Aquele usuário era 16, só que lááá no, no serviço de, de perfil, tinha alguma regra pra emancipado, que tá retornando esse is minor também, só que essa regra não mora lá no código de quem tá mexendo em bugs, que a

### 12:30
pessoa não sabe disso. Então vai adicionando essa complexidade das coisas estarem distribuídas, separadas, né? Às vezes fica mais difícil também de tu debugar o código, de tu encontrar problemas, né? Então estourou um problema em produção. Eu tenho cinquenta chamadas de microsserviço pra aquela mesma parte do sistema. Puta, qual foi o microsserviço que deu problema? Como é que eu faço esse rastreamento da onde iniciou, né, a raiz daquele problema? Fica mais difícil em serviços distribuídos também, né, que são serviços que utili-- fica mais difícil em aplicações distribuídas,

### 13:00
isso também, né? Porque eu tô utilizando ali vários microsserviços. Então, é tudo uma balança, tá? Não é aquilo que o pessoal fala, tipo: "não, microsserviço é a melhor coisa que tem e vamos sempre usar isso, ou o monolito é a melhor coisa que tem". Existem duas coisas pra propósitos diferentes, pra contextos diferentes. A gente tem que saber analisar esses trade-offs, esses cenários, pra poder tomar essa decisão, tá, pra poder tomar a decisão do que que a gente vai escolher pro nosso time, porque alguma coisa a gente vai botar na balança das coisas boas, mas com certeza vão vir coisas pra balança

### 13:30
das coisas ruins, tá? Hã, bom, e aqui só pra garantir que a gente entendeu, tá? Bom, e aí só pra quê? Bom, e aí só pra qu-- bom, e aqui só pra garantir que a gente entendeu, tá? Bom, e aqui só pra garantir que a gente entendeu, tá? Porque isso aqui pode confundir muitas pessoas. Um monolito vai ser uma coisa que vai ser implantada junta, né, um único deploy. Lá dentro

### 14:00
do teu código, do teu monolito, pode ter módulos. Ah, eu posso quebrar entre o módulo do financeiro, o módulo da matrícula, o módulo do aluno, né, que são as pastinhas, lá tá tudo separado. Beleza, mas isso aí é um monolito modular. Mas no final das contas, é um monolito, é um único deploy. E depois é um único ponto de entrada praquele teu, hã, praquela tua aplicação, né. Tá tudo hospedado ali num único, numa única instância, tá? E pra eu comunicar um módulo com o outro, é tudo chamada local, é tudo importando a classe um do outro, os

### 14:30
comunicando via interface, mas é chamada local. Então isso aqui é um monolito, um único processo, um único deploy. Quando eu tô falando de microsserviço, eu já tô quebrando isso aqui em deploys independentes, já são projetos diferentes. Eu posso inclusive ter o pa-- a parte do financeiro implementado em Python e Django, e a parte do acadêmico implementado em Java Spring, não teria problema nenhum, porque são aplicações diferentes, e elas se comunicam através de contratos de API, tá? Aí aqui já não é mais chamada local, não é acessando a classe um do outro, chamando a função do outro. Não, aqui

### 15:00
é via chamada de API, tá? Tem outras maneiras de comunicação também. Um serviço de mensageria, por exemplo, ou outros protocolos de comunicação, mas o mais comum aqui é a chamada de API. Um fazer um post no outro, get no outro, né, via HTTP aqui. E aí a coisa importante é: são dois processos diferentes, deploys independentes, são dois artefatos, né, e eles vão se comunicar via operações de rede, tá? Hã, boa. E aqui pra finalizar, né, porque acredito que isso aqui vai trazer

### 15:30
muita confusão pra quem tá vendo esse conceito pela primeira vez, é como que então os microsserviços comunicam. Pô, Fe, tu falou que tu separou a matrícula do, da cobrança. Mas como é que a cobrança vai avisar a parte de matrícula que o pagamento tá confirmado e que pode liberar a matrícula daquele aluno? Bom, isso aqui, uma das formas de resolver é a comunicação via HTTP mesmo. Da mesma maneira como o meu monolito poderia chamar o, o meu monolito aqui poderia chamar o Stripe ou chamar a Appmax pra consultar a consulta da cobrança

### 16:00
lá no Stripe ou na Appmax, né, a gente faz essa chamada, via chamada HTTP, fazendo um get ou fazendo um post pra postar as informações da nova cobrança que eu quero fazer. A mesma coisa eu vou fazer entre os meus microsserviços, né, eles vão se comunicar através de API. Então eu faço, por exemplo, a minha parte do checkout fazer um post em cobrança, né, avisando que tem que fazer a cobrança do pedido da Ana, e quando a cobrança for compi-- confirmada, o pagamento for confirmado, eu aviso lá o meu checkout, né, a resposta do

### 16:30
que que, do que que foi resultado ali, se deu certo ou não. Isso aqui pode fazer de novo uma, um, um novo post. Eu posso chamar aqui via webhook também, né. Esse checkout expõe o webhook, webhook nada mais é do que um endpoint do CRUD também, um endpoint que recebe informação. Quando o provedor de pagamento termina o processamento, processa tudo certinho, ele faz um post no endpoint de webhook da minha aplicação aqui, que então processa esse evento, né, o evento de pagamento confirmado, ou pagamento cancelado,

### 17:00
etc, e toma suas decisões ali internas, tá? E aí, vocês vão perceber que isso aqui começa a introduzir outras, hã, camadas de complexidade, né, que é a camada de complexidade de informação perdida na rede. Caso um serviço esteja indisponível, caso essa, esse post dê errado na chamada HTTP, eu começo a perder informações, eu começo a ter que pensar em mecanismos de tolerância à falha, que é um dos trade-offs aqui do sistema distribuído, né, o custo do sistema distribuído.

### 17:30
É aquilo que eu falei, vai me tra-- vai me ajudar a resolver alguns problemas, mas pode me trazer outros problemas, tá? Então a gente tem que ter isso aqui muito claro na nossa mente. Agora, se você quiser entender um desenho de arquitetura de uma aplicação distribuída, né, de uma aplicação que utiliza microsserviços e também ver um código na prática, eu recomendo que você assista esses outros dois vídeos aqui que tão linkados no card, tá? A gente tá quebrando bem essa série de, de arquitetura de software pra não ficar

### 18:00
tudo concentrado num único vídeo, pra ficar fácil de consumir em partes e também pra quem quiser pegar só uma partezinha e aprender, assiste só esse vídeo, quem quiser vê a série completa, tá? Mas se você quiser, hã, ir mais a fundo, já tá linkado aqui pra você continuar os estudos e ver isso aqui na prática. Agora, se você sente que tá meio perdido nos estudos, queria-- agora, se você sente que tá meio perdido nos estudos e você queria um roadmap mais personalizado pro seu cenário, né, pro seu tempo de experiência, e queria também ter acesso a plantão

### 18:30
de dúvidas e aulas ao vivo, e também fazer parte de eventos presenciais da nossa comunidade, dá uma olhada no link que tá aqui na descrição desse vídeo, porque a gente tá construindo algo muito legal aqui na comunidade do Keeper Academy e eu adoraria te ver por lá. O link tá aqui na descrição e vamos ficando por aqui. Até a próxima live ou até o próximo vídeo. Falou!
