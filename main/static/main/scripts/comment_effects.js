$(function(){
  $('div.comment_container').hover(
    function() { $(this).find('button.comment_delete').css('opacity', 1); },
    function() { $(this).find('button.comment_delete').css('opacity', 0); });
})
