// Variables de valores en cajas de texto
var precio_ultima_compra;
var $precio_ultima_compra = $("#id_ultima_compra");
var precios_text = $("[name*='-precio']");
var margen_text = $("[name*='-margen']");
var markup_text = $("[name*='-markup']");
var precios_mas_iva = $(".precio_mas_iva");
var tabindex = 3;

$( document ).ready(function() {
	
	$("#id_checa_iva").attr("tabIndex",1);
	$precio_ultima_compra.attr("tabIndex",2);

	$(document).find("input").attr("autocomplete","off");
	// Se recortan los decimales
	$precio_ultima_compra.focus();
	$precio_ultima_compra.select();

	
	
	precios_text.each( function(){
		var valor = $(this).val();
		valor = parseFloat(valor)
		$(this).val(valor.toFixed(2));
		$(this).attr("size","10");
		//Pone valores mas IVA
		var $precio_mas_iva = $(this).parent().parent().parent().find(".precio_mas_iva");
		var precio_lista = parseFloat($(this).val());
		if ($("#combo_impuesto").val() == "0") {
			$precio_mas_iva.val((precio_lista).toFixed(2));
		}
		else
		{
			$precio_mas_iva.val((precio_lista*1.16).toFixed(2));
		};	

		
	});
	
	margen_text.each( function(){
		var valor = $(this).val();
		valor = parseFloat(valor)
		$(this).val(valor.toFixed(2));
		$(this).attr("size","8");
	});
	$("#id_ultima_compra").attr("size","10");
	$("#id_ultima_compra").val(parseFloat($("#id_ultima_compra").val()).toFixed(2));
	// Termina de recortar Decimales

	// $("#id_iva_container").hide();
	get_valores();

});


function get_valores(){
	precio_ultima_compra = parseFloat($("#id_ultima_compra").val());
}

function cambia_precio_ultima_compra(){
	debugger
	var tipo_cambio = parseFloat($("#id_tipo_cambio_ultima_compra").val())

	if($("#id_es_moneda_local").val() == 'S')
	{
		tipo_cambio = 1
	}
	var costo_mn =  parseFloat($('#id_ultima_compra').val()) * tipo_cambio
	$("#id_costo_ultima_compra").val(costo_mn)
	get_valores();
	markup_text.each(function(){
		var $precio_lista = $(this).parent().parent().parent().find("[name*='-precio']");
		var precio_lista = parseFloat($precio_lista.val());
		var temporal = ((((precio_lista/precio_ultima_compra)-1)*100)>0)?(((precio_lista/precio_ultima_compra)-1)*100):0;
			$(this).val(temporal.toFixed(2));
		
	});
	margen_text.each(function(){
		var $markup = $(this).parent().parent().parent().find("[name*='-markup']");
		var markup = parseFloat($markup.val());
		//var temporal = markup/(1+(markup/100));
		var temporal = 0;
		$(this).val(temporal.toFixed(2));
		
	});
}

//Cambia precios de lista
function cambia_precio(){
	get_valores();
	var precio_lista = parseFloat($(this).val());
	var $margen = $(this).parent().parent().parent().find("[name*='-margen']");
	var $markup = $(this).parent().parent().parent().find("[name*='-markup']");
	var $precio_mas_iva = $(this).parent().parent().parent().find(".precio_mas_iva");
	var temporal = ((((precio_lista/precio_ultima_compra)-1)*100)>0)?(((precio_lista/precio_ultima_compra)-1)*100):0;
	//var margen = temporal/(1+(temporal/100));
	var margen = 0;
		$margen.val(margen.toFixed(2));
		$markup.val(temporal.toFixed(2));

		if (!$("#id_checa_iva").is(':checked'))
		{
			get_valores();
			if ($("#combo_impuesto").val() == "0") {
				$precio_mas_iva.val((precio_lista).toFixed(2));
			}
			else
			{
				$precio_mas_iva.val((precio_lista*1.16).toFixed(2));
			};		
		};
}	

//Cambia margenes
function cambia_margen(){
	get_valores();
	var margen = parseFloat($(this).val());
	var $markup = $(this).parent().parent().parent().find("[name*='-markup']");
	var $margen = $(this).parent().parent().parent().find("[name*='-margen']");
	var $precio_lista = $(this).parent().parent().parent().find("[name*='-precio']");
	var $precio_mas_iva = $(this).parent().parent().parent().find(".precio_mas_iva");


	var markup = margen/(1-(margen/100));
	var temporal = ((precio_ultima_compra*((margen/100)+1))>0)?((precio_ultima_compra*((margen/100)+1))):0;
	$precio_lista.val(temporal.toFixed(2));
	//$markup.val(markup.toFixed(2));
	var precio_lista = parseFloat($precio_lista.val());
	
	if ($("#combo_impuesto").val() == "0") {
		$precio_mas_iva.val((precio_lista).toFixed(2));
	}
	else
	{
		$precio_mas_iva.val((precio_lista*1.16).toFixed(2));
	};
}

//Cambia markup
function cambia_markup(){
	get_valores();
	var markup = parseFloat($(this).val());
	var $margen = $(this).parent().parent().parent().find("[name*='-margen']");
	var $precio_lista = $(this).parent().parent().parent().find("[name*='-precio']");
	var $precio_mas_iva = $(this).parent().parent().parent().find(".precio_mas_iva");


	
	var temporal = ((precio_ultima_compra*((markup/100)+1))>0)?((precio_ultima_compra*((markup/100)+1))):0;
	//var margen = markup/(1+(markup/100));
	var margen = 0;
	$margen.val(margen.toFixed(2));
	$precio_lista.val(temporal.toFixed(2));

	var precio_lista = parseFloat($precio_lista.val());
	
	if ($("#combo_impuesto").val() == "0") {
		$precio_mas_iva.val((precio_lista).toFixed(2));
	}
	else
	{
		$precio_mas_iva.val((precio_lista*1.16).toFixed(2));
	};
}

function cambia_ch_iva(){
	if ($(this).is(':checked'))
	{
		$("[name*='-precio']").attr("disabled",true);
	}
	else
	{
		$("[name*='-precio']").attr("disabled",false);
	};
}

//Cambia precios con Iva
function cambia_precio_mas_iva(){
	get_valores();
	var $precio_lista = $(this).parent().parent().find("[name*='-precio']");
	if ($("#combo_impuesto").val() == "0") {
		$precio_lista.val((parseFloat($(this).val())).toFixed(2));
	}
	else
	{
		$precio_lista.val((parseFloat($(this).val())/1.16).toFixed(2));
	};

	var precio_lista = parseFloat($precio_lista.val());
	var $margen = $(this).parent().parent().find("[name*='-margen']");

	var $markup = $(this).parent().parent().find("[name*='-markup']");

	var temporal = ((((precio_lista/precio_ultima_compra)-1)*100)>0)?(((precio_lista/precio_ultima_compra)-1)*100):0;
	//var margen = markup/(1+(markup/100));
	var margen = 0;
	$margen.val(margen.toFixed(2));
	$markup.val(temporal.toFixed(2));
}

function cargar_iva(){
	precios_text.each( function(){
		var valor = $(this).val();
		valor = parseFloat(valor)
		$(this).val(valor.toFixed(2));
		$(this).attr("size","10");
		//Pone valores mas IVA
		var $precio_mas_iva = $(this).parent().parent().parent().find(".precio_mas_iva");
		var precio_lista = parseFloat($(this).val());
		if ($("#combo_impuesto").val() == "0") {
			$precio_mas_iva.val((precio_lista).toFixed(2));
		}
		else
		{
			$precio_mas_iva.val((precio_lista*1.16).toFixed(2));
		};		
	});
}

$("#id_check_iva").on("change",cambia_ch_iva);
$("#id_ultima_compra").on("input",cambia_precio_ultima_compra);

margen_text.each(function(){
	$(this).on("input",cambia_margen);
	$(this).attr("tabIndex",tabindex);
	tabindex = tabindex+1;
});

markup_text.each(function(){
	$(this).on("input",cambia_markup);
	$(this).attr("tabIndex",tabindex);
	tabindex = tabindex+1;
});

precios_text.each(function(){
	$(this).on("input",cambia_precio);
	$(this).attr("tabIndex",tabindex);
	tabindex = tabindex+1;
});


precios_mas_iva.each(function(){
	$(this).on("input",cambia_precio_mas_iva);
	$(this).attr("tabIndex",tabindex);
	tabindex = tabindex+1;
});


$(".nombre_precio").each(function(index){
	$(this).text(precios_empresa[index]);
});

$("#combo_impuesto").on("change",cargar_iva);