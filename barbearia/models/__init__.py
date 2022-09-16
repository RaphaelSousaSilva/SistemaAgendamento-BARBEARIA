from .agendamento import Agendamento
from .barbeiro import Barbeiro
from .usuario import Usuario
from .servico import Servico


from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from barbearia.barbearia import db, admin
from flask import abort

class ControllerView(ModelView):

    form_excluded_columns = ['agendamentos']

    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.is_admin:
                return True
        return abort(404)

    def not_auth(self):
        return 'Não autorizado'

class UsuarioView(ControllerView):
    column_searchable_list = ['email', 'cpf']

    column_details_exclude_list = {'password_hash'}

    column_labels = {
        'password_hash' : 'Senha',
        'is_admin' : 'É administrador?',
        'data_nascimento' : "Data Nascimento (AAAA-MM-DD)",
    }


    form_args = {
        'password_hash': {
            'label': 'Senha',
        },

        'is_admin' : {
            'label' : 'É administrador?'
        }
    }

class AgendamentoView(ControllerView):
    column_list = ["id", "inicio_atendimento", "fim_atendimento", "usuario",
                    "barbeiro",
                    "servico",]

admin.add_view(UsuarioView(Usuario, db.session))
admin.add_view(ControllerView(Barbeiro, db.session))
admin.add_view(ControllerView(Servico, db.session))
admin.add_view(AgendamentoView(Agendamento, db.session, endpoint="agendamento_"))

