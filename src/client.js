displayView = function(){

};
window.onload = function(){
  if (localStorage.getItem("user_token") != "") {
      var profile_view = document.getElementById("profile_view");
      document.body.innerHTML = profile_view.innerHTML;
      document.getElementById("defaultOpen").click();
      fill_person_info();
      getPosts();
  } else {
    var welcome_view = document.getElementById("welcome_view");
    if (welcome_view != null) {
        document.body.innerHTML = welcome_view.innerHTML;
    }
  }

  displayView();
}

function fill_person_info(email="") {
  if (email =="") {
      var response = serverstub.getUserDataByToken(localStorage.getItem("user_token"));
  } else {
      var response = serverstub.getUserDataByEmail(localStorage.getItem("user_token"),email);
  }
  if (response.success) {
    for (key in response.data) {
      if (email=="") {
        document.getElementById(key).innerHTML += response.data[key];
      } else {
        document.getElementById("b_" + key).innerHTML += response.data[key];
      }
    }
  } else {
    return response.message;
  }

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

function signUp(){
  var form = document.getElementById("signup_form");
  var jsonObj = getFormData(form);
  var message = serverstub.signUp(jsonObj);
  var email = document.getElementById("email");

  if (message.success == false) {
    email.setCustomValidity(message.message); // Error doesn't show initially why?
    return false;
  } else {
    signIn(jsonObj.email, jsonObj.password);
    return true;
  }
}

function signIn(email = "", password = ""){
  if (email == "") {
    var form = document.getElementById("login_form");
    var jsonObj = getFormData(form);
    var response = serverstub.signIn(jsonObj.email_login, jsonObj.password);
  } else {
    var response = serverstub.signIn(email, password);
  }

  if (!response.success){
    document.getElementById("login_error").innerHTML = response.message;
    return false;
  } else {
    localStorage.setItem("user_token", response.data);
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

  document.getElementById(pageName).style.display = "flex";
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


function postMessage() {
  var form = document.getElementById("post_form");
  var message = getFormData(form);
  var response = serverstub.postMessage(localStorage.getItem("user_token"), message.message, null);
  if (response.success) {
      getPosts();
      form.reset();
  }
  return false;
}

function getPosts() {
  document.getElementById("feed").innerHTML = "";
  var response = serverstub.getUserMessagesByToken(localStorage.getItem("user_token"));
  var feed = document.getElementById("feed")
  for (i = 0; i < response.data.length; i++) {
    var node = document.createElement("div");
    var textnode = document.createTextNode(response.data[i].content);
    node.appendChild(textnode);
    feed.appendChild(node);
  }
}

function searchUser() {
  var form = document.getElementById("user_search_form");
  var formData = getFormData(form);
  var response = fill_person_info(formData.userEmail);
  if(response != null) {
    var inputField = document.getElementById("search_user_email_field");
    inputField.setCustomValidity(response);
  }
  return false;
}
