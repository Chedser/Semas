function showDialog(btn, user_id_){
	
	btn.disabled = "disabled";
		
		let dataToSend = {user_id: user_id_};
	
	$.ajax({
				url: '/handlers/show_dialog',             // указываем URL и
				dataType : "json",                     // тип загружаемых данных
				data: JSON.stringify(dataToSend),                // Данные для отправки
				type: "POST",
				contentType: "application/json",
				success: function (data, textStatus) { 
				if(data.response == 0){
						alert("Неизвестная ошибка");
						
				}else{
					window.location.replace("dialog?id=" + data.response);}
					btn.disabled = "";
				},
				fail: function (data, textStatus) { // вешаем свой обработчик на функцию success
						alert("Неизвестная ошибка");
						btn.disabled = "";
					}
			});
	
}

function openDialog(id){
	window.location.replace("dialog?id=" + id);
}

function sendMessage(btn, user_id){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	let message_dialog = $("#message_dialog").val().trim();
    var empty_pattern = /^\s+$/g;

	if(message === "" || message.match(empty_pattern)){
		alert("Заполните поле");
		btn.removeAttribute('disabled');
		return;}
	btn.setAttribute('disabled');

    let dataToSend = {
					receiver_id: id,
					message: message_dialog
					};


	$.ajax({
		url: 'api/message_send_user_page',
		type: 'POST',
		headers: {'X-CSRFToken': csrftoken},
		data: dataToSend,
		success: function(data, textStatus){
			if(data.message == 0){
				window.location.reload();
			}else{
				alert("Неизвестная ошибка");
				btn.removeAttribute('disabled');
			}

		},
		fail: function (data, textStatus) {
						alert("Неизвестная ошибка");
						$("#forum_create_btn").removeAttr("disabled");
						btn.removeAttribute('disabled');

	});

}





