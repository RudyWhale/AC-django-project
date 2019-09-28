$(function(){
  $('.comment_form>button').click(function(){
    var publpk = $(this).attr('data-pk');
    var text = $('.comment_form>textarea').val();
    var username = $(this).attr('data-username');
    if (text.trim()){
      $.get('../action/comment', {publication_pk: publpk, text: text},
        function(response){
          $('.comment_form').after(response);
          $('.comment_form>textarea').val("");
          $('.no_comments_label').remove();
        }
    ).fail(function(response){alert(response);})}
  });

  $('button.comment_delete').click(function(){
    if (confirm('Вы действительно хотите удалить комментарий? Это действие нельзя оменить')){
      var url = $(this).attr('data-url');
      var comment = $(this).parent().parent();
      $.get(
        url, {},
        function(response){
          comment.remove();
        }
      ).fail(function(response){ alert("При удалении комментария произошла ошибка"); });
    }
  });
})
