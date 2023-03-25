
function openTab(tabName, tabClass) {
  var i;
  var x = document.getElementsByClassName(tabClass);
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  document.getElementById(tabName).style.display = "block";
}

function expand(obj, rows){
	obj.rows = rows;
}

function getRadioValue(radios){
	let val = 2;
	for (let radio of radios) {
		if (radio.checked) {
			val = radio.value;
			break;
		}
	}
	
	return val;
	
}