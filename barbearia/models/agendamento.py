from barbearia.barbearia import db


class Agendamento(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    inicio_atendimento = db.Column(db.TIMESTAMP(), nullable=False, unique=True)
    fim_atendimento = db.Column(db.TIMESTAMP(), nullable=False, unique=True)
    usuario_ID = db.Column(db.Integer(), db.ForeignKey('usuario.id'))
    barbeiro_ID = db.Column(db.Integer(), db.ForeignKey('barbeiro.id'))
    servico_ID = db.Column(db.Integer(), db.ForeignKey('servico.id'))

    def __repr__(self):
        return f'Id do agendamento {self.id}'