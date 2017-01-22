$(function() {
    $("#scroll").prop({ scrollTop: $("#scroll").prop("scrollHeight") });

    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);

    chatsock.onmessage = function(message) {
      console.log("Got websocket message " + message.data);

      var data = JSON.parse(message.data);
      var chat = $("#chat");
      var ele = $('<tr></tr>');
      var chat_text = "<div id='time'>" + data.sent_at + "</div><div id='sender'>" + data.sender + "</div>";

      ele.append(
        $("<td class='convo-details'></td>").html(chat_text)
      );
      // ele.append(
      //   $("<td></td>").text(data.sender)
      // );
      ele.append(
        $("<td></td>").text(data.body)
      );

      chat.append(ele);
      $("#scroll").prop({ scrollTop: $("#scroll").prop("scrollHeight") });
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
