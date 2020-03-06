// Scroll page down to comments section and focus on comments form
function focus_comments(){
  $('div.artwork_desc_text').scrollTop($('div.artwork_desc_text')[0].scrollHeight - $('div#comments')[0].scrollHeight);
  $('div#comment_form>textarea').focus();
}
