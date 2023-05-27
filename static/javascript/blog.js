// Sử dụng hàm getCookieValue để lấy giá trị của cookie "username"
function getCookieValue(cookieName) {
  var name = cookieName + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var cookieArray = decodedCookie.split(";");

  for (var i = 0; i < cookieArray.length; i++) {
    var cookie = cookieArray[i];
    while (cookie.charAt(0) === " ") {
      cookie = cookie.substring(1);
    }
    if (cookie.indexOf(name) === 0) {
      return cookie.substring(name.length, cookie.length);
    }
  }
  return "";
}

var username = getCookieValue("username");
var thumbnail = getCookieValue("thumbnail");
if (username) {
  document.querySelector(".unlogin").style.display = "none";
  document.querySelector(".contact-us-wrap").style.display = "block";
  document.querySelector(".current-user img").src = thumbnail.replaceAll(
    '"',
    ""
  );
  document.querySelector(".current-user p").innerText = username;
} else {
  document.querySelector(".contact-us-wrap").style.display = "none"
  document.querySelector(".unlogin").style.display = "block";
}
console.log("Giá trị của cookie username: " + username);

const imageInput = document.getElementById("image-input");
const previewImage = document.getElementById("preview-image");

imageInput.addEventListener("change", function (event) {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = function () {
    previewImage.src = reader.result;
  };

  if (file) {
    reader.readAsDataURL(file);
  }
});
