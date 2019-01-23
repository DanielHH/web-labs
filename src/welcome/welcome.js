function validatePassword() {
  var password = document.getElementById('password');
  var repeat_password = document.getElementById('repeat_password');
  if (password.value.length < 8) {
    password.setCustomValidity("password must be at least 8 characters long");
  } else if (password.value != repeat_password.value) {
    password.setCustomValidity("");
    repeat_password.setCustomValidity("passwords must match");
  } else {
    repeat_password.setCustomValidity("");
  }
}
