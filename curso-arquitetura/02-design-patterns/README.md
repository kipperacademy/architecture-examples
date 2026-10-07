# Aula 02 — Design Patterns na Prática

Java 21+. Na pasta da aula:

```bash
cd /Users/fernanda/Desktop/kipperdev/curso-arquitetura/02-design-patterns
bash executar.sh sem-adapter
bash executar.sh compra
bash executar.sh sem-desconto
bash executar.sh outro-fornecedor
bash executar.sh singleton
```

O script compila antes de executar e localiza a própria pasta. Cada exemplo tem um `main` separado em `pratica/`.

- `DemoCompra`: Factory + Strategy + Adapter + Singleton, montados por injeção no construtor.
- `DemoSemAdapter`: erro intencional de unidade na chamada ao SDK.
- `DemoSemDesconto`: troca somente a política de preço.
- `DemoSingleton`: duas compras compartilham o mesmo registro; ambas enxergam o total 2.
- `DemoOutroFornecedor`: troca somente o fornecedor escolhido na Factory.

Tudo é simulado localmente: não há cobrança, API ou acesso à rede. A aplicação usa centavos; o SDK fictício recebe reais como texto. Com preço de R$ 100 e desconto Pix de 10%, o total esperado é R$ 90. O erro sem Adapter faz o SDK interpretar R$ 9.000.

Roteiro em `roteiro.md`; [18 slides no Excalidraw](https://app.excalidraw.com/s/5pZP9SZcJC3/9VUYBPV17tF), também salvos em `teoria.excalidraw`. Áudio de revisão: `preparacao-para-gravar.mp3` (3min49s). Aula de 30 minutos: quatro blocos de 5 minutos + 10 de prática.

Código preparado, ainda não compilado nem executado.

`RegistroCompras` é um contador didático em memória, usado em uma única thread. Cada execução Java começa do zero; ele não persiste compras nem coordena múltiplos processos.
