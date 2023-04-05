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

function FindUserByLink(){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let user_link = $("#user_link_inpt").val().trim();
    if (user_link === ""){return;}

    let user_id_ = +user_link.split("/")[4];

    	$.ajax({
				url: 'api/su/find_user',             // указываем URL и
				headers: {'X-CSRFToken': csrftoken},
				data: { user_id: user_id_ },                // Данные для отправки
				type: "POST",
				success: function (data, textStatus) {
				if(data.message == -1) {alert("Пользователь не найден"); return;}
				let parsed = jQuery.parseJSON(data.message)[0];
				let content = "<tr>" +
				"<td>" + parsed.id + "</td>" +
				"<td>" +
					"<a href=/user/" + parsed.id + " target=_blank>" +
						"<img class=w3-circle src=/static/" + parsed.avatar + " style=height:30px;width:30px/>" + parsed.nick +
					"</a>" +
				"</td>" +
				"<td id=status_tr_" + parsed.id + ">" + parsed.is_blocked + "</td>" +
				"<td></td>";

				let blocked_content = "";

				 if (!parsed.is_blocked){
				    blocked_content = "<td>" +
				                         "<a class=underline onclick=BlockUser(this," + parsed.id + ")>Заблокировать</a>" +
				                       "</td>";
				 }else{
				   blocked_content = "<td>" +
				                         "<a class=underline onclick=BlockUser(this," + parsed.id + ")>Разблокировать</a>" +
				                       "</td>";
				 }

				 content += blocked_content;

				$("#users_table").html(content);

				},

				fail: function (data, textStatus) { // вешаем свой обработчик на функцию success
						alert("Неизвестная ошибка");
					}
			});
	}

	function DeleteForum(obj, forum_id_){
	const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

	$.ajax({
				url: '../api/su/delete_forum',
				headers: {'X-CSRFToken': csrftoken},
				data: { forum_id: forum_id_ },
				type: "POST",
				success: function (data, textStatus) {

				if (data.message == 0){
                    obj.innerText = "";
                    $(obj).attr("disabled", "disabled");
                    $("#status_tr_" + forum_id_).html("Удален");
				}

				},

				fail: function (data, textStatus) {
						alert("Неизвестная ошибка");
					}
			});

}

function FindForumByLink(){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let forum_link = $("#forum_link_inpt").val().trim();
    if (forum_link === ""){return;}

    let forum_id_ = +forum_link.split("/")[4];

    	$.ajax({
				url: '../api/su/find_forum',
				headers: {'X-CSRFToken': csrftoken},
				data: { forum_id: forum_id_ },
				type: "POST",
				success: function (data, textStatus) {
				if(data.message == -1) {alert("Форум не найден"); return;}
				let parsed = jQuery.parseJSON(data.message)[0];
				let content = "<tr>" +
				"<td>" + parsed.id + "</td>" +
				"<td>" +
					"<a href=/forum/" + parsed.id + " target=_blank>" +
						  parsed.topic +
					"</a>" +
				"</td>" +
				"<td id=status_tr_" + parsed.id + "></td>" +
				"<td>" +
				     "<a class=underline onclick=DeleteForum(this," + parsed.id + ")>Удалить</a>" +
				"</td>";

				$("#forums_table").html(content);

				},

				fail: function (data, textStatus) {
						alert("Неизвестная ошибка");
					}
			});
	}

function Exit(){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

	$.ajax({
				url: '/api/su/exit',
				type: "POST",
				headers: {'X-CSRFToken': csrftoken},
				success: function (data, textStatus) {
                    window.location.replace("/su");
				},
				fail: function (data, textStatus) { }
			});

}

