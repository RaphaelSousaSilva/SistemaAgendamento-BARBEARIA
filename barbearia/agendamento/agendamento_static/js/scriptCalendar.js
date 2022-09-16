function DataHora(evento, objeto){
	var keypress=(window.event) ? event.keyCode:evento.which;
	campo = eval (objeto);
	if (campo.value == '00/00/0000 00:00:00')
	{
		campo.value=""
	}
 
	caracteres = '0123456789';
	separacao1 = '/';
	separacao2 = ' ';
	separacao3 = ':';
	conjunto1 = 2;
	conjunto2 = 5;
	conjunto3 = 10;
	conjunto4 = 13;
	conjunto5 = 16;
	if ((caracteres.search(String.fromCharCode (keypress))!=-1) && campo.value.length < (19))
	{
		if (campo.value.length == conjunto1 )
		campo.value = campo.value + separacao1;
		else if (campo.value.length == conjunto2)
		campo.value = campo.value + separacao1;
		else if (campo.value.length == conjunto3)
		campo.value = campo.value + separacao2;
		else if (campo.value.length == conjunto4)
		campo.value = campo.value + separacao3;
		else if (campo.value.length == conjunto5)
		campo.value = campo.value + separacao3;
	}
	else
		event.returnValue = false;
};

$(document).ready(function(){
    $("#addAgend").on("submit", function(event){
        event.preventDefault();
        $.ajax({
            method: "POST",
            url: '/agendar',
            data: new FormData(this),
            contentType: false,
            processData: false,
            success: function(retorno){
				if (retorno['sit']){
					$("#msg-agendamento").html(retorno['msg']);
					location.reload();
				}else{
					$("#msg-agendamento").html(retorno['msg']);
				}
            }
        })
    });

	$(".btn-novo-agend").on("click", function(){
		$("#cadastrar").modal("show")
	});
	$(".btn-editar-agend").on("click", function(){
		$(".visualizar-agend").slideToggle();
		$(".form-edit").slideToggle();
	});
	$(".btn-cancelar-edit").on("click", function(){
		$(".form-edit").slideToggle();
		$(".visualizar-agend").slideToggle();
	});
	$("#editAgend").on("submit", function(event){
        event.preventDefault();
        $.ajax({
            method: "POST",
            url: '/edita_agendamento',
            data: new FormData(this),
            contentType: false,
            processData: false,
            success: function(retorno){
				if (retorno['sit']){
					$("#msg-edit").html(retorno['msg']);
					location.reload();
				}else{
					$("#msg-edit").html(retorno['msg']);
				}
            }
        })
    });
});
