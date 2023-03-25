const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

var change_ava_form = document.getElementById("change_ava_form"); // Форма отправки авы
var change_ava_button = document.getElementById("change_ava_button"); // Кнопка, на которую нажимают, когда отправляют аву

var ava_file = document.getElementById("ava_file").files[0]; // Сам файл  
var ava_preview = document.getElementById("ava_preview"); // Превью авы
var ctx_canvas = ava_preview.getContext('2d');
var MAX_FILE_SIZE = document.getElementById("MAX_FILE_SIZE");  // Максимальный размер  файла

var success_ava_loading_container = document.getElementById("success_ava_loading_container"); // Появляется если аву отправили
var progressbar = document.getElementById("progressbar"); // Прогрессбар
var progressbar_container = document.getElementById("progressbar_container"); // Прогрессбар-контэйнер
var errors_ava_loading_div = document.getElementById("errors_ava_loading_div"); // Див ошибок     

var errors_txt = "";

var load_ava_flag = false; 


function choose_file(ava){

var ava_file = ava.files[0]; // Сам файл  
var accept = ["image/jpeg","image/png"]; // Список поддерживаемых файлов

   if(accept.indexOf(ava_file.type) == -1){
       errors_txt += "Неверный формат<br />";
    }else if(ava_file.size > 3000000){
      errors_txt += "Размер авы должен быть <= 3мБ<br>";
    }

        if(errors_txt === ""){
        ava_preview.style.display = "block"; // Показываем канву
         var image_obj = new Image();    
        var imageUrl = URL.createObjectURL(ava_file);    
        image_obj.src = imageUrl;
        image_obj.weight = 100;
        image_obj.height = 100;   
        load_ava_flag = true;
        change_ava_button.style.display = "block";

        image_obj.onload = function(){
        URL.revokeObjectURL(imageUrl);	
        ctx_canvas.drawImage(image_obj, 0, 0, 100, 100);
        }
        
    } else{
            errors_ava_loading_div.innerHTML = errors_txt;
    }

}


function upload(ava_file){ 

        var formData = new FormData();
        formData.append('MAX_FILE_SIZE', MAX_FILE_SIZE.value);
        formData.append('avatar',  ava_file);
        

$.ajax({
    xhr: function() {
        var xhr = new window.XMLHttpRequest();
        // Upload progress
        xhr.upload.addEventListener("progress", function(evt){
            if (evt.lengthComputable) {
                var percentComplete = evt.loaded / evt.total;
                progressbar.style.width = percentComplete + "%";
            }
       }, false);
       // Download progress
       xhr.addEventListener("progress", function(evt){
           if (evt.lengthComputable) {
               var percentComplete = evt.loaded / evt.total;
               progressbar.style.width = percentComplete + "%";
           }
       }, false);
       return xhr;
    },
    type: 'POST',
    url: "api/change_avatar",
    data: formData,
	headers: {'X-CSRFToken': csrftoken},
	cache: false, 
	contentType: false,
	processData: false, 
	dataType : 'json',
    success: function(data){
					if(data.message == 0){
					change_ava_button.style.display = "none"; // Скрываем кнопку Сменить
					//success_ava_loading_container.style.display = "block"; // Показываем кнопку ахуенно 
					ava_preview.style.display = "none"; // Скрываем канву
					progressbar_container.style.display = "none"; // Скрываем прогрессбар
					alert("Успешно!");
					window.location.reload();
					}else{
						window.location.reload();}

    },
	failed:function(data){
		alert("Неизвестная ошибка");
	}

});

}


/* Главная функция */

change_ava_form.onsubmit = function() {
   var ava_file = document.getElementById("ava_file").files[0]; // Сам файл   
    progressbar_container.style.display = "block";
    
    if (ava_file && load_ava_flag) {
      upload(ava_file);
    }
  
    return false;
}