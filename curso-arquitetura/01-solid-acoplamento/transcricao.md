# Transcrição — Aula 1: SOLID e acoplamento
Fonte: [aula1_Bananecos FHD - Cam Extra - 10-01-55.mp4](https://drive.google.com/file/d/1XxR1N4v7GXtBWG_Y_M50knvL-oP-wsPF/view), gravação FHD da pasta compartilhada no Google Drive. Duração falada: 29min08s. Transcrição automática em português pelo ElevenLabs Scribe. Timestamps agrupados em blocos de 30 segundos a partir dos tempos por palavra. O texto não foi revisado palavra a palavra.
Fonte: `aula1_Bananecos FHD - Cam Extra - 10-01-55.mp4` na pasta compartilhada do Google Drive. Duração falada: 29min08s. Transcrição automática em português pelo ElevenLabs Scribe; timestamps gerados a partir dos tempos por palavra. O texto não foi revisado palavra a palavra.

## Texto com timestamps

### 00:00
Esse vídeo é uma continuação da nossa série de vídeos de arquitetura de software aqui no canal. E hoje a gente vai discutir um dos princípios mais importantes quando a gente fala sobre design de código, que é o princípio do SOLID. E pra organizar essa aula, a gente vai ter dez minutos de parte teórica e no final, mais dez minutos de parte prática pra você entender como que realmente esses princípios se aplicam no dia a dia do nosso código. Então sem mais enrolações, bora pro vídeo.

### 00:30
Então vamo lá, quando a gente fala sobre SOLID, a gente tá falando sobre um princípio que vai con-- então vamo lá, quando a gente fala sobre SOLID, a gente tá falando sobre um conceito que vai conter cinco princípios de design de código orientado a objetos, tá? Então isso aqui vai se aplicar principalmente pras linguagens que trabalham com paradigma de orientação a objetos, como por exemplo o Java, que é o mais famoso aqui do nosso canal. Mas você também

### 01:00
pode acabar vendo esses princípios serem aplicados em aplicações que trabalham com TypeScript, onde a gente consegue trabalhar com a arquitetura de classes, ou no próprio Python, onde a gente também consegue organizar o nosso código com classes. O JavaScript também permite que a gente crie clo-- o JavaScript também permite que a gente crie códigos utilizando a estrutura de classes, mas por ele conter menos tipagem, vai acabar ficando um pouco mais difícil da gente aplicar esses-- vai acabar ficando um pouco mais difícil da gente aplicar esses cinco

### 01:30
princípios na sua completude. E aí, quais são esses cinco princípios? É o S da responsabilidade única, o O do aberto e fechado, L da substituição de Liskov, segregação de interfaces, que é o nosso I, e o D que é a inversão de dependência. Mas pra gente conseguir entender esses princípios, primeiro vamos pegar um exemplo. Então imagina o seguinte: que a gente trabalha no-- então imagina o seguinte: que a gente trabalha em um sistema que controla a matrícula dos alunos através do pagamento.

### 02:00
E aí, sempre com-- e aí, sempre quando um pagamento for confirmado, es-- e aí, sempre quando um pagamento for con-- e aí, sempre quando um pagamento for confirmado, o acesso desses alunos deve ser liberado ao curso. Então digamos que a Ana, a Bia e a Clara acabaram de fazer o registro da sua matrícula. E então o pagamento delas foi confirmado pelo nosso sistema de pagamentos. Assim que o pagamento for confirmado, o nosso sistema era pra liberar o acesso ao curso pra essas três alunas e depois disso,

### 02:30
enviar uma notificação pras alunas de que o acesso foi liberado e que elas já podem começar a consumir essas aulas. Mas aí vem uma grande pergunta né: e se o nosso e-mail cair? Então se eu tiver utilizando ali algum provedor de e-mail ou um próprio sistema interno meu de disparo de e-mails, mas por algum motivo esse sistema está com problema e não está no ar. O que que aconteceria com a nossa aplicação? Bom, se a nossa aplicação está acoplada, o que iria acontecer é: caso-- bom, se a nossa aplicação está acoplada, o que iria

### 03:00
acontecer é: caso o serviço de e-mail ou algum outro serviço de notificação que a gente esteja utilizando não esteja funcionando, muito provavelmente isso ia, muito provavelmente isso ia, muito provavelmente isso ia travar todas as novas matrículas, então as alunas nem iriam receber o acesso ao curso. E pra eu fazer a troca do notificador que eu tiver utilizando, eu teria um grande trabalho também. Por quê? Porque quando a gente fala sobre acoplamento, a gente tá falando que o nosso código, ele tá totalmente acoplado

### 03:30
a algum... Porque quando a gente fala de-- por quê? Porque quando a gente fala de acoplamento, a gente tá falando que o nosso código ele tá totalmente acoplado ao funcionamento de coisas externas ou até de outros módulos dentro da nossa aplicação. E agora na prática vai ficar bem mais fácil de entender o que que é esse acoplamento. Mas coloquem na cabeça que se o seu código está acoplado, isso significa que qualquer mudança que você for fazer, como por exemplo, e-mail tá fora do ar eu quero trocar pra WhatsApp.

### 04:00
Vai exigir que você refatore vários lugares, por exemplo, dentro da matrícula e dentro do acesso ao curso que não tem nada a ver com o sistema de notificação. Mas por conta do seu código de matrícula e seu código ali que controla o acesso ao curso está totalmente acoplado ao provedor de e-mail que você tava utilizando, essa troca acaba ficando muito custosa. E aí pra corrigir esse tipo de problema, a gente come-- e aí pra corrigir esse tipo de problema, a gente consegue aplicar os princípios do SOLID. E vamos começar com o princípio do S, né, a responsabilidade

### 04:30
única. Esse princípio basicamente diz que uma classe ela deve ter somente uma única responsabilidade e uma única razão pra mudar. E ela vai ser ligada a um ator principal ou um grupo responsável. Então por exemplo, digamos que eu pudesse-- então por exemplo, digamos que eu pudesse ter uma classe que se chama o controle acadêmico. Dentro dessa classe de controle acadêmico eu posso controlar a matrícula do meu aluno, o status se ele foi aprovado ou não, o, o e-mail que vai ser enviado, o status do pagamento.

### 05:00
Só que aí eu tô criando um monte de coisas dentro de uma única classe e tô acoplando o funcionamento dessas coisas, porque essa ca-- porque essa classe vai acabar não tendo uma única razão pra mudar. Se eu tiver que mudar o pagamento, vou ter que alterar essa classe. Se eu tiver que mudar o status do aluno, vou ter que mexer nessa classe. Se eu tiver que mudar a forma como eu libero a matrícula, vou ter que mexer nessa classe. Então, uma única classe vai acabar tendo mais de uma responsabilidade ligada a mais de um ator principal. O que é um grande problema que vai causar, o que é um

### 05:30
grande proble-- o que é um grande problema que, o que é o grande problema, o que é um grande problema, porque toda vez que você for fazer uma alteração, você vai acabar respingando em outras partes da tua aplicação que não tinham nada a ver, mas por estarem acopladas dentro do mesmo código, elas podem acabar sendo impactadas, tá? E aí, no princípio da responsabilidade única, a gente segue ali a, a ideia de separar essas responsabilidades em diferentes classes. Então eu vou ter uma classe pra cuidar da matrícula, uma classe pra cuidar

### 06:00
do pagamento, uma classe pra cuidar do meu aluno, uma classe pra cuidar do meu serviço de notificação, tá? Tudo separado O outro princípio que a gente vai discutir aqui é o O, né, que é o princípio do aberto e fechado ou open closed principle. Isso aqui basicamente diz que uma classe ela tem que tá sempre aberta pra extensão de comportamento, ou seja, adicionar novos comportamentos àquela classe, mas fechada pra modificar reg-- mas fechada pra modificação de regras já estáveis.

### 06:30
Por que que isso aqui é importante? Porque se a gente vai lá e modifica a forma como uma classe funcionava e várias outra cla-- e várias outras classes já utilizavam aquela classe da maneira como ela era antes, eu vou causar um grande impacto na minha aplicação, vou ter que mudar um monte de lugar, tá? E aí, principalmente se tiver acoplado, eu vou ter mais um problema porque estariam acoplados ainda com a parte interna dessa minha classe, com todos os métodos que ela expõe. Então, pra que a gente

### 07:00
faça mudanças de maneira mais saudável e mais estável nas nossas classes, a gente tem que seguir a ideia de que uma classe ela só tá aberta somente pra extensão de comportamento e nunca pra modificar regras que já existiam naquela classe. Fê, mas eu preciso mudar uma regra que já existia naquela classe. Mudou a nossa, nossa regra de negócio, o PO pediu pra gente modificar, o que que eu faço aqui? Eu não posso mudar? Não, a gente até pode fazer refatorações, pode mudar um método que já existia, adicionar,

### 07:30
né, mudar algumas regras que, que já tavam estáveis por um-uma solicitação de negócio. Agora eu tô fazendo uma feature nova, tá? Uma feature que não tem nada a ver com a parte de pagamento, que eu vou mexer lá na, que eu vou mexer lá nas quantidades de status de matrícula do aluno. Só que aí por algum motivo eu quero já ir lá trocar um monte de coisa na classe de pagamento, porque tá errado, porque aquilo lá tá antigo, porque eu quero refatorar, porque eu acho que esse, essa função deveria retornar o status sozinho e não retornar o objeto inteiro, aí eu já vou

### 08:00
mudar outra classe. Cara, não, não é o momento. Só vai fazer essa refatoração quando isso for tomado e de decisão, né, junto com o teu time, quando isso tiver bem alinhado, porque senão isso pode acabar causando mais problemas do que resolver problemas. Daí aqui a gente quer utilizar princípios de design de código pra evitar problemas. Então, seguindo aqui o princípio do aberto e fechado, uma classe vai ser sempre aberta pra estender o comportamento dela. Então eu vou adicionar novas coisas que vão permitir que ela tenha novas

### 08:30
ações, novos comportamentos, mas modificar regras já estáveis eu tenho que ficar com olho bem aberto e tomar cuidado pra evitar isso daqui. Próximo princípio é o L, né, substituição de Liskov. Esse aqui diz que um subtipo deve sempre substituir o tipo esperado sem quebrar o seu contrato de comportamento. O que que isso aqui significa? Bom, se eu tenho alguma classe que chama ali uma outra classe que se chama... Bom, se eu tenho ali uma classe que se chama no-- bom, se eu tenho ali uma classe principal

### 09:00
que acaba chamando a minha classe notificador pra enviar uma mensagem, por exemplo, pra Ana, se eu substituir esse notif-- se eu substituir, se eu substituir, se eu substituir esse tipo esperado, se eu substituir esse tipo esperado por um outro tipo. Se eu substituir, se eu substituir esse subtipo. Se eu substituir, se eu substituir essa classe por uma

### 09:30
outra classe que segue esse mesmo tipo, ou seja, a classe que segue o tipo da outra é um subtipo, né? Se eu troco por uma outra classe que respeita o mesmo tipo dessa classe, isso não era pra quebrar nada, né, não era pra quebrar o contrato de comportamento. E agora, vendo lá no código, vai ficar muito mais claro como isso aqui se traduz. É indo pra parte de segregação de interfaces ou interface segregation principle, né. Isso aqui basicamente diz que nenhum cliente, ou seja, o cliente seria uma classe que consome

### 10:00
a nossa classe, tá? Então, digamos que tu tenha a tua aplicação Java ou tua aplicação JavaScript, tu tem um monte de classes. Sempre quando uma classe chama a outra, essa classe que chamou a segunda classe é a cliente dela. Ela tá chamando, pedindo ações e pedindo comportamentos pra aquela classe que foi acionada. Então, a ideia aqui é que nenhum cliente deve depender de operações que não utiliza. Então, aqui vai impactar muito naquilo que eu expliquei pra vocês do acoplamento. Se eu tenho ali uma classe de matrícula e essa classe de matrícula, ela precisa

### 10:30
por algum motivo consultar a minha classe de pagamentos ou a minha classe de financeiro pra saber o status desse pagamento, ela só vai fazer a consulta do status. Ah, mas o financeiro retorna o ID do boleto, retorna o valor, retorna quantas vezes foi parcelado, retorna, hã, se pode processar aquele boleto de novo, ele retorna o storage onde o boleto... Não, matrícula não, não, não precisa saber disso. Eu não dependo disso, eu só dependo do status. A única regra aqui, a regra de negócio que afeta a matrícula é: se o status do pagamento

### 11:00
tá confirmado, a matrícula tá liberada. Se tem outro status, a matrícula não tá liberada. Não me importa o que que tem dentro de financeiro, se eu posso consultar, se eu posso estornar, se eu posso emitir uma nova nota, se eu posso fazer um invoice em dólares, não me importa, tá? E aí matrícula não deveria depender dessas implementações internas da classe financeira. Então, o que o financeiro vai fazer é exportar uma classe. Então o que o financeiro vai fazer é exportar uma interface, né, que recorta somente

### 11:30
essa necessidade externa. Essa parte de estorno, de emitir nota, de pegar o ID do boleto, de consultar qual banco foi pago, tudo isso aqui fica na responsabilidade de financeiro, não fica na responsabilidade de matrícula, então tudo vai residir lá dentro. E as classes clientes que quiserem consumir financeiro vão somente consultar essa interface exposta que esconde um monte dessa, dessa implementação interna e exporta somente ali uma camadinha de abstração com o necessário

### 12:00
que as outras classes precisam pra continuar seu funcionamento, que seria consultar pagamento ponto consulta, né. Só quero consultar o status de pagamento, não quero saber todo o resto que tu tem. E esse aqui é o princípio do segregação de interfaces. E aí pra finalizar a nossa parte teórica, a gente tem E aí pra finalizar a nossa parte teórica, a gente tem o princípio da inversão de dependência. Esse princípio aqui é muito, mas muito utilizado nas aplicações que trabalham com o framework do Java Spring, que com certeza se você

### 12:30
tá estudando programação orientada a objetos, se tá estudando Java, você já topou com Java Spring. Então quando você for ver um código Java Spring, você vai ver que esse princípio aqui da inversão de dependência é muito utilizado, tá? E muito utilizado pelos próprios módulos nativos do Spring. O que que isso aqui diz? Isso aqui diz que políticas de alto nível e detalhes devem depender de abstrações, e não um dos outros. Então, digamos aqui de novo aquele exemplo do notificador, né. Eu tenho minha classe de matrícula e essa

### 13:00
classe de matrícula ela precisa notificar o-o-o aluno ou o cliente quando a matrícula for liberada. Pra isso, ela vai usar um notificador. A gente vai ch-- criar essa classe notificador. Essa classe notificador, ela vai ter as-- essa classe, essa classe notificador, ela vai ter somente método, por exemplo, o método enviar, que é enviar ali o dado pro aluno, que é enviar ali o acesso, né, pro aluno, notificar ele de que a matrícula foi liberada. Esse notificador vai ser a nossa interface,

### 13:30
né? E aí quando a gente for implementar, de fato, quem vai fazer o envio da nossa da-- e aí quando a gente for implementar, de fato, quem vai fazer o envio dessa notificação, seja um e-mail, seja um WhatsApp, seja Telegram ou qualquer outro tipo de notificação que eu vou utilizar, eu vou fazer essas implementações respeitarem a interface e não o contrário. Eu não vou definir uma interface que funcione da maneira como o serviço de e-mail lá que eu tô usando funciona. "Ah, eu tô usando a Twilio, então eu vou ter que botar um primeiro

### 14:00
create recipe, depois create body e-mail, depois enviar." Não, entendeu? Não, o que eu tenho que expor aqui é uma interface, tá, hã, que somente vai dizer ali a ação que eu tenho, que é, por exemplo, enviar, ou a-as possibilidades de consultas de dados que eu tenho. E aí essa classe de e-mail, quando eu for integrar lá com a Twilio, ou for integrar-- ou quando eu for integrar com a Resend, ou for integrar com a AWS SNS, aí eu vou fazer essa classe respeitar essa interface. Eu-eu inverti

### 14:30
essa dependência, entende? E agora eu faço todas as classes clientes, as classes que vão utilizar o notificador, dependerem somente da interface, combinando aqui com o princípio também de segregação de interfaces, tá? Onde eu exponho só o que eu preciso, faço a classe de fora, né, a classe cliente depender só da classe, faço a classe, faço a classe, faço a classe de fora, né, a classe cliente depender só dessa interface de alto nível que eu defini, e aí então eu faço as classes

### 15:00
de implementação, hã, implementarem essa abstração, tá? E agora vamos pro código pra tudo isso aqui ficar muito mais claro e vocês saírem do vídeo compreendendo esses conceitos cem por cento na prática. Acho que eu tô segurando essa tosse há horas. Desculpa.

### 15:30
Não, tranquilo. Quer um café? Não, eu tenho aqui. Então vamo cons-- então vamo considerar, então vamo con-- então vamo continuar trabalhando nesse exemplo que a gente tava falando das

### 16:00
matrículas e da notificação e do pagamento. Então digamos que a gente tem essa seguinte classe aqui. Isso aqui não tá-- então vamo continuar, então vamo continuar no nosso exemplo das matrículas e dos alunos e do sistema de notificação. Aqui, pra gente entender esses conceitos, eu criei somente um código de exemplo. Aqui a gente não tá utilizando nenhum framework externo, tá? A gente tá utilizando somente o Java puro, a título de, a título... Aqui

### 16:30
a gente tá somente utilizando o Java puro a título de aprendizado, tá? Se isso aqui realmente fosse uma API que a gente vai utilizar em produção, provavelmente a gente já tá usando o Spring ou algum outro framework, e também, né, integrando ali com serviços HTTP e etc. Aqui é só pra gente entender os conceitos mesmo. Então vamo lá. A gente tem aqui a nossa classe main, né, que é onde começa tudo aqui o nosso programa Java. E aí, e aí nós temos aqui um booleano fictício, né, só pra controlar se o nosso serviço

### 17:00
de e-mail está disponível ou não. Vamos di-dizer que o nosso serviço de e-mail tá fora do ar, então eu tô utilizando ali algum serviço externo, seja Twilio, seja Resend, AWS, tá fora do ar, tá bom? E eu tenho aqui as minhas matrículas, né, uma... E eu tenho aqui as minhas matrículas, né, que respeita essa classe aqui matrículas acopladas. Essa classe de matrículas, cês já tão vendo que ela tá lidando com muita coisa. Então as matrículas já dependem diretamente do pagamento, já define aqui o e-mail do cliente, já define os acessos,

### 17:30
e vai fazendo essa confirmação, enviando o e-mail e liberando os acessos, tá? Aí, quando a gente lista, no-- aí quando a gente inicia novos pedidos, digamos que a gente vai iniciar o pedido da Ana, o pedido da Bia e o pedido da Clara. Todas elas já vão vir com o status de pagamento confirmado. Digamos que a gente já recebeu ali de um sistema externo o status desse pagamento tá confirmado. Agora eu quero só processar esses pedidos e liberar a matrícula pra essas alunas, tá? Então vou fazer um loop entre essa lista

### 18:00
e vou liberar a matrícula pras minhas alunas, né? Chamando matrículas.confirmar, que é pra confirmar aquela matrícula. Só que como o meu sistema de e-mail tá fora do ar, o que vai acontecer é, eu vou entrar aqui nes-nessa confirmação, eu vou fazer, ó, pagamentos.consultarpedido, o status é diferente de confirmado? Não, não é. Então eu posso cons-continuar. Se fosse, eu ia dar um return, porque aquele pagamento não tá confirmado, eu não tenho que liberar o acesso pra aquela aluna. Aí eu faço o e-mail.enviar Mandando o pedido da

### 18:30
aluna e o acessos ponto adicionar o-a aluna, né? Adicionar, enviar o e-mail pra aluna e adicionar o acesso dela. Só que como isso aqui tá fora do ar, a nossa aplicação vai quebrar antes de chegar aqui na parte de acessos e eu vou acabar nunca notificando as minhas alunas porque o e-mail tá fora do ar e também nunca liberando o acesso pra elas. Então deixa, então deixa eu mostrar isso aqui pra vocês. Eu vou executar aqui a nossa classe aqui no

### 19:00
terminal. Então deixa, então deixa eu mostrar isso aqui pra vocês. Eu vou executar essa nossa classe main aqui no terminal e a gente vai ver ó, e-mail fora do ar. E aí o que aconteceu foi na Ana, na Bia e na Clara, os e-mails tavam fora do ar e nenhum

### 19:30
acesso foi liberado. Se eu troco pro e-mail tá no ar, né, boto aqui true, eu rodo novamente, o e-mail... E-mail disponível. Ah, tá. Se eu troco, se eu troco, se eu troco pro e-mail

### 20:00
aqui ficar no ar, né, ou seja, ele voltou a ficar disponível e eu venho aqui e faço build de novo da minha classe, né, porque senão não vai alterar. Deixa eu fazer aqui. Beleza. E vamos fazer a execução. A gente vai ver que agora o e-mail foi enviado pra Ana, enviado pra Bia e enviada pra Clara, né, enviado pra Clara. E agora eu tenho três de três acessos liberados. Então eu tenho aquele acoplamento extremo aqui com o serviço de e-mail, porque eu tô diretamente instanciando dentro

### 20:30
da classe de matrículas u-uma classe de e-mail e fazendo esse envio direto aqui dentro, né? E eu também não tenho nenhuma, nenhuma prevenção a falhas aqui. Então, caso aconteça alguma falha com o envio do e-mail, eu nem libero o acesso. E aí agora a gente vai ver um outro exemplo, que é o exemplo do desacoplamento, então... Então...

### 21:00
Então, então, então, então vamo analisar essa nossa classe aqui. Bom, aqui em cima nada mudou, né, eu ainda tenho aqui a listagem dos pedidos e eu tenho a iniciação da minha classe matrículas. Só que agora, olha só o diferente aqui, tá, deixa eu puxar a outra class-classe aqui pro lado pra vocês perceberem. Olha o que tá acontecendo aqui. No, na instanciação de matrículas, eu tô passando pra essa matrícula uma classe dos, do pagamento local, né, que ela deve acionar e do notificador. Se a gente olhar aqui quando tava acoplado, eu

### 21:30
só fazia aqui ó, matrículas acopladas e passava só se o e-mail tava disponível, mas isso aqui só a título de, de fazer ele falhar. Mas se a gente entrasse no, na implementação dessa classe, a gente conseguia ver, a gente conseguia ver que a própria classe de ma-- A gente conseguia, a gente conseguia ver que a própria classe de matrículas criava a instância de e-mail e criava a instância de pagamento. O que que isso significava? Que matrículas, primeiro

### 22:00
já tava dependendo cem por cento dessas classes existirem, né, e ela mesmo controlando ali as dependências externas que ela ia ter. Na parte do desacoplamento, a gente já inverteu a ótica, tá vendo? Matrículas lá dentro ó, só depende de interfaces. Depende duma interface de consulta de pagamento e uma interface de notificador. Se a gente entrar aqui em consulta de pagamento ó, é uma interface que expõe o método status pagamento. E notificador também é uma interface

### 22:30
que expõe o método enviar, tá? E matrículas precisa dessas duas dependências aqui, precisa de uma classe de pagamentos e uma de notificador. Só que ela recebe isso através do construtor dela. Então no construtor da classe de matrículas, eu recebo essa dependência de fora, tá? Aí ó, inversão de dependência, tô recebendo de fora isso, tá? E respeitando somente, e olhando somente pra classe, e olhando somente pra interface, né, e não pra classe que implementa aquilo. Então matrículas

### 23:00
agora depende de um notificador e depende de um pagamentos. E aí, continuando aqui no nosso desacoplamento, a gente vê que esse notificador é instanciado aqui em cima, né, pela classe mais de fora, instanciando um new e-mail. Quando a gente entra nessa classe e-mail, a gente consegue ver que e-mail implements notificador. Então a classe e-mail implementa a interface de notificador. E pra ela fazer isso, a implementação, ela precisa expor o método enviar. Só que olha só o pulo do gato aqui.

### 23:30
Eu consigo ter uma outra classe de notificador, como por exemplo o WhatsApp ou o Telegram, que também implementa a mesma interface notificador. Só que a única coisa que ela precisa fazer é expor o método enviar. Aqui dentro desse método, cês percebem que eu tô só fazendo um system.out, tá? A ideia é que aqui dentro, dentro do, do corpo des-desse método, tivesse a implementação de fato de eu conectar com o sistema da Twilio, de eu montar a mensagem do e-mail, de eu enviar pegando o e-mail do usuário, pegando o meu from, montando ali o título do e-mail e fazer o envio.

### 24:00
Mesma coisa do WhatsApp, conectar com a API do WhatsApp, pegar o número do usuário do banco de dados, fazer o envio, etc, tá? Aqui eu tô só colocando um system.out a título de, de aprendizado mesmo. Mas vocês conseguem ver que agora eu consigo ter duas classes com implementações diferentes, né, aqui o corpo diferente, mas respeitando a mesma interface. E aí a, e a mesma coisa aqui pra pagamento, tá? Eu poderia, eu tenho aqui o meu pagamento local que eu chamei, mas eu poderia tá usando Abacate Pay, poderia tá usando Stripe, poderia tá usando a Transfera, poderia tá

### 24:30
usando o UV, qualquer sistema de pagamento externo aqui eu poderia tá usando. Eu ia criar uma nova classe, eu poderia vir aqui final class Abacate Pay, por exemplo, Abacate Pay, hã Implementation, né, ou integration, sei lá. Eu ia dizer que Abacate Pay implements consulta pagamento, né, aí eu ia consultar meu banco de dados. É, consulta pagamento ficou muito específico pra consulta, mas digamos que fosse aqui o meu pagamento provider, né, eu ia chamar essa interface de provedor de pagamentos. E aí eu poderia implementar

### 25:00
aqui, pagamento provider tem que ter o método, hã, charge Pix, tem que ter o método refund, né, etc, etc, etc. Ia fazer a implementação integrando com o sistema da Abacate Pay. Caso quisesse criar integração com o Stripe, ia fazer a mesma coisa. Hã, Stripe Implementation implements pagamento provider. E aí tem que expor os métodos charge Pix, refund, etc, etc, etc. Todos respeitando a mesma interface. Só que aí, a moral aqui é que a minhas classes i-internas vão depender somente de uma abstração,

### 25:30
que é a abstração do consulta de pagamento, a abstração do notificador, e elas não vão depender diretamente da implementação que tá dentro daquela classe. E aí eu consigo ter o seguinte: se o meu e-mail tá fora do ar, né, e eu tô rodando aqui as matrículas, eu consigo facilmente trocar aqui a instância de e-mail por WhatsApp, né. Troco aqui por WhatsApp e pronto, passa a funcionar, tá? Vocês vão ver isso aqui executando. Coisa que eu não conseguiria fazer quando tava tudo acoplado e quando eu não tava seguindo os princípios

### 26:00
de inversão de dependência, de segregação de interface, de segregação de respo-- de, de se-- de separação de responsabilidades. Então aqui vocês estão vendo um código que tá tentando aplicar todos esses princípios de design de código que a gente viu ali na parte teórica. Então aqui, então aqui ó, eu vou executar pra mostrar pra vocês. Deixa eu abrir aqui meu terminal. E a gente vai fazer, primeiro deixa eu voltar aqui pra e-mail pra vocês verem que eu vou ter o e-mail aqui fora do ar, certo?

### 26:30
E vou fazer aqui a compilação no meu código. E vou fazer aqui a compilação no meu código. Vou fazer a execução agora, só que a da classe Demo Desacoplamento. Pronto, versão desacoplada, acessos liberados três de três. Então eu não tive mais aquele problema de não liberar acesso. Por quê? Porque lá dentro de matrículas eu já implementei também uma tolerância a falhas. Então eu faço o envio da notificação, mas caso falhe,

### 27:00
eu adiciono aquilo ali numa fila de tipo avisos pendentes, mas mesmo assim eu faço a liberação do acesso pro, pro meu aluno, tá? Só que aí, beleza, tá falhando a notificação, eu continuei liberando os acessos, esse problema da falha eu já corrigi, poderia ter corrigido lá no acoplado também, tá? Essa parte aqui de corrigir o, o fato de, de não fazer a liberação do acesso, eu poderia ter, ter corrigido naquela classe acoplada. Mas a, o pulo do gato tá aqui. E-mail tá fora do ar? Tá fora do ar. O que que eu faço agora? Então eu posso trocar aqui pra usar o WhatsApp,

### 27:30
tá? Posso trocar aqui pra usar o WhatsApp. E aí eu compilo aqui tudo de novo. Beleza. Faço a execução e agora eu vejo ó, versão desacoplada, que é o título aqui só pra gente entender qual que tá rodando. WhatsApp enviado pra Ana, WhatsApp enviado pra Bia, WhatsApp enviado pra Clara. Nenhum aviso pendente, acessos liberados. Nossa, eu só troquei a classe aqui, pô, mas aí eu teria que fazer um deploy novo pra ficar trocando a classe quando caísse um serviço? Não, ia só fazer um if else. Eu faço um ping lá no e-mail, e-mail tá online, eu injeto

### 28:00
a classe e-mail, utilizo a classe e-mail. Se não tá, hã, online, eu só troco pra classe WhatsApp. Eu já prevejo tudo isso no meu código. Mas como matrícula só depende de um notificador, eu poderia injetar qualquer coisa aqui pra ela, desde que respeite a interface de notificador. E mesma coisa pra pagamentos. E aí, aqui nós já conseguimos entender, hã, mais na prática como que funcionam esses princípios de design de código e principalmente como não criar aplicações acopladas. Se você quiser se aprofundar nesses estudos,

### 28:30
aprender mais sobre a arquitetura, a gente tá criando uma série de vídeos de arquitetura aqui no nosso canal. A playlist vai tá aparecendo aqui na tela pra você continuar os seus estudos. E se você quiser um roadmap— E se você quiser um roadmap de estudos personalizado pra você, quiser um acompanhamento mais próximo com plantão de dúvidas e também participar de um evento presencial da nossa comunidade, eu deixei um link aqui na descrição de uma coisa muito bacana que a gente tá construindo aqui pra nossa comunidade e, e, e,

### 29:00
e vamos ficando por aqui. Te vejo na próxima aula ou no próximo vídeo. Falou! Pronto
