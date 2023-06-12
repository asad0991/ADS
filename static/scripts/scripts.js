function appearonclick(){
  if(document.getElementById('signup-form').style.transform== "translateY(-75%)"){
    document.getElementById('signup-form').style.transform= "translateY(0%)"
    document.getElementById('signup-form').style.width= "14rem"
    document.getElementById('login').style.height='27rem';
  }
  else{
  document.getElementById('signup-form').style.transform= "translateY(-75%)";
  document.getElementById('signup-form').style.width= "40rem"
  document.getElementById('login').style.height='32rem';
}
}
if ( window.history.replaceState ) {
  window.history.replaceState( null, null, window.location.href );
}
function wait(){
var x = document.getElementsByClassName("toggle");
  var i;
  for (i = 0; i < x.length; i++) {
      x[i].style.display = 'block';
  }
  document.getElementById("x-button").style.display="block";

}
function menuclick(){
  document.getElementById("mobile").style.transition="1s";
  document.getElementById("mobile").style.width="60%";

  setTimeout(wait, 190);
  console.log("Hi");

}
function menuoff(){
  var x = document.getElementsByClassName("toggle");
    var i;
    for (i = 0; i < x.length; i++) {
        x[i].style.display = 'none';
    }
  document.getElementById("mobile").style.width="0%";
  document.getElementById("x-button").style.display="none";
}



var app = angular.module("myApp", []);

app.controller("myCtrl", function($scope, $http, $window) {
  $scope.downloadvideo = function(name) {
    $http({
      method: 'GET',
      url: '/api/download',
      params: {
        videoname: name,
      }
    }).then(function (response) {
      // Handle success
      var filename = response.headers('Content-Disposition').split('filename=')[1];
      var blob = new Blob([response.data], { type: response.headers('Content-Type') });
      var url = $window.URL || $window.webkitURL;
      var fileUrl = url.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = fileUrl;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
}, function(response) {
  // Handle error
  console.log(response.statusText);
      console.log(response.data);
    }, function (response) {
      // Handle error
      console.log(response.statusText);
    });
  }
});




