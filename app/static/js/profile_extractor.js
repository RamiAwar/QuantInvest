//-------- Helper functions -----------
var disable_chart = function(){
 
    $("#chart-container").busyLoad("show", {
        background: "rgba(0, 0, 0, 0.6)"
    });
}

var enable_chart = function(){

    $("#chart-container").busyLoad("hide");
}




// -------- SLIDERS ---------------

var t = (function(){

var expected_returns_slider = document.getElementById('expected-returns-slider');
var expected_risk_slider = document.getElementById('expected-risk-slider');

var min_expected_returns = expected_returns_slider.dataset.rangeValueMin;
var max_expected_returns = expected_returns_slider.dataset.rangeValueMax;

var min_expected_risk = expected_risk_slider.dataset.rangeValueMin; 
var max_expected_risk = expected_risk_slider.dataset.rangeValueMax;


console.log(max_expected_risk);




})();




var noUiSlider = (function() {

    
    // $('.input-slider-container').each(function() {

    //     var slider = $(this).find('.input-slider');
    //     var sliderId = slider.attr('id');
    //     var minValue = slider.data('range-value-min');
    //     var maxValue = slider.data('range-value-max');

    //     var sliderValue = $(this).find('.range-slider-value');
    //     var sliderValueId = sliderValue.attr('id');
    //     var startValue = sliderValue.data('range-value-low');

    //     var c = document.getElementById(sliderId),
    //             d = document.getElementById(sliderValueId);

    //     noUiSlider.create(c, {
    //             start: [parseInt(startValue)],
    //             connect: [true, false],
    //             //step: 1000,
    //             range: {
    //                     'min': [parseInt(minValue)],
    //                     'max': [parseInt(maxValue)]
    //             }
    //     });

    //     c.noUiSlider.on('update', function(a, b) {
    //             d.textContent = a[b];
    //     });
    // })
    // }

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
    //         }), c.noUiSlider.on("update", function(a, b) {
    //                 f[b].textContent = a[b]
    //         })
    // }

})();







var portfolio_chart = (function() {

    var $chart = $('#portfolio-performance-chart');

    function init($chart) {

        var salesChart = new Chart($chart, {
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
                    callbacks: {
                        label: function(item, data) {
                            var label = data.datasets[item.datasetIndex].label || '';
                            var yLabel = item.yLabel;
                            var content = '';

                            if (data.datasets.length > 1) {
                                content += '<span class="popover-body-label mr-auto">' + label + '</span>';
                            }

                            content += '<span class="popover-body-value">$' + yLabel + 'k</span>';
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

        $chart.data('chart', salesChart);

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

})();