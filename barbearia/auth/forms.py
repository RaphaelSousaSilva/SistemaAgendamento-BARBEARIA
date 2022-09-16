from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from barbearia.models import Usuario


class RegisterForm(FlaskForm):
    username = StringField(label='Nome:', validators=[DataRequired(), Length(min=2, max=30)])
    cpf = StringField(label='CPF:', validators=[DataRequired(), Length(11)])
    telefone = StringField(label='Telefone:', validators=[DataRequired(), Length(11)])
    email = StringField(label='Email:', validators=[DataRequired(), Email()])
    senha = PasswordField(label='Senha:', validators=[DataRequired(), Length(min=6)])
    confirmaSenha = PasswordField(label='Confirme a Senha:', validators=[EqualTo('senha')])
    submit = SubmitField(label='Criar Conta')
    data_nascimento = StringField(label='Data de Nascimento:', validators=[DataRequired(), Length(max=14)])


    def validate_username(self, username_to_check):
        user = Usuario.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Nome de usuário existente, por favor use outro')

    def validate_email(self, email_to_check):
        email = Usuario.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('E-mail já em uso, tente novamente')

class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    senha = PasswordField(label="Senha", validators=[DataRequired()])
    submit = SubmitField(label='Entre')