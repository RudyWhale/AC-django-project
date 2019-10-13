$(function(){
  var removeErrorsMessage = function(){
    if ($('.form_errors').length && !$('.login_warning').not('.form_errors').length){
      $('.form_errors').remove();
    }
  };

  $('input.inp_name').focusout(function(){
    var text = $(this).val();
    if (text.trim()){
      $('.space_in_username').remove();
      if (text.indexOf(' ') >= 0){
        var message = "Имя профиля не может содержать пробел";
        ($('<p class="login_warning space_in_username"></p>').text(message)).prependTo($('.login_form'));
        $('.inp_name').css('border-bottom', '1px solid red');
      }
      else {
        $('.inp_name').css('border-bottom', '1px solid black');
        removeErrorsMessage();
      }

      $.get(
        './check_nickname',
        {name: text},
        function(message){
          $('.name_exists').remove();
          if (message){
            ($('<p class="login_warning name_exists"></p>').text(message)).prependTo($('.login_form'));
            $('.inp_name').css('border-bottom', '1px solid red');
          }
          else {
            $('.inp_name').css('border-bottom', '1px solid black');
            removeErrorsMessage();
          }
        }
    )}
  });

  $('input.inp_email').focusout(function(){
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    var text = $(this).val();
    if (text) {
      if (!regex.test(text)) {
        if (!$('.invalid_email').length){
          var message = "Пожалуйста, введите корректный email адрес";
          ($('<p class="login_warning invalid_email"></p>').text(message)).prependTo($('.login_form'));
          $('.inp_email').css('border-bottom', '1px solid red');
        }
      }
      else {
        $('.invalid_email').remove();
        $('.inp_email').css('border-bottom', '1px solid black');

        $.get(
          './check_email',
          {email: text},
          function(message){
            $('.email_exists').remove();
            if (message){
              ($('<p class="login_warning email_exists"></p>').text(message)).prependTo($('.login_form'));
              $('.inp_email').css('border-bottom', '1px solid red');
            }
            else {
              $('.inp_email').css('border-bottom', '1px solid black');
              removeErrorsMessage();
            }
          }
        )

        removeErrorsMessage();
      }
    }
  });

  $('input.pass2, input.pass1').focusout(function(){
    var length = $(this).val().length;

    if (length){
      if (length < 6){
        if (!$('.password_too_short').length){
          var message = "Пароль должен быть не короче 6 символов";
          ($('<p class="login_warning password_too_short"></p>').text(message)).prependTo($('.login_form'));
          $(this).css('border-bottom', '1px solid red');
        }
      }
      else {
        $('.password_too_short').remove();
        $(this).css('border-bottom', '1px solid black');
        removeErrorsMessage();
      }

      var pass1 = $('.pass1').val();
      var pass2 = $('.pass2').val();

      if (pass1 && pass2){
        if (pass1 != pass2){
          if (!$('.wrong_pass_repeat').length){
            var message = "Пароли не совпадают";
            ($('<p class="login_warning wrong_pass_repeat"></p>').text(message)).prependTo($('.login_form'));
            $('.pass1').css('border-bottom', '1px solid red');
            $('.pass2').css('border-bottom', '1px solid red');
          }
        }
        else {
          $('.wrong_pass_repeat').remove();
          $('.pass1').css('border-bottom', '1px solid black');
          $('.pass2').css('border-bottom', '1px solid black');
          removeErrorsMessage();
        }
      }
    }
  });

  $('input.avatar_inp').change(function(){
    var file = ($(this))[0].files[0];

    if (file.size > 1048576){
      $(this).value = '';

      if (!$('.too_big_avatar').length){
        var message = "Размер аватара не должен превышать 1Мбайт";
        ($('<p class="login_warning too_big_avatar"></p>').text(message)).prependTo($('.login_form'));
        $(this).css('border-bottom', '1px solid red');
      }
    }
    else{
      $('.too_big_avatar').remove();
      $(this).css('border-bottom', '1px solid black');
      removeErrorsMessage();
    }
  });

  $('form.login_form').submit(function(){
    // Finds empty field if it exists
    var is_clean_field = false;
    $('.login_input>input').each(function(index) {
      if (!$(this).val().trim()) {is_clean_field = true;}
      if (is_clean_field) {return false;}
    });

    if ($('.login_warning').length || is_clean_field){
      if (!$('.form_errors').length){
        var message = "Пожалуйста, корректно заполните все поля формы для регистрации";
        ($('<p class="login_warning form_errors"></p>').text(message)).prependTo($('.login_form'));
      }
      return false;
    }
  });
});
