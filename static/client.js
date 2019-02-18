
var devurl = 'localhost:5000';

function displayView(view, ){
  document.body.innerHTML = document.getElementById(view).innerHTML;
};

window.onload = function(){
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
      var response = JSON.parse(this.responseText);
      if (response.success == true) {
        displayView("profile_view");
        document.getElementById("defaultOpen").click();
        fillPersonInfo();
        getPosts();
        openWebSocketConnection();
      }
    } else if (this.readyState == 4 && this.status != 200) {
      var response = JSON.parse(this.responseText);
      console.log(response)
      displayView("welcome_view");
    }
  };
  sendXHR(xmlhttp, "POST", "http://" + devurl + "/checklogin")
}

function signUp(){
  var form = document.getElementById("signup_form");
  var jsonObj = getFormData(form);
  var email = document.getElementById("email");
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
      var response = JSON.parse(this.responseText);
      if (response.success == false) {
        email.setCustomValidity(response.message); // Q Error doesn't show initially why?
      } else {
        signIn(jsonObj.email, jsonObj.password);
      }
    }
  };
  sendXHR(xmlhttp, "POST", "http://localhost:5000/signup", jsonObj, false)

  return false;
}

function signIn(email = "", password = ""){
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var response = JSON.parse(this.responseText)
        if (!response.success){
          document.getElementById("login_error").innerHTML = response.message;
          return false;
        } else {
          localStorage.setItem("user_token", response.data);
          displayView("profile_view");
          document.getElementById("defaultOpen").click();
          fillPersonInfo();
          getPosts();
          openWebSocketConnection();
        }
    };
  }
  if (email == "") {
    var form = document.getElementById("login_form");
    var jsonObj = getFormData(form);
      sendXHR(xmlhttp, "POST", "http://localhost:5000/signin",
      {"email": jsonObj.email_login, "password": jsonObj.password}, false);
  } else {
      sendXHR(xmlhttp, "POST", "http://localhost:5000/signin",
      {"email": email, "password": password}, false);
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
  sendXHR(xmlhttp, "POST", "http://localhost:5000/changepassword", jsonObj)
  return false;
}

function postMessage(email = null) {
  var form = document.getElementById("post_form");
  var to_email = document.getElementById("email").innerHTML;
  if (email != null) {
    form = document.getElementById("b_post_form");
    to_email = document.getElementById("b_email").innerHTML;
  }
  var message = getFormData(form);
  message.to_email = to_email;
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
          for (i = 0; i < response.messages.length; i++) {
            var node = document.createElement("div");
            var textnode = document.createTextNode(response.messages[i]);
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
    sendXHR(xmlhttp, "POST", "http://localhost:5000/getmessagesbyemail", {"email": email})
  }
}

function fillPersonInfo(email="") {
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
        if (email != "") {
          sessionStorage.setItem("searched_user", email);
          getPosts(email);
        }
      } else {
        var inputField = document.getElementById("search_user_email_field");
        inputField.setCustomValidity(response.message); // Q: Varför måste man klicka två ggr för att felmeddelandet ska synas?
      }
      return response;
    }
  };

  if (email == "") {
      sendXHR(xmlhttp, "POST", "http://localhost:5000/getuserbytoken")
  } else {
      sendXHR(xmlhttp, "POST", "http://localhost:5000/getuserbyemail", {"email": email})
  }
}

function searchUser() {
  var form = document.getElementById("user_search_form");
  var formData = getFormData(form);
  fillPersonInfo(formData.userEmail);
  //  formData.reset(); Q: Asynkront problem. Tar förmodligen bort objektet som används och fuckar allt.
  return false;
}

function sendXHR(req, method, url, data = null, needAuth = true, asych = true) {
  req.open(method, url, asych);
  if (needAuth) {
    var token = localStorage.getItem("user_token");
    req.setRequestHeader('Authorization', 'Bearer ' + token); // MAYBE REMOVE 'BEARER' CUZ SAVE IT LIKE THAT ALREADY
  }
  req.send(JSON.stringify(data));
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

function openWebSocketConnection() {
  var connection = new WebSocket('ws://' + devurl + '/ping')
  connection.onopen = function() {
    connection.send('sadasdasdasd')
  }

  connection.onmessage = function(e) {
    console.log('Server: ' + e.data)
  }
}
