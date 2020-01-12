$(function(){
  $('.logout_btn').click(function(){
    if (confirm('Вы действительно хотите выйти из своего аккаунта?')){
      var url = $(this).attr('data-url');
      $.get(url, {}, function(){});
    }
    else {
      return false;
    }
  })
})
