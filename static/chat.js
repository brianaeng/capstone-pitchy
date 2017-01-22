$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);

    chatsock.onmessage = function(message) {
      console.log("Got websocket message " + message.data);

      var data = JSON.parse(message.data);
      var chat = $("#chat");
      var ele = $('<tr></tr>');

      ele.append(
        $("<td></td>").text(data.formatted_timestamp)
      );
      ele.append(
        $("<td></td>").text(data.sender)
      );
      ele.append(
        $("<td></td>").text(data.body)
      );

      chat.append(ele);
  };

    $("#chatform").on("submit", function(event) {
      var message = {
        sender: $('#handle').val(),
        body: $('#message').val(),
      };
      chatsock.send(JSON.stringify(message));
      $("#message").val('').focus();
      return false;
    });
});
