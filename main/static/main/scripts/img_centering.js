function onimageload(img){
  $(img).css('left', function(){ return ($(this).parent().width() - $(this).width()) / 2; });
  $(img).css('opacity', '1');
}

$(function(){
  $(window).resize(function(){
    $('img.center').css('left', function(){ return ($(this).parent().width() - $(this).width()) / 2; });
  });
})
