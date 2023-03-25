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





