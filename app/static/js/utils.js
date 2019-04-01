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

function get_random(length) { return Math.floor(Math.random()*(length)); }

function get_random_sample(array, size) {

    var length = array.length, start = get_random(length);

    for(var i = size; i--;) {
        var index = (start + i)%length, rindex = get_random(length);
        var temp = array[rindex];
        array[rindex] = array[index];
        array[index] = temp;
    }

    var end = start + size, sample = array.slice(start, end);
    if(end > length)
        sample = sample.concat(array.slice(0, end - length));
    
    return sample;
}

var generate_random_colors_array = function(n){
    var colors_array = ["#F44336", "#E91E63", "#9C27B0", "#673AB7", "#3F51B5", "#4CAF50", "#009688", "#00BCD4", "#03A9F4", "#2196F3", "#8BC34A", "#CDDC39", "#FFEB3B", "#FFC107", "#FF9800", "#FF5722", "#795548", "#9E9E9E", "#607D8B", ]
    return get_random_sample(colors_array, n);
}


// Simple interface for updating pie and line chart data
var update_chart = function(chart, labels, data, pie=false) {
    
    if(labels.length != data.length){
        console.log("ERROR: data length and labels length provided are different, cannot update charts.")
        return false;
    }
    
    chart.data().data.content.chart.data.datasets[0].data = data;
    chart.data().data.content.chart.data.labels = labels;

    if(pie){
        chart.data().data.content.data.datasets[0].backgroundColor = generate_random_colors_array(labels.length);
    }

    chart.data().data.content.chart.update();

    return true;

}


var update_charts = function($portfolio_chart, $pie_chart, portfolio_weights, portfolio_performance){

    // TODO: Enable portfolio performance updates after integration with backtesting api : priority (1)

    // update_chart($portfolio_chart, ["Test","Test","Test","Test","Test","Test","Test","Test"], [0,0,0,10,0,0,0,0,0]);
    update_chart($pie_chart, portfolio_weights['labels'], portfolio_weights['data'], true);

}



// PieChart constructor, basically returns a customized Chart instance for custom styled pie charts.
class PieChart{

    constructor(dom_element, chart_label, data_labels=[""], data=[0]){

        this.element = dom_element;

        this.content = new Chart(dom_element, {
            type: 'pie',
            data: {
              labels: data_labels,
              datasets: [
                {
                  label: "Dataset 1",
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
                    titleFontColor: "#eee",
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


// PortfolioChart class that returns a customized Chart instance for drawing a stylized line chart
class PortfolioChart{

    constructor($chart){
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
                labels: [''],
                datasets: [{
                    label: 'Performance',
                    data: [0]
                }]
            }
        });
    }

}