
function auth(){
	
	$("#auth_form").on("submit", function(event){
		event.preventDefault();
			let login = $("#login").val().trim();
			let pass = $("#pass").val().trim();
			const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
			
			if(login== "" || pass == ""){
				alert("Пусто");
			return;
		
		}
		
		$("input[type='submit']").first().attr("disabled", "disabled");
		
		let dataToSend = {
					login: login,
					pass: pass
					};
				
	$.ajax({
				url: 'api/auth',
				data: dataToSend,
				type: "POST",
				headers: {'X-CSRFToken': csrftoken},
				success: function (data, textStatus) { 
				switch (data.message){
						case 0:
						window.location.replace("/user/" + data.id); break;
						case 1: alert("Неверный ввод"); break;
						case 2: alert("Неверный пользователь или пароль"); break;
						case 5: alert("Пользователь заблокирован"); break;
						
					}
				$("input[type='submit']").first().removeAttr("disabled");
				},
				fail: function (data, textStatus) { // вешаем свой обработчик на функцию success
						alert("Неизвестная ошибка");
						$("input[type='submit']").first().removeAttr("disabled");
					}
			});

	})
}

