from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10), nullable=False)
    hora_entrada = db.Column(db.String(5), nullable=False)
    fornecedor = db.Column(db.String(100), nullable=False)
    nome_motorista = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    placa = db.Column(db.String(7), nullable=False)
    hora_saida = db.Column(db.String(5), nullable=True)
    observacao = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Registro {self.id}>'
