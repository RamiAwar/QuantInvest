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

    window.scrollTo(0, 0);


}

var clear_errors = function(){
    $('#error-container').html("");
}

var show_info = function(error_message){

    $('#error-container').append('<div class="alert alert-info alert-info alert-dismissible fade show" role="alert">\
                <span class="alert-inner--text">' + error_message + '</span>\
                <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>\
    </div>');

    window.scrollTo(0, 0);

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
var update_chart = function(chart, labels, data, pie=false, upper=[], lower=[]) {

    if(pie){

        chart.data().data.content.chart.data.datasets[0].data = data;
        chart.data().data.content.chart.data.labels = labels;

        chart.data().data.content.data.datasets[0].backgroundColor = generate_random_colors_array(labels.length);
        chart.data().data.content.chart.update();

    }else{

        chart.data().data.chart.data.datasets[0].data = data;

        chart.data().data.chart.data.datasets[1] = {
            'data': upper,
            'label': "Upper limit",
            'borderColor': "#2dce89",
            'borderWidth': "2"
        };

        chart.data().data.chart.data.datasets[2] = {
            'data': lower, 
            'label': "Lower limit",
            'borderColor': "#f5365c",
            'borderWidth': "2"
        }

        // chart.data().data.chart.data.datasets[2].data = lower;

        chart.data().data.chart.data.labels = labels;

        chart.data().data.chart.options.scales.yAxes[0].ticks.min = Math.min.apply(Math, lower);
        chart.data().data.chart.options.scales.yAxes[0].ticks.max = Math.max.apply(Math, upper);

        chart.data().data.chart.update();

    }

    

    return true;

}


var update_charts = function($portfolio_chart, $pie_chart, weights_labels, weights_values, performance_labels, performance_values, performance_upper, performance_lower){

    // Enable portfolio performance updates after integration with backtesting api
    update_chart($portfolio_chart, performance_labels, performance_values, false, performance_upper, performance_lower);
    update_chart($pie_chart, weights_labels, weights_values, true);

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
                layout:{
                    padding:{
                        left: 0,
                        right: 0,
                        top: 0,
                        bottom:0
                    }
                },
                scales: {
                    xAxes: [{
                        type: 'time',
                        time: {
                            unit: 'month',
                            tooltipFormat: 'DD/MM/YYYY'
                        },
                        ticks: {
                            autoSkip: true,
                            maxTicksLimit: 8
                        }
                    }],
                    yAxes: [{
                        gridLines: {
                            color: Charts.colors.gray[900],
                            zeroLineColor: Charts.colors.gray[900]
                        },
                        ticks: {
                            beginAtZero:false,
                            padding:0,
                            callback: function(value) {
                                if (!(value % 10)) {
                                    return '$' + value;
                                }
                            }
                        }
                    }]
                },
                tooltips: {
                    displayColors: false,
                    backgroundColor: "#fff",
                    bodyFontColor: "#444",
                    titleFontColor: "#444",
                    callbacks: {
                        label: function(item, data) {
                            var label = data.datasets[item.datasetIndex].label || '';
                            var yLabel = item.yLabel;
                            var content = '';

                            // console.log(label)
                            // console.log(yLabel)

                            if (data.datasets.length > 1) {
                                content += label + "   " ;
                            }

                            content += '$' + Math.round(yLabel);
                            return content;
                        }
                    }
                }
            },

            data: {
                labels: [''],
                datasets: [{
                    label: 'Total Value',
                    data: [0],
                    borderWidth: 2
                    // hoverBackgroundColor: "rgba(232,105,90,0.8)",
                },
                {
                    label: "Upper Limit",
                    data: [0],
                    borderWidth:2
                },{
                    label: "Lower Limit",
                    data: [0],
                    borderWidth:2
                }]
            }
        });
    }

}

var update_portfolio_summary = function(container, statistics, initial_value, final_value){
    
    // Update basic 3 stats
    $("#" + container + ' .portfolio-expected-return').html((statistics["expected_return"]*100).round(2) + "%")
    $("#" + container + ' .portfolio-volatility').html((statistics["volatility"]*100).round(2) + "%")
    $("#" + container + ' .portfolio-sharpe-ratio').html((statistics["sharpe_ratio"]).round(3))


    // Update initial/final portfolio values
    $("#" + container + ' .portfolio-initial-value').html("$" + initial_value)
    $("#" + container + ' .portfolio-final-value').html("$" + final_value)


    // Update start/end dates
    $("#" + container + ' .portfolio-start-date').html($('#start-date').val());
    $("#" + container + ' .portfolio-end-date').html($('#end-date').val());
    
}

var update_ticker_list = function(container, portfolio_weights){
    
    // Update ticker list constituents
    $("#" + container).html(""); // clear contents

    for(var i = 0; i < portfolio_weights["data"].length; i++){

        var row = "<tr>" + 
                    '<th scope="row">' + 
                        '<div class="media align-items-center">' +
                            '<div class="media-body">' + 
                                '<span class="name mb-0  text-sm">' + portfolio_weights["labels"][i] + '</span>' +
                            '</div>' +
                        '</div>' + 
                    '</th>' + 
                    '<td class="budget"> ' + 
                     portfolio_weights["data"][i] + "%" + 
                    '</td>' + 
                '</tr>';

        $('#' + container).append(row);
    
    }
}