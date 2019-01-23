function validateForm() {
  var x = document.forms["signup_form"]["password"].value;
  var y = document.forms["signup_form"]["repeat_password"].value;

  if (x.length() >= 8) {
    //do something
  }
}
