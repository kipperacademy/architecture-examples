#!/usr/bin/env python3
"""Gera o deck editável da aula no formato portátil do Excalidraw."""

import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "apresentacao.excalidraw"
elements = []
counter = 0


def base(kind, x, y, w, h, *, frame=None, stroke="#1e1e1e", bg="transparent", rough=0):
    global counter
    counter += 1
    return {
        "id": f"lv{counter:05d}", "type": kind, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid",
        "strokeWidth": 2, "strokeStyle": "solid", "roughness": rough, "opacity": 100,
        "groupIds": [], "frameId": frame, "roundness": {"type": 3} if kind == "rectangle" else None,
        "seed": counter * 7919, "version": 1, "versionNonce": counter * 104729,
        "isDeleted": False, "boundElements": [], "updated": 1791450000000,
        "link": None, "locked": False,
    }


def rect(x, y, w, h, color, *, frame, stroke=None):
    elements.append(base("rectangle", x, y, w, h, frame=frame, stroke=stroke or color, bg=color, rough=1))


def text(x, y, w, value, *, frame, size=28, color="#1e1e1e", align="left"):
    lines = value.split("\n")
    h = size * 1.25 * len(lines)
    item = base("text", x, y, w, h, frame=frame, stroke=color)
    item.update({"text": value, "originalText": value, "fontSize": size, "fontFamily": 1,
                 "textAlign": align, "verticalAlign": "top", "containerId": None,
                 "autoResize": True, "lineHeight": 1.25})
    elements.append(item)


def card(x, y, w, h, label, detail, color, *, frame, label_size=29, detail_size=22):
    rect(x, y, w, h, color, frame=frame)
    text(x + 22, y + 22, w - 44, label, frame=frame, size=label_size)
    if detail:
        text(x + 22, y + 68, w - 44, detail, frame=frame, size=detail_size, color="#495057")


def arrow(x1, y1, x2, y2, *, frame, color="#9c36b5", label=None, label_y=None):
    global counter
    counter += 1
    elements.append({
        "id": f"lv{counter:05d}", "type": "arrow", "x": x1, "y": y1,
        "width": x2 - x1, "height": y2 - y1, "angle": 0, "strokeColor": color,
        "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 3,
        "strokeStyle": "solid", "roughness": 1, "opacity": 100, "groupIds": [],
        "frameId": frame, "roundness": None, "seed": counter * 7919, "version": 1,
        "versionNonce": counter * 104729, "isDeleted": False, "boundElements": [],
        "updated": 1791450000000, "link": None, "locked": False,
        "points": [[0, 0], [x2 - x1, y2 - y1]], "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": "arrow", "elbowed": False,
    })
    if label:
        text(x1, label_y if label_y is not None else y1 - 36, max(120, x2 - x1), label,
             frame=frame, size=18, color="#687078", align="center")


def slide(number, title, subtitle, draw):
    x = (number - 1) % 3 * 1800
    y = (number - 1) // 3 * 1000
    f = f"lvframe{number}"
    frame = base("frame", x, y, 1600, 900, stroke="#1e1e1e")
    frame.update({"id": f, "roughness": 1, "name": f"{number:02d}. {title}",
                  "customData": {"slidesOrder": number - 1}})
    elements.append(frame)
    rect(x, y, 1600, 900, "#ffffff", frame=f, stroke="#ffffff")
    rect(x + 58, y + 72, 10, 130, "#e5dbff", frame=f, stroke="#9c36b5")
    text(x + 100, y + 70, 1420, title, frame=f, size=44)
    text(x + 100, y + 145, 1400, subtitle, frame=f, size=26, color="#687078")
    draw(x, y, f)
    text(x + 100, y + 855, 650, "CURSO ARQUITETURA  /  05", frame=f, size=18, color="#687078")
    text(x + 1430, y + 855, 100, f"{number:02d} / 09", frame=f, size=18, color="#687078")


def s1(x, y, f):
    text(x + 120, y + 265, 1360, "Como uma aplicação sai do meu computador\ne chega até qualquer pessoa?", frame=f, size=40)
    xs = [x + 115, x + 490, x + 865, x + 1240]
    labels = [("LOCALHOST", "meu computador", "#d0ebff"), ("IP PÚBLICO", "endereço da VPS", "#e5dbff"),
              ("DOMÍNIO", "nome que o DNS resolve", "#fff3bf"), ("GET /cursos", ":8080 → JSON", "#d3f9d8")]
    for px, (a, b, c) in zip(xs, labels): card(px, y + 435, 300, 150, a, b, c, frame=f, label_size=26, detail_size=20)
    for px in xs[:-1]: arrow(px + 310, y + 510, px + 360, y + 510, frame=f)
    text(x + 120, y + 690, 1300, "Exemplo da aula: uma rota Java, três cursos fictícios, porta 8080.", frame=f, size=25, color="#9c36b5")


def s2(x, y, f):
    card(x + 150, y + 330, 380, 210, "Cliente", "curl ou navegador\nquem inicia a requisição", "#d0ebff", frame=f)
    card(x + 670, y + 330, 380, 210, "IP da VPS", "203.0.113.10\nendereço de exemplo", "#e5dbff", frame=f)
    card(x + 1190, y + 330, 300, 210, "Porta 8080", "processo Java\nGET /cursos", "#d3f9d8", frame=f, label_size=27)
    arrow(x + 540, y + 435, x + 650, y + 435, frame=f, label="rede", label_y=y + 390)
    arrow(x + 1060, y + 435, x + 1170, y + 435, frame=f, label="TCP", label_y=y + 390)
    text(x + 150, y + 640, 1320, "IP identifica um destino de rede. Porta identifica um serviço naquele destino.", frame=f, size=26, color="#1971c2")
    text(x + 150, y + 710, 1300, "Preveja: saber o IP basta se nada estiver escutando em 8080?", frame=f, size=24, color="#687078")


def s3(x, y, f):
    card(x + 130, y + 300, 600, 270, "Seu computador", "localhost:8080\n→ loopback deste computador\n→ processo local", "#d0ebff", frame=f, label_size=31, detail_size=25)
    card(x + 870, y + 300, 600, 270, "VPS da aula", "localhost:8080\n→ loopback da VPS\n→ processo que roda na VPS", "#e5dbff", frame=f, label_size=31, detail_size=25)
    text(x + 735, y + 395, 120, "≠", frame=f, size=48, color="#9c36b5", align="center")
    text(x + 150, y + 640, 1350, "localhost quer dizer “este ambiente”, visto por quem fez a chamada.", frame=f, size=28, color="#9c36b5")
    text(x + 150, y + 720, 1300, "Enviar http://localhost:8080/cursos para alguém não aponta para o seu computador.", frame=f, size=23, color="#687078")


def s4(x, y, f):
    card(x + 125, y + 350, 360, 170, "api.exemplo.com", "nome digitável", "#fff3bf", frame=f)
    card(x + 625, y + 350, 330, 170, "DNS", "consulta registros", "#e5dbff", frame=f)
    card(x + 1090, y + 350, 380, 170, "203.0.113.10", "IP público da VPS", "#d0ebff", frame=f)
    arrow(x + 500, y + 435, x + 610, y + 435, frame=f, label="pergunta", label_y=y + 390)
    arrow(x + 970, y + 435, x + 1070, y + 435, frame=f, label="registro A", label_y=y + 390)
    text(x + 150, y + 630, 1340, "DNS resolve o nome para endereços. O registro A contém um IPv4; AAAA pode apontar para IPv6.", frame=f, size=24, color="#495057")
    text(x + 150, y + 710, 1300, "DNS não inicia o Java, não abre firewall e não configura HTTPS.", frame=f, size=26, color="#9c36b5")


def s5(x, y, f):
    cards = [
        (x + 100, "1 · DNS", "api.exemplo.com\n→ IP da VPS", "#fff3bf"),
        (x + 405, "2 · Internet", "HTTPS :443\nIP público", "#d0ebff"),
        (x + 710, "3 · Nginx", "termina TLS\ne faz proxy", "#e5dbff"),
        (x + 1015, "4 · Java", "127.0.0.1:8080\nGET /cursos", "#d3f9d8"),
        (x + 1320, "5 · JSON", "resposta\n3 cursos", "#d3f9d8"),
    ]
    for px, a, b, c in cards: card(px, y + 350, 260, 190, a, b, c, frame=f, label_size=23, detail_size=21)
    for px in [x + 365, x + 670, x + 975, x + 1280]: arrow(px, y + 445, px + 30, y + 445, frame=f)
    text(x + 130, y + 645, 1320, "O cliente chega pela porta pública 443. A aplicação Java continua na 8080, privada na VPS.", frame=f, size=24, color="#9c36b5")


def s6(x, y, f):
    card(x + 120, y + 300, 575, 300, "Única rota", "GET  /cursos\n\n200  application/json\n\n[\n  { id: 1, nome: Java do zero },\n  { id: 2, nome: APIs com Java },\n  { id: 3, nome: Deploy na VPS }\n]", "#d3f9d8", frame=f, label_size=31, detail_size=23)
    card(x + 830, y + 300, 600, 300, "Comando no computador", "mvn -q package\njava -jar target/catalogo-cursos-1.0.0.jar\n\ncurl http://localhost:8080/cursos", "#d0ebff", frame=f, label_size=31, detail_size=23)
    text(x + 130, y + 680, 1330, "JDK 21 · HttpServer · sem framework web · sem banco · dados estáticos e fictícios", frame=f, size=23, color="#687078")


def s7(x, y, f):
    card(x + 120, y + 320, 360, 230, "1 · Empacotar", "Maven gera\no arquivo JAR", "#d0ebff", frame=f)
    card(x + 620, y + 320, 390, 230, "2 · VPS Hostinger", "Ubuntu + Java\nsystemd executa\ncomo usuário cursos", "#e5dbff", frame=f, label_size=27, detail_size=22)
    card(x + 1150, y + 320, 350, 230, "3 · Nginx", "recebe a chamada\ne encaminha", "#fff3bf", frame=f)
    arrow(x + 490, y + 435, x + 605, y + 435, frame=f, label="SCP / SSH", label_y=y + 390)
    arrow(x + 1020, y + 435, x + 1135, y + 435, frame=f, label="127.0.0.1:8080", label_y=y + 390)
    text(x + 140, y + 650, 1310, "Se a sessão SSH fechar, systemd mantém o serviço e reinicia em caso de falha.", frame=f, size=24, color="#9c36b5")


def s8(x, y, f):
    card(x + 120, y + 300, 420, 290, "DNS", "A  api.exemplo.com\n   → IP público da VPS", "#fff3bf", frame=f, label_size=32, detail_size=26)
    card(x + 590, y + 300, 420, 290, "Firewall", "permitir 80/tcp e 443/tcp\nmanter 8080 privado\npermitir sua porta SSH", "#d0ebff", frame=f, label_size=32, detail_size=24)
    card(x + 1060, y + 300, 420, 290, "HTTPS", "Nginx + certificado\n\nhttps://api.exemplo.com/cursos", "#d3f9d8", frame=f, label_size=32, detail_size=24)
    text(x + 135, y + 690, 1330, "No hPanel e no Ubuntu, confira as regras do firewall. DNS não substitui nenhuma delas.", frame=f, size=23, color="#9c36b5")


def s9(x, y, f):
    text(x + 120, y + 280, 1360, "Explique o caminho sem pular etapas", frame=f, size=38)
    card(x + 140, y + 385, 390, 210, "IP", "qual VPS recebe\na conexão?", "#d0ebff", frame=f)
    card(x + 605, y + 385, 390, 210, "Domínio", "como o nome chega\na um IP?", "#fff3bf", frame=f)
    card(x + 1070, y + 385, 390, 210, "Localhost", "de quem é o\nloopback?", "#e5dbff", frame=f)
    text(x + 150, y + 675, 1300, "Fechamento: nome → IP → porta pública → proxy → processo → GET /cursos", frame=f, size=25, color="#9c36b5")


slide(1, "Do localhost à produção", "Como publicar uma API Java em uma VPS Hostinger", s1)
slide(2, "O que é um endereço IP?", "Um destino da rede precisa de um serviço que aceite a conexão.", s2)
slide(3, "O que localhost realmente aponta?", "O loopback de quem iniciou a requisição.", s3)
slide(4, "O que é um domínio?", "Um nome que o DNS resolve para endereços IP.", s4)
slide(5, "Como a requisição chega à aplicação?", "Cada etapa tem um papel diferente no caminho até o Java.", s5)
slide(6, "Uma rota GET /cursos em Java 21", "Aplicação mínima: porta 8080 e resposta JSON estática.", s6)
slide(7, "Da sua máquina para a VPS", "O JAR vira um processo persistente; o proxy conecta as portas.", s7)
slide(8, "Domínio, firewall e HTTPS", "Para o público acessar, o caminho precisa estar completo.", s8)
slide(9, "Recapitule o caminho", "Volte às previsões e peça à turma para explicar cada salto.", s9)

OUT.write_text(json.dumps({
    "type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
    "elements": elements, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}
}, ensure_ascii=False), encoding="utf-8")
print(f"{OUT}: {len(elements)} elementos, 9 quadros")
