from flask import Blueprint

auth_bp = Blueprint("auth", __name__, template_folder="templates", static_folder="auth_static")

from barbearia.auth import routes