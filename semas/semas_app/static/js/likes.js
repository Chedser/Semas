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