from pathlib import Path
import sqlite3
import sys

pasta = Path(__file__).parent
modo = sys.argv[1] if len(sys.argv) > 1 else "com-transacao"
if modo not in {"sem-transacao", "com-transacao"}:
    raise SystemExit("Use: sem-transacao | com-transacao")

with sqlite3.connect(":memory:", isolation_level=None) as banco:
    banco.executescript((pasta / "sql/estrutura.sql").read_text())
    try:
        if modo == "com-transacao":
            banco.execute("BEGIN")
        banco.execute("INSERT INTO financeiro_recebimentos VALUES ('pedido-bia')")
        banco.execute("INSERT INTO academico_matriculas VALUES ('pedido-bia', 'Bia', 1)")
        if modo == "com-transacao":
            banco.execute("COMMIT")
    except sqlite3.IntegrityError:
        if banco.in_transaction:
            banco.execute("ROLLBACK")
        print("Vaga 1 já ocupada. Segunda escrita rejeitada pelo banco.")

    recebimentos = banco.execute("SELECT pedido FROM financeiro_recebimentos ORDER BY pedido").fetchall()
    matriculas = banco.execute("SELECT aluna FROM academico_matriculas ORDER BY aluna").fetchall()
    print("Recebimentos:", [linha[0] for linha in recebimentos])
    print("Matrículas:", [linha[0] for linha in matriculas])
