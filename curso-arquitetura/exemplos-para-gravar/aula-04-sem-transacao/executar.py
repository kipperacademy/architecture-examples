from pathlib import Path
import sqlite3
import sys

fixture = Path(sys.argv[1])
source = Path(__file__).with_name("sem-transacao.sql")
with sqlite3.connect(":memory:", isolation_level=None) as db:
    db.executescript(fixture.read_text())
    try:
        for statement in source.read_text().split(";"):
            if statement.strip():
                db.execute(statement)
    except sqlite3.IntegrityError:
        if db.in_transaction:
            db.execute("ROLLBACK")
        print("Vaga 1 já ocupada. Segunda escrita rejeitada pelo banco.")
    print("Recebimentos:", [r[0] for r in db.execute("SELECT pedido FROM financeiro_recebimentos ORDER BY pedido")])
    print("Matrículas:", [r[0] for r in db.execute("SELECT aluna FROM academico_matriculas ORDER BY aluna")])
