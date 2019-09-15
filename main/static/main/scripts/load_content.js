$(function(){
  $('button.load_more_btn').click(function(){
    var url = $(this).attr('data-url');
    var shown = $('div.content_item_artwork').length;

    $.get(url, {from_tstamp: $(this).attr('data-timestamp'), shown: shown},
      function(result){
        if (result){
          $('div.load_more').before(result);
        }
        else {
          $('button.load_more_btn').remove();
        }
      })
  });
})
