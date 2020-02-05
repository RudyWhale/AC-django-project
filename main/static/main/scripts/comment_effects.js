function show_comment_btns(btn) { $(btn).children('p.comment_datetime').children('button.comment_btn').css('opacity', 1); };
function hide_comment_btns(btn) { $(btn).children('p.comment_datetime').children('button.comment_btn').css('opacity', 0); };

function send_on_enter(textarea) {
  $(textarea).keydown(function(event){
      if (event.which == 13){
        $(textarea).siblings('button').click();
        return false;
      }
    }
  );
};

function dont_send_on_enter(textarea) {
  $(textarea).off('keydown');
};

function reply_form_toggle(btn) {
  var form = btn.parent().siblings('div.reply_form');
  $(form).slideToggle(100, function() { $(this).children('textarea').focus(); });
};
