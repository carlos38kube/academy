(function () {
  var API = "https://api.jivops.com";
  var token = localStorage.getItem("jivops_token");

  function toLogin() {
    localStorage.removeItem("jivops_token");
    window.location.href = "login.html";
  }

  if (!token) {
    toLogin();
    return;
  }

  fetch(API + "/me", {
    headers: { "Authorization": "Bearer " + token }
  })
    .then(function (res) {
      if (!res.ok) throw new Error("unauthorized");
      return res.json();
    })
    .then(function (user) {
      if (user.is_subscribed) {
        document.documentElement.classList.add("jivops-unlocked");
      } else {
        window.location.href = "suscripcion.html";
      }
    })
    .catch(toLogin);
})();
