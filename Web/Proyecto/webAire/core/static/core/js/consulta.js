google.charts.load('current', { packages: ['corechart'] });
google.charts.setOnLoadCallback(drawChart);

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
            $('#uiz').css("background-color", "gray")
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



function drawChart() {
    const data = new google.visualization.DataTable();
    data.addColumn('datetime', 'Fecha'); // Eje X como fechas
    data.addColumn('number', 'Sensor');   // Primera serie
    data.addColumn('number', 'Pronóstico'); // Segunda serie
  
    data.addRows([
        [new Date('2024-01-20 00:00:00'), 7, 6],
        [new Date('2024-01-21 00:00:00'), 8, 7],
        [new Date('2024-01-22 00:00:00'), 8, 7.5],
        [new Date('2024-01-23 00:00:00'), 9, 8.5],
        [new Date('2024-01-24 00:00:00'), 9, 9],
        [new Date('2024-01-25 00:00:00'), 9, 9.5],
        [new Date('2024-01-26 00:00:00'), 10, 10],
        [new Date('2024-01-27 00:00:00'), 11, 11],
        [new Date('2024-01-28 00:00:00'), 14, 12],
        [new Date('2024-01-29 00:00:00'), 14, 13],
        [new Date('2024-01-30 00:00:00'), 15, 14]
    ]);
  
    const options = {
        title: 'Gráfica 1. Valores del ozono registrados vs los pronosticados',
        curveType: 'function',
        legend: { position: 'bottom' },
        hAxis: { format: 'yyyy-MM-dd HH:mm:ss', title: 'Fecha' }, // Formato de fecha
        vAxis: { title: 'Valor de Ozono' },
        colors: ['blue', 'red']
    };
  
    const chart = new google.visualization.LineChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}