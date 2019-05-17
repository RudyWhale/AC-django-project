$(function(){
  $.each($('img.center'), function(i, img) {
    img.onload = function(){
      $(this).css('left', function(){ return ($(this).parent().width() - $(this).width()) / 2; });
      $(this).css('opacity', '1');
    };
    if (img.complete) img.load();
  });

  $(window).resize(function(){
    $('img.center').css('left', function(){ return ($(this).parent().width() - $(this).width()) / 2; });
  });
})
