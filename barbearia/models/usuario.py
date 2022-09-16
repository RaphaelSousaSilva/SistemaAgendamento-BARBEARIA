from sqlalchemy.orm import backref
from barbearia.barbearia import db, login_manager,bcrypt
from flask_login import UserMixin, current_user
from flask_bcrypt import check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    cpf = db.Column(db.String(length=14), nullable=False)
    telefone = db.Column(db.String(length=14), nullable=False)
    data_nascimento = db.Column(db.Date(), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)
    agendamentos = db.relationship('Agendamento', backref='usuario', lazy='select')

    def __repr__(self):
        return f'email: {self.email}\ncpf: {self.cpf}'

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)       #checks if the password in database matches the one attempted by user


