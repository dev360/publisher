$(function(){
  function geneticFormSubmit() {
    var form = $(this);
    var url = form.attr('action');
    var data = form.serialize();

    form.find('ul.errorlist').remove();

    $.ajax({
      url: url,
      type: 'POST',
      dataType: 'json',
      data: data,
      success: function(data, status, request) {
        location.href = data['success_url'];
      },
      error: function(request) {
        var data = JSON.parse(request.responseText)['error'];
        var el;

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
