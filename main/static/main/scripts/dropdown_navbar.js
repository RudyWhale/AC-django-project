function dropdown(btn) {
  $(btn).toggleClass('disabled');
  $('ul.navbar_ul').slideToggle(100);
}

function notifications(btn) {
  if ($('p.user_notifications_count').length){
    $('div.notifications_list').slideDown(100);
    $('p.user_notifications_count').remove();
    var url = $(btn).attr('data-url');
    $.get(url);
  }
  else {
    $('div.notifications_list').slideUp(100);
    $(btn).addClass('disabled');
    $(btn).attr('onclick', '');
  }
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
