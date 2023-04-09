function SetPageLike(btn,user_id_){
		const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
		$(btn).attr("disabled", "disabled");

		let dataToSend = {
					user_id:user_id_
					};

		$.ajax({
				url: 'api/set_page_like',
				data: dataToSend,
				type: "POST",
				headers: {'X-CSRFToken': csrftoken},
				success: function (data, textStatus) {
                    if (data.message != -1){
                        if (data.message == 0){
                            $("#page_likes_count_span").html("");
                        }else{
                            $("#page_likes_count_span").html(data.message);
                        }
                        $(btn).removeAttr("disabled");

                    }
				},
				fail: function (data, textStatus) {
						$(btn).removeAttr("disabled");
					}
			});
}

function SetWallMessageLike(btn,message_id_){
		const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
		$(btn).attr("disabled", "disabled");

		let dataToSend = {
					message_id:message_id_
					};

		$.ajax({
				url: '/user/api/set_wall_message_like',
				data: dataToSend,
				type: "POST",
				headers: {'X-CSRFToken': csrftoken},
				success: function (data, textStatus) {
                    if (data.message != -1){
                        if (data.message == 0){
                            $("#wall_message_likes_count_span" + message_id_).html("");
                        }else{
                            $("#wall_message_likes_count_span" + message_id_).html(data.message);
                        }
                        $(btn).removeAttr("disabled");

                    }
				},
				fail: function (data, textStatus) {
						$(btn).removeAttr("disabled");
					}
			});
}

function SetForumMessageLike(btn,message_id_){
		const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
		$(btn).attr("disabled", "disabled");

		let dataToSend = {
					message_id:message_id_
					};

		$.ajax({
				url: '../api/set_forum_message_like',
				data: dataToSend,
				type: "POST",
				headers: {'X-CSRFToken': csrftoken},
				success: function (data, textStatus) {
                    if (data.message != -1){
                        if (data.message == 0){
                            $("#forum_message_likes_count_span" + message_id_).html("");
                        }else{
                            $("#forum_message_likes_count_span" + message_id_).html(data.message);
                        }
                        $(btn).removeAttr("disabled");

                    }
				},
				fail: function (data, textStatus) {
						$(btn).removeAttr("disabled");
					}
			});
}

function SetForumMainMessageLike(btn,forum_id_){
		const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
		$(btn).attr("disabled", "disabled");

		let dataToSend = {
					forum_id:forum_id_
					};

		$.ajax({
				url: '../api/set_forum_main_message_like',
				data: dataToSend,
				type: "POST",
				headers: {'X-CSRFToken': csrftoken},
				success: function (data, textStatus) {
                    if (data.message != -1){
                        if (data.message == 0){
                            $("#forum_main_message_likes_count_span").html("");
                        }else{
                            $("#forum_main_message_likes_count_span").html(data.message);
                        }
                        $(btn).removeAttr("disabled");

                    }
				},
				fail: function (data, textStatus) {
						$(btn).removeAttr("disabled");
					}
			});
}