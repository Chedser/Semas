
$( document ).ready(function() {

	$("#auth_form").on("submit", function(event){
		event.preventDefault();
			const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
			let login = $("#login").val().trim();
			let pass = $("#pass").val().trim();

			if(login === "" || pass === ""){
				alert("Пусто");
			return;

		}

		$("input[type='submit']").first().attr("disabled", "disabled");

		let dataToSend = {
					login: login,
					pass: pass};

	$.ajax({
				url: '/api/suauth',             // указываем URL и
				dataType : "json",                     // тип загружаемых данных
				data: dataToSend,                // Данные для отправки
				type: "POST",
				headers: {'X-CSRFToken': csrftoken},
				success: function (data, textStatus) {
                     if (data.message == 0){
                        alert("Неверный пользователь или пароль");
                        $("input[type='submit']").first().removeAttr("disabled");
                     }else{
                      	let date = new Date(Date.now() + 1000e3);
								date = date.toUTCString();
								setCookie("su", date, {"expires":date})
                      window.location.replace("/admin");
                      }

				},
				fail: function (data, textStatus) { // вешаем свой обработчик на функцию success
						alert("Неизвестная ошибка");
						$("input[type='submit']").first().removeAttr("disabled");
					}
			});

	})
});

