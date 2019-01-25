displayView = function(){

};
window.onload = function(){
  if (localStorage.getItem("user_token") != "") {
      document.body.innerHTML = document.getElementById("profile_view").innerHTML;
  } else {
      document.body.innerHTML = document.getElementById("welcome_view").innerHTML;
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
