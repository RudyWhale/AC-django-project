$(function() {
  $('textarea.limited_length').keyup(function() {
    var max_len = $(this).attr('maxlength');
    var label = $(this).parent().find('p.symbols_left_label');
    var hide = label.hasClass('hide');
    label.text("осталось символов: " + (max_len - $(this).val().length));

    if (max_len - $(this).val().length <= 100) {
      label.css('opacity', '1');
    }
    else if (hide) {
      label.css('opacity', '0');
    }
  });

  $('textarea.limited_length').focusout(function(){
    $(this).val($(this).val().trim())
  })
})

$(function() {
  $('textarea.limited_length').keyup();
})
