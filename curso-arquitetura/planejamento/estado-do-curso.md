# Curso de Arquitetura — retomada em 06/10/2026

## Origem e critério

Conversa recuperada: **30/09/2026**, sessão `01a0f268-c891-77b0-a20f-0b40d7690b8a`, iniciada no workspace `kipperdev-gbrain/sun-valley-v1`. O histórico contém o pedido de slides nativos, exemplos Java pequenos, um main por demonstração, contexto suficiente em cada aula e os ajustes de SOLID → Patterns → Clean/Hexagonal. A pasta atual foi conferida diretamente; não se presumiu que o caminho antigo ainda fosse o destino.

Consulta atual: Pora MCP `list_contents`, primeiro outubro, depois todos os vídeos para identificar a continuação. O campo retornado é **deadline**, prazo editorial; ele não comprova data/hora de sessão de gravação. As oito aulas abaixo estão em Backlog no Pora. O status editorial não representa o estado dos arquivos preparados.

Excalidraw conferido ao vivo: coleção [Curso Arquitetura](https://app.excalidraw.com/o/5pZP9SZcJC3/3NwJ9OEXFLw). Antes desta retomada, continha somente as aulas 01, 02 e 03, correspondentes às três pastas locais. Snapshot de agenda: [pora-2026-10-06.json](pora-2026-10-06.json).

## Agenda e materiais

| Prazo Pora | Pasta | Aula | Situação na retomada |
|---|---|---|---|
| 08/10 | 01 | SOLID, Acoplamento, Coesão e Modularização | Roteiro, Java, 10 frames e áudio existentes |
| 13/10 | 03 | Clean Architecture e Hexagonal | Roteiro, Java, 17 frames e áudio existentes |
| 15/10 | 02 | Design Patterns | Roteiro, Java, 18 frames e áudio existentes |
| 20/10 | 04 | Monólito Modular | Materiais novos nesta retomada |
| 22/10 | 05 | Do localhost à produção | Materiais novos nesta retomada |
| 29/10 | 06 | Sistemas Escaláveis | Materiais novos nesta retomada |
| 05/11 | 07 | Monólito vs Microserviços | Materiais novos nesta retomada |
| 12/11 | 08 | Arquitetura Assíncrona | Materiais novos nesta retomada |

Há **6 aulas em outubro e 2 em novembro**. A introdução já gravada é Aula 0, fora dessa lista. Não reabrir o curso com uma repetição da introdução genérica.

## Divergências encontradas

- A ordem editorial põe Clean/Hexagonal (13/10) antes de Patterns (15/10). O histórico e as pastas preservam a decisão Patterns → Clean/Hexagonal. Não alterei datas, títulos ou status no Pora. Os roteiros novos são independentes de uma ordem obrigatória de visualização.
- O título editorial de Patterns não cita Singleton, mas a decisão da conversa e os materiais o incluem. A aula existente tem 30 minutos.
- A capa de SOLID foi acrescentada depois dos nove frames originais. A ordem nativa precisa ser lida por `slidesOrder`, não pela posição do frame na lista JSON.
- Após o pedido do estúdio, o áudio de SOLID foi atualizado para as cinco demos; Clean/Hexagonal também ganhou áudio alinhado. Os antigos foram preservados nas pastas de autoria.

## Materiais anteriores

- [Aula 01 — SOLID](https://app.excalidraw.com/s/5pZP9SZcJC3/5RgMqDzDCcI).
- [Aula 02 — Patterns](https://app.excalidraw.com/s/5pZP9SZcJC3/9VUYBPV17tF).
- [Aula 03 — Clean/Hexagonal](https://app.excalidraw.com/s/5pZP9SZcJC3/9nu1j8fbpQ3).

Os arquivos anteriores foram preservados. A auditoria de existência/estrutura não equivale a uma nova revisão integral da narração ou de todos os diagramas antigos.

## Continuação preparada

| Aula | Proposta de duração | Experiência principal |
|---|---|---|
| 04 | 25 min | Mesma falha de vaga: autocommit deixa recebimento parcial; rollback desfaz a primeira escrita |
| 05 | 25 min | Servidor HTTP, configuração e contador que reinicia com o processo |
| 06 | 30 min | Cinco leituras viram uma; mudança na origem não atualiza automaticamente a cópia |
| 07 | 25 min | Timeout após efeito: retry gera duas cobranças; mesma chave preserva uma |
| 08 | 35 min | Intenção de evento guardada; redelivery repete efeito sem deduplicação |

São propostas de duração para cobrir os títulos atuais, não decisões antigas já aprovadas. O material contém tópicos e orientação para a professora, sem fala engessada.

## Limites para a gravação

- Demos 06–08 são simulações locais explícitas dos mecanismos. Não chamar mapas em memória de Redis, broker ou idempotência durável.
- Aula 04 usa Java para os módulos e SQLite real via driver padrão de Python para a transação. Nenhuma biblioteca precisa ser baixada.
- Aula 05 inclui Dockerfile e comandos, mas o daemon Docker estava desligado. Ensaio de container fica pendente; nenhuma aplicação foi implantada publicamente.
- O pedido posterior do estúdio incluiu áudio: oito MP3s disponíveis, 3min49s–3min59s, decodificação integral validada. Sete novos via ElevenLabs; aula 02 preservada. Sem escuta humana integral.

## Entrega do estúdio

- `studio/content.json`: oito IDs reais do Pora, links individuais de slides e fila na ordem pedagógica. Introdução publicada aparece separadamente como já gravada.
- `studio/briefings.json`: resumo, pontos essenciais, texto e MP3 de cada aula.
- `studio/examples.json`: 29 exemplos isolados. Somente fontes nas pastas abertas ao aluno; dados/compilação fora delas.
- `studio/server.py`: estado persistente, apenas uma aula em gravação e fila durável de sincronização. A mudança remota só ocorre após Concluir gravação. Nenhuma aula foi marcada como gravada durante a construção.
- Coleção Excalidraw atualizada com aulas 04–08, 46 slides nativos adicionais. Cópias locais preservam os elementos editáveis.

## Validação

15 demos anteriores executadas; 14 demos novas finitas executadas com resultados esperados. Os 29 exemplos isolados foram validados, com compilação apenas para o servidor HTTP. O sandbox impede abrir portas locais; por isso a aula HTTP e o servidor do estúdio não puderam ser executados com socket nesta sessão. Docker também permanece sem ensaio no daemon. Testes automatizados do fluxo local e MCP usam respostas controladas: não simulam uma gravação real no Pora.

Evidências em `.context/validacao/`. A data editorial foi mantida. Estado inicial confirmado pela Fernanda em 06/10: somente a introdução foi gravada. As oito restantes ficam na fila; no Pora continuam Backlog até a conclusão de cada gravação.
