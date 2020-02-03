function comment_delete(btn){
  if (confirm('Вы действительно хотите удалить комментарий? Это действие нельзя оменить')){
    var url = btn.attr('data-url');
    var comment = btn.parent().parent();
    $.get(
      url, {},
      function(response){
        comment.remove();
      }
    ).fail(function(response){ alert("При удалении комментария произошла ошибка"); });
  }
};


function comment_send(btn){
  var publpk = btn.attr('data-pk');
  var url = btn.attr('data-url');
  var text = $('.comment_form>textarea').val();

  if (text.trim()){
    $.get(url, {publication_pk: publpk, text: text},
      function(response){
        $('#comment_form').after(response);

        $('div.comment_container').hover(
          function() { on_comment_hover_in( $(this).children('p.comment_datetime').children('button.comment_btn')); },
          function() { on_comment_hover_out( $(this).children('p.comment_datetime').children('button.comment_btn')); }
        );

        $('.comment_form>textarea').val("");
        $('.comment_form>textarea').keyup();
        $('.no_comments_label').remove();
      }
    ).fail(function(){ alert("Произошла ошибка"); });
  }
};


function reply_send(btn) {
  var comment_pk = btn.attr('data-pk');
  var url = btn.attr('data-url');
  var txtarea = btn.siblings('textarea');
  var text = txtarea.val();
  var form = btn.parent();
  var replies_container = btn.parent().siblings('div.comment_replies');

  if (text.trim()){
    $.get(url, {comment_pk: comment_pk, text: text},
      function(response){
        replies_container.append(response);

        $('div.comment_replies>div.comment_container').hover(
          function() { on_comment_hover_in( $(this).children('p.comment_datetime').children('button.comment_btn')); },
          function() { on_comment_hover_out( $(this).children('p.comment_datetime').children('button.comment_btn')); }
        );

        txtarea.val("").keyup();
        form.slideUp(300);
      }
    ).fail(function(){ alert("Произошла ошибка"); });
  }
}


function like_send(btn){
  var publpk = btn.attr('data-pk');
  $.get('../action/like', {publication_pk: publpk},
    function(response){
      $('.publication_likes_count').text(response.count);
      btn.text(response.label);
    },
    'json'
  ).fail(function(){ alert("Произошла ошибка"); });
};


function submit_send(btn){
  var profilepk = btn.attr('data-pk');
  $.get('../action/subscribe', {profile_pk: profilepk},
    function(response){
      $('#subs_count_' + profilepk).text(response.count);
      var btnselector = '#subs_btn_' + profilepk;
      $(btnselector).text(response.label);
    }
  ).fail(function(){ alert('Произошла ошибка'); });
};


function not_auth_alert(){
  alert('Войдите на сайт для того, чтобы иметь возможность отмечать понравившиеся работы, оставлять комментарии и подписываться на любимых художников');
};


function self_sub_alert(){ alert('Вы не можете подписаться на собственный аккаунт'); }
