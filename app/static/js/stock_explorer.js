function liveSearch(value){

    value = value.trim(); // remove any spaces around the text

    
    if(value != ""){ // don't make requests with an empty string
    
        $.ajax({
            url: SEARCH_ENDPOINT,
            data: {searchText: value.toUpperCase()},
            dataType: "json",
            success: function(data){
                var res = "";
                // create the html with results
                for(i in data.results){
                    res += "<tr><td class='budget'>"+data.results[i]+"</td></tr>";
                }

                $("#stocks-list").html(res);
            }
        });
    }
    else{
        $("#stocks-list").html(""); // set the results empty in case of empty string
    }
}
