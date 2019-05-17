$(function(){
  // onclick event listener
  $('.publication_likes_btn').click(function(){
    var publpk = $(this).attr('data-pk');
    $.get('../action/like', {publication_pk: publpk},
      function(data){
        if (data.error_msg == ''){
          $('.publication_likes_count').text(data.count);
          $('.publication_likes_btn').text($('.publication_likes_btn').text() == 'нравится' ? "не нравится" : "нравится");
        }
        else{
          alert(data.error_msg);
        }
      },
      'json'
    )
  })
})
