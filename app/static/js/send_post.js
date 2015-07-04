function sendPost() {
    console.log("in function");
    var sendPostRequest;

    // Get content from textbox
    var content = document.getElementById("wmd-input").value;
    var csrfToken = document.getElementById("csrf_token").value;

    // Setup request
    if (window.XMLHttpRequest) {
        sendPostRequest = new XMLHttpRequest();
    } else {
        sendPostRequest = new ActiveXObject("Microsoft.XMLHTTP");
    }

    sendPostRequest.onreadystatechange = function () {

        if (sendPostRequest.readyState == 4 && sendPostRequest.status == 200) {
            var response = sendPostRequest.responseText;
            alert(response);
            console.log(response);
            $("#wmd-input").val("");
            getLatestPosts();
        }
    }

    jQuery(document).ready(function ($) {
        jQuery("#wmd-preview").hide('fast');  
    });

    var url = $("#send-post-url").data()["url"];

    sendPostRequest.open("POST", url, true);
    sendPostRequest.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    sendPostRequest.send("&post=" + content + "&csrf_token=" + csrfToken);
}