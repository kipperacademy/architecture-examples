CREATE TABLE financeiro_recebimentos (pedido TEXT PRIMARY KEY);
CREATE TABLE academico_matriculas (
    pedido TEXT PRIMARY KEY,
    aluna TEXT NOT NULL,
    vaga INTEGER UNIQUE NOT NULL
);
INSERT INTO financeiro_recebimentos VALUES ('pedido-ana');
INSERT INTO academico_matriculas VALUES ('pedido-ana', 'Ana', 1);
