$(function(){
  $('.comment_form>button').click(function(){
    var publpk = $(this).attr('data-pk');
    var text = $('.comment_form>textarea').val();
    var username = $(this).attr('data-username');
    if (text.trim()){
      $.get('../action/comment', {publication_pk: publpk, text: text},
        function(message){
          if (message == ''){
            var cmt_author = $('<h6></h6>').text(username + ':');
            var cmt_text = $('<p></p>').text(text);
            var comment = $('<div class="comment_container"></div>').append(cmt_author).append(cmt_text);
            $('.comment_form').after(comment);
            $('.comment_form>textarea').val("");
            $('.no_comments_label').remove();
          }
          else{
            alert(message);
          }
        }
    )}
  })
})
