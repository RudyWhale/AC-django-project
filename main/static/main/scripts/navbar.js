function notifications(btn) {
  $('div.notifications_list').slideToggle(100);
}

function clear_notifications(btn) {
  var url = $(btn).attr('data-url');
  $.get(url, {}, function() {
    $('div.notifications_list').slideUp(100, function(){
      $('div.notifications_list').html('<div class="notification_empty_label"><p>Нет новых уведомлений</p></div>');
    })
    $('p.user_notifications_count').remove();
  });
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
