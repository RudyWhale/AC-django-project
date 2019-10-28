// var resize = function(){
//   var elem = $(this);
//   var current = elem.height() + 10;
//   elem.height(0);
//   var real = elem[0].scrollHeight - 10;
//
//   if (real > current){
//     elem.height(real);
//   }
//   else if (real < current){
//     if (real < 40) real = 40;
//     elem.height(real);
//   }
// }
//
// var create = function(elem, text1, text2){
//   var new_elem = $('<textarea class="auto_height article_data" />').val(text1);
//   new_elem.on('input', resize);
//   new_elem.keydown(keyProcess);
//   elem.before(new_elem);
//   new_elem.trigger('input');
//   elem.val(text2);
//   elem.caretToStart();
// }
//
// var keyProcess = function(event){
//   var key = event.which || event.keyCode;
//
//   if (key == 13){
//     var text = $(this).val();
//     lines = text.split('\n');
//     last_line = lines[lines.length - 1];
//     text = text.substring(0, text.lastIndexOf('\n'));
//     if (!last_line.trim()){
//       create($(this), text, '');
//     }
//   }
// }
//
// alert('before');
//
// $(document).bind('webpageReady', function(){
//   alert('happened');
//
//   // Auto height
//   $('textarea.auto_height').on('input', resize);
//
//   // Article text writing processing
//   $('textarea.article_data').keydown(keyProcess);
// });
//
// $(document).trigger('webpageReady');
//
// $(function(){
//   $(document).trigger('webpageReady');
//   alert('ready');
// })

$(function(){
  $('input.image_inp').change(function(){
    var file = ($(this))[0].files[0];
    var max_size = $(this).attr('data-max_size');

    if (file.size > max_size){
      ($(this))[0].value = '';
      alert('Размер изображения не должен превышать 1Мбайт');
    }
  });

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
})
