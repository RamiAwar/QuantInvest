//-------- Helper functions -----------
var disable_charts = function(){
    
    $('.chart-container').each(function(){
        $(this).busyLoad("show", {
            background: "rgba(0, 0, 0, 0.6)"
        })
    })
}

var enable_charts = function(){

    $('.chart-container').each(function(){
        $(this).busyLoad("hide")
    })
}

var check_job = function(job_id){

    // Make an ajax post request to the api server, at endpoint check jobs
    data = {
        "job_id": job_id
    }

    $.ajax({
        type: 'POST',
        url: GET_JOB_ENDPOINT,
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(data),  
        context: $(this),
        success: function(response) {
            
            console.log("Get job status successful: Received: ")
            console.log(response);

            if(response["is_finished"]){

                // Update charts with whatever

                // Re-enable everything 
                enable_charts();
                $('#submit').prop('disabled', false);

            }else{

                setTimeout((function(){
                    check_job(job_id);
                }), 400);
            }
        },
        error: function() {
            console.log("Error fetching job status")
        }
    });

}


// TODO: Inconsistent style
function removeData(chart) {
    
    chart.data.forEach((dataset) => {
        
        dataset.data.pop();

    });
    chart.update();
}

function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
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
        
        console.log($chart.data().chart.data);

        $chart.data().chart.data.labels = ["Test","Test","Test","Test","Test","Test","Test","Test"]
        $chart.data().chart.data.datasets[0].data[5] = 0
        $chart.data().chart.update();

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

    

    $('#submit').click(function() {
        
        // Disable submit button until job is finished
        $('#submit').prop("disabled", true);

        // Display loading sign on charts
        disable_charts();

        // Get slider data and submit to optimizer as a job        
        var data = {
            "expected_returns": expected_returns_slider.noUiSlider.get(),
            "expected_risk": expected_risk_slider.noUiSlider.get(),
            "time_range": time_range_slider.noUiSlider.get()
        };

        

        $.ajax({
            type: 'POST',
            url: OPTIMIZER_ENDPOINT,
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),  
            context: $(this),
            success: function(response) {
                
                console.log("Success: received: ")
                console.log(response);
                
                job_id = response["job_id"];

                // Then check for job result, and display that
                check_job(job_id);

            },
            error: function() {
                console.log("Error")
            }
        });

        






    });



});