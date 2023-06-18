var stompClient = null;

function setConnected(connected) {
    $("#connect").prop("disabled", connected);
    $("#disconnect").prop("disabled", !connected);
    if (connected) {
        $("#conversation").show();
    }
    else {
        $("#conversation").hide();
    }
    $("#greetings").html("");
}

function connect() {
    var socket = new SockJS('/ws');
    stompClient = Stomp.over(socket);
    stompClient.connect({}, function (frame) {
        setConnected(true);
        console.log('Connected: ' + frame);
        stompClient.subscribe('/topic/answers', function (answering) {
            showGreeting(JSON.parse(answering.body));
        });
    });
}

function disconnect() {
    if (stompClient !== null) {
        stompClient.disconnect();
    }
    setConnected(false);
    console.log("Disconnected");
}

function sendName() {

    reply = "<div class=\"bubble reply reply-freeform say\">"
            + "<span class=\"bubble-content\">" + $("#ask").val() + "</span>"
            + "</div>"
    $("#greetings").append(reply);

    stompClient.send("/app/question", {}, JSON.stringify({'ask': $("#ask").val()}));
}

function showGreeting(messages) {

    for(i = 0; i < messages.length; i++){
        str = "<div class=\"bubble say\">"
                + "<span class=\"bubble-content\">" + messages[i].says + "</span>"
                + "</div>";
        $("#greetings").append(str);
    }
}

$(function () {
    $("form").on('submit', function (e) {
        e.preventDefault();
    });
    $( "#connect" ).click(function() {
        connect();
    });
    $( "#disconnect" ).click(function() {
        disconnect();
    });
    $( "#send" ).click(function() { sendName(); });

    $( "#btn-modal" ).click(function() {
        connect();
    });
});