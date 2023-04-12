
function reg(){
	
	$("#change_pass_form").on("submit", function(event){
		event.preventDefault();
			let old_pass = $("#old_pass").val().trim();
			let new_pass = $("#new_pass").val().trim();
			let new_pass_repeat = $("#new_pass_repeat").val().trim();
			const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

			
			if(old_pass == "" ||
				new_pass == "" ||
				new_pass_repeat == ""){
				alert("Пусто");
				return;}
		
		if(new_pass != new_pass_repeat){
			alert("Пароли не совпадают");
			return;
		}

		if(old_pass === new_pass){
		    alert("Старый и новый пароли совпадают");
		    return;
		}
		
		$("#change_pass_btn").attr("disabled", "disabled");


	$.ajax({
				url: '../api/change_pass',
				data: {pass: new_pass},
				type: "POST",
				headers: {'X-CSRFToken': csrftoken},
				success: function (data, textStatus) { 
                    if(data.message == 0){
                        $("#old_pass").val("");
                        $("#new_pass").val("");
                        $("#new_pass_repeat").val("");
                        alert("Пароль успешно изменен");
                    }else{
                        alert("Неизвестная ошибка");
                    }
				$("#change_pass_btn").removeAttr("disabled");
				},
				fail: function (data, textStatus) {
						$("#change_pass_btn").removeAttr("disabled");
					}
			});

	})
}

$(document).ready(function(){
 reg();
});


