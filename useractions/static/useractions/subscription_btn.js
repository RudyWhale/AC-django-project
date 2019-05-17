$(function(){
  // onclick event listener
  $('.subscribe_btn').click(function(){
    var profilepk = $(this).attr('data-pk');
    $.get('../action/subscribe', {profile_pk: profilepk},
      function(data){
        if (data.error_msg == ''){
          $('#subs_count_' + profilepk).text(data.count);
          var btnselector = '#subs_btn_' + profilepk;
          $(btnselector).text($(btnselector).text() == 'подписаться' ? 'отписаться' : 'подписаться');
        }
        else{
          alert(data.error_msg);
        }
      },
      'json'
    )
  })
})
