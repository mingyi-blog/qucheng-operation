(function () {
  function share(type) {
    var url = location.href;
    var title = document.title;
    var u;
    if (type === "weibo") {
      u = "https://service.weibo.com/share/share.php?url=" +
        encodeURIComponent(url) + "&title=" + encodeURIComponent(title);
    } else if (type === "qq") {
      u = "https://connect.qq.com/widget/shareqq/index.html?url=" +
        encodeURIComponent(url) + "&title=" + encodeURIComponent(title);
    } else if (type === "copy") {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(function () {
          alert("链接已复制，去粘贴给朋友吧");
        });
      } else {
        prompt("复制此链接：", url);
      }
      return;
    } else if (type === "weixin" || type === "pyq") {
      var box = document.getElementById("wx-qr");
      if (!box) return;
      var label = type === "weixin" ? "微信" : "朋友圈";
      box.innerHTML =
        "<p>长按二维码分享到" + label + "</p>" +
        '<img alt="qrcode" src="https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=' +
        encodeURIComponent(url) + '">';
      box.hidden = false;
      return;
    }
    if (u) window.open(u, "_blank");
  }

  var btns = document.querySelectorAll(".share-btn");
  for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function () {
      share(this.getAttribute("data-share"));
    });
  }
})();
