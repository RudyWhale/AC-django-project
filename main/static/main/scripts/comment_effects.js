var on_comment_hover_in = function(btn){ btn.find('button.comment_delete').css('opacity', 1); };
var on_comment_hover_out = function(btn){ btn.find('button.comment_delete').css('opacity', 0); };

$(function(){
  $('div.comment_container').hover(
    function() { on_comment_hover_in($(this)); },
    function() { on_comment_hover_out($(this)); });
});
