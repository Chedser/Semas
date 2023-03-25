function blockUser(obj, user_id_){
	let dataToSend = {
					user_id: user_id_
					};

	let block_tr = document.getElementById("status_tr_" + user_id_);
	
	$.ajax({
				url: 'handlers/block_user',             // указываем URL и
				dataType : "json",                     // тип загружаемых данных
				data: JSON.stringify(dataToSend),                // Данные для отправки
				type: "POST",
				contentType: "application/json",
				success: function (data, textStatus) { 
				switch (data.response){
					case 0: obj.innerText = "Заблокировать";  break;
					case 1: obj.innerText = "Разблокировать"; break;
					default: alert("Неизвестная ошибка");
				}
				block_tr.innerText = data.response;
				},
				
				fail: function (data, textStatus) { // вешаем свой обработчик на функцию success
						alert("Неизвестная ошибка");
					}
			});

}
