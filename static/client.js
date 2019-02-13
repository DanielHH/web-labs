function displayView(view){
  document.body.innerHTML = document.getElementById(view).innerHTML;
};

window.onload = function(){
  if (localStorage.getItem("user_token") != null) {
    displayView("profile_view");
    document.getElementById("defaultOpen").click();
    fill_person_info();
    getPosts();
  } else {
    displayView("welcome_view");
  }
}

function fill_person_info(email="") {
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var response = JSON.parse(this.responseText);
        if (response.success) {
          for (key in response.user) {
            if (email=="") {
              document.getElementById(key).innerHTML = response.user[key];
            } else {
              document.getElementById("b_" + key).innerHTML = response.user[key];
            }
          }
        } else {
          return response.message;
        }
    }
  };
  if (email == "") {
      sendXHR(xmlhttp, "POST", "http://localhost:5000/getuserbytoken")
  } else {
      sendXHR(xmlhttp, "POST", "http://localhost:5000/getuserbyemail", {"email": email})
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
  var email = document.getElementById("email");

  var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
      console.log(this.responseText);
      var response = JSON.parse(this.responseText);
      if (response.success == false) {
        email.setCustomValidity(response.message); // Q Error doesn't show initially why?
      } else {
        signIn(jsonObj.email, jsonObj.password);
        fill_person_info();
        displayView("profile_view");
      }
    }
  };
  sendXHR(xmlhttp, "POST", "http://localhost:5000/signup", jsonObj, false)

  return false;
}

function signIn(email = "", password = ""){
  var xmlhttp = new XMLHttpRequest();
  if (email == "") {
    var form = document.getElementById("login_form");
    var jsonObj = getFormData(form);
    xmlhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          var response = JSON.parse(this.responseText)
          if (!response.success){
            document.getElementById("login_error").innerHTML = response.message;
            return false;
          } else {
            localStorage.setItem("user_token", response.data);
          }
      };
      sendXHR(xmlhttp, "POST", "http://localhost:5000/signin",
      {"email": jsonObj.email_login, "password": jsonObj.password}, false)
    }
  } else {
    xmlhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          var response = JSON.parse(this.responseText)
          if (!response.success){
            document.getElementById("login_error").innerHTML = response.message;
            return false;
          } else {
            localStorage.setItem("user_token", response.data);
          }
      };
      sendXHR(xmlhttp, "POST", "http://localhost:5000/signin",
      {"email": email, "password": password}, false)
    }
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

  var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var response = JSON.parse(this.responseText)
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
    };
  }
  sendXHR(xmlhttp, "POST", "http://localhost:5000/changepassword", null)
  return false;
}

function postMessage(email = null) {
  var form = document.getElementById("post_form");
  if (email != null) {
    form = document.getElementById("b_post_form");
  }
  var message = getFormData(form);
  message.to_email = getUserDataByToken().email // MAYBE WITH SQUARE BRACKETS
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var response = JSON.parse(this.responseText)
        if (response.success) {
            getPosts(email);
            form.reset();
        }
    };
  }
  sendXHR(xmlhttp, "POST", "http://localhost:5000/postmessage", message)
  return false; // MAYBE REMOVE THIS BUT THEN WE IN TROUBLE YO
}

function getPosts(email = null) {
  var feed = document.getElementById("feed");
  var response;
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var response = JSON.parse(this.responseText)
        if (response.success) {
          for (i = 0; i < response.data.length; i++) {
            var node = document.createElement("div");
            var textnode = document.createTextNode(response.data[i].content);
            node.appendChild(textnode);
            feed.appendChild(node);
          }
        }
    };
  }
  if (email == null) {
    // MAYBE MOVE OUT feed.innerHTML = "";. WE SHALL SEE
    feed.innerHTML = "";
    sendXHR(xmlhttp, "POST", "http://localhost:5000/getmessagesbytoken")
  } else {
    feed = document.getElementById("b_feed");
    feed.innerHTML = "";
    sendXHR(xmlhttp, "POST", "http://localhost:5000/getmessagesbyemail")
  }
}

function searchUser() {
  var form = document.getElementById("user_search_form");
  var formData = getFormData(form);
  var response = fill_person_info(formData.userEmail);
  if(response != null) {
    var inputField = document.getElementById("search_user_email_field");
    inputField.setCustomValidity(response);
  } else {
    sessionStorage.setItem("searched_user", formData.userEmail);
    getPosts(formData.userEmail);
    form.reset();
  }
  return false;
}

function signOut() {
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var response = JSON.parse(this.responseText)
        if (response.success) {
          sessionStorage.setItem("searched_user", null);
          localStorage.setItem("user_token", "");
          displayView("welcome_view");
        }
    };
  }
  sendXHR(xmlhttp, "POST", "http://localhost:5000/signout");
}

function sendXHR(req, method, url, data = null, needAuth = true, asych = true) {
  if (needAuth) {
    var token = localStorage.getItem("user_token");
    req.setRequestHeader('Authorization', 'Bearer ' + token); // MAYBE REMOVE 'BEARER' CUZ SAVE IT LIKE THAT ALREADY
  }
  req.open(method, url, asych);
  req.send(JSON.stringify(data));
}
