//-------- Helper functions -----------
var disable_chart = function(){
 
    $("#chart-container").busyLoad("show", {
        background: "rgba(0, 0, 0, 0.6)"
    });
}

var enable_chart = function(){

    $("#chart-container").busyLoad("hide");
}

$(document).ready(function(){

// -------- SLIDERS ---------------


    // Values here are passed from server
    var expected_returns_slider = document.getElementById('expected-returns-slider');
    var expected_risk_slider = document.getElementById('expected-risk-slider');

    var time_range_slider = document.getElementById("time-range-slider"),
        time_range_slider_min = document.getElementById("time-range-slider-value-low"),
        time_range_slider_max = document.getElementById("time-range-slider-value-high");



    // TODO: on change value, send ajax request to optimizer and wait for response. :priority (1)
    // Disable sliders upon request, enable again upon response received and after updating chart
    // expected_returns_slider.setAttribute('disabled', true)
    



// var noUiSlider = (function() {

//     if ($("#input-slider-range")[0]) {
//             var c = document.getElementById("input-slider-range"),
//                     d = document.getElementById("input-slider-range-value-low"),
//                     e = document.getElementById("input-slider-range-value-high"),
//                     f = [d, e];

//             noUiSlider.create(c, {
//                     start: [parseInt(d.getAttribute('data-range-value-low')), parseInt(e.getAttribute('data-range-value-high'))],
//                     connect: !0,
//                     range: {
//                             min: parseInt(c.getAttribute('data-range-value-min')),
//                             max: parseInt(c.getAttribute('data-range-value-max'))
//                     }
    
//             }), c.noUiSlider.on("update", function(a, b) {
//                     f[b].textContent = a[b]
//             })
//     }
// })()
    
    // Initialize expected returns slider
    noUiSlider.create(expected_returns_slider, {
        start:0,
        range:{'min':0, '50%':50, max:100},
        pips: {mode:'range', density:10},
        tooltips: wNumb({decimals:2})
    })

    // Initialize expected risk slider
    noUiSlider.create(expected_risk_slider, {
        start:0,
        range:{min:0, max:100},
        pips: {mode:'range', density:10},
        tooltips: wNumb({decimals:2})
    })
    
    
    // Initialize time range slider
    f = [time_range_slider_min, time_range_slider_max];
    noUiSlider.create( time_range_slider, {

        start: 
        [
            parseInt(time_range_slider_min.getAttribute('data-range-value-low')), 
            parseInt(time_range_slider_max.getAttribute('data-range-value-high'))
        ],
        connect: true,
        range: {
            min: parseInt( time_range_slider.getAttribute('data-range-value-min')),
            max: parseInt( time_range_slider.getAttribute('data-range-value-max'))
        },
        step: 1,
        pips: {
            mode: 'range',
            density: 20
        },
        tooltips: [wNumb({decimals: 0}), wNumb({decimals: 0})],

    }),  

    time_range_slider.noUiSlider.on("update", function(a, b){
        f[b].textContent = a[b];
    })








    // if ($("#input-slider-range")[0]) {
    //         var c = document.getElementById("input-slider-range"),
    //                 d = document.getElementById("input-slider-range-value-low"),
    //                 e = document.getElementById("input-slider-range-value-high"),
    //                 f = [d, e];

    //         noUiSlider.create(c, {
    //                 start: [parseInt(d.getAttribute('data-range-value-low')), parseInt(e.getAttribute('data-range-value-high'))],
    //                 connect: !0,
    //                 range: {
    //                         min: parseInt(c.getAttribute('data-range-value-min')),
    //                         max: parseInt(c.getAttribute('data-range-value-max'))
    //                 }
    //
    //         }), c.noUiSlider.on("update", function(a, b) {
    //                 f[b].textContent = a[b]
    //         })
    // }

// })();
    


    var pie_chart = new Chart(document.getElementById("chart-pie"), {
        type: 'pie',
        data: {
          labels: ["MSFT", "TSLA", "WYNN", "GOOG", "AMZN"],
          datasets: [
            {
              label: "Stock Tickers",
              backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
              data: [30,10,15,15,30]
            }
          ]
        },
        options: {
          title: {
            display: true,
            text: 'Portfolio'
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




    var $chart = $('#portfolio-performance-chart');

    function init($chart) {

        var portfolio_chart = new Chart($chart, {
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

        // Save to jQuery object
        $chart.data('chart', portfolio_chart);

    };

    // Events
    if ($chart.length) {
        init($chart);
    }

    // $( "#searchForm" ).submit(function( event ) {
 
    //     // Stop form from submitting normally
    //     event.preventDefault();

    //     // Get some values from elements on the page:
    //     var $form = $( this ),
    //     term = $form.find( "input[name='s']" ).val(),
    //     url = $form.attr( "action" );

    //     // Send the data using post
    //     var posting = $.post( url, { s: term } );

    //     // Put the results in a div
    //     posting.done(function( data ) {
    //         var content = $( data ).find( "#content" );
    //         $( "#result" ).empty().append( content );
    //     });
    // });


    $('#form').submit(function(e) {
        
        e.preventDefault();
        var data = {};
        var Form = this;
        
        $.each(this.elements, function(i, v) {
            var input = $(v);
            data[input.attr("name")] = input.val();
            delete data["undefined"];
        });

        $.ajax({
            type: 'POST',
            url: OPTIMIZER_ENDPOINT,
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),
            context: Form,
            success: function(callback) {
                console.log(callback);
                // Watch out for Cross Site Scripting security issues when setting dynamic content!
                $(this).text('Hello ' + callback.first_name + ' ' + callback.last_name  + '!');
            },
            error: function() {
                $(this).html("error!");
            }
        });
    });



});