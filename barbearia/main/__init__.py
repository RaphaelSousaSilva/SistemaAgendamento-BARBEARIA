from flask import Blueprint

main_bp = Blueprint("main", __name__, static_folder="main_static", template_folder="templates")

from barbearia.main import routes