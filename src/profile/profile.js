window.onload = function(){
  // Get the element with id="defaultOpen" and click on it
  document.getElementById("defaultOpen").click();
}

function openPage(pageName, elmnt, color) {
  var colors = ["#81A4CD", "#3E7CB1", "#054A91"];
  var i, tabcontent, tablinks;

  tabcontent = document.getElementsByClassName("tabcontent");
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
    tablinks[i].style.backgroundColor = colors[i];
  }

  document.getElementById(pageName).style.display = "block";
  //elmnt.style.backgroundColor = color;
}
