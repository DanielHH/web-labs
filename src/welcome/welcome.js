function validateForm() {
  var password = document.forms["signup_form"]["password"].value;
  var repeated_password = document.forms["signup_form"]["repeat_password"].value;
  if (password.length < 8 || password != repeated_password) {
    
    return false;
  }
}
