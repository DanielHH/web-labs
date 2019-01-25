window.onload = function(){
  // Get the element with id="defaultOpen" and click on it
  document.getElementById("defaultOpen").click();
}

function openPage(pageName, elmnt, color) {
  var i, tabcontent, tablinks;

  tabcontent = document.getElementsByClassName("tabcontent");
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
    tablinks[i].style.backgroundColor = "";
  }

  document.getElementById(pageName).style.display = "block";
  elmnt.style.backgroundColor = color;
}
