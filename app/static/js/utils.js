//-------- Helper functions -----------

// Enable busy loader on all .chart-container DOM 
var disable_charts = function(){
    
    $('.chart-container').each(function(){
        $(this).busyLoad("show", {
            background: "rgba(0, 0, 0, 0.6)"
        })
    })
}


// Remove busy loader from all .chart-container DOM
var enable_charts = function(){

    $('.chart-container').each(function(){
        $(this).busyLoad("hide")
    })
}


// Add error to #error-container defined in base.html, which also displays flashed messages from flask
var show_error = function(error_message){

    $('#error-container').append('<div class="alert alert-info alert-danger alert-dismissible fade show" role="alert">\
                <span class="alert-inner--text">' + error_message + '</span>\
                <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>\
    </div>');

}

function get_random_color() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

var generate_random_colors_array = function(n){
    var colors = [];
    for(var i = 0; i < n; i++){
        colors.push(String(get_random_color()));
    }
    return colors;
}

class PieChart{

    constructor(dom_element, chart_label, data_labels, data){
        
        this.chart = new Chart(dom_element, {
            type: 'pie',
            data: {
              labels: data_labels,
              datasets: [
                {
                  label: "test",
                  backgroundColor: generate_random_colors_array(data_labels.length),
                  data: data
                }
              ]
            },
            options: {
              title: {
                display: true,
                text: chart_label
              },
              tooltips: {

                    backgroundColor: "#fff",
                    bodyFontColor: "#444",
                    titleFontColor: "#444",
                    callbacks: {
                        label: function(item, data) {
                            var label = data.datasets[item.datasetIndex].label || '';
                            
                            var content = '';
                            content += data.labels[item.index] + " "
                            content += data.datasets[item.datasetIndex].data[item.index] + '%';
                            return content;
                        }
                    }
                }
            }
        });
    }
}

class PortfolioChart{

    constructor(){
        this.chart = new Chart($chart, {
            type: 'line',
            options: {
                scales: {
                    yAxes: [{
                        gridLines: {
                            color: Charts.colors.gray[900],
                            zeroLineColor: Charts.colors.gray[900]
                        },
                        ticks: {
                            callback: function(value) {
                                if (!(value % 10)) {
                                    return '$' + value + 'k';
                                }
                            }
                        }
                    }]
                },
                tooltips: {
                    backgroundColor: "#fff",
                    bodyFontColor: "#444",
                    titleFontColor: "#444",
                    callbacks: {
                        label: function(item, data) {
                            var label = data.datasets[item.datasetIndex].label || '';
                            var yLabel = item.yLabel;
                            var content = '';

                            if (data.datasets.length > 1) {
                                content += '<span class="popover-body-label mr-auto">' + label + '</span>';
                            }

                            content += '$' + yLabel + 'k';
                            return content;
                        }
                    }
                }
            },

            data: {
                labels: ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Performance',
                    data: [0, 120, 10, 30, 15, 40, 20, 60, 60]
                }]
            }
        });
    }

}
