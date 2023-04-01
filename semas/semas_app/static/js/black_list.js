function FindUserByLink(){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let user_link = $("#user_link_inpt").val().trim();
    if (user_link === ""){return;}

    let user_id_ = +user_link.split("/")[4];

    	$.ajax({
				url: 'api/find_user',             // указываем URL и
				headers: {'X-CSRFToken': csrftoken},
				data: { user_id: user_id_ },                // Данные для отправки
				type: "POST",
				success: function (data, textStatus) {
				if(data.message == 1) {alert("Пользователь не найден"); return;}
				if(data.message == 2) {alert("Это ваша страница"); return;}
				let parsed = jQuery.parseJSON(data.message)[0];

				let blocked_content = "";
                let yes_no = "";
				 if (!parsed.is_blocked){
				    blocked_content = "<td>" +
				                         "<a class=underline onclick=BlockUser(this," + parsed.id + ")>Заблокировать</a>" +
				                       "</td>";
				    yes_no = "Нет";
				 }else{
				   blocked_content = "<td>" +
				                         "<a class=underline onclick=BlockUser(this," + parsed.id + ")>Разблокировать</a>" +
				                       "</td>";
				   yes_no = "Да";
				 }

				let content = "<tr>" +
				"<td>" + parsed.id + "</td>" +
				"<td>" +
					"<a href=/user/" + parsed.id + " target=_blank>" +
						"<img class=w3-circle src=/static/" + parsed.avatar + " style=height:30px;width:30px/>" + parsed.nick +
					"</a>" +
				"</td>" +
				"<td id=status_tr_" + parsed.id + ">" + yes_no + "</td>" +
				"<td></td>";



				 content += blocked_content;

				$("#users_table").html(content);

				},

				fail: function (data, textStatus) { // вешаем свой обработчик на функцию success
						alert("Неизвестная ошибка");
					}
			});
	}

function BlockUser(obj, user_id_){
	const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

	$.ajax({
				url: 'api/block_user',             // указываем URL и
				headers: {'X-CSRFToken': csrftoken},
				data: { user_id: user_id_ },                // Данные для отправки
				type: "POST",
				success: function (data, textStatus) {

				let yes_no = "Да";
				switch (data.message){
					case 0: obj.innerText = "Заблокировать";
					yes_no = "Нет";
					break;
					case 1: obj.innerText = "Разблокировать"; break;
				}
				$("#status_tr_" + user_id_).html(yes_no);
				},

				fail: function (data, textStatus) { // вешаем свой обработчик на функцию success
						alert("Неизвестная ошибка");
					}
			});

}