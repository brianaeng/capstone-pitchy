$(function (){
  $('#search').keyup(function(e) {
    //Actions only triggered with numbers, letters, and backspace
    if (e.which <= 90 && e.which >= 48 || e.which == 8) {
      //If the input value is empty (such as if a user pressed backspace all the way to empty it), clear the search results html instead of keeping last letter search
      if ($('#search').val() === '') {
        $('#search-results').html("");
      }
      //Else, AJAX request to the search view and call searchSuccess for results render
      else {
        $.ajax({
          type: "POST",
          url: "/search/",
          data: {
            'search_text': $('#search').val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
          },
          success: searchSuccess,
          dataType: 'html'
        });
      }
    }
  });
});

function searchSuccess(data, textStatus, jqXHR) {
  //Adds search results data from search view to results ul
  $('#search-results').html(data);
}
