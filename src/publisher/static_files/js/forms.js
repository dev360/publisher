$(function(){
  $('#subscribe_form').submit(function() {
    var form = $(this);
    var url = form.attr('action');
    var data = form.serialize();

    $.ajax({
      url: url,
      type: 'POST',
      dataType: 'json',
      data: data,
      success: function(data, status, request) {
        // close it
      },
      error: function(request) {
        var data = JSON.parse(request.responseText);
        var el;

        for (var key in data) {
          el = form.find('#id_' + key).parent();
          el.prepend('<ul class="errorlist">' + "<li>" + data[key].join("</li><li>") + "</li>" + '</ul>');
        }
      }
    });

    return false;
  });
});
