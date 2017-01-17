$(function (){
  $('#search').keyup(function(e) {
    if ((e.which <= 90 && e.which >= 48 || e.which == 8) && $('#search').val() !== '') {
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
  });
});

function searchSuccess(data, textStatus, jqXHR) {
  $('#search-results').html(data);
}
