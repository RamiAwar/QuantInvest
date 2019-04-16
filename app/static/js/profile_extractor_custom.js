var counter = 1;
var limit = 100;

function addInput(divName){
    if (counter == limit)  {
		
		alert("You have reached the limit of adding " + counter + " inputs");
    
    } else {
		
		var newdiv = document.createElement('div');

		newdiv.innerHTML = '<div class="form-group"> ' + 
          ' <label class="form-control-label">Ticker ' + (counter + 1) + ' </label> ' + 
          ' <input class="form-control form-control-alternative" type="text"> ' + 
        '</div>';
				
		document.getElementById(divName).appendChild(newdiv);
		
		counter++;
     }
}



OPTIMIZATION_CONSTRAINTS = {

    "max-sharpe": '<input class="d-none" id="target-return">'+
          '<input class="d-none" id="target-volatility">',

    "min-volatility": '<input class="d-none" id="target-return">' +
          '<input class="d-none" id="target-volatility">',

    "min-volatility-target": '<label class="form-control-label">Target portfolio return</label>' + 
                             '<input class="form-control" type="number" value="0.2" id="target-return">',

    "max-return-target": '<label class="form-control-label">Target portfolio volatility</label>' + 
                             '<input class="form-control" type="number" value="0.13" id="target-volatility">'
       
}

var change_opt_constraints = function(event){

    var value = event.target.value;

    $("#constraints-container").html(OPTIMIZATION_CONSTRAINTS[value]);

}


// TODO: Validate inputs using javascript : priority (2)
var validate_inputs = function(ticker_list){
    
    // Check stocks list greater than or equal to 2
    if(ticker_list.length < 2){
        show_error("Invalid request: More than 1 stock is required to build a portfolio.")
        return false;
    }

    // Check time span range start > 01/01/2015
    start_moment = moment($('#start-date').val(), "YYYY-MM-DD");
    end_moment = moment($('#end-date').val(), "YYYY-MM-DD");

    if(!end_moment.isAfter(start_moment)){
        show_error("Invalid request: End date is before start date.");
        return false;
    }

    if(moment("2014-12-31").isAfter(start_moment)){
        show_error("Invalid request: Please select a starting date after 2015")
        return false;
    }

    // Check optimization parameters non empty
    
    



    return true;

}

Number.prototype.round = function(places) {
  return +(Math.round(this + "e+" + places)  + "e-" + places);
}

var update_portfolio_summary = function(statistics, portfolio_weights, initial_value, final_value){
    
    // Update basic 3 stats
    $('#portfolio-expected-return').html((statistics["expected_return"]*100).round(2) + "%")
    $('#portfolio-volatility').html((statistics["volatility"]*100).round(2) + "%")
    $('#portfolio-sharpe-ratio').html((statistics["sharpe_ratio"]).round(3))


    // Update initial/final portfolio values
    $('#portfolio-initial-value').html("$" + initial_value)
    $('#portfolio-final-value').html("$" + final_value)


    // Update start/end dates

    $('#portfolio-start-date').html($('#start-date').val());
    $('#portfolio-end-date').html($('#end-date').val());

    // Update ticker list constituents
    $('#portfolio-ticker-list').html(""); // clear contents

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

        $('#portfolio-ticker-list').append(row);
    
    }
    
}


$(document).ready(function(){

    // Keeping track of chart creation
    var firsttime = true;

    var $start_date = $('#start-date')
    var $end_date = $('#end-date')
        
    // --- Initialize charts -----
    // Initialize pie chart
    var $pie_chart = $('#chart-pie-custom')
    var pie_chart = null
    

    $('#custom-pie-chart-container').hide();
    $('#custom-portfolio-performance-chart-container').hide();
    $('#portfolio-weights-container').hide();
    $('#portfolio-statistics-container').hide();

    // Initialize portfolio performance chart
    var $portfolio_chart = $('#portfolio-performance-chart-custom');
    var portfolio_chart = null


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
                
                console.log(response);

               

                // TODO: Better error handling here : priority (4)
                if(response["is_finished"]){

                    performance_values = response["result"]["performance"]["data"]
                    performance_labels = response["result"]["performance"]["labels"]

                    portfolio_weights = response["result"]["weights"]
                    weights_values = portfolio_weights["data"]
                    weights_labels = portfolio_weights["labels"]

                    update_charts($portfolio_chart, $pie_chart, weights_labels, weights_values, performance_labels, performance_values);

                    // Update portfolio summary
                    update_portfolio_summary(response["result"]["statistics"], portfolio_weights, performance_values[0].round(0), performance_values.slice(-1)[0].round(0));

                    enable_charts();

                    $('#submit-custom').prop("disabled", false);
                    $('#tabs-icons-text-2-tab').removeClass("disabledTab");

                }else if(response["is_failed"]){

                    // Display error

                    enable_charts();                    
                    $('#submit-custom').prop("disabled", false);
                    $('#tabs-icons-text-2-tab').removeClass("disabledTab");

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

	$('#submit-custom').click(function() {

        var ticker_list = []
        $("#dynamic-ticker-list :input").each(function(){
            var val = $(this).val().toUpperCase().trim();
            if (val !== ""){
                ticker_list.push(val);    
            }
            
        })


        
        if(!validate_inputs(ticker_list)) return false;


        // Disable page navigation and submit button until job is finished
        $('#submit-custom').prop("disabled", true);
        $('#tabs-icons-text-2-tab').addClass("disabledTab");
        
        // Display loading sign on charts
        if(firsttime){
            // Chart hiding has to be in this convoluted way due to chartjs bugs
            firsttime = false;

            // Show chart containers
            $('#custom-pie-chart-container').show();
            $('#custom-portfolio-performance-chart-container').show();
            $('#portfolio-weights-container').show();
            $('#portfolio-statistics-container').show();

            // Create charts
            portfolio_chart = new PortfolioChart($portfolio_chart, "Portfolio");
            pie_chart = new PieChart($pie_chart, "Portfolio");

            // Save to jQuery objects
            $pie_chart.data('data', pie_chart)
            $portfolio_chart.data('data', portfolio_chart);

            disable_charts(); 

        }else{
            disable_charts();    
        }


        console.log(ticker_list)



        // Get time range
        var start_date = $start_date.val();
        var end_date = $end_date.val();
    
        // Get optimization method
        var optimization_method = $('#optimization-select').val()

        // Get initial portfolio amount
        var initial_amount = $('#initial-amount-input').val()
        
        // Get target risk and target return (will be empty strings if not user inputted)
        var target_risk = $('#target-volatility')
        var target_return = $('#target-return')

        // Compile form data into an object
        data = {
            "ticker_list": ticker_list,
            "initial_amount": initial_amount,
            "start_date": start_date,
            "end_date": end_date,
            "optimization_method": optimization_method,
            "optimization_parameters": {}
        }

        // Send ajax request to server to begin optimization job
        $.ajax({
            type: 'POST',
            url: OPTIMIZER_ENDPOINT,
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),  
            context: $(this),
            success: function(response) {
                


                console.log(response);

                job_id = response["job_id"];


                // Then check for job result, and display that
                check_job(job_id);

            },
            error: function() {
                console.log("Error sending ajax request to initiate job")
            }
        });


    });

})