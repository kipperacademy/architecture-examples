# Transcrição — Aula 2: Design Patterns na prática
Fonte: [aula2_Bananecos FHD - Cam Extra - 10-42-34.mp4](https://drive.google.com/file/d/1v7GeLBqwcl3-gnuRgru2u4XHAEHNPXJY/view), gravação FHD da pasta compartilhada no Google Drive. Duração falada: 39min08s. Transcrição automática em português pelo ElevenLabs Scribe. Timestamps agrupados em blocos de 30 segundos a partir dos tempos por palavra. O texto não foi revisado palavra a palavra.
Fonte: `aula2_Bananecos FHD - Cam Extra - 10-42-34.mp4` na pasta compartilhada do Google Drive. Duração falada: 39min08s. Transcrição automática em português pelo ElevenLabs Scribe; timestamps agrupados em blocos de 30 segundos a partir dos tempos por palavra. O texto não foi revisado palavra a palavra.

## Texto com timestamps

### 00:00
Esse vídeo faz parte da nossa série de vídeos de arquitetura de software aqui do nosso canal. E no vídeo de hoje a gente vai aprender alguns design patterns que são muito utilizados na nossa comunidade. E, e nesse vídeo a gente vai, e nesse vídeo, e nesse vídeo, e nesse vídeo a gente vai discutir alguns design patterns que são fundamentais... Esse vídeo, esse vídeo, esse vídeo faz parte de uma

### 00:30
série de vídeos de arquitetura de software aqui no nosso canal, e no vídeo de hoje a gente vai falar sobre padrões de projeto ou design patterns. E a gente vai discutir quatro design patterns que são muito utilizados na comunidade, principalmente pra quem trabalha com Java ou programação orientada a objetos. O vídeo vai funcionar da seguinte forma: nos primeiros dez minutos a gente vai discutir uma parte mais teórica falando sobre cada padrão. O vídeo vai, o vídeo vai funcionar da seguinte forma: eu vou--

### 01:00
o vídeo vai funcionar da seguinte forma, o vídeo vai funcionar da seguinte forma: eu vou primeiro explicar a teoria, eu vou pri-- o vídeo vai funcionar da seguinte forma: eu vou primeiro explicar a teoria de cada design pattern e depois eu vou partir pro código com exemplo em Java pra você entender como aquele padrão de projeto pode ser aplicado no seu código. E aí você pode, e aí você pode, e aí, e aí, e aí você pode transferir esse mesmo conhecimento pra qualquer linguagem que permita

### 01:30
você implementar o paradigma de orientação a objetos. E aí, e aí, e aí, e aí você pode transferir esse mesmo conhecimento pra qualquer linguagem de programação que você esteja trabalhando. Seja Java, seja Java, JavaScript, TypeScript, Python, C Sharp, PHP, você consegue pegar esse fundamento e esse mesmo conceito e aplicar pra realidade daquela linguagem. Então sem mais enrolações, bora pro vídeo.

### 02:00
Hmmm. Bom. Bom, bom, bom, bom, nessa aula de design patterns na prática, a gente vai passar pelos quatro principais design

### 02:30
patterns. Bom, bom, nessa aula de design patterns na prática eu reuni aqui os quatro principais design patterns que são aplicados por muitos frameworks, seja pra quem trabalha com Spring, pra quem trabalha com Angular, pra quem trabalha com Next ou NestJS, você vai ver algum desses design patterns aqui sendo aplicados, mesmo que você, mesmo que involuntariamente. E a ideia aqui é que vocês também consigam aplicar esses design patterns na escrita do código de vocês

### 03:00
ou no momento que vocês forem guiar a inteligência artificial. Então a gente vai passar por Factory, Singleton, Strategy e Adapter. Inclusive, esse conceito aqui da Adapter vai ajudar muito pra quem for estudar depois sobre arquitetura hexagonal ou arquitetura limpa. Então começando com o que são design patterns, né? Design patterns são padrões pra resolver problemas comuns. E esses padrões eles vão nascer de um problema comum, né, um problema que seja recorrente. Então o que aconteceu foi:

### 03:30
ao longo da história da engenharia de software, foram se encontrando alguns problemas ali no momento da escrita e do design do nosso código mesmo que eram recorrentes entre diversos projetos. Então eu tava trabalhando lá na Microsoft, o outro trabalhando na IBM, o outro trabalhando no Google, mas todo mundo apesar de produtos diferentes, propostas e objetivos diferentes de empresas, alguns, alguns problemas, alguns problemas, alguns problemas acabavam sendo comuns entre todos

### 04:00
os códigos dessas empresas. E foi aí que nasce, e foi aí que nasceu, e foi aí que nasceu, e foi aí que nasceu o, e foi aí que nasceu os design patterns ou os padrões de código. A ideia aqui é compartilhar uma estrutura que vai nos ajudar a resolver esse problema, tá? Só que essa estrutura ela só vai ajudar... E a ideia aqui, e a ideia aqui, e a ideia aqui,

### 04:30
e a ideia aqui é propor uma, e a ideia, e a ideia dos design patterns é propor uma estrutura pro nosso código que nos ajude a resolver esse problema. E aí começando com o design pattern de Factory, a gente vai tá falando, e aí começando... E aí começando, e aí começando, e aí começando com o design pattern de Factory, a gente precisa, e aí começando com o design pattern de Factory, a gente primeiro precisa

### 05:00
entender o problema que ele resolve. Bom, a estrutura proposta pelo design pattern de Factory só vai ajudar quando ela acomodar uma mudança identificável. Ou seja, o que que seria essa mudança identificável? Digamos que a gente tem um sistema, tá, nosso ali, que trabalha com dois, hã, provedor, que trabalha com dois fornecedores, tá? Digamos que a gente tenha um fornecedor legado, ou seja, a gente utilizava antes alguma outra API terceira, uma API antiga, e agora a gente tá utilizando

### 05:30
um fornecedor novo, tá? E aí a gente... Então,

### 06:00
então Então pra gente entender . Então pra gente, então pra gente,

### 06:30
então pra gente entender o primeiro design pattern que a gente vai ver na aula de hoje, que é o design pattern de factory, a gente primeiro precisa entender o problema que ele resolve, tá? O factory basicamente diz pra gente separar a parte de criar uma instância, de usar uma instância. Então, a gente não precisa que a classe que usa aquela instância, né, então a classe cliente de uma outra classe, seja a mesma classe que instancia ela, né, que cria essa nova instância. Então a gente pode ter

### 07:00
um ponto único que vai conhecer essa parte da construção e a gente vai ter o consumidor que vai só receber esse objeto pronto. Vamo entender quando isso aqui se torna útil, tá? Imagina que a nossa aplicação, ela utilizava anteriormente algum provedor legado, né, a gente usava ali algum serviço de um fornecedor, a gente criou uma classe, hã, chamada, hã, Payment Provider, né, Legacy, Payment Provider Legacy, que ela precisa receber um monte de informação, precisa receber nosso certificado digital, nosso CNPJ, nossa

### 07:30
API key, hã, o nome da nossa empresa, o nome dos sócios, um monte de informação. Só que agora a gente tá migrando, né, prum novo fornecedor, um fornecedor novo, a gente tá usando aí o Avocado Pay, vamo pensar, né, ou a UV, não sei, o Stripe. Tamo migrando daquele legado prum novo provedor de pagamentos e esse provedor, pra gente criar uma instância do cliente dele, a gente só precisa passar a nossa API key e o ID da nossa conta. Não precisa passar certificado digital, não precisa passar nome da empresa, nome do

### 08:00
sócio, não precisa de mais nada, tá? Mas as duas classes, a gente vai ter ali a classe Legacy e a classe Nova, elas respeitam a mesma interface, tá? As duas expõem os mesmos métodos, o método de charge, o método de refund, tá? Então elas tão respeitando os mesmos, hã, a, a mesma interface. Só que pra instanciar cada uma dessas implementações, eu preciso passar parâmetros diferentes, porque o, o, o provedor que tá ali por baixo pede coisas diferentes mesmo, tá? E aí eu ia ter um

### 08:30
problema, né, se se a classe que fosse consumir, hã, se a classe que fosse consumir essa, esse cliente, utilizar ele, tivesse que conhecer a construção de cada uma das minhas implementações, eu ia ter que ficar, eu ia ter que, eu ia ter que ficar, eu ia ter que ficar, eu ia ter que criar, eu ia ter, eu ia ter que criar uma dependência com etapa de construção de cada classe. E aí eu posso fazer, e aí eu posso, e aí, e

### 09:00
aí eu posso, então, então, então eu posso, então eu posso pegar essa parte da construção e abstrair pra uma outra classe que a gente vai chamar de factory, e a classe de consumidor só vai usar o contrato direto, né, só vai usar o contrato exposto por aquelas classes de implementação e receber o objeto já pronto, tá? Só que obviamente vai ter uma classe por fora, como por exemplo ali a nossa classe Main, que vai ser a classe que vai escolher a opção que vai ser usada. Ah,

### 09:30
é pra iniciar com o Legacy ou é pra iniciar com o New, né, com o novo provedor. Então vai ter alguém que vai escolher essa opção, a fa-- a factory vai montar essa instância, ela que vai instanciar, e então o consumidor só vai utilizar esse objeto e depender do contrato, tá? E aí, deixa eu mostrar um exemplo que vai ficar muito mais claro. Então vamo abrir aqui o nosso código. E aqui a gente tem uma classe que é uma classe de factory, tá? Então essa classe de factory a gente chamou de pagamento factory, que é pra seguir aquele exemplo do paga-- do, do Payment Provider, né.

### 10:00
E ela vai expor um método que vai se chamar Criar, tá? E aí vocês percebam que essa classe aqui ela tem um método estático de criar. Por que que ela tem esse método estático? Porque eu não quero ficar criando também instâncias da minha factory. Eu quero só chamar pagamento factory ponto criar. Eu não quero fazer pagamento factory, né, new pagamento factory, depois pagamento ponto criar. Então, ao ser estático, eu consigo chamar diretamente esse método. E o que esse método faz é, ele compara qual é o fornecedor que foi, hã, solicitado, o fornecedor que foi pedido, né, se foi o legado

### 10:30
ou o local, e então retorna à instância ou do legado ou do local. Mas o bacana é que essa classe de factory é a que vai conhecer o, os detalhes da construção de cada uma dessas classes, de cada uma dessas classes. Então se o meu legado aqui, como eu falei pra vocês, precisasse de um certificado digital, precisasse do CNPJ, precisasse do nome dos sócios, nome dos sócios, hã, sei lá, precisasse do endereço, API key, nananá, quem ia conhecer isso ia ser a factory, ela ia buscar essas

### 11:00
informações onde ela precisa. E aqui o pagamento local só ia precisar, por exemplo, do API key e do CNPJ. E ela que conhece essas diferenças de construção, tá? Ela faz a instanciação, ela cria a instância dessa classe dependendo do que for pedido, né, do fornecedor que foi pedido, e só retorna isso. Se a gente olhar o pagamento legado, ele implementa a interface pagamento. E se a gente olhar aqui, o pagamento local também implementa.

### 11:30
E se a gente olhar aqui, e se a gente olhar aqui, o pagamento local ele implementa o consulta pagamento. Mas eu poderia ter esse pagamento local aqui implementando a mesma interface. Então eu poderia vir aqui e botar implements pagamento, implementar a classe pagamento. E aqui eu ia ter que exportar a, o método cobrar, né. Então aqui eu tenho que chamar de cobrar e aqui eu ia ter que retornar um inteiro, né, então aqui eu ia retornar um inteiro.

### 12:00
E aqui é só fazer, sei lá, um Um System.out.println cobrando no novo, né. E eu posso receber e vou retornar o in-- o inteiro que eu recebi aqui.

### 12:30
Então, por exemplo, recebi o valor, vou retornar o valor mais zero um, digamos que foi minha taxa, né? O valor mais um real, digamos que foi a minha taxa. Então agora eu tenho o pagamento local e o pagamento legado, né, implementando-- e o pagamento legado, né, implementando a mesma interface, só que com diferenças de implementação. Então o pagamento legado aqui tá usando a SDK do provider legado, tá tendo que

### 13:00
fazer uns cálculo, mover ponteiro, etc, sei lá, tá fazendo coisas diferentes. E o pagamento novo tá aqui com a implementação, né, hã, mais atualizada, mais simples, digamos assim, que foi por isso que a gente tá fazendo essa refatoração, só que tudo, toda essa construção tá concentrada na minha factory. E aí o legal, e aí o legal,

### 13:30
e aí o legal, e aí o legal é o seguinte: a classe-- Aí o legal é o seguinte: a classe que vai decidir qual provider eu vou utilizar vai ser a classe mais de fora. Então digamos que eu tenho a minha classe Main chamando meu pagamentoFactory.criar, ó, tá vendo que eu tô chamando direto o método. Eu não precisei fazer assim, ó, new pagamentoFactory, tá? A factory não é pra gente criar instância, é pra ter métodos abstratos mesmo. E aí isso aqui me retorna um objeto do tipo pagamento. Eu pego esse pagamento e injeto no meu checkout.

### 14:00
A minha classe de checkout, ela depende só da interface de pagamento, tá vendo? Só depende dessa interface aqui. Eu não sei se por fora eu tô usando o legado, se eu tô usando o novo, não importa, tá? E também aqui na classe Main, ele não se importa em saber a construção de cada uma dessas classes de pagamento, ela só se importa em chamar a factory. Quem usa muito isso aqui da factory de maneira abstraída e que a gente acaba nem vendo é o próprio Spring lá do Java. Então agora vamos seguir pro nosso próximo design pattern, que é o design pattern

### 14:30
de-- Agora vamos seguir, agora vamos seguir, agora vamos seguir pro nosso próximo design pattern, que é o design pattern de Singleton. Esse design pattern de Singleton recebe o problema de in-- Esse design pattern do Singleton resolve o problema de compartilhamento de instâncias. Então a ideia aqui no Singleton é que a gente consiga compartilhar uma única instância por execução. Então,

### 15:00
a gente vai ter uma classe que vai controlar a criação dessa instância e fornecer o acesso pras outras classes consumidoras da mesma referência, né. Então digamos que a gente tenha ali de novo a classe Main instanciando o pagamento provider, e aquele pagamento provider eu poderei injetar no meu checkout, eu poderei injetar nas minhas matrículas, eu poderei injetar onde quer que eu precisasse, certo? Hã, claro, evitando sempre um acoplamento, mas poderia fazer a injeção da mesma instância que eu criei. E aí todas essas

### 15:30
classes consumidoras, seja a matrícula, seja checkout, seja a classe user, iam tá utilizando a mesma instância do pagamento provider. E dessa forma eu consigo ter compartilhamento de status, e dessa forma eu consigo ter, e dessa forma eu consigo ter o quê? Compartilhamento de estado, tá? E esses-- E dessa forma eu consigo ter o quê? Compartilhamento de estado. E esse design pattern aqui, ele vai ser muito utilizado, principalmente quando a gente tiver criando um repository,

### 16:00
né, ou uma classe que vai fazer a conexão com o nosso banco de dados. Então a gente vai criar uma instância de uma classe que se, que cria uma conexão com o banco de dados, né, e essa classe vai ser um Singleton. Eu vou compartilhar essa conexão com todas as classes que vão precisar consultar no meu banco. Dessa maneira, eu não preciso abrir várias conexões com o meu banco, eu compartilho a mesma conexão, né. E aí o Singleton me ajuda nisso, porque eu tenho um compartilhamento de estado. Caso, dentro dessa classe, né, que eu criei ali a instância, tivesse alguma variável, por exemplo, um contador, e eu fosse

### 16:30
aumentando esse contador, eu conseguiria ter o compartilhamento desse valor entre as classes também, tá? Mas isso aqui já não é muito utilizado. Acho que o exemplo mais claro aqui que a gente pode ter é esse exemplo do banco de dados. Então como é que vai funcionar? Eu vou ter uma cla-- a classe Consumidor um e a classe Consumidor dois, as duas pegando a instância ali do, do, do cliente que elas tão usando, seja um cliente do banco de dados, seja o cliente do pagamento provider, seja até uma instância da, da classe matrícula, sei lá, e usando, né, apontando as

### 17:00
duas pra mesma referência, tá? E o bacana é o seguinte, que o mecanismo de criação, ele vai ficar... E aí o bacana é o seguinte, e o bacana, e o bacana, e aí o bacana é o seguinte, e aí o bacana é o seguinte.

### 17:30
E aí o bacana, e aí o bacana é o seguinte: é que a gente salve essa instância que a gente criou em alguma outra classe mais de fora, né. E aí sempre quando alguém precisar acessar essa mesma instância, vai chamar ali um getInstance. Então, vamo juntar aqui com o exemplo da factory. Digamos que a gente tenha aqui a classe mais de fora, que é essa Registro de Compras. A Registro de Compras inicia uma nova instância, hã, de pagamentos, digamos, só que chamando a factory de pagamentos. Aí ela salva essa instância numa variável, que ela vai chamar aqui de instância,

### 18:00
e sempre quando alguma outra classe precisar dessa instância, é só chamar o getInstance que ela vai retornar a mesma instância, né. Então eu vou fazer o meu new aqui uma única vez, eu vou criar uma insta-- uma instância daquela classe uma única vez, e depois eu vou retornar o mesmo objeto sempre. Eu vou sempre referenciar o mesmo objeto, tá? E aqui trazendo o exemplo do contador, né. Digamos que eu tenho o, a classe Registro Ana e a Registro Bia, as duas chamam a mesma referência, né, de Registro Compras, e lá dentro

### 18:30
de Registro Compras eu tenho um contador. Daí esse contador começa em zero, depois em um, e quando a Bia chamar, vai incrementar pra dois, né, não vai zerar de novo pra um, porque a instância é a mesma, tá? Então, hã, elas vão tá, no final das contas, hã, atualizando ali o mesmo campo, caaaso esse campo, seja um campo do escopo da classe, né, não do escopo do método. Se isso aqui for um contador que vive somente dentro do escopo do método, eu vou chamar o método uma vez, o método vai executar, depois que aquele método para a execução, eu perco aquela,

### 19:00
aquela informação, né. Eu só vou conseguir compartilhar esses estados, caaaso seja uma variável que tá salva no escopo da classe, não no escopo dos métodos. E aí vamos abrir aqui de novo o nosso exemplo, tá? O exemplo aqui do Singleton.

### 19:30
Então olha só. Então olha só. Então olha só. Então olha, então olha só o que a gente tem aqui. A gente tem a nossa classe Main, que tá criando o registro de compras pra Ana e pra Bia. As duas, eu tô chamando essa classe aqui, Registro Compras, que tem

### 20:00
um, um método estático de getInstance né. E aqui o que ele faz no getInstance é criar, é retornar a instância do registro de compras que tá sendo criado aqui como, né, uma dependência-- que tá sendo criado aqui como... Que tá sendo criado aqui como... Que tá sendo criado aqui como a dependên-- que tá sendo criado aqui na raiz da classe Registro de Compras, onde eu já faço um mil registro de compras, tá? E aí aqui eu tenho a minha quantidade, por exemplo,

### 20:30
e eu vou salvando essa quantidade, compartilhando ela também entre, hã, entre as execuções. E aí o que eu faço é, Registro Ana e Registro Bia, eu recupero através do getInstance. Só que eu posso fazer aqui a Ana e a Bia usarem um método de checkout diferente, né, então eu posso aqui fazer um pagamento fac-- então eu posso fazer aqui uma chamada pro pagamentoFactory.criar né, pra criar aqui o provider Legacy pro checkout da Ana e criar o provider novo, por exemplo, e sem desconto pra Bia.

### 21:00
Só que as duas compartilhando o mesmo registro de compras, né, que seria a mesma instância ali. E quando a gente executar isso aqui ó, cês vão ver que o valor do registro de compras é compartilhado.

### 21:30
E aí quando, e aí quando a gente executar isso aqui ó, a gente vai ver que... E aí quando e... E aí quando a gen-- e aí quando a gente executar is-- e aí quando a gente executar isso aqui ó, cês vão

### 22:00
ver que a compra vistas por Ana e compra vistas por Bia, as duas vão printar dois, tá? Onde eu tô puxando aqui registro Ana e registro Bia.quantidade. Por quê? Porque é a mesma instância da classe, né, então mesmo que a Ana foi a primeira a comprar, quando eu chamo a quantidade aqui do registro Ana, ele printa o dois também, porque a Bia acabou incre, hã, incrementando isso pra dois. Se eu fizesse esse System.out antes do chaga-chamamento da Bia, antes do chamamento da Bia ó, eu faço, hã, comprar,

### 22:30
eu faço compra-compraAna.comprar, faço o print, depois comprar Bia.comprar, cês vão ver que isso aqui já vai mudar. Então deixa eu fazer aqui. A re-- deixa eu buildar de novo e agora a gente vai executar. Tá. Peraí. E

### 23:30
aí vocês vão ver aqui ó, que quando a gente for executar, quando printar o da Ana, vai printar um e quando printar o da Bia depois vai printar dois.

### 24:00
Por quê? Porque eu printei antes da Bia completar a compra. Quando eu tava printando, né, depois das duas já terem completado a compra, a quantidade foi incrementada pra dois aqui pela Bia. E mesmo que a Ana tava chamando aqui a, a referência que ela recebeu do registro compras, como a referência pra mesma classe que a Bia também recebeu Elas acabam compartilhando esse estado interno, né, as classes ali, porque é a mesma classe, é a mesma instância. E aí, hã, eu acabo printando aqui a compra vistas como dois pras duas, né. Então

### 24:30
se eu venho aqui e recompilo novamente e executo, a gente vai ver que agora volta pra dois, né, quando eu faço o print depois da Bia já ter comprado. Por que que isso acontece? Se a gente entra aqui em checkout, a gente vai ver ó, no checkout eu tô fazendo primeiro o-o cálculo do preço, preço calculado, pagamento.cobrar e então registro. Registro que aquela compra aconteceu no meu registro de compras. Como o registro de compras é uma única instância, é um Singleton compartilhado entre os dois checkouts, né, acaba

### 25:00
incrementando ali o-o estado interno. E agora vamos pra nossa próxima. E agora, e agora, e agora, e agora, e agora pra gente finalizar aqui o entendimento de Singleton, uma única coisa tem que ficar na mente de vocês, tá? Que esse escopo, ele vai terminar nessa execução. Então, a JVM vai iniciar a execução desse código, vai criar essa instância. Enquanto o código tá rodando, a instância é a mesma e eu mantenho esse valor

### 25:30
ali salvo. Caso eu reinicie esse meu programa, né, execute de novo ou a-acabe ali a execução, que foi o meu caso, e executo mais uma vez, ele não fica incrementando, ó, não virou quatro aqui, continua sendo dois. Por quê? Porque quando para a execução, morre tudo, eu perco aquela instância. A instância vai ser recriada novamente quando eu executo o código de novo, tá? Então a cada nova JV-JVM, né, a cada nova execução, digamos assim, vai iniciar novamente aquela instância. O Singleton vai persistir somente durante a execução do programa, tá? Quando

### 26:00
vocês fazem lá o npm run dev e mantém o servidor rodando, tá rodando. O Singleton foi criado, consegue sendo compartilhado por todas as classes. Matou a execução do servidor, aquele Singleton morreu também. E aí quando executar o servidor de novo, ele vai ser reiniciado, uma nova instância vai ser criada, todas as variáveis internas deles vai ser, hã, recriadas, né, e-e v-vão ser voltadas ali pro seu valor original, tá? Então se eu quisesse persistir isso mesmo, sem perder nunca, eu tenho que salvar no banco de dados. Aqui a gente tá

### 26:30
usando esse estado interno mais como exemplo, mas como eu disse, não é uma boa prática. Aqui eu vou usar essa, essa vantagem do Singleton pra, só pra cenários onde realmente faz sentido o compartilhamento desse estado, como é o caso que eu falei pra vocês da instância do banco de dados. Eu posso criar a instância uma única vez ali no início da minha aplicação, quando ela inicia a execução, depois eu compartilho entre todas as classes. Quando o servidor morre, quando a execução para, porque eu vou fazer um deploy, porque eu parei aqui na minha máquina, porque eu vou trocar, hã, o servidor que eu tô usando, daí aquela

### 27:00
conexão com o banco de dados vai ser, hã, quebrada, né, aquele, aquela classe vai ser morta, porque o programa já não tá mais executando, e depois só vai ser iniciado quando o programa iniciar novamente. Mas nesse caso não tem problema, né, porque eu não, não, não preciso salvar a conexão com o banco de dados no banco de dados, tá? Boa. Então agora vamos pro próx-- vixe, tomar uma água.

### 28:30
Então agora... Então agora vamo-- então agora vamos pros nossos últimos dois design

### 29:00
patterns que-- então agora vamos pros nossos últimos design patterns, começando aqui com o design pattern de strategy, mas eu vou mostrar o strategy na prática somente quando a gente for ver ali a parte do adapter, porque vai ficar mais fácil de entender as coisas. Então o strategy é um design pattern que vai definir que o contrato, o con-- então o s-o strategy é um-- então o strategy é um design pattern que vai nos ajudar a definir o contrato, o contexto e as alternativas

### 29:30
disponíveis pra cada contexto, tá? Então o-o nome strategy é justamente o que vocês tão pensando, estratégia. Então a gente vai usar esse design pattern quando a gente precisa de-- então a gente vai usar esse design pattern quando a gente precisa decidir entre diferentes estratégias de alguma coisa, tá? Vamos usar aqui o exemplo de calcular o preço final, tá, no checkout. Digamos que vai ter cenários onde eu vou precisar usar a estratégia de implementar um desconto no Pix, que aí o cálculo do pagamento, né, o cálculo ali

### 30:00
do valor final vai ter que aplicar esse desconto E por que que vai ter um cálculo? Ah, porque o-o valor do produto vai tá salvo em centavos no banco, o valor do, do, do cupom de desconto tá salvo em reais, eu tenho que, hã, colocar todos na mesma, né, moeda e eu tenho que aplicar o desconto em cima do valor do produto, eu tenho que ver se isso não passa os trinta por cento máximo de desconto, que é a política da nossa empresa. Então tem toda uma estratégia por trás de aplicar o desconto, não é só reduzir o valor. Então isso aqui é uma estratégia diferente. Quando eu vou fazer o cálculo do valor

### 30:30
final e não tem desconto nenhum, a única coisa que eu preciso fazer é traduzir de centavos pra real, hã, ver se aquilo ali não estoura o limite de compras que o cliente pode fazer no dia. Digamos que por algum motivo eu controle que o meu cliente só pode gastar mil reais por dia na minha loja, porque eu quero evitar que as pessoas ficam comprando, tipo, eu vendo atacado, vendo, hã, mouse a dois reais, eu não quero que os cara comprem duzentos mil mouse porque não dá. Daí os cara só pode gastar mil reais na minha loja, né. Tem lojas que têm esse controle. Aí aqui eu só ia precisar

### 31:00
fazer esse controle, né, se não tá passando do limite, mas não ia ter que ter todo um cálculo ali do desconto, né, diferente quando a pessoa paga no Pix. Só que são duas estratégias diferentes, mas no final das coisa-- mas no final, mas no final das contas, o resultado é o mesmo, né. É um valor final, é o montante que esse usuário vai pagar. Aí a gente vai utilizar a, o design pattern, né, a técnica aqui de strategy, justamente pra gente concentrar essa decisão numa classe que a gente vai chamar, por exemplo, de política de preço.

### 31:30
E a gente vai usar, e aí a gente vai usar aqui o design pattern de strategy, justamente pra gente controlar essas alternativas e decidir dependendo do contexto, né. Então o contexto de fora vai chamar o comportamento, né, e vai utilizar ali a política de preço, que então vai escolher a alternativa, se é a sem desconto ou se é a desconto no Pix, então vai aplicar aquela alternativa escolhida, né, aquela estratégia de pagamento, por exemplo. Então, digamos aqui ó, só pra vocês

### 32:00
entenderem em que momento eu teria essas diferentes estratégias, né, porque às vezes fica difícil de, da gente conseguir entender, tipo, tá, mas por que que eu teria diferentes estratégias pra uma mesma ação? Bom, imagina que pro mesmo preço eu posso ter uma política diferente, né. Digamos aqui que eu tô fazendo a venda de um produto que custa dez mil centavos, tá? E aí, e aí, e aí, e aí, e aí quando o meu cliente for pagar no Pix, eu tenho que pegar esse preço, multiplicar por noventa,

### 32:30
né, porque vai ter um desconto ali de, de dez por cento, então eu multiplico por noventa, divido por cem pra chegar no desconto final, né, no valor final. Quando esse preço não vai ter desconto nenhum, eu só pego e retorno o valor final. Isso aqui é aquilo que eu falei pra vocês, são duas estratégias diferentes. Pra eu não precisar ficar criando um if pra cada, hã, né, estratégia, pra cada campanha aqui que eu chamei, eu uso o design pattern de strategy, porque senão eu ia ter que ficar criando um monte de if na minha classe. Ah, não, no cartão

### 33:00
quando vai parcelar em duas vezes é dois por cento de desconto. No Pix é cinco por cento, no boleto é, não tem desconto, mas o frete é grátis. Quando o cliente tá pagando, hã, com, sei lá, parcelamento com juros, a gente dá um bônus pra ele de cinco de cashback, porque ele pagou um monte de juros e a gente quer que ele volte. Então percebam que podem ter estratégias diferentes. E a cada estratégia, se eu não utilizasse o design pattern de estratégia, eu ia ficar encadeando if. Ah, if tal coisa, faz tal coisa. If tal coisa, faz

### 33:30
tal coisa. If tal-- aí eu ia ter aqueles ifs enormes, né? Gigantescos, que esse é o problema que a gente tá resolvendo com a estratégia. E aí pra eu evitar esses ifs enormes, eu uso o design pattern de strategy, tá? Aí agora... Aí agora, e aí agora, e aí agora, e agora, e agora a gente vai pro design pattern final, que é o design pattern de adapter, que a gente vai

### 34:00
colar todas as pontas, tá? Então o adapter é o design pattern que a gente usa pra traduzir uma interface em uma implementação, né. Quem assistiu a última aula, onde a gente falou sobre, hã, segregação de interfaces, que a gente tava falando sobre acoplamento e injeção de dependência e inversão de dependência também, né. Vale lembrar que a gente criou interfaces pra evitar que as nossas classes fossem acopladas direto em implementação de classes externas, né. E o adapter

### 34:30
é um design pattern que a gente pode usar pra traduzir uma interface em uma implementação. Então, de, de novo, aquele exemplo do pagamentos, né, eu posso ter vários payment providers que eu tô usando. Eu posso ter uma única interface de payment provider que vai, hã, definir que todo payment provider tem que expor o método charge. Mas aí eu posso ter o payment provider pro Abacate Pay, pro Stripe, pra UV, pro Transfera, pro Pagar-me, sei lá, né, eu posso integrar minha aplicação com todos esses

### 35:00
providers. O que vai traduzir a minha interface pra, pra implementação interna de cada dos providers vai ser esse meu adapter. Então eu vou criar uma nova classe, por exemplo, hã, Abacate Pay Adapter, que vai implementar a classe Payment Provider. Eu vou criar a minha classe Pagar-me Adapter, que vai implementar a minha interface de Payment Provider, entende? Então é isso que o adapter vai fazer. Vai fazer essa tradução da interface pra implementação, tá? E aí vamo lá olhar o exemplo que vai ficar muito

### 35:30
mais claro. Então deixa eu abrir aqui o nosso código, tá? E vamo pensar no seguinte. Então, então olha só. Então olha só. Então olha, então olha só, lembra que a gente viu aqui essa classe de pagamento legado?

### 36:00
Essa classe de pagamento legado ela tá implementando a nossa interface de pagamento, tá? Que é aqui o nosso contrato A minha classe de pagamento legado eu chamei ela de um adapter porque ela tá implementando a interface. Por que que ela é um adapter? Porque ela tá adaptando o meu SDK de pagamento legado pra obedecer a interface de pagamento, aí ela tá fazendo essa adaptação. E aí aqui eu instancio o meu SDK antigo, eu posso chamar certificado digital, eu posso fazer tudo que eu precisasse fazer. Os detalhes da implementação

### 36:30
não me importam, isso aqui vai ficar abstraído dentro dessa classe. O bacana é que essa classe ela vai tá sempre respeitando a minha interface, o meu contratinho, né, definido aqui no meu código. As classes que forem utilizar o pagamento depois, o pagamento provider, vão utilizar, vão depender somente da interface de pagamento, né? E não vão saber se ali por baixo tá rodando o pagamento legado ou tá rodando o pagamento novo, tá? E o bacana é que eu vou criando esses adapters pra adaptar a minha interface pra uma implementação. E aí, indo pra

### 37:00
parte do strategy, aqui o que a gente poderia fazer ó, é criar uma interface de política preço. E aí eu criar várias políticas de preço, política de preço no Pix, política de preço no cartão, política de preço no boleto, política de preço no pagamento em dinheiro, todas respeitando a mesma interface, mas implementando estratégias diferentes. E aí no final eu vou ter um strategy que toma a decisão de qual política de preço eu vou utilizar no momento de calcular o valor, né? E aí eu tô combinando aí adapter que adapta uma interface prum,

### 37:30
pra uma implementação, no caso aqui do nosso pagamento, e também o strategy que eu vou ter uma interface única que define como a política de preço tem que comportar e depois um strategy que chama todas as políticas de preço disponíveis e dependendo do cenário, do contexto ela decide qual política de preço utilizar. Se vai usar Pix, se vai usar cartão, se vai usar boleto, né, sem precisar ficar criando um monte de if com, hã, um monte de if com um monte de linha, né, ali dentro com, com a implementação de cada cenário. E aí, se você quiser,

### 38:00
e aí se você quiser, e aí se você, e aí se você quiser continuar seus estudos de arquitetura de software, continuar se aprofundando, eu recomendo que você continue assistindo essa playlist de vídeos que tá aparecendo aqui na tela. A gente tá lançando a cada semana uma nova, a gente tá lançando a cada semana um novo vídeo dessa série de vídeos de arquitetura e cada aula a gente tá indo cada vez mais profundo. E se você quiser um roadmap de estudos, mas se você quiser... Mas se você quiser um passo...

### 38:30
Mas se você quiser dar um passo além, mas se você quiser dar um passo além, mas se você ainda se sentir, mas se você ainda se sente meio perdido do que estudar, mas se você ainda se sente meio perdido do que que você precisa estudar, qual o próximo tópico e gostaria de um roadmap de estudos personalizado pro seu cenário, ter acesso a um plantão de dúvidas com aulas ao vivo e também participar de eventos presenciais da nossa comunidade, dá uma olhada nesse link que eu deixei aqui na descrição que a gente tá

### 39:00
criando algo muito legal aqui pra nossa comunidade através do Keeper Academy. Esse vídeo vai ficando por aqui, te vejo na próxima live ou no próximo vídeo, falou.
