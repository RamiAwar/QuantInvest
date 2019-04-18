$(document).ready(function(){

// -------- SLIDERS ---------------


    // Values here are passed from server
    var expected_returns_slider = document.getElementById('expected-returns-slider');
    var expected_risk_slider = document.getElementById('expected-risk-slider');

    var time_range_slider = document.getElementById("time-range-slider"),
        time_range_slider_min = document.getElementById("time-range-slider-value-low"),
        time_range_slider_max = document.getElementById("time-range-slider-value-high");


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


    // Check initialization (from risk assesser quiz)
    if(basic == true){


        // Set expected returns and expected volatility sliders to their respective generated Values
        // These variables are defined in another script inside the HTML, so that they can have access 
        // to the flask variables 
        expected_returns_slider.noUiSlider.set(quiz_expected_return)
        expected_risk_slider.noUiSlider.set(quiz_expected_risk)

        // Display info message to user
        show_info("Your generated expected return and risk values have been set as the slider values. Click optimize to generate your optimal portfolio using the provided time range.")
    }


        
    // ------------------- CHARTS -----------------------------

    // Initialize pie chart 
    var $pie_chart = $('#chart-pie')
    var pie_chart = new PieChart($pie_chart, "Portfolio", ["tesla", "msft", "googl", "amzn", "plx", "ret"], [25,10, 5, 20, 13, 27])
    // Save to jQuery object
    $pie_chart.data('data', pie_chart)


    // Initialize portfolio chart
    var $portfolio_chart = $('#portfolio-performance-chart');
    var portfolio_chart = new PortfolioChart($portfolio_chart);
    // Save to jQuery object
    $portfolio_chart.data('chart', portfolio_chart);


    $('#submit').click(function() {
        
        // Disable submit button until job is finished
        $('#submit').prop("disabled", true);

        // Display loading sign on charts
        disable_charts();

        // Get slider data and submit to optimizer as a job        
        var data = {
            "optimization_method":"target-return-volatility",
            "target_return": expected_returns_slider.noUiSlider.get(),
            "target_volatility": expected_risk_slider.noUiSlider.get(),
            "start_date": (parseInt(time_range_slider.noUiSlider.get()[0]))+"-01-01",
            "end_date": (parseInt(time_range_slider.noUiSlider.get()[1]))+"-01-01",
            "initial_amount": parseInt($("#initial-amount-input-basic").val())
        };

        

        $.ajax({
            type: 'POST',
            url: OPTIMIZER_ENDPOINT,
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),  
            context: $(this),
            success: function(response) {
                
                job_id = response["job_id"];

                // Then check for job result, and display that
                check_job(job_id);

            },
            error: function() {
                console.log("Error")
            }
        });
    });

    // TODO: Refactor this function to accept a callback function and call it on success : priority (1)

    // Function to check requested job status by polling API endpoint.
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
                
                console.log("Get job status - Received: ")
                console.log(response);


                // TODO: Better error handling here : priority (4)
                if(response["is_finished"]){

                   
                    performance_values = response["result"]["performance"]["total"]
                    performance_upper = response["result"]["performance"]["upper"]
                    performance_lower = response["result"]["performance"]["lower"]
                    performance_labels = response["result"]["performance"]["labels"]

                    portfolio_weights = response["result"]["weights"]
                    weights_values = portfolio_weights["data"]
                    weights_labels = portfolio_weights["labels"]

                    update_charts($portfolio_chart, $pie_chart, weights_labels, weights_values, performance_labels, performance_values, performance_upper, performance_lower);

                    // Update portfolio summary
                    update_portfolio_summary("#portfolio-summary-basic", response["result"]["statistics"], portfolio_weights, performance_values[0].round(0), performance_values.slice(-1)[0].round(0));
                    
                    enable_charts();
                    
                    $('#submit').prop('disabled', false);

                }else if(response["is_failed"]){

                    // Display error

                    enable_charts();
                    $('#submit').prop('disabled', false);
                    show_error("Unknown server error occured. Try again later.")

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



});