
function SendWallMessage(btn){
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        let wall_msg = $("#wall_msg_inpt").val().trim();
		let wall_msg_hidden_val = +$("#wall_msg_hidden").val()

		if(wall_msg == ""){return;}
		var empty_pattern = /^\s+$/g;
		if(wall_msg.match(empty_pattern)){ return;}
		$(btn).attr("disabled", "disabled");

		let dataToSend = {
					message:wall_msg,
					receiver_id: wall_msg_hidden_val
					};

		$.ajax({
				url: 'api/send_wall_message',
				data: dataToSend,
				type: "POST",
				headers: {'X-CSRFToken': csrftoken},
				success: function (data, textStatus) {
				switch (data.message){
						case 0:
								window.location.reload();break;
						case 1: alert("Неизвестная ошибка"); break;

					}
				},
				fail: function (data, textStatus) {
						alert("Неизвестная ошибка");
						$(btn).removeAttr("disabled");
					}
			});
}

function ShowDeleteMsgSpan(message_id){
    if($('#delete_msg_span'+message_id) == null) {return;}
    $('#delete_msg_span'+message_id).css('display','inline-block');
}

function HideDeleteMsgSpan(message_id){
    if($('#delete_msg_span'+message_id) == null) {return;}
    $('#delete_msg_span'+message_id).css('display','none');
}

function DeleteWallMessage(span,message_id_, user_id_, sender_id_){
		if($(span).attr("disabled")) {return;}
		const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
		$(span).attr("disabled", "disabled");

		let dataToSend = {
					message_id:message_id_,
					user_id: user_id_,
					sender_id: sender_id_
					};

		$.ajax({
				url: 'api/delete_wall_message',
				data: dataToSend,
				type: "POST",
				headers: {'X-CSRFToken': csrftoken},
				type: "POST",
				success: function (data, textStatus) {
				if(data.message == 0){
								$("#wall_message"+message_id_).css("color","grey");
								$("#wall_message"+message_id_).html("Сообщение удалено");
								$(span).html("");
					}
				},
				fail: function (data, textStatus) {
						alert("Неизвестная ошибка");
						$(span).removeAttr("disabled");
					}
			});

}

$( document ).ready(function() {

  $("#wall_msg_btn").on('click', function(){
        SendWallMessage(this);
  });

  $('#wall_msg_inpt').on('keydown', function(e) {
  if (e.which === 13) {
    SendWallMessage($("wall_msg_btn"));
  }
})
});
