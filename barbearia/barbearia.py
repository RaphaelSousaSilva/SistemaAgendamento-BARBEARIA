from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from requests import Request
from barbearia.config import Config
from flask_babelex import Babel


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login_page"
login_manager.login_message = "Você deve estar logado para acessar está página"
login_manager.login_message_category = "danger"
request = Request(app)
admin = Admin(app)
babel = Babel(app)


from barbearia.auth import auth_bp
app.register_blueprint(auth_bp)

from barbearia.main import main_bp
app.register_blueprint(main_bp)

from barbearia.agendamento import agendamento_bp
app.register_blueprint(agendamento_bp)

from barbearia.models import Usuario, Barbeiro, Servico

with app.app_context():
    db.create_all()
    if Usuario.query.filter_by(id=1).first() == None:
        usuario_admin = Usuario(username='admin', email='admin@admin.com', cpf='11111111111', \
                            telefone='11912345678', data_nascimento='01/01/2000',\
                            password_hash= bcrypt.generate_password_hash('senha123').decode('utf-8'), is_admin=True)
        usuario_teste = Usuario(username='usuario_teste', email='usuarioteste@email.com',\
                            password_hash=bcrypt.generate_password_hash('senha123').decode('utf-8'),\
                            cpf='41190822212', telefone='11914515678', data_nascimento='01/01/2001')
        db.session.add(usuario_admin)
        db.session.add(usuario_teste)
        db.session.commit()
    #### APENAS PARA TESTES ####
    if Barbeiro.query.all() == []:
        barbeiro1 = Barbeiro(nome='Raphael')
        barbeiro2 = Barbeiro(nome='Lucas')
        barbeiro3 = Barbeiro(nome='Fábio')
        barbeiro4 = Barbeiro(nome='Lino')
        db.session.add(barbeiro1)
        db.session.add(barbeiro2)
        db.session.add(barbeiro3)
        db.session.add(barbeiro4)
        servico1 = Servico(desc='Corte Simples', preco=25)
        servico2 = Servico(desc='Corte + barba', preco=45)
        servico3 = Servico(desc='Seladinho', preco=35)
        servico4 = Servico(desc='Química', preco=50)
        db.session.add(servico1)
        db.session.add(servico2)
        db.session.add(servico3)
        db.session.add(servico4)
        db.session.commit()