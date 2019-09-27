function set_artwork(img) {
  var container = $(img).parent();

  if ($(img).width() > container.width()){
    $(img).css({
      'height': function() { return (container.width() / $(img).width()) * $(img).height(); },
      'top': function() { return (container.height() - $(this).height()) / 2; },
      'left': 0
    });
  }
  else {
    $(img).css({
      'left': function(){ return (container.width() - $(this).width()) / 2; },
      'top': 0
    })
  }
}

function on_content_image_load(img){
  $(img).css('left', function(){ return ($(this).parent().width() - $(this).width()) / 2; });
  $(img).css('opacity', '1');
}

function on_artwork_load(img){
  set_artwork(img);
  $(img).css('opacity', '1');
}

function on_avatar_load(img){
  var container = $(img).parent().parent();

  if ($(img).width() > $(img).height()){
    $(img).css('left', function(){ return (container.width() - $(this).width()) / 2; });
  }
  else {
    $(img).css({
      'height': function(){ return (container.width() / $(this).width()) * $(this).height(); },
      'top': function(){ return (container.height() - $(this).height()) / 2; }
    });
  }
}

$(function(){
  $(window).resize(function(){
    $('img.center').each(function(index) {
      var container = $(this).parent();

      if ($(this).height() < container.height() && $(this).width() < container.width()){
        // Grow image
        $(this).css('height', container.height());
        set_artwork($(this));
      }
      else {
        // Reduce and center image
        set_artwork($(this));
      }
    });

    $('img.hor_center').each(function(index) {
      $(this).css('left', function(){ return ($(this).parent().width() - $(this).width()) / 2; });
    })
  });
})
