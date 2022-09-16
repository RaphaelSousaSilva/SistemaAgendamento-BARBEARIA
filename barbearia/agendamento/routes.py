from datetime import datetime
from flask.json import jsonify
from flask_login.utils import login_required, current_user
from flask import render_template, redirect, url_for, flash, request
from barbearia.models import Agendamento, Barbeiro, Servico
from barbearia.agendamento import agendamento_bp
from barbearia.agendamento.forms import AgendamentoForm
from barbearia.barbearia import db
from barbearia.models.servico import Servico


# Incio agendamento routes
@agendamento_bp.route("/agendamento")
@login_required
def agendamento_page():
    form = AgendamentoForm()
    servico = Servico()
    barbeiro = Barbeiro()

    #definindo as opções de servicos e barbeiros no html pegando do banco de dados
    form.servico.choices = [(servico.id, servico.desc) for servico in Servico.query.all()]
    form.barbeiro.choices = [(barbeiro.id, barbeiro.nome) for barbeiro in Barbeiro.query.all()]
    if current_user.is_authenticated:
        if current_user.is_admin:
            agendamentos = Agendamento.query.all()
        else:
            u_id = current_user.get_id()
            agendamentos = Agendamento.query.filter_by(usuario_ID=u_id).all()
    else:
        agendamentos=[]
    return render_template("calendar.html", agendamentos=agendamentos, form=form, servico=servico, barbeiro=barbeiro)

@agendamento_bp.route("/agendar", methods=["GET", "POST"])
@login_required
def agendar():
    msg_final = lambda msg="houve algum erro" : {"sit" : False, "msg" : f'<div class="alert alert-danger" role="alert">{msg}</div>'}
    if request.method == "POST":
    
        inicio_atendimento = request.form['inicio_atendimento']
        fim_atendimento = request.form['fim_atendimento']
        if fim_atendimento <= inicio_atendimento:
            msg = 'A data final deve ser maior que a inicial'
            return jsonify(msg_final(msg))

        #reformatando datas para o padrao do BD
        inicio_atendimento_atualizado = datetime.strptime(inicio_atendimento, '%d/%m/%Y %H:%M:%S')
        fim_atendimento_atualizado = datetime.strptime(fim_atendimento, '%d/%m/%Y %H:%M:%S')
        diferenca_entre_datas = (fim_atendimento_atualizado - inicio_atendimento_atualizado).total_seconds()
        
        #checa se a diferença entre o horario inicial e final é mais de 1 hora e meia
        #para evitar inputs erroneos do usuario
        if diferenca_entre_datas > 5400.0:
            msg = 'O tempo final do atendimento não pode ser maior que 1 hora e meia'
            return jsonify(msg_final(msg))
        
        #instacia o novo agendamento no BD
        novo_agendamento = Agendamento(inicio_atendimento=inicio_atendimento_atualizado, fim_atendimento=fim_atendimento_atualizado,
                            usuario_ID=current_user.get_id(), barbeiro_ID=request.form['barbeiros'], 
                            servico_ID=request.form['servico'] )
        db.session.add(novo_agendamento)
        db.session.commit()
        db.session.close()
        msg_final = {"sit" : True, "msg" : '<div class="alert alert-success" role="alert"> Agendamento registrado com sucesso</div>'}
    return jsonify(msg_final)


@agendamento_bp.route("/edita_agendamento", methods=["GET", "POST"])
@login_required
def editar_agendamento():
    #usando uma funçao lambda que recebe a situcao (boolean), alerta(referente ao bootstrap) e uma msg personalizada
    funcao_msg = lambda msg, sit, alerta : {"sit" : sit, "msg" : f'<div class="alert alert-{alerta}" role="alert">{msg}</div>'}
    msg_final = funcao_msg("houve algum erro", False, "danger")
    if request.method == "POST":
        inicio_atendimento = request.form['inicio_atendimento']
        fim_atendimento = request.form['fim_atendimento']
        if fim_atendimento <= inicio_atendimento:
            msg = 'A data final deve ser maior que a inicial'
            return jsonify(funcao_msg(msg, False, "danger"))

        #reformatando datas para o padrao do BD
        inicio_atendimento_atualizado = datetime.strptime(inicio_atendimento, '%d/%m/%Y %H:%M:%S')
        fim_atendimento_atualizado = datetime.strptime(fim_atendimento, '%d/%m/%Y %H:%M:%S')
        diferenca_entre_datas = (fim_atendimento_atualizado - inicio_atendimento_atualizado).total_seconds()
        #checa se a diferença entre o horario inicial e final é mais de 1 hora e meia
        #para evitar inputs erroneos do usuario
        if diferenca_entre_datas > 5400.0:
            msg = 'O tempo final do atendimento não pode ser maior que 1 hora e meia'
            return jsonify(funcao_msg(msg, False, "danger"))

        agendamento_a_ser_editado = Agendamento.query.filter_by(id=request.form['id']).first()
        agendamento_a_ser_editado.servico_ID = request.form['servico']
        agendamento_a_ser_editado.barbeiro_ID = request.form['barbeiros']
        agendamento_a_ser_editado.inicio_atendimento = inicio_atendimento_atualizado
        agendamento_a_ser_editado.fim_atendimento = fim_atendimento_atualizado
        db.session.commit()
        return jsonify(funcao_msg("Agendamento atualizado com sucesso", True, "success"))
    return jsonify(funcao_msg)


@agendamento_bp.route("/deleta_agendamento", methods=["GET", "DELETE"])
@login_required
def deletar_agendamento():
    funcao_msg = lambda msg, sit, alerta : {"sit" : sit, "msg" : f'<div class="alert alert-{alerta}" role="alert">{msg}</div>'}
    msg_final = funcao_msg("houve algum erro ao apagar o agendamento", False, "danger")
    if request.method == "DELETE":
        # agendamento_id = request.args.get("id")
        agendamento_id = request.form['id']
        if not agendamento_id:
                return jsonify(funcao_msg("houve um erro com o id", False, "danger"))
        agendamento_a_ser_removido = Agendamento.query.filter_by(id=agendamento_id).first()
        db.session.delete(agendamento_a_ser_removido)
        db.session.commit()
        db.session.close()
        msg_final = funcao_msg("Agendamento removido com sucesso", True, "success")

    return jsonify(msg_final)