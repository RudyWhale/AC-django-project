$(function(){
  var deg = 30;
  var header = $('div.header');

  setInterval(function(){
    deg = (deg + 1) % 360;
    header.css('background-image', 'linear-gradient(' + deg + 'deg, #003967 0%, #126559 100%)');
  }, 100);
})
