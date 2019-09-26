function onimageload(img){
  $(img).css('left', function(){ return ($(this).parent().width() - $(this).width()) / 2; });
  $(img).css('opacity', '1');
}

function onavatarload(img){
  if ($(img).width() > $(img).height()){
    $(img).css('left', function(){ return ($(this).parent().parent().width() - $(this).width()) / 2; });
  }
  else {
    $(img).css('height', function(){ return ($(this).parent().parent().width() / $(this).width()) * $(this).height(); });
    $(img).css('top', function(){ return ($(this).parent().parent().height() - $(this).height()) / 2; });
  }
}

$(function(){
  $(window).resize(function(){
    $('img.center').css('left', function(){ return ($(this).parent().width() - $(this).width()) / 2; });
  });
})
