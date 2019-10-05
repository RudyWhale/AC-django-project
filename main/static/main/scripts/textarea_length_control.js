$(function() {
  $('textarea.length_control').keyup(function() {
    var max_len = $(this).attr('data-max_len');
    $(this).val($(this).val().substring(0, max_len));
    if (max_len - $(this).val().length <= 100) {
      var label = $('p.comment_length_label');
      label.text("осталось символов: " + (max_len - $(this).val().length));
      label.css('opacity', '1');
    }
    else {
      $('p.comment_length_label').css('opacity', '0');
    }
  });
})
