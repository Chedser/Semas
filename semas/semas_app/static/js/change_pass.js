
function reg(){
	
	$("#reg_form").on("submit", function(event){
		event.preventDefault();
			let login = $("#login_reg").val().trim();
			let nick = $("#nick_reg").val().trim();
			let sex = getRadioValue($('input[type="radio"]'));
			let pass = $("#pass_reg").val().trim();
			let pass_repeat = $("#pass_repeat_reg").val().trim();
			const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
			
			
			if(login == "" || 
				pass == "" ||
				nick == "" ||
				pass_repeat_reg == ""){
				alert("Пусто");
				return;}
		
		if(pass != pass_repeat){
			alert("Пароли не совпадают");
			return;
		}
		
		$("#reg_btn").attr("disabled", "disabled");
		
		let dataToSend = {
					login: login,
					nick:nick,
					sex: sex,
					pass: pass};
				
	$.ajax({
				url: 'api/reg',             // указываем URL и
				data: dataToSend,                // Данные для отправки
				type: "POST",
				headers: {'X-CSRFToken': csrftoken},
				success: function (data, textStatus) { 
				switch (data.message){
						case 0:
								alert(nick + ", Вы зарегистрированы! Теперь авторизуйтесь");
								window.location.reload();break;
						case 1: alert("Пользователь существует"); break;
						case 2: alert("Неверный ввод"); break;
						case 3: alert("Пользователь существует"); break;
						case 4: alert("Неизвестная ошибка"); break;
						
					}
				$("#reg_btn").first().removeAttr("disabled");
				},
				fail: function (data, textStatus) { // вешаем свой обработчик на функцию success
						alert("Неизвестная ошибка");
						$("#reg_btn").first().removeAttr("disabled");
					}
			});

	})
}

$(document).ready(function(){
 auth();
 reg();
});


