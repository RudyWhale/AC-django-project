function on_comment_hover_in(btn) { btn.css('opacity', 1); };
function on_comment_hover_out(btn) { btn.css('opacity', 0); };

function reply_form_toggle(btn) {
  var form = btn.parent().siblings('div.reply_form');
  $(form).slideToggle(100, function() { $(this).children('textarea').focus(); });
};

$(function(){
  $('div.comment_container').hover(
    function() { on_comment_hover_in( $(this).children('p.comment_datetime').children('button.comment_btn')); },
    function() { on_comment_hover_out( $(this).children('p.comment_datetime').children('button.comment_btn')); }
  );
});
