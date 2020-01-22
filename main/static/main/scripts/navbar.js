function notifications(btn) {
  $('div.notifications_list').slideToggle(100);

  if ($('div.notification_item').length) {
    $('p.user_notifications_count').remove();
    var url = $(btn).attr('data-url');
    $.get(url);
  }
}

function logout(btn){
  if (confirm('Вы действительно хотите выйти из своего аккаунта?')){
    var url = $(btn).attr('data-url');
    $.get(url, {}, function(){ location.reload(); });
  }
}

function dropdown(btn) {
  $(btn).toggleClass('disabled');
  $('ul.navbar_ul').slideToggle(100);
}

$(function(){
  $(window).resize(function(){
    if ($(this).width() > 800){
      $('ul.navbar_ul').show();
      $('div.dropdown_btn').hide();
    }
    else {
      $('ul.navbar_ul').hide();
      $('div.dropdown_btn').show();
    }
  });
})
