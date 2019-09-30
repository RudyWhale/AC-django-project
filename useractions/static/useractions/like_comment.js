var comment_delete = function(btn){
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

var comment_send = function(btn){
  var publpk = btn.attr('data-pk');
  var text = $('.comment_form>textarea').val();
  var username = btn.attr('data-username');
  if (text.trim()){
    $.get('../action/comment', {publication_pk: publpk, text: text},
      function(response){
        $('.comment_form').after(response);
        $('.comment_form>textarea').val("");
        $('.no_comments_label').remove();
      }
    ).fail(function(){alert("Произошла ошибка");});}
};

var not_auth_alert = function(){
  alert('Войдите на сайт для того, чтобы иметь возможность отмечать понравившиеся работы и оставлять комментарии');
}

var like_send = function(btn){
  var publpk = btn.attr('data-pk');
  $.get('../action/like', {publication_pk: publpk},
    function(response){
      $('.publication_likes_count').text(response);
      $('.publication_likes_btn').text($('.publication_likes_btn').text() == 'нравится' ? "не нравится" : "нравится");
    }
  ).fail(function(){alert("Произошла ошибка");});
}
