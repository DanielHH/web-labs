displayView = function(){

};
window.onload = function(){
  document.body.innerHTML = document.getElementById("welcome_view").innerHTML;
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

function customFormSubmit(){
  var form = document.getElementById("signup_form");
  var fd = new FormData(form);
  var jsonObj = {};
  for (var [key, value] of fd.entries()) {
    jsonObj[key] = value;
  }
  var message = serverstub.signUp(jsonObj);

  var email = document.getElementById("email");
  if (message.success == false) {
    console.log("message is " + message.success);
    email.setCustomValidity(message.message);
  } else {
    email.setCustomValidity("");
  }
  alert("hello");
}
