function on_comment_hover_in(btn) { btn.find('button.comment_btn').css('opacity', 1); };
function on_comment_hover_out(btn) { btn.find('button.comment_btn').css('opacity', 0); };

function reply_form_toggle(btn) {
  var form = btn.parent().siblings('div.reply_form');
  $(form).slideToggle(100, function() { $(this).children('textarea').focus(); });
};

$(function(){
  $('div.comment_container').hover(
    function() { on_comment_hover_in($(this)); },
    function() { on_comment_hover_out($(this)); }
  );
});
