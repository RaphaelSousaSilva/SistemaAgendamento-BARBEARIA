from flask import Blueprint

agendamento_bp = Blueprint("agendamento", __name__, static_folder="agendamento_static", template_folder="templates")

from barbearia.agendamento import routes