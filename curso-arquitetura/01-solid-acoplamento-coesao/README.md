# SOLID, acoplamento e coesão

Requer JDK 21+. Cada demo tem seu próprio `main`, sem seleção de cenários no Java.

Partindo de `curso-arquitetura`, cada comando compila e executa uma demo:

```sh
bash 01-solid-acoplamento-coesao/executar.sh DemoEmail
bash 01-solid-acoplamento-coesao/executar.sh DemoAcoplamento
bash 01-solid-acoplamento-coesao/executar.sh DemoDesacoplamento
bash 01-solid-acoplamento-coesao/executar.sh DemoWhatsApp
bash 01-solid-acoplamento-coesao/executar.sh DemoPagamentoPendente
```

Em `DemoDesacoplamento.java`, troque `Notificador notificador = new Email(false);` por `Notificador notificador = new WhatsApp();` e execute novamente. `Matriculas` continua igual.

Para compilar e executar manualmente:

```sh
cd /Users/fernanda/Desktop/kipperdev/curso-arquitetura/01-solid-acoplamento-coesao
mkdir -p pratica/out
javac -encoding UTF-8 -d pratica/out pratica/*.java
java -cp pratica/out DemoDesacoplamento
```

Os atalhos anteriores `ok`, `falha`, `whatsapp` e `pendente` continuam disponíveis no script. `falha` executa as duas demos da falha em sequência.

Tudo é simulado localmente. Acessos e avisos pendentes ficam em memória; nenhum e-mail ou WhatsApp é enviado.

[Slides no Excalidraw](https://app.excalidraw.com/s/5pZP9SZcJC3/5RgMqDzDCcI). A sequência de gravação está em `roteiro.md`.
