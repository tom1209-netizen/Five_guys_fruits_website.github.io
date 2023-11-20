var thread_id = null; // Global variable to store thread ID

$(document).ready(function () {
    // Start a new conversation
    $.ajax({
        type: "GET",
        url: "/start",
    }).done(function (data) {
        thread_id = data.thread_id;
    });

    $("#messageArea").on("submit", function (event) {
        event.preventDefault();
        var rawText = $("#text").val();
        var date = new Date();
        var hour = date.getHours();
        var minute = date.getMinutes();
        var str_time = hour + ":" + minute;

        var userHtml = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' + rawText + '<span class="msg_time_send">' + str_time + '</span></div><div class="img_cont_msg"><img src="https://i.ibb.co/d5b84Xw/Untitled-design.png" class="rounded-circle user_img_msg" style="width: 50px; height: 50px"></div></div>';
        $("#messageFormeight").append(userHtml);

        // Sending message to Flask backend
        if (thread_id) {
            $.ajax({
                data: JSON.stringify({
                    thread_id: thread_id,
                    message: rawText,
                }),
                contentType: "application/json",
                type: "POST",
                url: "/chat",
            }).done(function (data) {
                // Display the bot's response
                var botResponse = data.response;
                var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.ibb.co/fSNP7Rz/icons8-chatgpt-512.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer">' + botResponse + '<span class="msg_time">' + str_time + '</span></div></div>';
                $("#messageFormeight").append($.parseHTML(botHtml));
            });
        }

        // Clear the input field
        $("#text").val("");
    });
});