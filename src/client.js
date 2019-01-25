displayView = function(){

};
window.onload = function(){
  if (localStorage.getItem("user_token") != "") {
      var profile_view = document.getElementById("profile_view");
      if (profile_view != null) {
          document.body.innerHTML = profile_view.innerHTML;
          document.getElementById("defaultOpen").click();
      }
  } else {
    var welcome_view = document.getElementById("welcome_view");
    if (welcome_view != null) {
        document.body.innerHTML = welcome_view.innerHTML;
    }
  }

  displayView();
}

function checkLength(password) {
    if (password.value.length < 8) {
      password.setCustomValidity("password must be at least 8 characters long");
    } else {
      password.setCustomValidity("");
  }
}

function isMatching(password, repeat_password) {
    if (password.value != repeat_password.value) {
      repeat_password.setCustomValidity("passwords must match");
    } else {
      repeat_password.setCustomValidity("");
  }
}

function clearValidation(element){
  element.setCustomValidity("");
}

function customFormSubmit(){
  var form = document.getElementById("signup_form");
  var jsonObj = getFormData(form);
  var message = serverstub.signUp(jsonObj);
  var email = document.getElementById("email");

  if (message.success == false) {
    email.setCustomValidity(message.message); // Error doesn't show initially why?
    return false;
  } else {
    document.body.innerHTML = document.getElementById("profile_view").innerHTML;
  }
}

function signIn(){
  var form = document.getElementById("login_form");
  var jsonObj = getFormData(form);
  var response = serverstub.signIn(jsonObj.email_login, jsonObj.password);
  console.log(response);

  if (!response.success){
    document.getElementById("login_error").innerHTML = response.message;
    return false;
  } else {
    localStorage.setItem("user_token", response.data);
    document.body.innerHTML = document.getElementById("profile_view").innerHTML;
  }
}

function getFormData(form){
  var fd = new FormData(form);
  var jsonObj = {};
  for (var [key, value] of fd.entries()) {
    jsonObj[key] = value;
  }

  return jsonObj;
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

function changePassword() {
  var form = document.getElementById("change_psw_form");
  var jsonObj = getFormData(form);
  var response = serverstub.changePassword(localStorage.getItem("user_token"), jsonObj.old_password, jsonObj.new_password);
  var statusText = document.getElementById("change_psw_status");
  statusText.innerHTML = response.message;
  if (response.success) {
    var elements = document.getElementsByTagName("input");
    for (var i=0; i < elements.length; i++) {
      if (elements[i].type == "password") {
        elements[i].value = "";
      }
    }
  }
  return false;
}
