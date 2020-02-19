// Centers image horizontally
function horisontal_center(img){
  var container = $(img).parent();

  $(img).css({
    'height': container.height(),
    'left': function(){ return (container.width() - $(this).width()) / 2; },
    'top': 0
  })
}

// Moves artwork image to the center of given space
function set_artwork(img) {
  var container = $(img).parent();

  if ($(img).width() > container.width()){
    // Reduce image
    $(img).css({
      'height': function() { return (container.width() / $(img).width()) * $(img).height(); },
      'top': function() { return (container.height() - $(this).height()) / 2; },
      'left': 0
    });
  }
  else if ($(img).height() < container.height() && $(img).width() < container.width()){
    // Grow image
    $(img).css('height', container.height());
    set_artwork($(this));
  }
  else {
    horisontal_center(img);
  }
}

// Hides image loading label and shows the image
function display_image(img){
  $(img).siblings('p.image_loading_label').css('opacity', '0');
  $(img).css('opacity', '1');
}

function on_artwork_load(img){
  set_artwork(img);
  display_image(img);
}

function on_content_image_load(img){
  horisontal_center(img);
  display_image(img);
}

function on_avatar_load(img){
  display_image(img);
}

$(function(){
  $(window).resize(function(){
    $('img.center').each(function(index) {
      var img = $(this);
      var container = img.parent();

      if (img.height() < container.height() && img.width() < container.width()){
        // Grow image
        img.css('height', container.height());
        set_artwork(img);
      }
      else {
        // Reduce and center image
        set_artwork(img);
      }
    });

    horisontal_center($('img.hor_center'));
  });
});
