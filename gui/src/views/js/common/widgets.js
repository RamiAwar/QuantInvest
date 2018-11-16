/**
 * @module widgets
 * @exports create_list
 * @description  Module for creating new widgets by dynamically creating html elements.
 * @author Rami Awar
 * @copyright MIT License
 */

$ = require('jquery')
 

/**
 * @brief Creates html list from javascript array
 * @details Requires javascript array of dictionaries with predefined parameters, and an element identifier to append html to. Can also 
 * support a search bar with a custom search function.
 * 
 * @param {Object[]} list_items - The list items that will form the list
 * @param {string} list_items[].title - The list item title.
 * @param {string} list_items[].description - The list item description.
 * @param {bool} list_items[].has_image - Boolean specifying whether list item includes image.
 * @param {string} list_items[].image_src - Image source string, required only if {has_image} is true.
 * 
 * @param element_id {string} HTML element identifier to fetch element which will have list appended to.
 * @param with_search {bool} Boolean specifying whether or not a search bar should precede the list.
 * @param search_placeholder {string}
 * @return None
 */

exports.create_list = function(array, element_id, with_search=false, search_placeholder=""){

  // Create html
  html = '<ul class="list-group">';


  // Check if search functionality is needed
  if( with_search == true){

    //TODO: Handle searching functionality when needed, keeping this class general purpose


    html += `<li class="list-group-header">
              <input class="form-control" type="text" placeholder="${search_placeholder}">
            </li>`
    
  }




  // Begin adding array items to list
  for(var i = 0; i < array.length; i++){
    html += `<li class="list-group-item">`;

    // Add image if specified
    if(array[i].has_image == true){
      html += `<img class="img-circle media-object pull-left" src="${array[i].image_src}" width="32" height="32">`;
    }

    // Add list item title and description
    html += `<div class="media-body">
                <strong>${array[i].title}</strong>
                <p>${array[i].description}</p>
              </div>
            </li>`;

    // Close list item tag if final item
    html += '</li>'; 
  }




  // Close unsorted list item
  html += '</ul>';




  // Add some event handling js, fetch jquery, add active property upon hovering over list-group-item
  html += `
    <script>
        $ = require('jquery')
        $(".list-group-item").hover(function(){$(this).addClass("active")}, function(){$(this).removeClass("active")});
    </script>`;

  $(`#${element_id}`).append(html);

}
