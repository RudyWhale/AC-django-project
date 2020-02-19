function set_image_bg(container) {
  var url = $(container).attr('data-bg');
  $(container).css('background-image', 'url(' + url + ')');
}

$(function() {
  $('.image_bg').each(function(index) {
    set_image_bg($(this));
  });
});
