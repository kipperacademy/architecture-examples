# Estúdio de arquitetura

Abra `start.command` no Finder para iniciar o estúdio em http://127.0.0.1:8765. O servidor permanece ativo após fechar a janela. Para usar outra porta, execute `STUDIO_PORT=8766 ./start.command`.

Selecione uma aula para abrir sua página dedicada. Use **Voltar para a fila** no topo para retornar ao pipeline. Na página da aula, ouça a preparação, confira os pontos e abra o Excalidraw e os exemplos. Clique em **Iniciar gravação** e, ao terminar, em **Concluir gravação**. A conclusão é salva localmente antes da sincronização com o Pora. A confirmação no Pora ocorre em segundo plano; falhas ficam visíveis e são repetidas automaticamente. O botão de repetir permite uma tentativa imediata. O progresso sobrevive ao reinício em `runtime/state.json`; não apague essa pasta durante a sessão.

Os exemplos abrem diretamente uma nova janela do Zed, com somente a pasta dedicada do exemplo. O Zed deve estar instalado em `/Applications/Zed.app`; se não estiver disponível, o estúdio informa o problema. O servidor só abre caminhos cadastrados em `examples.json` dentro de `exemplos-para-gravar`; não executa comandos enviados pelo navegador.

Metadados das aulas: `content.json`. Resumos e áudios: `briefings.json` e `audio/`. Exemplos: `examples.json`. As credenciais MCP são lidas da configuração local do Codex a cada solicitação e não são enviadas ao navegador nem salvas no estúdio. O log fica em `runtime/server.log`.

Requer Python 3.11 ou posterior. Verificação local, sem escrever no Pora: `python3 -m unittest discover -s studio -p 'test_server.py'` a partir da raiz do curso.

O botão **Voltar para a fila** devolve uma aula em gravação ou edição à fila. Uma gravação apenas iniciada volta localmente. Uma aula concluída também solicita **Gravação pendente** no Pora, com confirmação e tentativas automáticas. Se uma sincronização antiga estiver em andamento, sua confirmação não substitui a decisão mais recente. A introdução já publicada fica separada desse fluxo.

Cada ponto do briefing pode incluir uma consulta técnica expandida: **O que é**, **Como funciona**, **Na demo** e **Pergunta para o aluno**. A seleção de checklist permanece independente dessa explicação.
