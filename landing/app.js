/**
 * Created by Aya on 12/20/2016.
 */
$(document).ready(function () {
  $('#login-form').submit(function (e) {
    var username = $('#username').val();
    var password = $('#password').val();

    authLogin(username, password);
    e.preventDefault();
  });

  $('#reg-form').submit(function (e) {
    var username = $('#username-reg').val();
    var password = $('#password-reg').val();
    var firstname = $('#firstname').val();
    var lastname = $('#lastname').val();
    var email = $('#email').val();

    authRegister(username, password, firstname, lastname, email);
    e.preventDefault();
  });
});

authLogin = function (username, password) {
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "http://ec2-54-202-250-196.us-west-2.compute.amazonaws.com/User/login",
    data: {
      username: username,
      password: password
    },
    success: function (response) {
      console.log(response);
    },
    error: function (response) {
      console.log(response);
    }
  });
};
authRegister = function (username, password, firstname, lastname, email) {
  $.ajax({
    type: "POST",
    url: "http://ec2-54-202-250-196.us-west-2.compute.amazonaws.com/User/signup",
    dataType: "jsonp",
    data: {
      username:username,
      password: password,
      last_name: lastname,
      first_name: firstname,
      email: email
    },
    useDefaultXhrHeader: false,
    success: function (response, status, xhr) {
      console.log(response);
    },
    error: function (response, status, xhr) {
      console.log(response);
    }
  });
};
