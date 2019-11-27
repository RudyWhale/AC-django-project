$(function(){
  $('.login_input>input, .login_input>textarea').focusin(function(){
    $(this).parent().parent().css('background-color', '#6bb4bf');
  });

  $('.login_input>input, .login_input>textarea').focusout(function(){
    $(this).parent().parent().css('background-color', 'inherit');
  });

  $(':focus').trigger('focusin');
});
