from flask_wtf import FlaskForm, form
from sqlalchemy.util.langhelpers import constructor_copy
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import DateTimeField, DateField
from wtforms.validators import DataRequired, ValidationError

class ValidaData(object):
    def __init__(self, inicio, message=None):
        self.inicio = inicio
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.inicio]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.inicio)
        if field.data <= other.data:
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.inicio,
                'other_name': self.inicio
            }
            message = self.message
            if message is None:
                message = field.gettext('O fim do atendimento deve após %(other_name)s.')
            raise ValidationError(message % d)

class AgendamentoForm(FlaskForm):
    servico = SelectField(label='Selecione o Serviço', choices=[], validators=[DataRequired()])
    barbeiro = SelectField(label="Selecione o Barbeiro", choices=[], validators=[DataRequired()])
    inicio_atendimento = DateTimeField(label="Início do atendimento", validators=[DataRequired(), ValidaData("inicio_atendimento")])
    fim_atendimento = DateTimeField(label="Fim do atendimento", validators=[DataRequired()])
    submit = SubmitField(label="Agendar")
