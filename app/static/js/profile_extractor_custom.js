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
var validate_inputs = function(){
    return true;
}


$(document).ready(function(){


    var $start_date = $('#start-date')
    var $end_date = $('#end-date')
        
    // --- Initialize charts -----
    // Initialize pie chart
    var $pie_chart = $('#chart-pie-custom')
    var pie_chart = new PieChart($pie_chart, "Portfolio")
    // Save to jQuery object
    $pie_chart.data('data', pie_chart)


    // Initialize portfolio performance chart
    var $portfolio_chart = $('#portfolio-performance-chart-custom');
    var portfolio_chart = new PortfolioChart($portfolio_chart, "Portfolio");
    
    // Save to jQuery object
    $portfolio_chart.data('data', portfolio_chart);

    console.log($portfolio_chart.data())

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

                    update_charts($portfolio_chart,  $pie_chart, response["result"]["weights"], response["result"]["performance"]);

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
        
        if(!validate_inputs()) return false;    

        // Disable page navigation and submit button until job is finished
        $('#submit-custom').prop("disabled", true);
        $('#tabs-icons-text-2-tab').addClass("disabledTab");
        
        // Display loading sign on charts
        disable_charts();

        // Compile ticker list
        var ticker_list = []
        $("#dynamic-ticker-list :input").each(function(){
        	var val = $(this).val();
        	ticker_list.push(val)
        })

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