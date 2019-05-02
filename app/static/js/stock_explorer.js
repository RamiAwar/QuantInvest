function liveSearch(value){

    value = value.trim(); // remove any spaces around the text

    
    if(value != ""){ // don't make requests with an empty string
    
        $.ajax({
            type: "POST",
            url: SEARCH_ENDPOINT,
            data: JSON.stringify({searchText: value.toUpperCase()}),
            dataType: "json",
            contentType: 'application/json; charset=utf-8',
            context: $(this),
            success: function(data){
                var res = "";
                // create the html with results
                for(i in data.results){
                    if(i > 5) break;
                    res += "<tr><td class='budget bg-white card-shadow'>"+data.results[i]+"</td></tr>";
                }

                $("#stocks-list").html(res);
            }
        });
    }
    else{
        $("#stocks-list").html(""); // set the results empty in case of empty string
    }
}

