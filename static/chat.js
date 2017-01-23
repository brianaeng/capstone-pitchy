$(function() {
    // Starts scrollbar at bottom
    $("#scroll").prop({ scrollTop: $("#scroll").prop("scrollHeight") });

    // Check if wss or ws based on https or http
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";

    //Create new websocket
    var socket = new WebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);

    //Socket receives message, appends it to user's chat in real time
    socket.onmessage = function(message) {
      var data = JSON.parse(message.data);
      var chat = $("#chat");
      var ele = $('<tr></tr>');
      var chat_text = "<div id='time'>" + data.sent_at + "</div><div id='sender'>" + data.sender + "</div>";

      ele.append(
        $("<td class='convo-details'></td>").html(chat_text)
      );
      ele.append(
        $("<td></td>").text(data.body)
      );

      chat.append(ele);

      //After adding new message, scrollbar set to bottom
      $("#scroll").prop({ scrollTop: $("#scroll").prop("scrollHeight") });
    };

    //Socket sends message as JSON for consumer to handle
    $("#chatform").on("submit", function(event) {
      var message = {
        sender: $('#handle').val(),
        body: $('#message').val(),
      };
      
      socket.send(JSON.stringify(message));

      //Clears input
      $("#message").val('').focus();

      //Stop form submission
      return false;
    });
});
