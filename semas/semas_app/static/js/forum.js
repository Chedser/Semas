
function forum_create(){
	const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	let forum_topic = $("#forum_topic").val().trim();
	let forum_msg = $("#forum_msg").val().trim();
	
	var empty_pattern = /^\s+$/g;
	if(forum_topic === "" || forum_forum_msg === "" ||
	    forum_topic.match(empty_pattern) ||
		forum_msg.match(empty_pattern)){
		alert("Заполните поля");
		$("#forum_create_btn").removeAttr("disabled");
		return;}
	$("#forum_create_btn").attr("disabled", "disabled");
	
	let dataToSend = {
					topic: forum_topic,
					message:forum_msg
					};
	
	
	$.ajax({
		url: 'api/forum_create',
		type: 'POST',
		headers: {'X-CSRFToken': csrftoken},
		data: dataToSend,
		success: function(data, textStatus){
			if(data.message == 0){
				window.location.reload();
			}else{
				alert("Такое название форума уже существует");
				$("#forum_create_btn").removeAttr("disabled");
			}
		
		},
		fail: function (data, textStatus) {
						alert("Неизвестная ошибка");
						$("#forum_create_btn").removeAttr("disabled");
					}
		
	});
}

function forum_send_message(_id){
	const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	let forum_msg = $("#forum_msg").val().trim();
	
	var empty_pattern = /^\s+$/g;
	if(forum_msg.match(empty_pattern)){ 
		alert("Заполните поле");
		$("#forum_send_message_btn").removeAttr("disabled");
		return;}
	$("#forum_send_message_btn").attr("disabled", "disabled");
	
	let dataToSend = {
					id:_id,
					message:forum_msg
					};
	
	
	$.ajax({
		url: '../api/forum_send_message',
		type: 'POST',
		headers: {'X-CSRFToken': csrftoken},
		data: dataToSend,
		success: function(data, textStatus){
			if(data.message == 0){
				window.location.reload();
			}else{
				alert("Неизвестная ошибка");
				$("#forum_send_message_btn").removeAttr("disabled");
			}
		
		},
		fail: function (data, textStatus) {
						alert("Неизвестная ошибка");
						$("#forum_send_message_btn").removeAttr("disabled");
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

function DeleteForumMessage(span,message_id_, sender_id_){
		if($(span).attr("disabled")) {return;}
		const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
		$(span).attr("disabled", "disabled");

		let dataToSend = {
					message_id:message_id_,
					sender_id: sender_id_
					};

		$.ajax({
				url: '../api/forum_delete_message',
				data: dataToSend,
				type: "POST",
				headers: {'X-CSRFToken': csrftoken},
				success: function (data, textStatus) {
				if (data.message == 0){
								$("#forum_message"+message_id_).css("color","grey");
								$("#forum_message"+message_id_).html("Сообщение удалено");
								$(span).html("");
					}
				},
				fail: function (data, textStatus) {
						$(span).removeAttr("disabled");
					}
			});

}