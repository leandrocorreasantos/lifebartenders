function delete_event(event_id, elem){
  if(window.confirm("Deseja excluir o evento "+event_id+"?")){
    $.ajax({
      url: "/admin/agenda/delete",
      data: {'event_id': event_id},
      type: 'DELETE',
      success: function(resp){
        $(elem).fadeOut(500);
      }
    });
  }
}
