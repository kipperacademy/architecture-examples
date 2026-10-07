-- Modelo para discutir garantias. Não é usado pelas demos Java em memória.
CREATE TABLE matriculas (pedido_id TEXT PRIMARY KEY, aluna TEXT NOT NULL);
CREATE TABLE outbox (evento_id TEXT PRIMARY KEY, pedido_id TEXT NOT NULL, enviado INTEGER DEFAULT 0);

BEGIN;
INSERT INTO matriculas VALUES ('pedido-ana', 'Ana');
INSERT INTO outbox (evento_id, pedido_id) VALUES ('evento-1', 'pedido-ana');
COMMIT;

-- Em outro banco local, pertencente ao consumidor:
CREATE TABLE processados (evento_id TEXT PRIMARY KEY);
CREATE TABLE avisos (evento_id TEXT PRIMARY KEY, aluna TEXT NOT NULL);

BEGIN;
INSERT INTO processados VALUES ('evento-1');
INSERT INTO avisos VALUES ('evento-1', 'Ana');
COMMIT;
-- ACK somente após commit. Duplicidade do ID: rollback; verificar processamento
-- prévio confirmado; então ACK sem repetir o efeito. Não engolir outros erros.
