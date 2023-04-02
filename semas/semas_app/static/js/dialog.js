function scrollTop(){
	$("#dialog_messages").scrollTop($("#dialog_messages").prop('scrollHeight'));
	$("body").scrollTop($("body").prop('scrollHeight'));
}

function openDialog(id){
	window.location.replace("dialog/" + id);
}

function sendMessage(btn, user_id){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	let message_dialog = $("#message_dialog").val().trim();
    var empty_pattern = /^\s+$/g;

	if(message_dialog === "" || message_dialog.match(empty_pattern)){
		alert("Заполните поле");
		btn.removeAttribute('disabled');
		return;}
	btn.setAttribute('disabled','disabled');

    let dataToSend = {
					receiver_id: user_id,
					message: message_dialog
					};

	$.ajax({
		url: 'api/dialog_send_outer',
		type: 'POST',
		headers: {'X-CSRFToken': csrftoken},
		data: dataToSend,
		success: function(data, textStatus){
			if(data.message == 0){
				alert("Сообщение отправлено");
				window.location.reload();
			}else{
				btn.removeAttribute('disabled');
			}
		},
		fail: function (data, textStatus) {
						alert("Неизвестная ошибка");
						$("#forum_create_btn").removeAttr("disabled");
						btn.removeAttribute('disabled');

	    }

});

}

function SendMessageInner(btn){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	let message_dialog = $("#message_dialog").val().trim();
	let message_dialog_hidden_val = +$("#message_dialog_hidden").val();
    var empty_pattern = /^\s+$/g;

	if(message_dialog === "" || message_dialog.match(empty_pattern)){
		$(btn).removeAttr("disabled");
		return;}
	$(btn).attr("disabled", "disabled");

    let dataToSend = {
					dialog_id: message_dialog_hidden_val,
					message: message_dialog
					};

	$.ajax({
		url: '../api/dialog_send_inner',
		type: 'POST',
		headers: {'X-CSRFToken': csrftoken},
		data: dataToSend,
		success: function(data, textStatus){
			if(data.message == 0){
				window.location.reload();
			}else{
				$(btn).removeAttr("disabled");
			}
		},
		fail: function (data, textStatus) {
						alert("Неизвестная ошибка");
						$("#forum_create_btn").removeAttr("disabled");
						$(btn).removeAttr("disabled");

	    }

});

}

$( document ).ready(function() {

  $("#dialog_inner_btn").on('click', function(){
        SendMessageInner(this);
  });

  $('#message_dialog').on('keydown', function(e) {
  if (e.which === 13) {
    SendMessageInner($("#dialog_inner_btn"));
  }
    });

});





