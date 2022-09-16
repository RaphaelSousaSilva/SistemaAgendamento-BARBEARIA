from flask import render_template, redirect, url_for, flash, request
from barbearia.models import Usuario
from barbearia.barbearia import db
from barbearia.email_sender import email_cadastro
from flask_login import login_user, logout_user
from barbearia.auth import auth_bp
from barbearia.auth.forms import RegisterForm, LoginForm


@auth_bp.route('/cadastro', methods=["GET", "POST"])
def cadastro_page():
    form = RegisterForm()
    if form.validate_on_submit():
        novo_usuario = Usuario(username=form.username.data, password=form.senha.data,
                               email=form.email.data, cpf=form.cpf.data,
                               telefone=form.telefone.data, data_nascimento=form.data_nascimento.data)
        db.session.add(novo_usuario)
        db.session.commit()
        # email_cadastro(novo_usuario.username,novo_usuario.email)
        login_user(novo_usuario)
        flash(f'Conta criada com sucesso! Você está logado como: {novo_usuario.username}', category='success')
        return redirect(url_for("home_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Aconteceu um erro durante o cadastro: {err_msg}', category='danger')
    return render_template('cadastro.html', form=form)

@auth_bp.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Usuario.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.senha.data):
            login_user(attempted_user)
            flash(f'Você está logado como: {attempted_user.email}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Nome de usuário ou senha incorretos. Tente novamente.', category='danger')
    return render_template("login.html", form=form)

@auth_bp.route("/logout")
def logout_page():
    logout_user()
    flash("Você foi desconectado", category="info")
    return redirect(url_for("home_page"))
