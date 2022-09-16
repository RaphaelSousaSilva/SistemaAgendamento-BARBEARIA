from sqlalchemy.orm import backref
from barbearia.barbearia import db

class Barbeiro(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    nome = db.Column(db.String(length=50), nullable=False)
    agendamentos = db.relationship('Agendamento', backref='barbeiro', lazy='select')

    def __repr__(self):
        return f'Barbeiro {self.nome}'