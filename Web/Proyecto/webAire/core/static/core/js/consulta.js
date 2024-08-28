const mer = {
    estacion:"",
    valor:"",
    unidad:"",
    recomendacion:""
};

const uiz = {
    estacion:"",
    valor:"",
    unidad:"",
    recomendacion:""
};

$(document).ready(function(){

    var pronostico = false;

    $('#pronosticar').click(function(e){

        var contaminante = $('#contaminante').val();
        var prediccion1 = $('#1hora').is(':checked');
        var prediccion24 = $('#24horas').is(':checked');

        var estacion = 0;

        if(!prediccion1 && !prediccion24){
            alert("Seleccione una opción para la predicción!")
        } else {

            pronostico = false; //Limpiamos la variable que indica si se pronostico algo
            //Limpiamos valores para nueva prediccion
            $('#mer').css("background-color", "gray")
            $('#Estacion').html("<h3>Estación</h3>");
            $('#Valorp').html("Valor pronosticado: ");
            $('#Recomendacion').html("Recomendación: ");

            //Peticion para estación "mer"
            estacion = 27;
            $.ajax ({
                url:'api/prediccion/',
                type: 'POST',
                data: {estacion,contaminante,prediccion1},
                dataType: 'json',
                success: function(response){	
                    $('#mer').css("background-color", response.color_punto);
                    mer.estacion = response.nombre_estacion;
                    mer.valor = response.valor_contaminante;
                    mer.unidad = response.unidad;
                    mer.recomendacion = response.recomendaciones;
                    pronostico = true;
                }
            });

            //Peticion para estación "uiz"
            estacion = 41;
            $.ajax ({
                url:'api/prediccion/',
                type: 'POST',
                data: {estacion,contaminante,prediccion1},
                dataType: 'json',
                success: function(response){	
                    $('#uiz').css("background-color", response.color_punto);
                    uiz.estacion = response.nombre_estacion;
                    uiz.valor = response.valor_contaminante;
                    uiz.unidad = response.unidad;
                    uiz.recomendacion = response.recomendaciones;
                    pronostico = true;
                }
            });
        }
    });

    $('#mer').hover(function(e){
        if(pronostico){
            $('#Estacion').html("<h3>Estación " + mer.estacion + "</h3>");
            $('#Valorp').html("Valor pronosticado: " + mer.valor + " " + mer.unidad);
            $('#Recomendacion').html("Recomendación: " + mer.recomendacion);
        }
        
    });

    $('#uiz').hover(function(e){
        if(pronostico){
            $('#Estacion').html("<h3>Estación " + uiz.estacion + "</h3>");
            $('#Valorp').html("Valor pronosticado: " + uiz.valor + " " + mer.unidad);
            $('#Recomendacion').html("Recomendación: " + uiz.recomendacion);
        }
        
    });
});