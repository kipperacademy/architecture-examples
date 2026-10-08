# Aula: Do localhost à produção

Exemplo de apoio para a aula: uma API Java 21 com uma única rota `GET /cursos`, dados fictícios e porta `8080`. O servidor se liga a `127.0.0.1`; na VPS, o Nginx recebe HTTP/HTTPS e encaminha a chamada para a aplicação. Não há banco, login, framework web ou chamadas a serviços externos.

## Rodar no computador

Requer JDK 21 e Maven.

```sh
mvn -q package
java -jar target/catalogo-cursos-1.0.0.jar
```

Em outro terminal:

```sh
curl -i http://localhost:8080/cursos
```

A resposta é um JSON com três cursos fictícios. A rota é somente `GET /cursos`; outro caminho retorna `404` e outro método retorna `405`. `PORT` e `APP_BIND_ADDRESS` podem ser definidos pelo ambiente, com padrões `8080` e `127.0.0.1`.

## Preparar uma VPS Hostinger com Ubuntu

O passo a passo abaixo assume uma VPS Ubuntu com acesso SSH, um domínio sob seu controle e privilégios administrativos. Ele descreve uma implantação didática, sem Docker: JAR + `systemd` + Nginx. Troque `api.seudominio.com` pelo subdomínio real. O deploy não é feito automaticamente por este repositório.

### 1. Gere o JAR e envie para a VPS

Na sua máquina, dentro desta pasta:

```sh
mvn -q package
scp target/catalogo-cursos-1.0.0.jar root@IP_PUBLICO_DA_VPS:/tmp/catalogo-cursos.jar
```

Substitua `IP_PUBLICO_DA_VPS` pelo endereço público mostrado no hPanel. SSH normalmente usa a porta `22`; confirme a porta configurada para sua VPS.

### 2. Instale Java e Nginx, crie o usuário de serviço

Conecte-se por SSH e rode:

```sh
apt update
apt install -y openjdk-21-jre-headless nginx
useradd --system --home /opt/catalogo-cursos --shell /usr/sbin/nologin cursos
install -d -o cursos -g cursos /opt/catalogo-cursos
install -o cursos -g cursos -m 0644 /tmp/catalogo-cursos.jar /opt/catalogo-cursos/catalogo-cursos.jar
```

### 3. Mantenha o processo Java atrás do proxy

Copie `deploy/catalogo-cursos.service` para `/etc/systemd/system/catalogo-cursos.service`, depois inicie o serviço:

```sh
systemctl daemon-reload
systemctl enable --now catalogo-cursos
systemctl status catalogo-cursos
curl -i http://127.0.0.1:8080/cursos
```

O serviço escuta apenas no loopback da VPS (`127.0.0.1:8080`). Assim, a porta Java não precisa ficar acessível diretamente pela internet.

### 4. Aponte o domínio para o IP público

No DNS do domínio, crie um registro `A` com nome `api` apontando para o IP público IPv4 da VPS. A chamada será `api.seudominio.com`. Se a VPS e o domínio também estiverem configurados para IPv6, configure o `AAAA` correspondente. Aguarde a propagação e confira:

```sh
dig A +short api.seudominio.com
```

O resultado deve incluir o IP público da VPS. O domínio é um nome resolvido pelo DNS; não abre portas nem inicia o processo Java.

### 5. Configure o Nginx como entrada pública

Copie `deploy/nginx-catalogo-cursos.conf` para `/etc/nginx/sites-available/catalogo-cursos`, edite `server_name` para o domínio real e habilite a configuração:

```sh
ln -s /etc/nginx/sites-available/catalogo-cursos /etc/nginx/sites-enabled/catalogo-cursos
nginx -t
systemctl reload nginx
```

No firewall da VPS no hPanel e no firewall do sistema operacional, permita as portas de entrada `80/tcp` e `443/tcp`; mantenha também a porta SSH usada por você. Não abra `8080/tcp` para a internet nesta topologia.

### 6. Ative HTTPS e faça a chamada pública

Com o DNS resolvendo para a VPS e a porta 80 acessível, no Ubuntu com `snapd` instale o Certbot e emita o certificado para o subdomínio. O Certbot ajusta o Nginx para servir HTTPS:

```sh
snap install --classic certbot
ln -s /snap/bin/certbot /usr/local/bin/certbot
certbot --nginx -d api.seudominio.com
certbot renew --dry-run
```

Depois teste:

```sh
curl -i https://api.seudominio.com/cursos
```

O caminho completo é: navegador → DNS encontra o IP da VPS → conexão HTTPS em `443` → Nginx → `127.0.0.1:8080` → `GET /cursos` no Java → JSON volta pelo mesmo caminho.

Para investigar o processo:

```sh
journalctl -u catalogo-cursos -f
```

## Materiais da aula

- `roteiro.md`: plano de fala, perguntas de previsão e demonstração.
- `apresentacao.excalidraw`: deck editável em formato Excalidraw.
- `deploy/`: unidade `systemd` e configuração exemplo do Nginx.
- `nodejs/`: alternativa da API em Node.js com `Dockerfile` e Docker Compose.

## Referências

- Oracle, [API `HttpServer` do JDK 21](https://docs.oracle.com/en/java/javase/21/docs/api/jdk.httpserver/com/sun/net/httpserver/HttpServer.html).
- Hostinger, [como apontar um domínio para uma VPS](https://support.hostinger.com/en/articles/1583227-how-to-point-a-domain-to-your-vps-at-hostinger/).
- Hostinger, [como configurar o firewall de uma VPS](https://www.hostinger.com/tutorials/how-to-set-up-vps/).
- Nginx, [proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html).
- Electronic Frontier Foundation, [instruções do Certbot para Nginx](https://certbot.eff.org/instructions?os=ubuntufocal&tab=standard&ws=nginx).
