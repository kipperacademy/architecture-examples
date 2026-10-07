# Transcrição — Aula 6: Arquitetura assíncrona
Fonte: [aula6_Bananecos FHD - Cam Extra - 13-08-36.mp4](https://drive.google.com/file/d/1VngP8axes5sEnIpkOfZksdp8SsBkeb4p/view), gravação FHD da pasta compartilhada no Google Drive. Duração falada: 27min17s. Transcrição automática em português pelo ElevenLabs Scribe. Timestamps agrupados em blocos de 30 segundos a partir dos tempos por palavra. O texto não foi revisado palavra a palavra.
Fonte: `aula6_Bananecos FHD - Cam Extra - 13-08-36.mp4` na pasta compartilhada do Google Drive. Duração falada: 27min17s. Transcrição automática em português pelo ElevenLabs Scribe; timestamps agrupados em blocos de 30 segundos a partir dos tempos por palavra. O texto não foi revisado palavra a palavra.

## Texto com timestamps

### 00:00
Esse vídeo faz parte de uma série de vídeos de arquitetura de software que a gente tá fazendo aqui no nosso canal, e no vídeo de hoje a gente vai conversar-- e no vídeo de hoje a gente vai discutir alguns conceitos que são muito importantes pra você entender como funciona uma arquitetura de uma aplicação assíncrona. E quando eu digo uma aplicação assíncrona, eu não tô falando das chamadas HTTP que você faz, né, do fetch, do post que você faz lá no seu front-end

### 00:30
e faz o async/await. Não, aqui a gente tá falando sobre uma arquitetura de aplicação assíncrona, onde a gente tem uma aplicação distribuída, quebrada em microsserviços, conceito que a gente já viu em aulas anteriores e que seria bom você já entender pra conseguir assistir essa aula. Então a gente começa a estruturar essa aplicação pra que uma coisa converse com a outra e consiga ter reações a esses eventos. Então, sem mais enrolações, bora pro vídeo.

### 01:00
Bom, bom, quando a gente... Bom, quando a gente começa a falar sobre arquitetura assíncrona, a gente começa a se deparar... Bom, bom, esse vídeo faz parte de uma série de vídeos aqui do canal, onde a gente... Esse vídeo faz parte de uma série de

### 01:30
vídeos aqui do canal, onde a gente tá discutindo temas de arquitetura de software e engenharia de software. E no vídeo de hoje a gente vai se aprofundar um pouco mais em conceitos de arquitetura assíncrona, que acabam permeando muito os sistemas distribuídos. Aqui a gente não tá falando do assíncrono, do async/await lá do JavaScript, onde a gente faz uma chamada do front-end pro back-end e tem que esperar a resposta. Não, aqui a gente tá falando de sistemas distribuídos que já foram quebrados em microsserviços e essas diferentes peças do meu sistema

### 02:00
precisam se comunicar. E essa comunicação entre essas peças é assíncrona, e a gente pode gerenciar essa comunicação de diferentes formas. E é justamente esses conceitos que a gente vai aprofundar um pouco na aula de hoje. Então, sem mais enrolações, bora pro vídeo. Bom, quando a gente tá falando sobre um sistema distribuído, a gente tá falando que a gente vai ter múltiplas aplicações que vão estar ali se comunicando a fim de criar,

### 02:30
né, no final das contas, uma experiência pro meu usuário, né, uma aplicação que o meu usuário vai perceber como uma única aplicação, mas que por trás tá distribuído entre vários sistemas, né, vários motorzinhos ali, hã, rodando pra que o usuário consiga utilizar aquilo. Aqui a gente pode trazer exemplos como o próprio Mercado Livre, né. Você tá acessando ali o site do Mercado Livre, vai fazendo suas compras, adicionando ao carrinho, né, realizando o seu pedido. Mas por baixo dos panos a gente tem um sistema supercomplexo integrando camadas

### 03:00
de pagamento com camadas de busca, com camadas de catálogo e listagem de produtos, com camadas de shipping de transporte, né. E a gente consegue derivar esse mesmo exemplo pra o caso da Amazon. A gente consegue pegar o exemplo dos bancos também, que ali pra você, na interface, é só o aplicativo do banco, faz o Pix, pega os boletos, mas por trás, com certeza, aquilo ali tá quebrado em diferentes, né, serviços, cada um cuidando de uma parte do sistema. Então uma parte do Pix, outra parte do boleto,

### 03:30
outra parte do seu cartão de crédito, outra parte de fraude, outra parte da senha, da conta, da autenticação, enfim. Só que esses sistemas, pra que a gente consiga enxergar como uma única coisa e o usuário consiga utilizar, né, e de fato usar as nossas funcionalidades, eles precisam se comunicar. E é aqui que vai morar a parte da arquitetura assíncrona em sistemas distribuídos. Bom, bom,

### 04:00
bom, então quando a gente fala de arquitetura assíncrona, é isso que vai permitir continuar, né, o... Bom, quando a gente fala de arquitetura assíncrona, é isso que vai permitir que um sistema continue a sua execução depois do resultado final de outro serviço, tá? Então digamos aqui que eu tenho dois microsserviços, meu microsserviço de loja ou de catálogo, que se comunica com o estoque, né. Essa aplicação de loja pode ser uma aplicação Spring, pode ser um Django, pode ser um Next App, sei lá, qualquer coisa, tá?

### 04:30
Isso aqui é uma aplicação separada da aplicação do estoque. Inclusive, eles podem ter bancos de dados separados, tá? Essa aplicação vai se comunicar via API com a minha segunda aplicação, que é quem controla a minha parte do estoque, pedindo pra reservar o item, né, de ID sete. Essa aplicação de estoque não vai retornar diretamente, automaticamente uma resposta dizendo que tá tudo certo. Não, primeiro ela vai ter que fazer... Não, primeiro ela vai ter que fazer algumas validações, como por exemplo, a verificação se esse item existe,

### 05:00
né, e se é dessa loja mesmo, se tem esse item no estoque e se tá permitido fazer a reserva pra aquele item, porque eu posso ter itens ali, hã, muito, né, concorridos que eu não faço reserva, ou compra ou não compra, né. E depois de todas essas verificações, eu então retorno pra segunda aplicação de que aquilo está liberado, né, e que ela pode confirmar a reserva pro usuário. Só que enquanto isso aqui vai acontecendo na minha aplicação B, a outra aplicação tá aguardando, né, ela tem que aguardar uma resposta

### 05:30
pra reserva continuar. E isso aqui que a gente tem de troca de informações entre esses sistemas é o que a gente chama de uma arquitetura assíncrona. E pra gente trocar essas informações, não necessariamente a gente precisa fazer dessa maneira como eu mostrei pra vocês, né, de fazer chamadas de API, faz o post lá na aplicação B, fica esperando o retorno do post, quando chega o retorno, eu ajo, né. Eu posso simplesmente só fazer um aviso pro outro sistema, um aviso de estoque, seguir minha vida e só depois quando aquilo produzir um resultado a

### 06:00
um evento, eu retomo da onde eu parei, tá? E aí vocês vão ver aqui nessa, nessa aula algumas maneiras, algumas técnicas da gente fazer isso, tá? Então? Então? Então? Então? Então? Então, pra gente garantir que a gente-- então, pra gente garantir que a gente tá na mera-- então, pra gente garantir que a gente tá na mesma página, vamo rever aqui o que que o assíncrono significa. O assíncrono significa

### 06:30
eu aceitar uma informação agora e concluir ela depois, né. Então quando a gente tá falando de algo síncrono, eu vou fazer passo por passo, né, então passo um, passo dois, passo três, passo quatro, um seguido do outro, né, e de maneira linear. Quando eu tô falando de uma coisa síncrona, eu vou fazer o passo um, o passo dois, o passo três. Opa, o passo três não vai produzir um resultado agora, porque eu tenho que, não é só executar o passo três, tem que consultar o banco, tem que esperar o resultado do, do, do, do retorno lá do, do

### 07:00
Itaú, porque vai ter que confirmar a compra ou não, vou ter que consultar lá na transportadora, né. Tem, vai ter um tempo ali por trás, certo? Aí o que que eu faço? Eu beleza, disso-- eu beleza, eu beleza, produzo, eu beleza, produzo esse evento, né, de que eu preciso fazer esse passo três, mas então a minha aplicação segue a sua execução, né, permitindo que o usuário use as outras funcionalidades e continue rodando até que aquele passo três, de fato, né, gere o resultado. E quando ele produz um resultado,

### 07:30
então a minha aplicação que, que gerou aquele passo, retoma, né, a sua execução dali da onde ela tinha parado e, hã, continua o processamento, tá? Então isso aqui é o que uma, algo assíncrono significa. Então, puxando aqui de novo o exemplo dos estoques, eu posso ter o app da minha loja que vai pedir uma reserva, vai fazer um post em reservas. A API do estoque vai criar essa tarefa, né, e vai colocar no status pendente, tá? Pendente. Opa, mas como assim pendente? Exato, pendente. Vai retornar um 202 pra

### 08:00
minha API de loja aqui, pra minha aplicação de loja, né, dizendo que o status é o status 42 dessa reserva. Beleza, o app de loja sabe que o é, a, o app de estoque recebeu, mas ele não teve a confirmação da reserva, ele só sabe que o outro app tá vivo e recebeu, que tá processando. Esse app de estoque vai pegar e vai fazer aquilo que eu falei pra vocês, validar se aquele item existe, se é válido, se pode fazer reserva, se é estoque, nanana. Quando ele concluir, ele vai lá e vai salvar no banco de dados dele, ó, reserva concluída, vai mudar aquela, aquela

### 08:30
reserva quarenta e dois pra concluída. Só que então ele vai precisar avisar a loja, né. Nesse meio tempo, o usuário continua usando a loja, vai ficar ali como pendente pro usuário na tela, mas ele pode continuar botando coisa no carrinho, é, pagando outros produtos, trocando o seu nome, sua senha, vendo o catálogo, etc. Continua usando de boas. Quando a, a, a, o estoque aqui confirmou essa reserva, ele vai avisar, né, pro outro, pro meu outro app aqui, pro meu app de loja, né, o app fictício.

### 09:00
E aí esse app de loja pode fazer a leitura direto lá na API de estoque pra ver, né, o resultado e ver que aquilo ali foi, hã, foi concluído e confirmado. E eu poderia fazer essa leitura através dum pulling. O que que seria um pulling? Um pulling é, eu mando a, o request uma vez, né, faço o post de reserva e recebo o 202. Depois, eu fico refazendo um get de tempos em tempos, vou colocar ali um período, sei lá, de dez em dez segundos, de um em um minuto, fico fazendo aquele get, get, get, get, get, get, até que aquele get

### 09:30
me retorne um resultado diferente do que pendente, né. Isso aí seria um pulling. Eu tô fazendo esse pull, é, puxando, puxando, puxando, puxando, sempre pra ver se teve alguma atualização naquele status, né. Isso seria uma abordagem. Outra abordagem seria o seguinte: a minha aplicação de loja manda o post, né, recebe o status 202, beleza, recebi, segue aí tua vida e segue a vida, não vai fazer mais nada. Depois, quando a API de estoque finalizar e tiver concluído, o que que ela vai fazer? A API de estoque vai chamar o webhook

### 10:00
da minha, da minha loja. A minha loja vai ter um endpoint lá, hã, específico pra isso, pra receber atualizações de estoque, né. Vou criar lá um endpoint, hã, de post que é stock update, né, o reservation update. Quando a API de estoque terminar, ela faz um post na minha, no app da minha loja, né, no reservation update, a-avisando que aquela confirmação, que aquela reserva foi confirmada ou que deu errado, né. Então isso seria um, um funcionamento através de webhook. Vejam, são duas

### 10:30
estratégias diferentes, duas técnicas diferentes pra faz, produzir o mesmo resultado, né, e os dois trabalhando de forma assíncrona. Outra forma também seria eu trabalhar com uma fila, sei lá. Então imagina o seguinte, imagina aqui que o meu app, que é o produtor de pedidos, né, que seria da minha loja, aqui eu já dei um nome mais bonito, produtor de pedidos, ele vai publicar a tarefa de que eu preciso fazer um pedido, né, eu preciso fazer uma reserva. Só que essa minha loja é muito concorrida, né. Eu fiz aqui o lançamento de uma nova coleção

### 11:00
das minhas bolsas e tem um monte de gente querendo pegar minhas bolsas. Só que eu só posso fazer dez reservas de bolsa, mais do que isso não dá, porque senão vai, vai impactar minhas vendas. Então a gente só tem dez reservas de bolsa disponível e um monte de menina querendo comprar a bolsa e reservar, porque não vai pagar agora, vai pagar depois. Beleza, eu posso jogar isso pra uma fila. Essa fila, ela realmente é uma fila. Então, o que entrou primeiro, vai ser processado primeiro. O que entrou segundo, vai ser processado segundo. Uma fila, né, da-do significado que tem. Só que isso fica salvo no message broker,

### 11:30
que a gente chama. O message broker é o carinha que armazena essas mensagens. Então o app que produz os pedidos publica nessa fila, publica nesse message broker. E aí essas mensagens ficam aqui paradinhas aguardando serem consumidas, né. Mensagem um, mensagem dois, mensagem três. Até que tenha algum consumidor disponível pra fazer o consumo disso. O consumidor é quem vai pegar essa mensagem, processar e tomar uma ação com aquilo, né, com aquela mensagem. Então o produtor é esse cara que publica informações na fila

### 12:00
e o consumidor é quem puxa uma mensagem da fila e realiza alguma ação ou alguma mudança de status baseada naquela mensagem ou algum aviso e tal. Quem seria um consumidor dessa fila? Seria meu app de estoque. Então meu app de estoques vai retirando informação por informação, né, pedido de reserva por pedido de reserva, até que eu bata ali as dez reservas Máximas praquele item, praquela bolsa. Quando bater essas 10 reservas máximas, daí ele passa as próximas mensagens, mesmo que continuem chegando, ele já passa a

### 12:30
colocar como cancelado, né, que não pode fazer aquela reserva, que não tá mais disponível. E pras primeiras dez, ele conseguiu fazer. Então ele fazia e-essa entrega da informação do app produtor de pedidos pro app de estoque, não foi através de uma chamada, né, HTTP, isso aqui foi acho-- através dum mesh de-- isso aqui foi através dum message broker. O app de pedidos publicou no message broker e o app de estoques consumiu de lá. Um foi o produtor, o outro foi o consumidor daquela informação. E com essa informação, o app

### 13:00
de estoques produziu um resultado. Como que esse resultado agora vai ser avisado pro app, né, de, de, de pedidos ali, pro app da loja? Bom, aí eu posso usar aquela estratégia de novo do webhook, posso usar a estratégia do pooling também, ou posso usar um, um outro message broker, on-onde o app de pedidos fica consultando, né, atualizações deee, de reservas. Aí o app de, de avisos, aqui o app de estoques, poderia ficar, né, publicando as reservas ali

### 13:30
e o outro consumindo. Poderia, mas acho que aqui talvez não seria o mais, hã, interessante. Mas o que a gente precisa entender aqui, que é. Mas o que a gente precisa entender aqui é: o papel do produtor, que é o quem publica, o message broker, que é esse carinha que vai receber e encaminhar essas mensagens, e o consumidor é quem processa essa mensagem, né? E uma fila, ela vai guardar o trabalho pendente e distribuir as entregas entre consumidores, né. Então aqui, eu posso fazer o deploy de mais de uma instância da minha aplicação de estoque. E eu vou fazendo essa

### 14:00
distribuição, né, essa entrega pra as minhas diferentes instâncias, pra A e pra B, pra A e pra B, e distribuindo essa carga, o message broker pode fazer isso. Fê, o que que é esse message broker, né? É uma aplicação, é um serviço? Sim, isso aqui é uma aplicação, isso aqui é um software, no final das contas. Mas é que muitas vezes a gente já vai ter softwares prontos pra isso, né, a gente não vai precisar construir essa camada do message broker, a gente já vai usar um serviço pronto, como, por exemplo, o Kafka, né, ou serviços de mensageria da AWS, como por exemplo, o, o SQS,

### 14:30
né, da AWS, que é o Simple Queue Service, lá da AWS. E tem outras provedoras de nuvem que têm s-- hã, esses serviços de mensageria também já prontos, a gente só vai configurar lá, fazer o deploy de uma instância do nosso message broker e passar a produzir e consumir eventos de lá, tá? Mas no final das contas, isso aqui é um software também, tá? E aí. E aí, e aí, e aí uma coisa bacana da gente ter em mente aqui é que quando eu tenho duas instâncias de consumidores,

### 15:00
eles vão dividir a fila, né, eles vão dividindo esse trabalho, cada um consumindo um, um, um, um, e eu consigo consumir essas mensagens, né, de forma mais rápida, cada um fazendo uma parte do trabalho. Caso eu precisasse que dois consumidores diferentes consumissem a mesma mensagem, ou seja, eu vou ter um de estoques que vai tá consumindo aquilo, mas eu também vou ter a gerência, né, o serviço da gerência que vai ficar, por algum motivo, precisa, hã, monitorar as reservas. E eu quero que os dois, hã, recebam as mesmas mensagens. Quando o estoque processar, eu quero que

### 15:30
mesmo assim a gerência também possa ver, daí eu vou ter dois consumidores que não excluem a mensagem da fila, né. Ele só vai sair a mensagem da fila quando for consumido pelos dois, isso também é possível, tá? E outra coisa que é importante: a mensa-- o, o bro-- e outra coisa que é importante, o broker ter recebido a mensagem não significa que o trabalho foi concluído, né. Quando o app produtor de pedidos publicou isso na fila, ele só publicou, ele só garantiu que aquela mensagem chegou lá na fila pra ser processada depois, mas isso não garante que a reserva foi

### 16:00
concluída, né. Essa entrega, ela vai ir prum worker e, caso falhe, a mensagem pode ser reimputada na fila, né, caso, hã, o app de estoques não consiga processar, caso ele esteja fora do ar ou ele crasha ele no momento que ele tiver processando, aquilo ali pode voltar pra fila depois pra ser consumido por um outro consumidor, tá? Aí agora nós temos aqui a questão dos tópicos, tá? Tópicos, diferente das filas, são canais de publicação, mas que não vão ter essa, essa necessidade da gente controlar

### 16:30
a ordem, e, e ordem que chegou e ordem que saiu, tá? A ideia do tópico mesmo é que seja tipo que nem um tópico lá no, no fórum, no Reddit, poste, poste mensagens e o outro leia mensagens, tá? E aqui o bacana é, eu posso ter várias, hã... E aqui o bacana é. E aqui o bacana é que eu posso ter vários serviços consumindo de um mesmo tópico, né. Então eu vou ter aqui um funcionamento de pub-sub, que a gente chama. Pub é o publisher, é quem produz mensagens pro tópico, pra

### 17:00
quem posta mensagens no pó-- é pra quem posta mensagens no tópico, e os sub são subscribers, são pessoa, são. E o pub, e o sub são subscribers, ou seja, são serviços que se inscreveram pra ouvir as mensagens daquele tópico, né. E outro ba-- a outra coisa bacana aqui do tópico é que...

### 17:30
E outra ba-- e outra coisa. E outra coisa. E outra coisa bacana aqui do tópico é que eu inverto um pouco a ótica. Então lá a gente tava imaginando muito a parte de pedidos, fazendo a reserva e avisando a, o estoque, né. Agora eu posso pensar o seguinte: o pedido é feito, né, e já foi confirmado, não teve reserva. O pedido foi feito, tá?

### 18:00
Pedido feito. E eu posso ter vários serviços interessados nisso. Um serviço, que é o meu serviço de e-mail, que vai disparar lá as notificações no WhatsApp, no e-mail do consumidor, avisando que a compra tá sendo processada, etc. Eu posso ter também meu serviço de notas, que vai emitir a nota fiscal. Eu posso ter o meu serviço de entregas, né, de shipping, que vai mandar lá pra transportadora, a, o código de entrega pra já iniciar a rota, né. Eu posso ter vários, hã, microsserviços interessados naquele evento. E o meu app produtor de pedidos não faz

### 18:30
a mínima de quem tá interessado naquilo, entende? Agora a ótica mudou, não é ele tentando avisar o estoque pro estoque consumir o pedido dele e ele saber o resultado. Aqui ele não vai se importar com o resultado na outra ponta, entende? É que ele vai só postar que um pedido foi feito. Postei no tópico, ó, pedido feito, tá bom? Pedido tá feito. Quem se importa com isso, que se importe aí. Eu tô só te avisando que o pedido foi feito. Os outros que se importam com isso, vão ser subscribers desse tópico e vão se inscrever pra serem notificados daquilo, porque

### 19:00
agora eles se importam com aquilo. Então quando o pedido for feito, eu que sou aqui do serviço de e-mail, eu quero saber, porque eu quero mandar o e-mail de: "Uhul, boa compra" pro consumidor, mandar WhatsApp. Eu que sou o serviço de notas, eu preciso emitir essa nota sempre quando o pedido for feito, então eu me importo com aquilo. Então eu quero saber, então eu quero consumir aquele evento. Eu passo a ser, né, um subscriber. Eu que sou o serviço de transportadora, mesma coisa. Entendeu que a lógica mudou um pouco? Aqui eu tava muito querendo avisar, era eu da loja querendo avisar o outro direto: "Ô fulano, processa aí minha reserva,

### 19:30
por favor". Fulano seria o serviço, né? "Estoque, processa aí minha reserva e me confirma se dá pra confirmar, se dá pra reservar", né? E eu ficava aguardando essa confirmação se a reserva deu certo ou não. Agora, aqui no tópico, não, eu tô só avisando todo mundo: "Ó, quem é que esteja interessado, eu fiz um pedido aí". É tipo isso, eu tô gritando no, na boca do trombone. Os serviços que quiserem ouvir e reagir a isso, podem reagir e ouvir a isso, né? Isso aqui são eventos que são publicados nesse tópico, né, eventos, coisas que aconteceram. E eu posso

### 20:00
ter eventos publicados em fila também, mas é que em fila eu preciso muito garantir essa entrega, que foi entregue em ordem, que foi consumido. O tópico é um pouco, um pouco mais tipo, isso de evento mesmo. Ó, coisas aconteceram, eu tô postando aí que as coisas aconteceram e quem quiser reagir, que reaja, tá? E aí, outra coisa bacana aqui da gente ter em mente, é o efeito... E aí outra... E a outra coisa, e aí outra coisa bacana aqui pra gente ter em mente, é o ACK e a idempotência. O

### 20:30
ACK é o que a gente usa, né, pra confirmar o processamento de alguma coisa, tá? É acknowledge. O ACK, o ACK aqui, esse ACK, esse ACK aqui vem de acknowledge,

### 21:00
né, de reconhecimento. Então é como se fosse uma aplicação reconhecendo pra outra que recebeu aquilo. Então é aquilo de receber a confirmação, né? Então quando eu publico uma mensagem num broker, o broker me retorna um ACK, né, me retorna um acknowledge, tipo, ó: "Serviço de, de, de pedidos, eu recebi a tua mensagem e já tá aqui na fila, tá? Pode seguir a tua vida." Não confirma que foi processado, não confirma que os outros serviços já processaram aquilo. Só confirma, né, só faz um acknowledge de que aquela mensagem foi recebida,

### 21:30
tá? Então o ACK aqui vai confirmar esse processamento pelo broker, mas sem a confirmação de que foi processado. Quando a gente fala de idempotência, a gente tá falando sobre evitar a repetição de um efeito. Então digamos que o meu serviço... Então digamos que... Então digamos, então digamos aqui que o meu serviço tá postando mensagens no message broker, e aí, hã, por algum motivo, o message broker

### 22:00
caiu, né? Ele caiu e não... Digamos que... Então vamo imaginar, então vamo imaginar o seguinte cenário. Digamos aqui que o meu app de pedidos tá publicando ali os evento-- então, então vamo imaginar o seguinte cenário. Imagina que o meu app de transporte. Então vamo imaginar o seguinte cenário. Imagina que o meu serviço de transporte, né, que controla

### 22:30
lá as entregas, tá querendo publicar no broker de que houve uma entrega realizada, o evento E42. Eu vou lá e publico isso, né, no meu, no meu broker. Só que aí esse consumidor, né, quem consumiu aquela informação, já processou aquilo, salvou no banco local, registrou um aviso e salvou o ID na mesma transação. Só que aí isso aqui cai. Caiu, deu problema e eu não consigo retornar o acknowledge, né, pro outro carinha, pro, pra quem me entregou aquela informação.

### 23:00
Aí esse carinha aqui, ele vai achar que o outro não recebeu. Eu vou lá e faço a reentrega, envio de novo, faço um retry, né, tento de novo. Só que, como eu não recebi o re-- só que como eu, só que como eu passei o mesmo ID, esse consumidor aqui vai consultar por esse ID, E42, vai ver que já foi concluído. E então ele não vai repetir o mesmo efeito, ele não vai registrar que uma nova entrega foi feita aqui no sistema interno dele. Vai continuar persistindo o efeito que foi feito lá na primeira

### 23:30
etapa, né, mesmo que não tivesse recebido o ACK, porque aqui eu trabalhei com o conceito de idempotência. Usando um ID de idempotência, eu consegui evitar essa duplicação de informação e de efeito. O ID de idempotência vai resolver todos os problemas de falha e de retry? Não vai, não é bala de prata, isso aqui é só um exemplo, e um exemplo simples. Depois a gente vai ter mais vídeos aqui no canal entrando mais profundamente nisso. Se você quiser se aprofundar, vai tá na descrição do vídeo também, hã, cenários onde um, um ID de idempotência não funciona,

### 24:00
né, e que você teria que usar outras estratégias pra fazer esse controle da, da duplicidade dos dados, tá? Mas o que a gente precisa entender aqui é que o ACK é só confirma que o processamento, que o, que o, que a mensagem foi recebida, e o ID de idempotência é o que de fato vai controlar se aquilo foi processado ou não pelo consumidor, tá? E o, e quem vai se preocupar com isso normalmente é o consumidor da mensagem, pra evitar que lá no banco dele, ele duplique aquela informação, tá? Tá? Tá. E aqui indo

### 24:30
pra última parte, é a parte de falhas, e recuperar e acompanhar o trabalho Então, quando a gente trabalha com sistemas distribuídos, né, e com essa arquitetura assíncrona, a gente muito provavelmente vai ter sistemas fora do ar, ou se com-- tentando se comunicar com o outro. Então a gente muito provavelmente vai ter um sistema tentando se comunicar com outro fora do ar, a gente vai ter falhas em partes espalhadas do sistema e a gente vai ter que fazer retentativas e tentar de novo, né. Então aqui a gente vai trabalhar com retries, né, pra re-retentar processar uma coisa. A gente

### 25:00
vai ter DLQs, que são dead letter queries, que são filas de mensagens mortas, né. Então eu fui lá, postei uma mensagem numa fila. Essa mensagem foi tentar ser consumida aqui pelo app de, de, de estoque. Ele não conseguiu, tava fora do ar. Tentou entregar de novo, né, o message broker não conseguiu, tava fora do ar. Tentou de novo, não conseguiu. O estoque continua fora do ar. O message broker vai lá e joga isso pra uma fila de mensagens mortas, que nunca foram processadas, né, pra serem reprocessadas quando o estoque voltar pro ar.

### 25:30
Então isso aqui é uma estratégia. Eu, eu também, eu também posso querer, eu também posso querer impor limites, né, de retry, limite de tempo que aquela mensagem fica na fila, porque pode ser que mesmo que aquela reserva nunca foi processada e o, e a API de estoque nunca me respondeu, passado duas horas, a reserva é pra expirar mesmo e não é pra confirmar. Aí, caso o usuário queira, vai ter que tentar de novo. Então eu posso trabalhar com esses limites. Tá, eu também vou ter preocupações de rastreamento, de rastrear

### 26:00
uma informação entre um sistema e outro, né, porque podem ter bancos de dados separados. Aí como é que eu sei que aquela reserva se corresponde com aquele pedido e com aquela entrega, né, que tão três bancos de dados separados? Eu posso ter um ID em comum, né, salvo entre todos os sistemas, eu posso ter ali uma, uma-- eu posso ter ali, eu posso ter ali alguma informação que viaja entre eles pra que eu consiga fazer esse reconhecimento entre os sistemas. E eu também preciso ter um reca-- eu também preciso ter um caminho de recuperação, né, pra tentar me recuperar a, a essas

### 26:30
falhas. Mas isso aqui, como eu disse, são assuntos mais complexos, que a gente vai aprofundar futuramente em outros vídeos aqui do canal. E também, caso você queira ver isso aqui, hã, mais... E também, caso você queira ver isso aqui mais no detalhe e ter um roadmap de estudos personalizado pro seu cenário, pro seu momento atual, pras coisas que você sabe ou não sabe, ter acesso a plantão de dúvidas e essas aulas ao vivo, onde a gente entra mais a fundo nesses assuntos, e também participar dos nossos eventos presenciais aqui da nossa comunidade, dá uma olhada

### 27:00
no link que tá aqui na descrição desse vídeo, porque a gente tá construindo algo muito legal pro Keeper, porque a gente tá construindo algo muito legal pro Keeper Academy. Eu ado-- Porque a gente tá construindo algo muito legal pro Keeper Academy, eu adoraria te ver por lá. E esse vídeo vai ficando por aqui. Até a próxima aula ou até a próximo vídeo. Falou!
