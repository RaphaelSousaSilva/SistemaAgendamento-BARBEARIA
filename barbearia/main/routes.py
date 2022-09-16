from barbearia.barbearia import app
from flask import render_template
from barbearia.barbearia import db
from barbearia.main import main_bp


# db.create_all()

@main_bp.route('/home')
@app.route('/')
def home_page():
    return render_template('home.html')


@main_bp.route("/contact")
def contact_page():
    return render_template("contact.html")