function BlockUser(obj, user_id_){
	const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

	$.ajax({
				url: 'api/su/block_user',             // указываем URL и
				headers: {'X-CSRFToken': csrftoken},
				data: { user_id: user_id_ },                // Данные для отправки
				type: "POST",
				success: function (data, textStatus) {
				switch (data.message){
					case 0: obj.innerText = "Заблокировать";  break;
					case 1: obj.innerText = "Разблокировать"; break;
				}
				$("#status_tr_" + user_id_).html(data.message);
				},
				
				fail: function (data, textStatus) { // вешаем свой обработчик на функцию success
						alert("Неизвестная ошибка");
					}
			});

}
