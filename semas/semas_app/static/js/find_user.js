function FindUserByNick(btn){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let user_nick = $("#user_nick_inpt").val().trim();
    if (user_nick === ""){return;}

    let empty_pattern = /^\s+$/g;
	if(user_nick.match(empty_pattern)){ return;}
	$(btn).attr("disabled", "disabled");

    	$.ajax({
				url: '../api/find_user_by_nick',
				headers: {'X-CSRFToken': csrftoken},
				data: { nick: user_nick },
				type: "POST",
				success: function (data, textStatus) {
				if(data.message == -1) {
				    alert("Пользователь не найден");
				    $(btn).removeAttr("disabled");
				    return;
				}
				let parsed = jQuery.parseJSON(data.message);
				content = GetUsers(parsed);

				$("#users_container").html(content);
                    $(btn).removeAttr("disabled");
				},

				fail: function (data, textStatus) { // вешаем свой обработчик на функцию success
						$(btn).removeAttr("disabled");
					}
			});
	}

function GetUsers(users){

let content = "";

    users.forEach((item, index, array) => {
      let id = item.id;
      let nick = item.nick;
      let avatar = item.avatar;

      content += '<div class="w3-container w3-card w3-white w3-round w3-margin w3-center" id="users_container">' +
			'<a href = "user/' + id + '" target="_blank">' +
				'<img src="static/' + avatar + '" alt="Аватар"  style="width:50px; height:50px;"' +
				'class="w3-left w3-circle w3-margin-right avatar">' +
			'<h4>' + nick + '</h4>' +
			'</a><br />' +
			'<hr class="w3-clear">' +
		'</div>';

    });
    return content;
}