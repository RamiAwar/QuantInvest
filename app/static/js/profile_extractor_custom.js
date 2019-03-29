var counter = 1;
var limit = 100;

function addInput(divName){
    if (counter == limit)  {
		
		alert("You have reached the limit of adding " + counter + " inputs");
    
    } else {
		
		var newdiv = document.createElement('div');

		newdiv.innerHTML = '<div id="dynamicInput" class="form-group row col-xs-12 col-md-6"> ' + 
          ' <label class="form-control-label">Ticker ' + (counter + 1) + ' </label> ' + 
          ' <input class="form-control form-control-alternative" type="text" name="myInputs[]"> ' + 
        '</div>';
				
		document.getElementById(divName).appendChild(newdiv);
		
		counter++;
     }
}