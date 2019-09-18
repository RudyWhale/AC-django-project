$(function(){
  $('button.load_more_btn').click(function(){
    var url = $(this).attr('data-url');
    var shown = $('div.content_item_artwork').length;

    $.get(url, {from_tstamp: $(this).attr('data-timestamp'), shown: shown},
      function(result){
        content = result.content;
        hide_btn = result.hide_btn;

        if (content){
          $('div.load_more').before(content);

          if (hide_btn){
            $('button.load_more_btn').remove();
          }
        }
        else {
          $('button.load_more_btn').remove();
        }
      })
  });
})
