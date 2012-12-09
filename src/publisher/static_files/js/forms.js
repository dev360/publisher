$(function(){
  function geneticFormSubmit() {
    var form = $(this);
    var url = form.attr('action');
    var data = form.serialize();

    $.ajax({
      url: url,
      type: 'POST',
      dataType: 'json',
      data: data,
      success: function(data, status, request) {
        // TODO: alert and close
      },
      error: function(request) {
        var data = JSON.parse(request.responseText);
        var el;

        form.find('ul.errorlist').remove();

        for (var key in data) {
          el = form.find('#id_' + key + ',#id_' + key + '_0').closest('li');
          el.prepend('<ul class="errorlist">' + "<li>" + data[key].join("</li><li>") + "</li>" + '</ul>');
        }
      }
    });

    return false;
  }

  $('#subscribe_form').submit(geneticFormSubmit);
});
