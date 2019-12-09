$(function(){
  $('input.image_inp').change(function(){
    var file = ($(this))[0].files[0];
    var max_size = $(this).attr('data-max_size');

    if (file.size > max_size){
      ($(this))[0].value = '';
      alert('Размер изображения не должен превышать 1Мбайт');
    }
  });
})
