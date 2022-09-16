from sqlalchemy.orm import backref
from barbearia.barbearia import db

class Servico(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    desc = db.Column(db.String(length=50), nullable=False)
    preco = db.Column(db.Numeric(scale=2), nullable=False)
    agendamentos = db.relationship('Agendamento', backref='servico', lazy='select')

    def __repr__(self):
        return f'Servico {self.desc}'

    def __str__(self):
        return self.desc