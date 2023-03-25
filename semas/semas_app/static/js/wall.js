
function wall_message(btn,reсeiverId_){
		let wall_msg = $("#wall_msg_inpt").val().trim();
		const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
		if(wall_msg == ""){return;}
		var empty_pattern = /^\s+$/g;
		if(wall_msg.match(empty_pattern)){ return;}
		$(btn).attr("disabled", "disabled");
		
		let dataToSend = {
					message:wall_msg,
					receiver_id: reсeiverId_
					};
		
		$.ajax({
				url: 'api/wall_message',             // указываем URL и
				data: dataToSend,                // Данные для отправки
				type: "POST",
				headers: {'X-CSRFToken': csrftoken},
				type: "POST",
				success: function (data, textStatus) { 
				switch (data.message){
						case 0:
								window.location.reload();break;
						case 1: alert("Неизвестная ошибка"); break;
						
					}
				},
				fail: function (data, textStatus) { // вешаем свой обработчик на функцию success
						alert("Неизвестная ошибка");
						$(btn).removeAttr("disabled");
					}
			});
		
}