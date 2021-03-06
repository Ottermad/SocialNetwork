function sendMessage () {

    // Get the user to send the message to and the message to send
	var recipient = document.getElementById("recipient").value;
	var body = document.getElementById("body").value;
    var csrfToken = document.getElementById("csrf_token").value;


    // Create a new variable to hold request
    var sendMessageRequest;

    // Check if XMLHttpRequest exists (modern browsers - IE7+, Firefox, Chrome, Opera, Safari)
    if (window.XMLHttpRequest) {
        // if it does create a XMLHttpRequest
        sendMessageRequest = new XMLHttpRequest();
    }
    else {
        // otherwise deal with IE6, IE5
        sendMessageRequest=new ActiveXObject("Microsoft.XMLHTTP");
    }

    // Call back function for request
    sendMessageRequest.onreadystatechange=function() {

        // Check if request was sent successfully.
        if (sendMessageRequest.readyState==4 && sendMessageRequest.status==200) {

            // Get response body
            var json = sendMessageRequest.responseText;

            // Parse into JSON
            //json = JSON.parse(json);
            console.log(json);

            // Clear the text box
            $("#body").val("");
            getConversation(recipient);

        }
    }

    var url = $("#send-message-url").data()["url"];
    
    // Send a post request
    sendMessageRequest.open("POST", url,true);
    sendMessageRequest.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    sendMessageRequest.send("recipient=" + recipient + "&body=" + body + "&csrf_token=" + csrfToken);
}