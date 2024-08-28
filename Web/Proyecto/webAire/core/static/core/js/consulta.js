$(document).ready(function(){


    $('#pronosticar').click(function(e){

        alert("Entra")
        var contaminante = $('#contaminante').val();
        var prediccion1 = $('#1hora').is(':checked');
        var prediccion24 = $('#24horas').is(':checked');

        if(!prediccion1 && !prediccion24){
            alert("Seleccione una opción para la predicción!")
        } else {
            $.ajax ({
                url:'api/prediccion/',
                type: 'POST',
                data: {contaminante,prediccion1},
                dataType: 'json',
                success: function(response){	
                    alert(response)
                }
            });
        }


    });
});