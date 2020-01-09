function dropdown(btn) {
  $(btn).toggleClass('disabled');
  $('ul.navbar_ul').toggle("fast");
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
