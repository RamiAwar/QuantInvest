var counter = 1;
var limit = 100;

function addInput(divName){
    if (counter == limit)  {
		
		alert("You have reached the limit of adding " + counter + " inputs");
    
    } else {
		
		var newdiv = document.createElement('div');

		newdiv.innerHTML = '<div class="form-group row col-xs-12 col-md-6"> ' + 
          ' <label class="form-control-label">Ticker ' + (counter + 1) + ' </label> ' + 
          ' <input class="form-control form-control-alternative" type="text"> ' + 
        '</div>';
				
		document.getElementById(divName).appendChild(newdiv);
		
		counter++;
     }
}

$(document).ready(function(){



	$('#submit-custom').click(function() {
        
        // Disable submit button until job is finished
        $('#submit-custom').prop("disabled", true);

        // Display loading sign on charts
        disable_charts();

        // Compile ticker list
        var ticker_list = []
        $("#dynamic-ticker-list :input").each(function(){
        	var val = $(this).val();
        	ticker_list.push(val)
        })

        console.log(ticker_list)

        // Get slider data and submit to optimizer as a job        
        // var data = {
        //     "ticker_list": 
        //     // "method": ,
        //     // "expected_risk": ,
        //     // "expected_returns":             

        // };


        // $.ajax({
        //     type: 'POST',
        //     url: OPTIMIZER_ENDPOINT,
        //     dataType: 'json',
        //     contentType: 'application/json; charset=utf-8',
        //     data: JSON.stringify(data),  
        //     context: $(this),
        //     success: function(response) {
                
        //         console.log("Success: received: ")
        //         console.log(response);
                
        //         job_id = response["job_id"];

        //         // Then check for job result, and display that
        //         check_job(job_id, $portfolio_chart, $pie_chart);

        //     },
        //     error: function() {
        //         console.log("Error")
        //     }
        // });


    });

})