
function sendFriendRequest(btn, userId){
	btn.disabled = "disabled";
	const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	
	$.ajax({
				url: 'api/friend_request',             // указываем URL и
				data: {user_id:userId},                // Данные для отправки
				type: "POST",
				headers: {'X-CSRFToken': csrftoken},
				success: function (data, textStatus) { 
				if (data.message == 0){
						btn.removeAttribute("onclick");
						btn.disabled = "";	
						btn.style.backgroundColor = "yellow";
						btn.value = "Заявка отправлена";
					}else{alert("Неизвестная ошибка");}
				},
				fail: function (data, textStatus) { // вешаем свой обработчик на функцию success
						alert("Неизвестная ошибка");
						btn.disabled = "";
					}
			});
	
}

function cancelFriendRequest(btn, userId, flag = 1){
		btn.disabled = "disabled";
		const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	
	$.ajax({
				url: 'api/cancel_friend_request',             // указываем URL и
				data: {user_id:userId},                 // Данные для отправки
				type: "POST",
				headers: {'X-CSRFToken': csrftoken},
				success: function (data, textStatus) { 
				if (data.message == 0){
						btn.disabled = "";
						btn.removeAttribute("onclick");
						btn.style.backgroundColor = "yellow";
						if(flag == 0){btn.value = "Заявка отменена";
						
						}else{
							$("#accept_friend_request_btn" + userId).css({"display":"none"});
							$("#accept_friend_request_btn" + userId).removeAttr("onclick");
							btn.value = "Запрос отклонен";}
					}else{alert("Неизвестная ошибка");}
				},
				fail: function (data, textStatus) { // вешаем свой обработчик на функцию success
						alert("Неизвестная ошибка");
						btn.disabled = "";
					}
			});
	
}

function acceptFriendRequest(btn, userId){
		btn.disabled = "disabled";
		const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	
	$.ajax({
				url: 'api/accept_friend_request',             // указываем URL и
				data: {user_id:userId},                // Данные для отправки
				headers: {'X-CSRFToken': csrftoken},
				type: "POST",
				success: function (data, textStatus) { 
				
				if (data.message == 0){
						btn.disabled = "";
						btn.removeAttribute("onclick");
						btn.style.backgroundColor = "yellow";
							$("#cancel_friend_request_btn" + userId).css({"display":"none"});
							$("#cancel_friend_request_btn" + userId).removeAttr("onclick");
							btn.value = "Вы друзья";
				}else{alert("Неизвестная ошибка");}
				},
				fail: function (data, textStatus) { // вешаем свой обработчик на функцию success
						alert("Неизвестная ошибка");
						btn.disabled = "";
					}
			});
	
}

function deleteFriend(btn, userId){
		btn.disabled = "disabled";
		const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	
	$.ajax({
				url: 'api/delete_friend',             // указываем URL и
				data: {user_id:userId},                // Данные для отправки
				type: "POST",
				headers: {'X-CSRFToken': csrftoken},
				success: function (data, textStatus) { 
				
				if (data.message == 0){
						btn.disabled = "";
						btn.removeAttribute("onclick");
						btn.style.backgroundColor = "yellow";
						btn.value = "Удален";
				}else{alert("Неизвестная ошибка");}
				},
				fail: function (data, textStatus) { // вешаем свой обработчик на функцию success
						alert("Неизвестная ошибка");
						btn.disabled = "";
					}
			});
	
}

