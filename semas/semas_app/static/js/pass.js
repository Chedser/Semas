
function RestorePass(){
	
	$("#restore_pass_form").on("submit", function(event){
		event.preventDefault();
			let nick_inpt = $("#nick_inpt").val().trim();
			let email_inpt = $("#email_inpt").val().trim();
			let restored_pass_span = $("#restored_pass_span");
			let restored_pass_val = $("#restored_pass_val");
			const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

			restored_pass_span.css("display","none");
			restored_pass_val.html("");

			
			if(nick_inpt == "" ||
				email_inpt == ""){
				alert("Пусто");
				return;}

		$("#restore_pass_btn").attr("disabled", "disabled");

	$.ajax({
				url: 'api/restore_pass',
				data: {nick: nick_inpt,
				        email: email_inpt
				},
				type: "POST",
				headers: {'X-CSRFToken': csrftoken},
				success: function (data, textStatus) { 
                    if(data.message != 1 && data.message != 2){
                        $("#nick_inpt").val("");
                        $("#email_inpt").val("");
                        restored_pass_span.css("display","inline");
			            restored_pass_val.html(data.message);
                    }

                    if(data.message == 1){
                        alert("Неверный ник, email либо пользователь заблокирован");
                    }

                    if(data.message == 2){
                        alert("Неизвестная ошибка");
                    }

				$("#restore_pass_btn").removeAttr("disabled");
				},
				fail: function (data, textStatus) {
						$("#restore_pass_btn").removeAttr("disabled");
					}
			});

	})
}

function CopyPass(){
    	$("#copy_span").on("click", function(event){
            let text = $("#restored_pass_val").html();
            navigator.clipboard.writeText(text)
            .then(() => {
                    alert("Пароль скопирован в буффер обмена");
                    })
                .catch(err => {
                    alert("Неизвестная ошибка");
                });
	    });
}

$(document).ready(function(){
    RestorePass();
    CopyPass();
});


