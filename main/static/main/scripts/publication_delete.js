$(function(){
  $('button.publication_delete').click(function(){
    if (confirm('Вы действительно хотите удалить публикацию? Это действие нельзя отменить')){
      document.location.href = $(this).attr('href');
    }
    else {}
  })
})
